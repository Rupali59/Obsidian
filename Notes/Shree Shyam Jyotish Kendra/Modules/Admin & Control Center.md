## 🛠️ **Admin Settings & Controls**

This core system control panel empowers platform administrators to manage operations, roles, configurations, and business settings. It ensures security, flexibility, and autonomy in platform evolution.

---

### 🔐 **Role & Permission Manager** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Role Control Panel|
|**Internal Submodule**|`role_permissions`|
|**Roles with Access**|Superadmin|
|**Functionality**|Define custom roles, assign module access, update permissions in real-time|
|**Search/Filter by:**|Role, Permission, User ID|
|**Visual Design**|Role tree + matrix toggle view|

✅ **MVP Features**:

- Add/edit/delete roles
    
- Assign module-level permissions
    
- Access control per user or group
    

🟡 **Good to Have**:

- Time-bound or session-based permissions
    
- Permission templates (e.g., Junior Astrologer, Sales Manager)
    
- Auto-disable role after inactivity
    

---

### ⚙️ **Platform Configuration Panel** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|System Settings|
|**Internal Submodule**|`config_settings`|
|**Roles with Access**|Admin, Superadmin|
|**Functionality**|Define platform-wide behavior such as default timezone, currency, astrology system|
|**Search/Filter by:**|Keyword or module name|
|**Visual Design**|Accordion view grouped by categories (General, Astrology, API, Notifications)|

✅ **MVP Features**:

- Set currency, timezone, language
    
- Select Ayanamsa & astrology system (Lahiri, Raman, KP, etc.)
    
- Configure API keys, SMS/email credentials
    

🟡 **Good to Have**:

- Dynamic theme/color update
    
- Separate dev/staging/live configs
    
- Config rollback/version control
    

---

### 🧪 **Experiment Settings** — 🟡 **Good to Have**

|Attribute|Value|
|---|---|
|**UX Name**|A/B Tester & Flags|
|**Internal Submodule**|`feature_flags`|
|**Roles with Access**|Superadmin, Founders, Tech|
|**Functionality**|Enable/disable features, test layout/content/campaigns with subsets of users|
|**Search/Filter by:**|Flag name, Module, Status|
|**Visual Design**|Toggle + assignment grid view|

✅ **MVP Features**:

- N/A
    

🟡 **Good to Have**:

- Toggle any module as experiment
    
- Split testing interface for messages or campaigns
    
- User targeting by segment for test groups
    

---

### 👥 **Team Activity & Audit Logs** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Admin Activity Logs|
|**Internal Submodule**|`audit_logs`|
|**Roles with Access**|Admin, Superadmin|
|**Functionality**|Track all admin/staff actions: logins, edits, deletions, config changes|
|**Search/Filter by:**|User, Date, Action type|
|**Visual Design**|Timeline log or tabular dashboard|

✅ **MVP Features**:

- See full user activity
    
- Track permission changes
    
- Login/logout/unauthorized access attempts
    

🟡 **Good to Have**:

- Geo-tracking of login activity
    
- Filter by module/submodule activity
    
- Alert on sensitive action (e.g., delete Kundli)
    

---

### 📥 **Feedback & Support Inbox** — 🟡 **Good to Have**

|Attribute|Value|
|---|---|
|**UX Name**|Internal Feedback Hub|
|**Internal Submodule**|`support_inbox`|
|**Roles with Access**|Admin, Ops, Product|
|**Functionality**|Manage internal or client-reported issues, requests, feature feedback|
|**Search/Filter by:**|Tag, Type, Status|
|**Visual Design**|Ticket view or Kanban-style (Open, Assigned, Resolved)|

✅ **MVP Features**:

- N/A
    

🟡 **Good to Have**:

- Tag issues as “Bug / Feature / Complaint”
    
- Assign tickets to relevant staff
    
- Status tracking (Open/In Progress/Closed)