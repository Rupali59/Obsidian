### 📦 **Product Catalog** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Product List|
|**Internal Submodule**|`product_catalog`|
|**Roles with Access**|Admin, Inventory Manager|
|**Functionality**|Add, edit, or deactivate products like gemstones, yantras, books, or remedies|
|**Search/Filter by:**|Name, Type, Price, Stock Status, Vendor|
|**Visual Design**|Table view with image thumbnail, stock counter, inline edit buttons, filter dropdowns|

✅ **MVP Features**:

- Add/edit products with price, description, and image
    
- Set product categories (e.g., Gemstones, Reports)
    
- Track product visibility (active/inactive)
    
- Stock status indicator (low, out-of-stock)
    

🟡 **Good to Have**:

- Bulk upload via CSV
    
- Product ratings and reviews
    
- SEO metadata fields
    

---

### 📊 **Inventory Tracker** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Stock Overview|
|**Internal Submodule**|`inventory_tracker`|
|**Roles with Access**|Admin, Inventory Manager|
|**Functionality**|Monitor live stock, update quantities, set alerts|
|**Search/Filter by:**|Product Name, Category, Quantity Threshold|
|**Visual Design**|Color-coded inventory cards, progress bars, filterable table|

✅ **MVP Features**:

- Track stock levels per item
    
- Set low stock alerts
    
- Manual quantity update (after offline sales)
    

🟡 **Good to Have**:

- Auto alerts for reorder threshold
    
- Integration with external POS or eCommerce systems
    
- Batch expiry tracker (for incense, oils)
    

---

### 📥 **Order Management** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Order Dashboard|
|**Internal Submodule**|`order_management`|
|**Roles with Access**|Admin, Inventory Manager, Operations|
|**Functionality**|Track all orders placed by clients (astrology reports, gemstones, etc.)|
|**Search/Filter by:**|Order ID, Client Name, Product, Status, Date|
|**Visual Design**|Order pipeline (Pending → Packed → Shipped → Delivered), tag labels for status|

✅ **MVP Features**:

- View and filter all customer orders
    
- Update order status (with timestamps)
    
- Download invoice or order slip
    
- Assign order to fulfillment executive
    

🟡 **Good to Have**:

- Integration with shipping APIs (Delhivery, Bluedart)
    
- Auto-generated packing slips
    
- Payment status sync from Razorpay/Stripe
    

---

### 🔧 **Vendor/Procurement Management** — 🟡 **Good to Have**

|Attribute|Value|
|---|---|
|**UX Name**|Vendor Hub|
|**Internal Submodule**|`vendor_management`|
|**Roles with Access**|Admin, Inventory Manager|
|**Functionality**|Manage external vendors for gemstones, yantras, report printing|
|**Search/Filter by:**|Vendor Name, Product Supplied, Payment Terms|
|**Visual Design**|Vendor card view, contract uploads, contact logs|

✅ **MVP Features**:

- N/A
    

🟡 **Good to Have**:

- Vendor profiles with contact and order history
    
- Add preferred vendors for specific product types
    
- Auto reorder emails to vendor
    

---

### 🧾 **Invoice & Billing** — 🟡 **Good to Have**

|Attribute|Value|
|---|---|
|**UX Name**|Invoices|
|**Internal Submodule**|`billing_and_invoicing`|
|**Roles with Access**|Admin, Finance|
|**Functionality**|Generate, download, and track invoices for product orders|
|**Search/Filter by:**|Client, Invoice ID, Status, Date|
|**Visual Design**|Invoice cards, PDF view/download button, payment status label|

✅ **MVP Features**:

- N/A
    

🟡 **Good to Have**:

- Auto-generate invoice with order
    
- GST/tax breakdown
    
- Payment status and due alerts