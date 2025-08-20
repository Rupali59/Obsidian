> 📌 _“This module handles the full lifecycle of remedial item orders—from product recommendations to delivery tracking.”_

**Accessible To:**  
🧙‍♂️ Astrologers | 🧾 Admin | 📞 Sales | 📦 Inventory Manager

---

### 🧾 **Remedy Recommendations**

|Attribute|Value|
|---|---|
|**UX Name**|Remedies Suggested|
|**Internal Submodule**|`remedy_recommendations`|
|**Roles with Access**|Astrologers|
|**Functionality**|Recommend items to clients based on reading (gemstones, yantras, pujas).|
|**Inputs**|Client Name, Remedy Type, Reason/Planet, Urgency|
|**Visual Design**|- **Main View:** Suggestion Cards with dropdowns (gem type, purpose)  <br>- **Optional Fields:** Image, Link to product, Delivery Preference  <br>- **CTA Buttons:** “Add to Order”, “Save as PDF”, “Send to Sales”|

---

### 📦 **Orders Dashboard**

|Attribute|Value|
|---|---|
|**UX Name**|Remedy Orders|
|**Internal Submodule**|`order_tracking`|
|**Roles with Access**|Admin, Sales, Inventory Manager|
|**Functionality**|Central dashboard for all placed orders (online/offline).|
|**Order Status**|Pending, Processing, Shipped, Delivered, Cancelled|
|**Visual Design**|- **Main View:** Tabular view with status filters  <br>- **Columns:** Order ID, Client, Remedy, Status, Shipping Address  <br>- **CTAs:** Update Status, View Invoice, Cancel Order|

---

### 📍 **Shipping & Delivery Tracking**

|Attribute|Value|
|---|---|
|**UX Name**|Shipping Manager|
|**Internal Submodule**|`shipping_status`|
|**Roles with Access**|Inventory Manager, Admin|
|**Functionality**|Track and update delivery progress, shipping partner integration.|
|**Shipping Modes**|BlueDart, DTDC, Local Courier, In-person|
|**Visual Design**|- **Main View:** Delivery Timeline per Order  <br>- **Tracking Block:** Courier Partner, Tracking ID, ETA  <br>- **CTAs:** Update Tracking, Mark Delivered, Issue Refund|

---

### 🧮 **Stock & Inventory**

|Attribute|Value|
|---|---|
|**UX Name**|Inventory|
|**Internal Submodule**|`inventory_management`|
|**Roles with Access**|Inventory Manager, Admin|
|**Functionality**|Maintain remedy stock levels (gemstones, books, yantras, oils).|
|**Key Actions**|Add Stock, Set Low-Stock Alerts, Batch Management|
|**Visual Design**|- **Main View:** Table/Grid with stock counts and tags  <br>- **Color Indicators:** Low/Out-of-Stock  <br>- **CTAs:** Add Item, Edit Quantity, Archive Item|

---

### 💳 **Remedy Payments**

|Attribute|Value|
|---|---|
|**UX Name**|Remedy Payment Tracker|
|**Internal Submodule**|`remedy_payments`|
|**Roles with Access**|Admin, Sales|
|**Functionality**|View payment status for each remedy or item order.|
|**Visual Design**|- **Main View:** Table with filters by Client, Date, Mode  <br>- **Status Tags:** Paid, COD, Pending  <br>- **CTAs:** Send Invoice, Mark Paid, Issue Refund|

---
