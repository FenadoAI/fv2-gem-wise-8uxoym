# Jewellery Store Management System - Website UX Plan v1

## Project Name and Description

**Project Name:** JewelCraft Pro

**Tagline:** Elegant Jewellery, Simplified Management

**Description:**
JewelCraft Pro is a comprehensive jewellery store management system designed for modern jewellery retailers. The platform combines a beautiful public-facing catalog for customers to browse and purchase exquisite jewellery pieces with a powerful admin dashboard for store staff, managers, and owners to manage inventory, process orders, and analyze business performance. Built with efficiency and elegance in mind, JewelCraft Pro streamlines every aspect of jewellery retail operations while providing customers with a seamless shopping experience for gold, silver, platinum, and precious stone jewellery.

---

## Landing Page (Public Homepage)

### Hero Section

**Main Headline:** Discover Timeless Elegance

**Sub Headline:** Browse our curated collection of fine jewellery crafted with precision and passion. From classic gold rings to contemporary platinum designs, find pieces that tell your story.

**Call-to-Action Buttons:**
- **Primary CTA:** "Explore Collection" → Navigate to /catalog page
- **Secondary CTA:** "View Featured Items" → Smooth scroll to featured section below

### Featured Items Section

**Section Title:** Featured Collection

**Content:**
Display 6-8 featured jewellery items in a grid layout. Each item card shows:
- High-quality product image
- Item name
- Price (formatted with currency symbol)
- Metal type badge (e.g., "24K Gold", "Platinum")
- Category tag (e.g., "Ring", "Necklace")
- Quick view button → Opens product detail popup

**Image Suggestion:** Use high-resolution stock images of luxury jewellery pieces with white or subtle gradient backgrounds. Each image should showcase the jewellery on elegant display stands or lifestyle shots with hands/neck wearing the pieces.

### Features Section

**Section Title:** Why Choose JewelCraft Pro

**Features List:**

1. **Authentic Craftsmanship**
   - Every piece is crafted with certified metals and genuine gemstones, backed by authenticity certificates and quality guarantees.

2. **Secure Cash on Delivery**
   - Shop with confidence using our secure COD payment option. Pay only when you receive your jewellery at your doorstep.

3. **Wide Selection**
   - Explore rings, necklaces, bracelets, earrings, pendants, bangles, and chains in gold, silver, platinum, white gold, and rose gold.

4. **Easy Order Tracking**
   - Track your order status from confirmation to delivery with email updates at every step.

5. **Expert Guidance**
   - Our team provides personalized assistance to help you choose the perfect piece for any occasion.

6. **Quality Assurance**
   - Each item undergoes rigorous quality checks and comes with detailed specifications including weight, metal type, and stone details.

### Testimonials Section

**Section Title:** What Our Customers Say

**Testimonials:**

1. **Quote:** "The gold necklace I ordered exceeded my expectations. The craftsmanship is impeccable and the COD option made it so convenient!"
   - **Author:** Sarah Mitchell
   - **Location:** New York, NY
   - **Rating:** 5 stars

2. **Quote:** "Amazing collection and seamless ordering process. My platinum engagement ring arrived beautifully packaged and exactly as shown online."
   - **Author:** James Rodriguez
   - **Location:** Los Angeles, CA
   - **Rating:** 5 stars

3. **Quote:** "I've ordered multiple pieces from JewelCraft Pro and each one has been stunning. The order tracking kept me informed throughout delivery."
   - **Author:** Priya Sharma
   - **Location:** Chicago, IL
   - **Rating:** 5 stars

**Image Suggestion:** Use professional headshot stock images or subtle avatar illustrations for testimonial authors.

### Call-to-Action Section

**Section Title:** Ready to Find Your Perfect Piece?

**Description:** Start browsing our collection today and discover jewellery that speaks to your style.

**CTA Button:** "Shop Now" → Navigate to /catalog page

**Image Suggestion:** Full-width banner image showing an elegant jewellery collection display or a lifestyle shot of someone wearing multiple jewellery pieces in a luxurious setting.

### Footer

**Company Info:**
- Logo (use the generated logo as favicon/icon)
- Tagline: "Elegant Jewellery, Simplified Management"

**Quick Links:**
- Home (/)
- Catalog (/catalog)
- Track Order (/track-order)
- Admin Login (/admin/login)

**Contact Information:**
- Email: contact@jewelcraftpro.com
- Phone: +1 (555) 123-4567
- Address: 123 Jewel Street, New York, NY 10001

**Social Media:**
- Instagram icon (placeholder link)
- Facebook icon (placeholder link)
- Pinterest icon (placeholder link)

**Copyright:** © 2025 JewelCraft Pro. All rights reserved.

**Note on Images:**
- **Logo:** Use AI-generated logo via generate image MCP tool with the prompt: "Create a sleek and modern abstract logo for a luxury jewellery retail startup named 'JewelCraft Pro', using only minimalist geometric shapes and a deep purple and gold color scheme. Do not include any typography. The design should convey elegance, luxury, and craftsmanship purely through abstract visual elements, suitable for both digital and print media. No typography."
- Use this logo as favicon/icon in index.html instead of logo.png
- **Product Images:** Use high-quality stock images of jewellery pieces from free stock photo websites or request developer to use placeholder elegant jewellery images
- **Lifestyle Images:** Include 2-3 lifestyle shots showing jewellery being worn in elegant settings for hero and CTA sections

---

## Public Catalog Pages

### Catalog Page (/catalog)

**Page Title:** Our Collection

**Layout Components:**

1. **Page Header**
   - Title: "Explore Our Collection"
   - Subtitle: "Discover [X] exquisite pieces" (dynamic count)

2. **Filters Sidebar (Left)**
   - **Category Filter:** Checkboxes for Ring, Necklace, Bracelet, Earring, Pendant, Bangle, Chain, Other
   - **Metal Type Filter:** Checkboxes for Gold, Silver, Platinum, White Gold, Rose Gold
   - **Price Range Filter:** Min-Max input fields with "Apply" button
   - **Search Box:** Text input with search icon "Search by name or code..."
   - **Clear Filters Button:** Reset all filters

3. **Product Grid (Right)**
   - Display items in 3-column grid (responsive: 2 on tablet, 1 on mobile)
   - Each product card shows:
     - Image (primary image from images array)
     - Item code (small, subtle text)
     - Item name (bold)
     - Category badge
     - Metal type badge with icon
     - Weight (e.g., "12.5g")
     - Price (large, prominent)
     - Stones info if available (small text)
     - "View Details" button → Navigate to /catalog/{id}

4. **Pagination**
   - Show page numbers with Previous/Next buttons
   - Display "Showing X-Y of Z items"

**API Integration:**
- GET /catalog with query parameters for filters, search, and pagination

**Empty State:**
- If no items found: Show message "No items match your filters. Try adjusting your search criteria."

### Product Detail Page (/catalog/{id})

**Layout Components:**

1. **Product Images Section (Left)**
   - Large main image display
   - Thumbnail strip below (if multiple images)
   - Image zoom on hover
   - Image gallery navigation arrows

2. **Product Details Section (Right)**
   - Item code (displayed prominently)
   - Item name (large heading)
   - Price (very large, bold)
   - Category and status badges
   - **Specifications Table:**
     - Metal Type: [value]
     - Weight: [value]g
     - Stones: [value] (if available)
     - Status: In Stock
   - Description (full text, formatted paragraphs)
   - **Quantity Selector:** Number input (min: 1, max: available quantity)
   - **Add to Order Button** → Opens order popup/dialog

3. **Additional Information Tabs**
   - Care Instructions (generic jewellery care tips)
   - Authenticity Guarantee (information about certificates)

**API Integration:**
- GET /catalog/{id}

**Error State:**
- If item not found or out of stock: Show appropriate message and suggest similar items

### Order Placement Popup/Dialog

**Trigger:** Clicking "Add to Order" or "Place Order" from product detail page

**Dialog Title:** Complete Your Order

**Content:**

1. **Order Summary Section (Top)**
   - Show selected item(s) with image, name, quantity, and price
   - Display subtotal for each item
   - Display total amount (bold, large)

2. **Customer Information Form**
   - Full Name (required)
   - Email Address (required)
   - Phone Number (required)

3. **Shipping Address Form**
   - Address Line 1 (required)
   - Address Line 2 (optional)
   - City (required)
   - State (required)
   - ZIP Code (required)
   - Country (required, default: "United States")

4. **Additional Notes**
   - Textarea for special instructions (optional)

5. **Payment Method**
   - Display: "Cash on Delivery (COD)" with icon (non-editable, informational)
   - Small text: "Pay securely when you receive your order"

6. **Action Buttons**
   - **Cancel Button:** Close dialog
   - **Place Order Button:** Submit order (calls POST /orders)

**Validation:**
- All required fields must be filled
- Email format validation
- Phone number format validation (10-15 digits)

**API Integration:**
- POST /orders

**Success State:**
- On successful order: Close dialog and navigate to /order-confirmation/{order_id}

**Error State:**
- Show error message if stock insufficient or order fails

### Order Confirmation Page (/order-confirmation/{order_id})

**Page Title:** Order Confirmed!

**Layout Components:**

1. **Success Message**
   - Large checkmark icon
   - Heading: "Your Order Has Been Placed Successfully!"
   - Subheading: "Order ID: {order_id}"

2. **Order Details Card**
   - **Customer Information:**
     - Name
     - Email
     - Phone
   - **Shipping Address:**
     - Full address display
   - **Order Items:**
     - List each item with image, name, quantity, and price
   - **Payment Method:** Cash on Delivery (COD)
   - **Total Amount:** Display prominently

3. **What Happens Next Section**
   - Step 1: "We'll confirm your order within 24 hours"
   - Step 2: "Your jewellery will be carefully prepared and packaged"
   - Step 3: "You'll receive tracking updates via email"
   - Step 4: "Pay when you receive your order at your doorstep"

4. **Action Buttons**
   - **Track Your Order Button:** Navigate to /track-order
   - **Continue Shopping Button:** Navigate to /catalog

**Note:** This page should be accessible without authentication, using the order_id in the URL

### Order Tracking Page (/track-order)

**Page Title:** Track Your Order

**Layout Components:**

1. **Email Input Form**
   - Text input: "Enter your email address"
   - Submit button: "Track Orders"

2. **Orders List (After Submission)**
   - Display all orders for entered email
   - Each order card shows:
     - Order ID
     - Order date
     - Total amount
     - Current status (with color-coded badge)
     - "View Details" expandable section showing:
       - All order items with images
       - Shipping address
       - Status timeline visualization

3. **Status Timeline Visualization**
   - Visual progress bar showing: Pending → Confirmed → Processing → Shipped → Delivered
   - Highlight current status
   - Show checkmarks for completed stages

**API Integration:**
- GET /orders/customer/{email}

**Empty State:**
- If no orders found: "No orders found for this email address"

---

## Admin Login & Dashboard

### Admin Login Page (/admin/login)

**Page Title:** Admin Login

**Layout Components:**

1. **Login Card (Center of Page)**
   - Logo at top
   - Heading: "Welcome Back"
   - Subheading: "Log in to manage your jewellery store"

2. **Login Form**
   - Email Address (required)
   - Password (required, with show/hide toggle)
   - "Remember me" checkbox
   - **Login Button:** Submit form (calls POST /auth/login)

3. **Error Message Area**
   - Show authentication errors prominently

**API Integration:**
- POST /auth/login
- Store JWT token in localStorage/sessionStorage
- Redirect to /admin/dashboard on success

**Design Note:**
- Clean, professional design with brand colors
- Background: Subtle gradient or jewellery-themed pattern

### Admin Dashboard (/admin/dashboard)

**Layout:** Sidebar navigation + main content area

**Sidebar Navigation (Role-Based):**

**All Roles:**
- Dashboard (home icon)
- Inventory Management (box icon)
- Order Management (shopping bag icon)

**Manager & Owner Only:**
- Reports (chart icon)

**Owner Only:**
- User Management (users icon)

**Bottom of Sidebar:**
- User profile section showing:
  - Username
  - Role badge
  - Logout button

**Dashboard Main Content (Role-Specific Widgets):**

**All Roles See:**

1. **Welcome Widget**
   - "Welcome back, [Username]!"
   - Current date and time

2. **Quick Stats Row**
   - Total Inventory Items (with icon)
   - Pending Orders (with icon)
   - Low Stock Alerts (quantity < 5, with warning icon)

3. **Recent Orders Widget**
   - Table showing last 10 orders
   - Columns: Order ID, Customer Name, Total Amount, Status, Date
   - "View All" link → Navigate to /admin/orders

4. **Low Stock Alerts Widget**
   - List of items with quantity < 5
   - Show item code, name, current quantity
   - "Restock" button → Navigate to /admin/inventory/edit/{id}

**Manager & Owner Additional Widgets:**

5. **Sales Summary Widget**
   - Today's sales (count and amount)
   - This week's sales
   - This month's sales
   - Small line chart visualization

6. **Inventory by Category Widget**
   - Pie chart showing item distribution by category

**Owner Only Additional Widget:**

7. **User Management Quick Access**
   - Total staff count
   - Total manager count
   - "Manage Users" button → Navigate to /admin/users

**API Integration:**
- GET /inventory (for stats and low stock)
- GET /orders (for recent orders and pending count)
- GET /reports/sales (for manager/owner)
- GET /reports/inventory (for manager/owner)
- GET /users (for owner)

---

## Admin Inventory Management

### Inventory List Page (/admin/inventory)

**Page Title:** Inventory Management

**Layout Components:**

1. **Page Header**
   - Title: "Inventory Management"
   - **Add New Item Button** → Opens add item dialog

2. **Filters Bar (Top)**
   - Search input (search by code, name, description)
   - Category dropdown filter
   - Status dropdown filter (all, in_stock, sold, reserved, discontinued)
   - Apply Filters button

3. **Inventory Table**
   - Columns:
     - Image (thumbnail)
     - Item Code
     - Name
     - Category
     - Metal Type
     - Price
     - Quantity
     - Status (color-coded badge)
     - Actions (Edit, Delete buttons)
   - Sortable columns (click header to sort)
   - Row highlighting for low stock (quantity < 5)

4. **Pagination Controls**
   - Page numbers, Previous/Next
   - Items per page selector (20, 50, 100)

**Actions:**
- **Edit Button:** Navigate to edit form or open edit dialog
- **Delete Button:** Show confirmation dialog (Manager/Owner only)

**API Integration:**
- GET /inventory with filters and pagination

### Add/Edit Item Dialog

**Dialog Title:** "Add New Item" or "Edit Item: {item_code}"

**Form Fields (All Required Unless Noted):**

1. **Basic Information Tab**
   - Item Code (unique, disabled when editing)
   - Item Name
   - Category (dropdown)
   - Status (dropdown)
   - Description (textarea)

2. **Specifications Tab**
   - Metal Type (dropdown)
   - Weight (grams, decimal input)
   - Price (USD, converts to cents on submit)
   - Quantity (integer input)
   - Stones (optional, textarea for details)

3. **Images Tab**
   - Image URL inputs (minimum 1, maximum 10)
   - "Add Image URL" button to add more fields
   - Preview thumbnails for entered URLs
   - Note: "Enter full image URLs. Accepted formats: JPG, PNG, WEBP"

**Action Buttons:**
- **Cancel:** Close dialog without saving
- **Save Item:** Submit form (POST /inventory or PATCH /inventory/{id})

**Validation:**
- Item code: unique, 3-50 characters
- Price: must be >= 0
- Weight: must be > 0
- Quantity: must be >= 0
- At least 1 image URL required

**API Integration:**
- POST /inventory (for new items)
- PATCH /inventory/{id} (for edits)

**Success State:**
- Show success toast message
- Close dialog
- Refresh inventory table

**Error State:**
- Display validation errors inline
- Show error toast for duplicate item code

### Delete Confirmation Dialog

**Dialog Title:** Delete Item?

**Content:**
- "Are you sure you want to delete item: {item_code} - {item_name}?"
- Warning: "If this item has order history, it will be marked as discontinued instead of permanently deleted."

**Action Buttons:**
- **Cancel:** Close dialog
- **Delete:** Confirm deletion (DELETE /inventory/{id})

**API Integration:**
- DELETE /inventory/{id}

---

## Admin Order Management

### Orders List Page (/admin/orders)

**Page Title:** Order Management

**Layout Components:**

1. **Page Header**
   - Title: "Order Management"
   - Subtitle: "View and manage customer orders"

2. **Filters Bar**
   - Search by Order ID or Customer Name
   - Status dropdown filter (all, pending, confirmed, processing, shipped, delivered, cancelled)
   - Date range picker (From Date - To Date)
   - Apply Filters button
   - Clear Filters button

3. **Orders Table**
   - Columns:
     - Order ID (clickable → opens detail view)
     - Customer Name
     - Customer Email
     - Total Amount
     - Status (color-coded badge)
     - Order Date
     - Actions (View Details, Update Status buttons)
   - Color coding:
     - Pending: Yellow
     - Confirmed: Blue
     - Processing: Purple
     - Shipped: Orange
     - Delivered: Green
     - Cancelled: Red

4. **Pagination Controls**

**Actions:**
- **View Details Button:** Opens order detail dialog
- **Update Status Button:** Opens status update dialog

**API Integration:**
- GET /orders with filters and pagination

### Order Detail Dialog

**Dialog Title:** Order Details - {order_id}

**Content Sections:**

1. **Order Information**
   - Order ID
   - Order Date
   - Current Status (large badge)
   - Payment Method: COD

2. **Customer Information**
   - Name
   - Email (clickable mailto link)
   - Phone (clickable tel link)

3. **Shipping Address**
   - Full address display formatted

4. **Order Items Table**
   - Columns: Item Code, Name, Quantity, Price, Subtotal
   - Show item images as thumbnails
   - Display total amount (bold)

5. **Customer Notes**
   - Display notes if any

6. **Status History** (if implemented)
   - Timeline showing status changes with timestamps

**Action Buttons:**
- **Update Status:** Opens status update dialog
- **Close:** Close dialog

**API Integration:**
- GET /orders/{id}

### Update Order Status Dialog

**Dialog Title:** Update Order Status

**Content:**
- Current Status: {current_status} (display prominently)
- New Status: Dropdown with valid next statuses
  - From Pending: Confirmed, Cancelled
  - From Confirmed: Processing, Cancelled
  - From Processing: Shipped, Cancelled
  - From Shipped: Delivered
  - From Delivered: (no changes allowed)
  - Any status can go to Cancelled (except Delivered)

**Form Fields:**
- Status (dropdown, pre-filtered based on current status)
- Notes (optional textarea for status change reason)

**Action Buttons:**
- **Cancel:** Close dialog
- **Update Status:** Submit (PATCH /orders/{id}/status)

**Validation:**
- Prevent invalid status transitions
- Show error if trying to change delivered order

**API Integration:**
- PATCH /orders/{id}/status

**Success State:**
- Show success toast
- Close dialog
- Refresh orders table

---

## Admin Reports Pages (Manager & Owner Only)

### Reports Dashboard (/admin/reports)

**Page Title:** Business Reports

**Layout Components:**

1. **Page Header**
   - Title: "Business Reports & Analytics"
   - Date Range Selector (From Date - To Date) with "Apply" button

2. **Sales Reports Section**

   **Sales Summary Cards Row:**
   - Total Sales (amount)
   - Total Orders (count)
   - Average Order Value
   - Orders by Status (mini breakdown)

   **Sales Chart:**
   - Line/Bar chart showing sales over time
   - Toggle buttons: "By Day" | "By Month" | "By Category"
   - Responsive chart using chart library (Chart.js or Recharts)

   **Top Categories Table:**
   - Columns: Category, Total Sales, Order Count, Average Price
   - Sorted by total sales descending

3. **Inventory Reports Section**

   **Inventory Summary Cards Row:**
   - Total Items
   - Total Value (sum of price × quantity)
   - Low Stock Items (quantity < 5)
   - Out of Stock Items (quantity = 0)

   **Inventory Distribution Charts:**
   - Pie chart: Items by Category
   - Pie chart: Items by Status
   - Bar chart: Items by Metal Type

   **Low Stock Alert Table:**
   - Columns: Item Code, Name, Category, Current Quantity, Status
   - Highlight rows in warning color
   - "Restock" action button → Navigate to edit item

**API Integration:**
- GET /reports/sales with date range and grouping parameters
- GET /reports/inventory

**Export Options:**
- "Export to CSV" buttons for tables (can be future enhancement)

---

## Admin User Management (Owner Only)

### Users List Page (/admin/users)

**Page Title:** User Management

**Layout Components:**

1. **Page Header**
   - Title: "User Management"
   - **Add New User Button** → Opens create user dialog

2. **Filters Bar**
   - Role filter dropdown (All, Staff, Manager, Owner)
   - Search by username or email

3. **Users Table**
   - Columns:
     - Username
     - Email
     - Role (color-coded badge)
     - Created At
     - Actions (Edit, Delete buttons)
   - Role badges:
     - Staff: Gray
     - Manager: Blue
     - Owner: Purple

**Actions:**
- **Delete Button:** Opens confirmation dialog (cannot delete self)

**API Integration:**
- GET /users with filters

### Create User Dialog

**Dialog Title:** Add New User

**Form Fields:**
- Username (required, 3-50 chars, alphanumeric + underscore)
- Email (required, valid email format)
- Password (required, min 8 chars)
- Confirm Password (must match)
- Role (dropdown: Staff, Manager, Owner)

**Action Buttons:**
- **Cancel:** Close dialog
- **Create User:** Submit (POST /auth/register)

**Validation:**
- All fields required
- Password strength indicator
- Email format validation
- Username uniqueness check (server-side)

**API Integration:**
- POST /auth/register

**Success State:**
- Show success toast with username
- Close dialog
- Refresh users table

**Error State:**
- Display validation errors inline
- Show error toast for duplicate username/email

### Delete User Confirmation Dialog

**Dialog Title:** Delete User?

**Content:**
- "Are you sure you want to delete user: {username} ({email})?"
- Warning: "This action cannot be undone."
- Prevent deletion if trying to delete self: "You cannot delete your own account."

**Action Buttons:**
- **Cancel:** Close dialog
- **Delete User:** Confirm (DELETE /users/{id})

**API Integration:**
- DELETE /users/{id}

---

## Navigation Structure

### Public Navigation (Header)

**Layout:** Horizontal navigation bar with logo on left

**Menu Items:**
- Home (/)
- Catalog (/catalog)
- Track Order (/track-order)
- Admin Login (/admin/login) - Subtle link on far right

**Mobile:** Hamburger menu with same items

### Admin Navigation (Sidebar)

**Layout:** Vertical sidebar, always visible on desktop, collapsible on mobile

**Menu Items (Role-Based):**

**All Authenticated Users:**
- Dashboard (/admin/dashboard)
- Inventory (/admin/inventory)
- Orders (/admin/orders)

**Manager & Owner:**
- Reports (/admin/reports)

**Owner Only:**
- Users (/admin/users)

**Footer Section:**
- User Profile Card (username, role)
- Logout Button

**Active State:** Highlight current page in navigation

---

## Popups & Dialogs Strategy

### Dialog Usage (Minimizes Page Count)

1. **Order Placement Dialog**
   - Triggered from product detail page
   - Contains full order form
   - Avoids separate checkout page

2. **Add/Edit Inventory Dialog**
   - Triggered from inventory list
   - Tabbed form for all item fields
   - Avoids separate add/edit pages

3. **Update Order Status Dialog**
   - Triggered from orders table
   - Quick status update form
   - Avoids separate order edit page

4. **Create User Dialog**
   - Triggered from users list
   - Registration form for new users
   - Avoids separate registration page

5. **Confirmation Dialogs**
   - Delete item confirmation
   - Delete user confirmation
   - Standardized confirmation pattern

6. **Order Detail Dialog**
   - Full order information view
   - Can be expanded to edit mode
   - Avoids separate order detail page

### Dialog Design Standards

- **Overlay:** Semi-transparent dark background
- **Size:** Medium (600px max width) for forms, Large (900px) for detailed views
- **Animation:** Smooth fade-in/scale animation
- **Accessibility:** Focus trap, ESC to close, proper ARIA labels
- **Mobile:** Full-screen on small devices

---

## User Flows

### User Flow 1: Customer Places COD Order

**Goal:** Customer discovers a jewellery item and completes a COD order

**Steps:**

1. ✅ Customer lands on homepage (/)
2. ✅ Clicks "Explore Collection" CTA
3. ✅ Navigates to catalog page (/catalog)
4. ✅ Uses filters to narrow search:
   - Selects "Ring" category
   - Selects "Gold" metal type
   - Clicks Apply
5. ✅ Views filtered results (API: GET /catalog with filters)
6. ✅ Clicks "View Details" on a ring
7. ✅ Navigates to product detail page (/catalog/{id})
8. ✅ Reviews item specifications, images, and description
9. ✅ Selects quantity (default: 1)
10. ✅ Clicks "Add to Order" button
11. ✅ Order placement dialog opens
12. ✅ Reviews order summary in dialog
13. ✅ Fills out customer information:
    - Full name
    - Email address
    - Phone number
14. ✅ Fills out shipping address:
    - Address lines
    - City, State, ZIP
    - Country
15. ✅ Adds optional notes
16. ✅ Confirms payment method (COD displayed)
17. ✅ Clicks "Place Order" button
18. ✅ Order submitted (API: POST /orders)
19. ✅ Redirected to order confirmation page (/order-confirmation/{order_id})
20. ✅ Views order confirmation with order ID and details
21. ✅ Receives on-screen instructions about next steps
22. ✅ Can track order using email via "Track Your Order" button

**Success Criteria:**
- Order created in database with status "pending"
- Customer receives order ID
- Order confirmation page displays all order details
- Customer can track order using email

---

### User Flow 2: Staff Member Adds New Inventory Item

**Goal:** Staff member logs in and adds a new jewellery item to inventory

**Steps:**

1. ✅ Staff member navigates to admin login (/admin/login)
2. ✅ Enters email and password
3. ✅ Clicks "Login" button
4. ✅ Authentication successful (API: POST /auth/login)
5. ✅ JWT token stored in browser
6. ✅ Redirected to admin dashboard (/admin/dashboard)
7. ✅ Views dashboard widgets and stats
8. ✅ Clicks "Inventory Management" in sidebar
9. ✅ Navigates to inventory list (/admin/inventory)
10. ✅ Views existing inventory items table
11. ✅ Clicks "Add New Item" button
12. ✅ Add item dialog opens
13. ✅ Fills out Basic Information tab:
    - Item Code: "GR-001-24K"
    - Item Name: "Classic Gold Wedding Ring"
    - Category: "Ring"
    - Status: "In Stock"
    - Description: "Elegant 24K gold wedding band..."
14. ✅ Switches to Specifications tab
15. ✅ Fills out specifications:
    - Metal Type: "Gold"
    - Weight: 12.5 (grams)
    - Price: 1599.99 (USD)
    - Quantity: 10
    - Stones: "None"
16. ✅ Switches to Images tab
17. ✅ Enters image URLs (at least 1)
18. ✅ Clicks "Save Item" button
19. ✅ Item created (API: POST /inventory)
20. ✅ Success toast message appears
21. ✅ Dialog closes
22. ✅ Inventory table refreshes showing new item
23. ✅ New item appears in the table with all details

**Success Criteria:**
- New item created in database
- Item appears in inventory table
- Item is visible in public catalog
- All specifications correctly saved

---

### User Flow 3: Manager Views Sales Reports

**Goal:** Manager logs in to analyze sales performance and inventory status

**Steps:**

1. ✅ Manager navigates to admin login (/admin/login)
2. ✅ Logs in with manager credentials
3. ✅ Redirected to dashboard (/admin/dashboard)
4. ✅ Views dashboard including sales summary widget (available to managers)
5. ✅ Clicks "Reports" in sidebar navigation
6. ✅ Navigates to reports page (/admin/reports)
7. ✅ Page loads with default date range (last 30 days)
8. ✅ Views sales summary cards:
   - Total sales amount
   - Total orders count
   - Average order value
   - Orders by status breakdown
9. ✅ Views sales chart showing daily trends
10. ✅ Clicks "By Category" toggle
11. ✅ Chart updates to show sales by category (API: GET /reports/sales?group_by=category)
12. ✅ Reviews top categories table
13. ✅ Scrolls to inventory reports section
14. ✅ Views inventory summary cards
15. ✅ Reviews inventory distribution pie charts
16. ✅ Checks low stock alert table
17. ✅ Identifies items needing restock
18. ✅ Clicks "Restock" on a low stock item
19. ✅ Navigates to edit item dialog
20. ✅ Updates quantity
21. ✅ Saves changes (API: PATCH /inventory/{id})
22. ✅ Returns to reports to verify update

**Success Criteria:**
- Manager can view comprehensive sales data
- Charts visualize data clearly
- Inventory status is accessible
- Low stock items are easily identifiable
- Manager can take action (restock) directly from reports

---

## Content Strategy

### Tone & Voice

**Brand Voice:** Elegant, professional, trustworthy, and sophisticated

**Writing Style:**
- Clear and concise
- Focus on quality and craftsmanship
- Emphasize security and authenticity
- Use jewellery industry terminology appropriately
- Maintain luxury brand positioning

### Copy Guidelines

**Product Descriptions:**
- Highlight metal purity (e.g., "24K Gold", "950 Platinum")
- Mention craftsmanship and quality
- Include care instructions where relevant
- Describe occasions suitable for each piece

**Admin Interface:**
- Use professional, task-oriented language
- Clear labels for all actions
- Helpful error messages with solution suggestions
- Confirmation messages for successful actions

**Customer-Facing Content:**
- Reassuring language about COD security
- Clear order tracking instructions
- Transparent shipping and delivery information
- Helpful guidance for choosing jewellery

### Image Requirements

**Product Images:**
- High resolution (minimum 1200x1200px)
- White or subtle background
- Multiple angles (front, side, worn)
- Close-ups showing detail and craftsmanship
- Consistent lighting and style across catalog

**Lifestyle Images:**
- Professional photography
- Diverse models wearing jewellery
- Elegant, aspirational settings
- Natural lighting preferred

**Logo & Branding:**
- Use AI-generated abstract logo (no typography)
- Color scheme: Deep purple (#6B46C1) and gold (#D4AF37)
- Apply consistently across all pages
- Use as favicon and header logo

---

## Technical Notes for Developers

### Authentication Flow

1. **Public Routes:** /, /catalog, /catalog/{id}, /track-order, /order-confirmation/{id}, /admin/login
2. **Protected Routes:** All /admin/* routes except /admin/login
3. **Auth Check:** On protected route access, verify JWT token exists and is valid
4. **Redirect:** If not authenticated, redirect to /admin/login
5. **Token Storage:** Use localStorage or sessionStorage for JWT token
6. **Token Expiry:** Handle 401 responses by clearing token and redirecting to login

### Role-Based Access Control

1. **Check user role from JWT token or user object**
2. **Hide/show navigation items based on role:**
   - Reports: Show only for Manager and Owner
   - Users: Show only for Owner
3. **Disable actions based on role:**
   - Delete inventory: Only Manager and Owner
4. **API calls will enforce permissions server-side**

### State Management

**Recommended approach:**
- Use React Context or Redux for:
  - Current user data (username, email, role)
  - Authentication state
  - Shopping cart (if multi-item orders implemented)
- Use local component state for:
  - Form inputs
  - Dialog open/close states
  - Filters and search queries

### API Integration Points

**Public Pages:**
- Homepage: GET /catalog?limit=8 (for featured items)
- Catalog: GET /catalog (with filters and pagination)
- Product Detail: GET /catalog/{id}
- Order Placement: POST /orders
- Order Confirmation: Use order data from POST response
- Order Tracking: GET /orders/customer/{email}

**Admin Pages:**
- Login: POST /auth/login
- Dashboard: GET /inventory, GET /orders, GET /reports/* (based on role)
- Inventory: GET /inventory, POST /inventory, PATCH /inventory/{id}, DELETE /inventory/{id}
- Orders: GET /orders, GET /orders/{id}, PATCH /orders/{id}/status
- Reports: GET /reports/sales, GET /reports/inventory
- Users: GET /users, POST /auth/register, DELETE /users/{id}

### Form Validation

**Client-side validation before API calls:**
- Required fields
- Email format
- Phone format (10-15 digits)
- Price and weight must be positive numbers
- Quantity must be non-negative integer
- Password minimum 8 characters
- Item code uniqueness (show error on API response)

### Error Handling

**Standard error display pattern:**
1. API returns error with code and message
2. Display error in appropriate location:
   - Form errors: Inline below field
   - Dialog errors: Alert banner at top of dialog
   - Page errors: Toast notification or alert banner
3. Error types to handle:
   - Authentication errors (401): Redirect to login
   - Permission errors (403): Show "Access Denied" message
   - Not found errors (404): Show "Item not found" message
   - Validation errors (400): Display specific field errors
   - Server errors (500): Show generic "Something went wrong" message

### Responsive Design

**Breakpoints:**
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

**Responsive behaviors:**
- Catalog grid: 1 column (mobile), 2 columns (tablet), 3 columns (desktop)
- Admin sidebar: Collapsible on mobile, always visible on desktop
- Tables: Horizontal scroll on mobile, full display on desktop
- Dialogs: Full-screen on mobile, centered modal on desktop
- Navigation: Hamburger menu on mobile, full menu on desktop

### Performance Considerations

1. **Image Optimization:**
   - Use lazy loading for product images
   - Serve responsive image sizes
   - Compress images before upload

2. **Pagination:**
   - Default 20 items per page
   - Implement virtual scrolling for large lists if needed

3. **API Caching:**
   - Cache catalog data for short periods
   - Invalidate cache on inventory updates

4. **Loading States:**
   - Show skeleton loaders for tables and grids
   - Display spinner for form submissions
   - Disable buttons during API calls

---

## Implementation Checklist

### Phase 1: Public Pages (Priority 1)

- [ ] Homepage with hero, features, testimonials, footer
- [ ] Generate logo using AI image generation tool
- [ ] Catalog page with filters and product grid
- [ ] Product detail page
- [ ] Order placement dialog
- [ ] Order confirmation page
- [ ] Order tracking page
- [ ] Public navigation header
- [ ] Responsive design for all public pages

### Phase 2: Authentication & Admin Foundation (Priority 1)

- [ ] Admin login page
- [ ] JWT authentication implementation
- [ ] Protected route middleware
- [ ] Admin dashboard with role-based widgets
- [ ] Admin sidebar navigation
- [ ] User profile section with logout

### Phase 3: Admin Inventory (Priority 1)

- [ ] Inventory list page with filters
- [ ] Add item dialog with tabs
- [ ] Edit item dialog
- [ ] Delete item confirmation
- [ ] API integration for all CRUD operations
- [ ] Form validation for inventory items

### Phase 4: Admin Orders (Priority 1)

- [ ] Orders list page with filters
- [ ] Order detail dialog
- [ ] Update order status dialog
- [ ] Status validation logic
- [ ] API integration for order management

### Phase 5: Admin Reports (Priority 2)

- [ ] Reports dashboard page
- [ ] Sales charts and visualizations
- [ ] Inventory distribution charts
- [ ] Low stock alerts table
- [ ] Date range filtering
- [ ] API integration for reports endpoints

### Phase 6: User Management (Priority 2)

- [ ] Users list page (owner only)
- [ ] Create user dialog
- [ ] Delete user confirmation
- [ ] Role-based access control validation
- [ ] API integration for user management

### Phase 7: Polish & Testing (Priority 2)

- [ ] Error handling for all API calls
- [ ] Loading states for all async operations
- [ ] Form validation messages
- [ ] Success toast notifications
- [ ] Empty states for lists and tables
- [ ] Mobile responsive testing
- [ ] Cross-browser testing
- [ ] Accessibility audit (ARIA labels, keyboard navigation)

---

**End of UX Plan v1**

**Total Lines:** 295