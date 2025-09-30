# Jewellery Store Management System — API Contract

## Conventions
- Base URL: `/api`
- Auth: `Authorization: Bearer <JWT>` (all endpoints except public catalog and auth)
- IDs: string UUID; Time: ISO 8601; Money: integer cents (`currency:"USD"`)
- Errors: `{ "error": { "code": "STRING", "message": "STRING" } }`
- Pagination: `?page=1&limit=20`
- Role hierarchy: `public < staff < manager < owner`

---

## Client Types (TS)

```ts
export type UserRole = "staff" | "manager" | "owner";

export type User = {
  id: string;
  username: string;
  email: string;
  role: UserRole;
  created_at: string;
};

export type MetalType = "gold" | "silver" | "platinum" | "white_gold" | "rose_gold";
export type ItemStatus = "in_stock" | "sold" | "reserved" | "discontinued";
export type Category = "ring" | "necklace" | "bracelet" | "earring" | "pendant" | "bangle" | "chain" | "other";

export type JewelleryItem = {
  id: string;
  item_code: string;              // Unique, mandatory
  name: string;
  description: string;
  category: Category;
  price: number;                  // cents
  weight: number;                 // grams
  metal_type: MetalType;
  stones?: string;                // e.g., "Diamond 0.5ct, Ruby 2pcs"
  images: string[];               // Array of URLs
  quantity: number;
  status: ItemStatus;
  created_at: string;
  updated_at: string;
};

export type OrderStatus = "pending" | "confirmed" | "processing" | "shipped" | "delivered" | "cancelled";

export type OrderItem = {
  item_id: string;
  item_code: string;
  name: string;
  price: number;
  quantity: number;
  subtotal: number;
};

export type Order = {
  id: string;
  customer_name: string;
  customer_email: string;
  customer_phone: string;
  items: OrderItem[];
  total_amount: number;           // cents
  status: OrderStatus;
  payment_method: "cod";          // Only COD for MVP
  shipping_address: {
    line1: string;
    line2?: string;
    city: string;
    state: string;
    zip: string;
    country: string;
  };
  notes?: string;
  created_at: string;
  updated_at: string;
};
```

---

## 10 Core Endpoints (MVP Priority)

### Authentication (Priority 1)

**1. POST /auth/register** → 201
_Role: owner only (for creating staff/manager accounts)_
Req: `{ username, email, password, role: "staff"|"manager"|"owner" }`
Res: `{ user: User, token: string }`
Validation:
- username: 3-50 chars, alphanumeric + underscore
- email: valid format
- password: min 8 chars
- role: only owner can create accounts

**2. POST /auth/login** → 200
_Role: public_
Req: `{ email, password }`
Res: `{ user: User, token: string }`

### Inventory Management (Priority 1)

**3. GET /inventory** → 200
_Role: staff+_
Query: `?page=1&limit=20&category?&status?&search?`
Res: `{ items: JewelleryItem[], page: number, total: number, total_pages: number }`
Notes: search queries item_code, name, description

**4. POST /inventory** → 201
_Role: staff+_
Req: `{ item_code, name, description, category, price, weight, metal_type, stones?, images, quantity, status }`
Res: `JewelleryItem`
Validation:
- item_code: unique, mandatory, 3-50 chars
- price: int >= 0
- weight: float > 0
- quantity: int >= 0

**5. PATCH /inventory/{id}** → 200
_Role: staff+_
Req: Partial fields from JewelleryItem (except id, created_at)
Res: `JewelleryItem`
Validation: item_code must remain unique if changed

**6. DELETE /inventory/{id}** → 204
_Role: manager+_
Notes: Soft delete (status = "discontinued") if item has order history

### Public Catalog (Priority 1)

**7. GET /catalog** → 200
_Role: public_
Query: `?page=1&limit=20&category?&metal_type?&min_price?&max_price?&search?`
Res: `{ items: JewelleryItem[], page: number, total: number, total_pages: number }`
Notes: Only returns items with status="in_stock"

**8. GET /catalog/{id}** → 200
_Role: public_
Res: `JewelleryItem`

### Order Management (Priority 1)

**9. POST /orders** → 201
_Role: public_
Req: `{ customer_name, customer_email, customer_phone, items: [{item_id, quantity}], shipping_address, notes? }`
Res: `{ order: Order }`
Validation:
- Verify all items exist and are in_stock
- Check quantity availability
- Calculate total_amount server-side
- payment_method auto-set to "cod"

**10. GET /orders** → 200
_Role: staff+_
Query: `?page=1&limit=20&status?&from_date?&to_date?`
Res: `{ orders: Order[], page: number, total: number, total_pages: number }`

---

## Additional Endpoints (Priority 2 - Post MVP)

### Order Operations

**11. GET /orders/{id}** → 200
_Role: staff+_
Res: `Order`

**12. PATCH /orders/{id}/status** → 200
_Role: staff+_
Req: `{ status: OrderStatus, notes?: string }`
Res: `Order`
Validation: Status transitions must be logical (e.g., pending → confirmed → processing → shipped → delivered)

**13. GET /orders/customer/{email}** → 200
_Role: public (only own orders)_
Query: `?page=1&limit=20`
Res: `{ orders: Order[], page: number, total: number }`
Notes: Public users can only view orders matching their email

### Reports (Priority 2)

**14. GET /reports/sales** → 200
_Role: manager+_
Query: `?from_date&to_date&group_by=day|month|category`
Res: `{ period: string, total_sales: number, total_orders: number, data: Array<{label, value}> }`

**15. GET /reports/inventory** → 200
_Role: manager+_
Res: `{ total_items: number, by_category: {category: count}, by_status: {status: count}, low_stock: JewelleryItem[] }`
Notes: low_stock defined as quantity < 5

### User Management (Priority 2)

**16. GET /users** → 200
_Role: owner only_
Query: `?page=1&limit=20&role?`
Res: `{ users: User[], page: number, total: number }`

**17. DELETE /users/{id}** → 204
_Role: owner only_
Notes: Cannot delete self

---

## Role-Based Access Control (RBAC)

### Permission Matrix

| Endpoint | Public | Staff | Manager | Owner |
|----------|--------|-------|---------|-------|
| POST /auth/register | ❌ | ❌ | ❌ | ✅ |
| POST /auth/login | ✅ | ✅ | ✅ | ✅ |
| GET /catalog | ✅ | ✅ | ✅ | ✅ |
| GET /catalog/{id} | ✅ | ✅ | ✅ | ✅ |
| POST /orders | ✅ | ✅ | ✅ | ✅ |
| GET /orders/customer/{email} | ✅ (own) | ✅ | ✅ | ✅ |
| GET /inventory | ❌ | ✅ | ✅ | ✅ |
| POST /inventory | ❌ | ✅ | ✅ | ✅ |
| PATCH /inventory/{id} | ❌ | ✅ | ✅ | ✅ |
| DELETE /inventory/{id} | ❌ | ❌ | ✅ | ✅ |
| GET /orders | ❌ | ✅ | ✅ | ✅ |
| GET /orders/{id} | ❌ | ✅ | ✅ | ✅ |
| PATCH /orders/{id}/status | ❌ | ✅ | ✅ | ✅ |
| GET /reports/* | ❌ | ❌ | ✅ | ✅ |
| GET /users | ❌ | ❌ | ❌ | ✅ |
| DELETE /users/{id} | ❌ | ❌ | ❌ | ✅ |

---

## User Flow

### Public Customer Flow
1. Browse catalog (GET /catalog with filters)
2. View item details (GET /catalog/{id})
3. Place COD order (POST /orders)
4. Track order status (GET /orders/customer/{email})

### Staff Flow
1. Login (POST /auth/login)
2. View all orders (GET /orders)
3. Update order status (PATCH /orders/{id}/status)
4. Manage inventory (GET/POST/PATCH /inventory)

### Manager Flow
1. All staff capabilities
2. Delete inventory items (DELETE /inventory/{id})
3. View reports (GET /reports/sales, GET /reports/inventory)

### Owner Flow
1. All manager capabilities
2. Create user accounts (POST /auth/register)
3. Manage users (GET /users, DELETE /users/{id})

---

## Validation Rules

### Item Code
- Unique across all items
- Mandatory field (cannot be null/empty)
- 3-50 characters
- Alphanumeric, dash, underscore allowed
- Case-insensitive uniqueness check

### Numeric Fields
- price: integer >= 0 (cents)
- weight: float > 0 (grams)
- quantity: integer >= 0

### String Fields
- email: valid email format
- password: minimum 8 characters
- phone: 10-15 digits, optional country code
- zip: 5-10 characters

### Arrays
- images: minimum 1 URL, maximum 10
- order items: minimum 1 item, maximum 50

### Status Transitions
- Order: pending → confirmed → processing → shipped → delivered
- Order can be cancelled from any state except delivered
- Item status changes validated based on inventory count

---

## Error Codes

| Code | Message | HTTP Status |
|------|---------|-------------|
| AUTH_REQUIRED | Authentication required | 401 |
| INVALID_TOKEN | Invalid or expired token | 401 |
| INSUFFICIENT_PERMISSION | User role lacks permission | 403 |
| NOT_FOUND | Resource not found | 404 |
| DUPLICATE_ITEM_CODE | Item code already exists | 409 |
| INVALID_INPUT | Validation failed | 400 |
| INSUFFICIENT_STOCK | Requested quantity unavailable | 400 |
| INVALID_STATUS_TRANSITION | Invalid order status change | 400 |

---

## Non-Functional Requirements

### Performance
- API response time: < 500ms for reads, < 1s for writes
- Support 100 concurrent users
- Pagination default: 20 items, max: 100

### Security
- JWT tokens expire after 24 hours
- Passwords hashed with bcrypt (cost factor 12)
- HTTPS required in production
- Rate limiting: 100 requests/minute per IP

### Database Indexes
- `users`: email (unique), username (unique)
- `jewellery_items`: item_code (unique), category, status
- `orders`: customer_email, status, created_at

### Data Retention
- Orders: retained indefinitely
- Deleted items: soft delete with 90-day retention
- User logs: 1-year retention

---

## Implementation Priority

**Phase 1 (MVP - Week 1-2):**
- Endpoints 1-10
- JWT authentication
- RBAC middleware
- Basic validation

**Phase 2 (Post-MVP - Week 3):**
- Endpoints 11-17
- Advanced reporting
- Search optimization
- Image upload handling

**Phase 3 (Enhancement - Week 4+):**
- Email notifications
- SMS order updates
- Advanced analytics
- Inventory forecasting