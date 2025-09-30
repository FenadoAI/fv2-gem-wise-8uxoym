"""FastAPI server exposing AI agent endpoints."""

import logging
import os
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Literal, Optional

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field
from starlette.middleware.cors import CORSMiddleware

from ai_agents.agents import AgentConfig, ChatAgent, SearchAgent


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

# Security
security = HTTPBearer()

# Type aliases
UserRole = Literal["staff", "manager", "owner"]
MetalType = Literal["gold", "silver", "platinum", "white_gold", "rose_gold"]
ItemStatus = Literal["in_stock", "sold", "reserved", "discontinued"]
Category = Literal["ring", "necklace", "bracelet", "earring", "pendant", "bangle", "chain", "other"]
OrderStatus = Literal["pending", "confirmed", "processing", "shipped", "delivered", "cancelled"]


# Pydantic Models for Jewellery Store
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    role: UserRole
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)
    role: UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    user: User
    token: str


class ShippingAddress(BaseModel):
    line1: str
    line2: Optional[str] = None
    city: str
    state: str
    zip: str
    country: str


class JewelleryItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    item_code: str = Field(min_length=3, max_length=50)
    name: str
    description: str
    category: Category
    price: int = Field(ge=0)  # cents
    weight: float = Field(gt=0)  # grams
    metal_type: MetalType
    stones: Optional[str] = None
    images: List[str] = Field(min_length=1, max_length=10)
    quantity: int = Field(ge=0)
    status: ItemStatus
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class JewelleryItemCreate(BaseModel):
    item_code: str = Field(min_length=3, max_length=50)
    name: str
    description: str
    category: Category
    price: int = Field(ge=0)
    weight: float = Field(gt=0)
    metal_type: MetalType
    stones: Optional[str] = None
    images: List[str] = Field(min_length=1, max_length=10)
    quantity: int = Field(ge=0)
    status: ItemStatus


class JewelleryItemUpdate(BaseModel):
    item_code: Optional[str] = Field(None, min_length=3, max_length=50)
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[Category] = None
    price: Optional[int] = Field(None, ge=0)
    weight: Optional[float] = Field(None, gt=0)
    metal_type: Optional[MetalType] = None
    stones: Optional[str] = None
    images: Optional[List[str]] = Field(None, min_length=1, max_length=10)
    quantity: Optional[int] = Field(None, ge=0)
    status: Optional[ItemStatus] = None


class OrderItem(BaseModel):
    item_id: str
    item_code: str
    name: str
    price: int
    quantity: int
    subtotal: int


class OrderItemInput(BaseModel):
    item_id: str
    quantity: int = Field(gt=0)


class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_name: str
    customer_email: EmailStr
    customer_phone: str = Field(min_length=10, max_length=15)
    items: List[OrderItem]
    total_amount: int  # cents
    status: OrderStatus
    payment_method: Literal["cod"] = "cod"
    shipping_address: ShippingAddress
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class OrderCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: str = Field(min_length=10, max_length=15)
    items: List[OrderItemInput] = Field(min_length=1, max_length=50)
    shipping_address: ShippingAddress
    notes: Optional[str] = None


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
    notes: Optional[str] = None


class PaginatedResponse(BaseModel):
    page: int
    total: int
    total_pages: int


class ItemsResponse(PaginatedResponse):
    items: List[JewelleryItem]


class OrdersResponse(PaginatedResponse):
    orders: List[Order]


class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class StatusCheckCreate(BaseModel):
    client_name: str


class ChatRequest(BaseModel):
    message: str
    agent_type: str = "chat"
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    success: bool
    response: str
    agent_type: str
    capabilities: List[str]
    metadata: dict = Field(default_factory=dict)
    error: Optional[str] = None


class SearchRequest(BaseModel):
    query: str
    max_results: int = 5


class SearchResponse(BaseModel):
    success: bool
    query: str
    summary: str
    search_results: Optional[dict] = None
    sources_count: int
    error: Optional[str] = None


# Helper functions
def _ensure_db(request: Request):
    try:
        return request.app.state.db
    except AttributeError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=503, detail="Database not ready") from exc


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def create_access_token(user_id: str, email: str, role: UserRole) -> str:
    """Create a JWT access token."""
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode = {
        "sub": user_id,
        "email": email,
        "role": role,
        "exp": expire
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    request: Request = None
) -> Dict:
    """Decode JWT and return current user info."""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        email = payload.get("email")
        role = payload.get("role")

        if not user_id or not email or not role:
            raise HTTPException(
                status_code=401,
                detail={"error": {"code": "INVALID_TOKEN", "message": "Invalid token"}}
            )

        return {"id": user_id, "email": email, "role": role}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail={"error": {"code": "INVALID_TOKEN", "message": "Token expired"}}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail={"error": {"code": "INVALID_TOKEN", "message": "Invalid token"}}
        )


def require_role(allowed_roles: List[UserRole]):
    """Dependency to check if user has required role."""
    async def role_checker(current_user: Dict = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail={"error": {"code": "INSUFFICIENT_PERMISSION", "message": "User role lacks permission"}}
            )
        return current_user
    return role_checker


def _get_agent_cache(request: Request) -> Dict[str, object]:
    if not hasattr(request.app.state, "agent_cache"):
        request.app.state.agent_cache = {}
    return request.app.state.agent_cache


async def _get_or_create_agent(request: Request, agent_type: str):
    cache = _get_agent_cache(request)
    if agent_type in cache:
        return cache[agent_type]

    config: AgentConfig = request.app.state.agent_config

    if agent_type == "search":
        cache[agent_type] = SearchAgent(config)
    elif agent_type == "chat":
        cache[agent_type] = ChatAgent(config)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown agent type '{agent_type}'")

    return cache[agent_type]


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv(ROOT_DIR / ".env")

    mongo_url = os.getenv("MONGO_URL")
    db_name = os.getenv("DB_NAME")

    if not mongo_url or not db_name:
        missing = [name for name, value in {"MONGO_URL": mongo_url, "DB_NAME": db_name}.items() if not value]
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    client = AsyncIOMotorClient(mongo_url)

    try:
        app.state.mongo_client = client
        app.state.db = client[db_name]
        app.state.agent_config = AgentConfig()
        app.state.agent_cache = {}
        logger.info("AI Agents API starting up")
        yield
    finally:
        client.close()
        logger.info("AI Agents API shutdown complete")


app = FastAPI(
    title="AI Agents API",
    description="Minimal AI Agents API with LangGraph and MCP support",
    lifespan=lifespan,
)

api_router = APIRouter(prefix="/api")


@api_router.get("/")
async def root():
    return {"message": "JewelCraft Pro API"}


# ===== AUTHENTICATION ENDPOINTS =====

@api_router.post("/auth/register", response_model=Token, status_code=201)
async def register_user(
    user_data: UserCreate,
    request: Request,
    current_user: Dict = Depends(require_role(["owner"]))
):
    """Register a new user (owner only)."""
    db = _ensure_db(request)

    # Check if email already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail={"error": {"code": "DUPLICATE_EMAIL", "message": "Email already exists"}}
        )

    # Check if username already exists
    existing_username = await db.users.find_one({"username": user_data.username})
    if existing_username:
        raise HTTPException(
            status_code=409,
            detail={"error": {"code": "DUPLICATE_USERNAME", "message": "Username already exists"}}
        )

    # Create user
    hashed_password = hash_password(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        role=user_data.role
    )

    user_doc = user.model_dump()
    user_doc["password"] = hashed_password
    await db.users.insert_one(user_doc)

    # Create token
    token = create_access_token(user.id, user.email, user.role)

    return Token(user=user, token=token)


@api_router.post("/auth/login", response_model=Token)
async def login_user(login_data: UserLogin, request: Request):
    """Login and get JWT token."""
    db = _ensure_db(request)

    # Find user
    user_doc = await db.users.find_one({"email": login_data.email})
    if not user_doc:
        raise HTTPException(
            status_code=401,
            detail={"error": {"code": "INVALID_CREDENTIALS", "message": "Invalid email or password"}}
        )

    # Verify password
    if not verify_password(login_data.password, user_doc["password"]):
        raise HTTPException(
            status_code=401,
            detail={"error": {"code": "INVALID_CREDENTIALS", "message": "Invalid email or password"}}
        )

    # Create user object and token
    user = User(
        id=user_doc["id"],
        username=user_doc["username"],
        email=user_doc["email"],
        role=user_doc["role"],
        created_at=user_doc["created_at"]
    )
    token = create_access_token(user.id, user.email, user.role)

    return Token(user=user, token=token)


@api_router.get("/auth/me", response_model=User)
async def get_me(request: Request, current_user: Dict = Depends(get_current_user)):
    """Get current user info."""
    db = _ensure_db(request)
    user_doc = await db.users.find_one({"id": current_user["id"]})
    if not user_doc:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "NOT_FOUND", "message": "User not found"}}
        )
    return User(**user_doc)


# ===== INVENTORY MANAGEMENT ENDPOINTS =====

@api_router.get("/inventory", response_model=ItemsResponse)
async def get_inventory(
    request: Request,
    current_user: Dict = Depends(require_role(["staff", "manager", "owner"])),
    page: int = 1,
    limit: int = 20,
    category: Optional[Category] = None,
    status: Optional[ItemStatus] = None,
    search: Optional[str] = None
):
    """Get inventory items (staff+)."""
    db = _ensure_db(request)

    # Build query
    query = {}
    if category:
        query["category"] = category
    if status:
        query["status"] = status
    if search:
        query["$or"] = [
            {"item_code": {"$regex": search, "$options": "i"}},
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]

    # Pagination
    limit = min(limit, 100)  # Max 100 items per page
    skip = (page - 1) * limit

    # Get items
    items_cursor = db.jewellery_items.find(query).skip(skip).limit(limit).sort("created_at", -1)
    items = await items_cursor.to_list(length=limit)
    total = await db.jewellery_items.count_documents(query)
    total_pages = (total + limit - 1) // limit

    return ItemsResponse(
        items=[JewelleryItem(**item) for item in items],
        page=page,
        total=total,
        total_pages=total_pages
    )


@api_router.post("/inventory", response_model=JewelleryItem, status_code=201)
async def create_item(
    item_data: JewelleryItemCreate,
    request: Request,
    current_user: Dict = Depends(require_role(["staff", "manager", "owner"]))
):
    """Add new jewellery item (staff+)."""
    db = _ensure_db(request)

    # Check if item_code already exists (case-insensitive)
    existing_item = await db.jewellery_items.find_one(
        {"item_code": {"$regex": f"^{item_data.item_code}$", "$options": "i"}}
    )
    if existing_item:
        raise HTTPException(
            status_code=409,
            detail={"error": {"code": "DUPLICATE_ITEM_CODE", "message": "Item code already exists"}}
        )

    # Create item
    item = JewelleryItem(**item_data.model_dump())
    await db.jewellery_items.insert_one(item.model_dump())

    return item


@api_router.get("/inventory/{item_id}", response_model=JewelleryItem)
async def get_item(
    item_id: str,
    request: Request,
    current_user: Dict = Depends(require_role(["staff", "manager", "owner"]))
):
    """Get single inventory item (staff+)."""
    db = _ensure_db(request)

    item = await db.jewellery_items.find_one({"id": item_id})
    if not item:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "NOT_FOUND", "message": "Item not found"}}
        )

    return JewelleryItem(**item)


@api_router.patch("/inventory/{item_id}", response_model=JewelleryItem)
async def update_item(
    item_id: str,
    item_update: JewelleryItemUpdate,
    request: Request,
    current_user: Dict = Depends(require_role(["staff", "manager", "owner"]))
):
    """Update jewellery item (staff+)."""
    db = _ensure_db(request)

    # Check if item exists
    item = await db.jewellery_items.find_one({"id": item_id})
    if not item:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "NOT_FOUND", "message": "Item not found"}}
        )

    # If item_code is being updated, check uniqueness
    update_data = item_update.model_dump(exclude_unset=True)
    if "item_code" in update_data and update_data["item_code"] != item["item_code"]:
        existing_item = await db.jewellery_items.find_one(
            {"item_code": {"$regex": f"^{update_data['item_code']}$", "$options": "i"}}
        )
        if existing_item:
            raise HTTPException(
                status_code=409,
                detail={"error": {"code": "DUPLICATE_ITEM_CODE", "message": "Item code already exists"}}
            )

    # Update item
    update_data["updated_at"] = datetime.now(timezone.utc)
    await db.jewellery_items.update_one({"id": item_id}, {"$set": update_data})

    # Get updated item
    updated_item = await db.jewellery_items.find_one({"id": item_id})
    return JewelleryItem(**updated_item)


@api_router.delete("/inventory/{item_id}", status_code=204)
async def delete_item(
    item_id: str,
    request: Request,
    current_user: Dict = Depends(require_role(["manager", "owner"]))
):
    """Delete jewellery item (manager+)."""
    db = _ensure_db(request)

    # Check if item exists
    item = await db.jewellery_items.find_one({"id": item_id})
    if not item:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "NOT_FOUND", "message": "Item not found"}}
        )

    # Check if item has order history
    order_with_item = await db.orders.find_one({"items.item_id": item_id})

    if order_with_item:
        # Soft delete (mark as discontinued)
        await db.jewellery_items.update_one(
            {"id": item_id},
            {"$set": {"status": "discontinued", "updated_at": datetime.now(timezone.utc)}}
        )
    else:
        # Hard delete
        await db.jewellery_items.delete_one({"id": item_id})

    return None


# ===== PUBLIC CATALOG ENDPOINTS =====

@api_router.get("/catalog", response_model=ItemsResponse)
async def get_catalog(
    request: Request,
    page: int = 1,
    limit: int = 20,
    category: Optional[Category] = None,
    metal_type: Optional[MetalType] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    search: Optional[str] = None
):
    """Get public catalog (only in_stock items)."""
    db = _ensure_db(request)

    # Build query - only show in_stock items
    query = {"status": "in_stock"}

    if category:
        query["category"] = category
    if metal_type:
        query["metal_type"] = metal_type
    if min_price is not None:
        query.setdefault("price", {})["$gte"] = min_price
    if max_price is not None:
        query.setdefault("price", {})["$lte"] = max_price
    if search:
        query["$or"] = [
            {"item_code": {"$regex": search, "$options": "i"}},
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]

    # Pagination
    limit = min(limit, 100)
    skip = (page - 1) * limit

    # Get items
    items_cursor = db.jewellery_items.find(query).skip(skip).limit(limit).sort("created_at", -1)
    items = await items_cursor.to_list(length=limit)
    total = await db.jewellery_items.count_documents(query)
    total_pages = (total + limit - 1) // limit

    return ItemsResponse(
        items=[JewelleryItem(**item) for item in items],
        page=page,
        total=total,
        total_pages=total_pages
    )


@api_router.get("/catalog/{item_id}", response_model=JewelleryItem)
async def get_catalog_item(item_id: str, request: Request):
    """Get single catalog item (public)."""
    db = _ensure_db(request)

    item = await db.jewellery_items.find_one({"id": item_id, "status": "in_stock"})
    if not item:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "NOT_FOUND", "message": "Item not found"}}
        )

    return JewelleryItem(**item)


# ===== ORDER MANAGEMENT ENDPOINTS =====

@api_router.post("/orders", response_model=Order, status_code=201)
async def create_order(order_data: OrderCreate, request: Request):
    """Place a COD order (public)."""
    db = _ensure_db(request)

    # Validate items and calculate total
    order_items = []
    total_amount = 0

    for item_input in order_data.items:
        item = await db.jewellery_items.find_one({"id": item_input.item_id})

        if not item:
            raise HTTPException(
                status_code=404,
                detail={"error": {"code": "NOT_FOUND", "message": f"Item {item_input.item_id} not found"}}
            )

        if item["status"] != "in_stock":
            raise HTTPException(
                status_code=400,
                detail={"error": {"code": "ITEM_NOT_AVAILABLE", "message": f"Item {item['item_code']} is not available"}}
            )

        if item["quantity"] < item_input.quantity:
            raise HTTPException(
                status_code=400,
                detail={"error": {"code": "INSUFFICIENT_STOCK", "message": f"Insufficient stock for item {item['item_code']}"}}
            )

        subtotal = item["price"] * item_input.quantity
        order_items.append(OrderItem(
            item_id=item["id"],
            item_code=item["item_code"],
            name=item["name"],
            price=item["price"],
            quantity=item_input.quantity,
            subtotal=subtotal
        ))
        total_amount += subtotal

    # Create order
    order = Order(
        customer_name=order_data.customer_name,
        customer_email=order_data.customer_email,
        customer_phone=order_data.customer_phone,
        items=order_items,
        total_amount=total_amount,
        status="pending",
        shipping_address=order_data.shipping_address,
        notes=order_data.notes
    )

    await db.orders.insert_one(order.model_dump())

    # Update inventory quantities
    for item_input in order_data.items:
        await db.jewellery_items.update_one(
            {"id": item_input.item_id},
            {"$inc": {"quantity": -item_input.quantity}, "$set": {"updated_at": datetime.now(timezone.utc)}}
        )

    return order


@api_router.get("/orders", response_model=OrdersResponse)
async def get_orders(
    request: Request,
    current_user: Dict = Depends(require_role(["staff", "manager", "owner"])),
    page: int = 1,
    limit: int = 20,
    status: Optional[OrderStatus] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
):
    """Get all orders (staff+)."""
    db = _ensure_db(request)

    # Build query
    query = {}
    if status:
        query["status"] = status
    if from_date:
        query.setdefault("created_at", {})["$gte"] = datetime.fromisoformat(from_date)
    if to_date:
        query.setdefault("created_at", {})["$lte"] = datetime.fromisoformat(to_date)

    # Pagination
    limit = min(limit, 100)
    skip = (page - 1) * limit

    # Get orders
    orders_cursor = db.orders.find(query).skip(skip).limit(limit).sort("created_at", -1)
    orders = await orders_cursor.to_list(length=limit)
    total = await db.orders.count_documents(query)
    total_pages = (total + limit - 1) // limit

    return OrdersResponse(
        orders=[Order(**order) for order in orders],
        page=page,
        total=total,
        total_pages=total_pages
    )


@api_router.get("/orders/{order_id}", response_model=Order)
async def get_order(
    order_id: str,
    request: Request,
    current_user: Dict = Depends(require_role(["staff", "manager", "owner"]))
):
    """Get single order (staff+)."""
    db = _ensure_db(request)

    order = await db.orders.find_one({"id": order_id})
    if not order:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "NOT_FOUND", "message": "Order not found"}}
        )

    return Order(**order)


@api_router.patch("/orders/{order_id}/status", response_model=Order)
async def update_order_status(
    order_id: str,
    status_update: OrderStatusUpdate,
    request: Request,
    current_user: Dict = Depends(require_role(["staff", "manager", "owner"]))
):
    """Update order status (staff+)."""
    db = _ensure_db(request)

    # Check if order exists
    order = await db.orders.find_one({"id": order_id})
    if not order:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "NOT_FOUND", "message": "Order not found"}}
        )

    # Update order
    update_data = {"status": status_update.status, "updated_at": datetime.now(timezone.utc)}
    if status_update.notes:
        update_data["notes"] = status_update.notes

    await db.orders.update_one({"id": order_id}, {"$set": update_data})

    # Get updated order
    updated_order = await db.orders.find_one({"id": order_id})
    return Order(**updated_order)


# ===== EXISTING AI AGENT ENDPOINTS =====


@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate, request: Request):
    db = _ensure_db(request)
    status_obj = StatusCheck(**input.model_dump())
    await db.status_checks.insert_one(status_obj.model_dump())
    return status_obj


@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks(request: Request):
    db = _ensure_db(request)
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]


@api_router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(chat_request: ChatRequest, request: Request):
    try:
        agent = await _get_or_create_agent(request, chat_request.agent_type)
        response = await agent.execute(chat_request.message)

        return ChatResponse(
            success=response.success,
            response=response.content,
            agent_type=chat_request.agent_type,
            capabilities=agent.get_capabilities(),
            metadata=response.metadata,
            error=response.error,
        )
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Error in chat endpoint")
        return ChatResponse(
            success=False,
            response="",
            agent_type=chat_request.agent_type,
            capabilities=[],
            error=str(exc),
        )


@api_router.post("/search", response_model=SearchResponse)
async def search_and_summarize(search_request: SearchRequest, request: Request):
    try:
        search_agent = await _get_or_create_agent(request, "search")
        search_prompt = (
            f"Search for information about: {search_request.query}. "
            "Provide a comprehensive summary with key findings."
        )
        result = await search_agent.execute(search_prompt, use_tools=True)

        if result.success:
            metadata = result.metadata or {}
            return SearchResponse(
                success=True,
                query=search_request.query,
                summary=result.content,
                search_results=metadata,
                sources_count=int(metadata.get("tool_run_count", metadata.get("tools_used", 0)) or 0),
            )

        return SearchResponse(
            success=False,
            query=search_request.query,
            summary="",
            sources_count=0,
            error=result.error,
        )
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Error in search endpoint")
        return SearchResponse(
            success=False,
            query=search_request.query,
            summary="",
            sources_count=0,
            error=str(exc),
        )


@api_router.get("/agents/capabilities")
async def get_agent_capabilities(request: Request):
    try:
        search_agent = await _get_or_create_agent(request, "search")
        chat_agent = await _get_or_create_agent(request, "chat")

        return {
            "success": True,
            "capabilities": {
                "search_agent": search_agent.get_capabilities(),
                "chat_agent": chat_agent.get_capabilities(),
            },
        }
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Error getting capabilities")
        return {"success": False, "error": str(exc)}


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
