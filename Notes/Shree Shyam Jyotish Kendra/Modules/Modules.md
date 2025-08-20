.

---

## 📁 Sidebar – Visual Layout (Hierarchical)

	🌟 Dashboard
	├── 📈 KPI Overview
	├── 🗓️ Daily Planner
	└── 👥 Role-Based Widgets
	
	👤 Clients
	├── 🔍 Client Directory
	├── 📑 Client Profile
	├── 📜 Reports & Documents
	├──📋 Lead Tracker  
	├──🧲 Source-wise Leads  
	└──📈 Conversion Dashboard

	
	🧙‍♂️ Consultants
	├── 🧑‍🏫 Consultant Profiles
	├──🗓️ Availability Calendar
	├── 📂 Assigned Clients
	└── ✅ Consultant Tasks
	    
	
	💬 Appointments & Calls
	├── 🕒 Scheduled Calls
	├── 📥 Incoming Leads
	└── 📋 Past Sessions Log
	
	📦 Inventory
	├── 💎 Gemstone Stock
	├── 🧾 Purchase Ledger
	└── 🚚 Vendor Info
	
	🧿 Orders & Remedies
	├── 🪬 Remedies Suggested
	├── 📦 Order List
	├── 🏷️ Pricing Management
	├── 📦 Shipping Tracker
	└── 🧮 Inventory Adjustment
	
	📜 Content & Media
	├── ✍️ Article Manager
	├── 🎥 Video & Reels
	└── 🔮 Astro Highlights
	
	📣 Campaigns & Outreach
	├── 📤 Email Campaigns
	├── 💬 WhatsApp Blasts
	├──🧪 A/B Testing  
	├──📆 Campaign Scheduler
	└── 🔍 SEO & Keywords
	
	📊 Analytics & Reports
	├── 📈 Lead Funnel
	├── 💸 Revenue by Source
	├──📆 Time-wise Performance
	└──📍 Drop-offs & Bottlenecks
	
	🛡️  Approvals & Compliance
	├── 📄 Report Approval Queue  
	├── 🧾 Session Review Log  
	└── 📚 Audit Trail
	
	🏢 Office Ops
	├── 🧰 Device Registry
	├── 📝 Internal Tasks
	├──📌 Notices & Updates
	└──📎 Knowledge Base
	
	🤝 CRM & Leads
	├── 📋 Lead Tracker
	├── 🧲 Source-wise Leads
	└── 📈 Conversion Dashboard
	
	⚙️ Settings
	├── 🌐 Site Config
	├── ⚙️ API & Tools
	└── 🔒 Access Control
		├── 👥 Role Manager
		└── 🔑 Login & Auth Logs
	
	🤖 Telegram Bot
	├── 📲 Bot Setup
	├── 👥 Subscriber DB
	└── 🧾 Interaction Logs

---

## Module Table

| UX Name                 | Module Name (Internal) | Access                              | Purpose                                             |
| ----------------------- | ---------------------- | ----------------------------------- | --------------------------------------------------- |
| 🌟 Dashboard            | `dashboard_module`     | All roles                           | Daily visibility of KPIs, appointments, quick links |
| 👤 Client Management    | `clients_module`       | Astrologer, Admin, Sales            | Manage profiles, docs, and interactions             |
| 🧙‍♂️ Consultant Panel  | `consultant_module`    | Admin, Astrologer                   | Schedule, assign clients, log tasks                 |
| 💬 Appointments & Calls | `appointments_module`  | Admin, Astrologer, Sales            | Track, reschedule, approve appointments             |
| 📦 Inventory Management | `inventory_module`     | Admin, Inventory                    | Manage gemstone stocks, vendors, alerts             |
| 🧿 Orders & Remedies    | `remedy_orders_module` | Astrologer, Admin, Sales, Inventory | Remedy suggestions, order management                |
| 📜 Content & Media      | `content_module`       | Admin, Marketing                    | Upload/manage reels, blogs, shorts                  |
| 📣 Campaigns & Outreach | `marketing_module`     | Admin, Marketing, Sales             | Email/WA campaigns, SEO tracking, groups            |
| 📊 Analytics & Reports  | `analytics_module`     | Admin, Management                   | Performance tracking across all verticals           |
| 🔒 Access Control       | `auth_module`          | Admin, Dev                          | User access, login logs, role matrix                |
| 🏢 Office Ops           | `office_ops_module`    | Admin, Staff                        | Task management, device registry, updates           |
| 🤝 Leads & CRM          | `crm_leads_module`     | Admin, Sales                        | Sales pipeline, lead notes, conversion logs         |
| ⚙️ Settings             | `settings_module`      | Admin                               | Platform settings and backend configuration         |
| 🤖 Telegram Bot Manager | `telegram_module`      | Admin, Marketing                    | Bot config, interaction logs, subscriber DB         |

---

## 🌟 **Dashboard**

**Accessible to:** All Roles  
**Submodules & Features:**

- ### 📈 **KPI Overview**
    
    _Roles:_ Admin, Manager  
    _Functionality:_ Show overall performance metrics  
    _Visual:_ Line/Bar Charts, Info Cards
    
- ### 🗓️ **Daily Planner**
    
    _Roles:_ All  
    _Functionality:_ Tasks, appointments, reminders  
    _Visual:_ Timeline, Checkboxes, CTA: “Complete Task”
    
- ### 👥 **Role-Based Widgets**
    
    _Roles:_ Dynamic (based on login role)  
    _Functionality:_ Astrologer → next calls, Admin → revenue  
    _Visual:_ Custom cards, CTA buttons, List view
    

---

## 👤 **[[Client Management]]**

**Accessible to:** Astrologers, Admin, Sales  
**Submodules:**

- ### 🔍 **Client Directory**
    
    _Functionality:_ Filter/search clients by name, DOB, zodiac, status  
    _Visual:_ Table with filter bar, Search bar, Tags
    
- ### 📁 **Client Profile**
    
    _Functionality:_ View/edit profile, history  
    _Visual:_ Tabbed layout: Profile | Calls | Orders | Notes
    
- ### 📜 **Reports & Documents**
    
    _Functionality:_ Upload/view client charts, remedies  
    _Visual:_ File cards, Preview modals, Download CTAs
    

---

## 📆 **[[Appointments]]**

**Accessible to:** Astrologers, Admin  
**Submodules:**

- ### 🗓️ **Calendar View**
    
    _Functionality:_ Monthly/weekly view, filter by astrologer  
    _Visual:_ Calendar widget with color-coded status
    
- ### 📝 **Appointment Tracker**
    
    _Functionality:_ Missed/rescheduled logs, approval queue  
    _Visual:_ List with status tags, Approval CTA
    
- ### ➕ **New Booking**
    
    _Functionality:_ Create/edit appointment  
    _Visual:_ Form modal, Autocomplete for client
    

---

## 📥 **[[Lead Management]]**

**Accessible to:** Sales, Admin  
**Submodules:**

- ### 🌡️ **Lead Funnel**
    
    _Functionality:_ Hot/Warm/Cold segmentation  
    _Visual:_ Funnel chart, Kanban drag-to-update status
    
- ### 📂 **Lead List**
    
    _Functionality:_ Search, view notes, reminders  
    _Visual:_ Table view with tags, Reminder icons
    
- ### 🔁 **Conversion Tool**
    
    _Functionality:_ Convert lead → client  
    _Visual:_ CTA Button: “Convert”, Side-by-side form
    

---

## 💬 **[[Marketing Strategy & Campaigns]]**

**Accessible to:** Marketing, Admin  
**Submodules:**

- ### 🧰 **Builder (WhatsApp/Email)**
    
    _Functionality:_ Create campaigns  
    _Visual:_ Drag-and-drop layout, CTA preview buttons
    
- ### 📂 **Contact Groups**
    
    _Functionality:_ Birthday, inactive, transit-matching lists  
    _Visual:_ Smart filters, Segment manager cards
    
- ### 🔄 **Auto Drip Campaigns**
    
    _Functionality:_ Trigger-based flows  
    _Visual:_ Flow diagram with triggers/actions
    
- ### 🕓 **Campaign History**
    
    _Functionality:_ Logs of past campaigns  
    _Visual:_ List, Tags (Success/Failed)
    

---

## 📦 **[[Inventory & Product Management]]**

**Accessible to:** Admin, Back Office  
**Submodules:**

- ### 📟 **Product Catalog**
    
    _Functionality:_ View/edit gemstones, remedies  
    _Visual:_ Grid view, Quantity counters, Edit CTA
    
- ### 📋 **Order Tracker**
    
    _Functionality:_ Track product order status  
    _Visual:_ Step-tracker UI (Ordered → Delivered)
    
- ### 📉 **Low Stock Alerts**
    
    _Functionality:_ Auto alerts for critical items  
    _Visual:_ Notification badges, Email alerts
    
- ### 🛋 **Shipping Details**
    
    _Functionality:_ Manage courier, dispatch tracking numbers  
    _Visual:_ Timeline view, Dispatch CTAs, PDF invoice links
    

---

## 📊 **[[Analytics & Reports]]**

**Accessible to:** Admin, Management  
**Submodules:**

- ### 💸 **Revenue Reports**
    
    _Functionality:_ Revenue by astrologer/service  
    _Visual:_ Pie charts, Line graphs
    
- ### ♻️ **Booking Trends**
    
    _Functionality:_ Compare weekly/monthly stats  
    _Visual:_ Heatmaps, Calendar overlays
    
- ### 🥪 **Campaign Insights**
    
    _Functionality:_ Open rates, reach  
    _Visual:_ Bar graphs, A/B test comparison
    

---

## ✅ **[[Approvals & Compliance]]**

**Accessible to:** Admin  
**Submodules:**

- ### ✔️ **Appointment Approvals**
    
    _Functionality:_ Pending request reviews  
    _Visual:_ Approval queue list with action buttons
    
- ### 📣 **Campaign Review**
    
    _Functionality:_ Check before broadcast  
    _Visual:_ Preview modals, Approve/Reject buttons
    
- ### ⚠️ **Escalation Log**
    
    _Functionality:_ Complaints & issue resolution  
    _Visual:_ Ticket list with priority badges
    

---

## 🧠 **[[Astro Insights Engine ]]**

**Accessible to:** Astrologers, Admin  
**Submodules:**

- ### 🔍 **Client Triggers**
    
    _Functionality:_ See clients due for transit-based sessions  
    _Visual:_ Alert tiles, Client lists
    
- ### 🛍️ **Remedy Recommendations**
    
    _Functionality:_ Suggest product/service based on chart  
    _Visual:_ Recommendation cards with “Send to Client” CTA
    

---

## 🧲 **[[Experiments]]**

**Accessible to:** Admin, Marketing  
**Submodules:**

- ### 🦬 **A/B Tests**
    
    _Functionality:_ Test campaign performance  
    _Visual:_ Split metrics view
    
- ### 🤭 **Sandbox Tools**
    
    _Functionality:_ Run test flows, new services  
    _Visual:_ Button-based flows, toggles
    

---

## ⚙️ **[[Admin & Control Center]]**

**Accessible to:** Admin only  
**Submodules:**

- ### 🔐 **User Roles & Permissions**
    
    _Functionality:_ Set access by role  
    _Visual:_ Role matrix table, toggles
    
- ### 🛠️ **Settings & Branding**
    
    _Functionality:_ Update platform settings  
    _Visual:_ Form-based controls, Logo uploads
    
- ### 📃 **Audit Logs**
    
    _Functionality:_ Track changes and edits  
    _Visual:_ Timeline view
    

---

## 🔗 **[[Tools & Integrations]]**

**Accessible to:** Admin  
**Submodules:**

- ### 🤖 **Telegram Bot Setup**
    
    _Functionality:_ Connect and sync with bot  
    _Visual:_ Step wizard, Test CTA
    
- ### 💳 **Payment Gateway**
    
    _Functionality:_ Check payment system status  
    _Visual:_ Green/Red indicators, Logs