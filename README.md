# JewelCraft Pro - Jewellery Store Management System

A full-stack web application for managing a jewellery store with public catalog and admin dashboard.

## Features

### Public Features
- Browse jewellery catalog with filtering and search
- View detailed product information
- Place COD (Cash on Delivery) orders
- Responsive design for mobile and desktop

### Admin Features
- **Authentication**: JWT-based login with role-based access
- **Inventory Management**: Add, edit, delete jewellery items
- **Order Management**: View and update order status
- **User Management**: Create staff and manager accounts (owner only)
- **Dashboard**: Quick stats and actions

### Role Hierarchy
- **Staff**: Manage inventory (add/edit), view orders
- **Manager**: Staff permissions + delete items, view reports
- **Owner**: Full access including user management

## Tech Stack

### Backend
- FastAPI (Python)
- MongoDB (AsyncIOMotorClient)
- JWT authentication (bcrypt password hashing)
- Pydantic for validation

### Frontend
- React 19
- React Router v7
- Tailwind CSS
- Axios for API calls

## Default Credentials

**Owner Account:**
- Email: `owner@jewelcraft.com`
- Password: `OwnerPass123`

⚠️ **Change this password in production!**

## Quick Start

The application is already running:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs

### Test the Application
1. Visit http://localhost:3000 to see the public catalog
2. Click "Admin" or visit /login to access admin dashboard
3. Use owner credentials above to login
4. Explore inventory management, orders, and user management

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Register user (owner only)
- `GET /api/auth/me` - Get current user

### Public Catalog
- `GET /api/catalog` - Get catalog items
- `GET /api/catalog/:id` - Get single item

### Inventory (Staff+)
- `GET /api/inventory` - List all items
- `POST /api/inventory` - Add new item
- `PATCH /api/inventory/:id` - Update item
- `DELETE /api/inventory/:id` - Delete item (manager+)

### Orders
- `POST /api/orders` - Place order (public)
- `GET /api/orders` - List orders (staff+)
- `PATCH /api/orders/:id/status` - Update order status

## Testing

### Backend API Tests
```bash
cd backend
python -m pytest tests/test_jewellery_api.py -v
```

✅ All 20 tests passing, covering:
- Authentication and authorization
- Inventory CRUD operations
- Order placement and management
- Duplicate item code validation
- Stock management
- Public catalog access

## Key Features

### Mandatory Item Code
Each jewellery item must have a unique `item_code` field. Case-insensitive uniqueness enforced.

### COD Payment
All orders use Cash on Delivery. No online payment processing required for MVP.

### Inventory Management
- Staff can add/edit items
- Managers can delete items
- Soft delete for items with order history
- Automatic stock reduction on order placement

### Order Flow
1. Customer browses public catalog
2. Places order with shipping details
3. Staff receives order (status: pending)
4. Staff updates status through lifecycle
5. Inventory automatically updated

## Project Structure

```
.
├── backend/
│   ├── server.py           # Main FastAPI app (834 lines)
│   ├── create_owner.py     # Bootstrap script
│   ├── requirements.txt
│   └── tests/
│       └── test_jewellery_api.py (20 tests)
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── contexts/
│   │   │   └── AuthContext.js  # Auth state management
│   │   ├── api/
│   │   │   └── client.js       # API client
│   │   └── pages/
│   │       ├── HomePage.js            # Public landing
│   │       ├── CatalogPage.js         # Browse products
│   │       ├── ProductDetailPage.js   # Order placement
│   │       ├── LoginPage.js           # Admin auth
│   │       ├── DashboardPage.js       # Admin home
│   │       ├── InventoryPage.js       # Manage items
│   │       ├── OrdersPage.js          # Manage orders
│   │       └── UsersPage.js           # Manage users
│   └── package.json
└── plan/
    ├── api-contract.md      # Complete API specification
    ├── design-system.md     # UI/UX design system
    └── website-ux-plan-v1.md  # User experience plan
```

## Security Features
- JWT tokens (24-hour expiration)
- Bcrypt password hashing
- Role-based access control
- Protected API routes
- CORS configuration

## Implementation Summary

**Backend**: 10+ RESTful endpoints with MongoDB, JWT auth, role-based access control, and comprehensive testing.

**Frontend**: 8 pages (3 public, 5 admin) with React Router, protected routes, and responsive Tailwind CSS styling.

**Database**: MongoDB collections for users, jewellery_items, and orders with proper indexing.

All MVP requirements met:
✅ Public catalog with COD orders
✅ Role-based admin dashboard (staff/manager/owner)
✅ Inventory management with unique item codes
✅ Order tracking and status updates
✅ User management (owner only)
✅ Fully tested backend (20/20 tests passing)

## License
MIT
