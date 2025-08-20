## 🔌 **Tools & Integrations**

This module connects third-party services (e.g., CRM tools, astrology APIs, messaging platforms, analytics tools) to enhance platform capabilities and automation.

---

### 🧿 **Astrology Software Integrations** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Astrology Engine Connect|
|**Internal Submodule**|`astro_integration`|
|**Roles with Access**|Admin, Astrologer, Superadmin|
|**Functionality**|Connect external astrology engines (e.g., Jagannatha Hora, AstroSage API, Cosmic Insights)|
|**Search/Filter by:**|Plugin name, system, zodiac type|
|**Visual Design**|Plugin list with config button|

✅ **MVP Features**:

- Support 1–2 API integrations (e.g., AstroSage API)
    
- Fetch Kundli + planetary data
    
- Store birth charts with fallback support
    

🟡 **Good to Have**:

- Multiple engine fallback hierarchy
    
- Custom astrological plugin builder
    
- Live planetary transit fetch on dashboard
    

---

### 📞 **Messaging & Notifications Integration** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Message Connector|
|**Internal Submodule**|`notif_channels`|
|**Roles with Access**|Admin, Ops, Support|
|**Functionality**|Enable WhatsApp, SMS, Email, Telegram bots for alerts, confirmations, promotions|
|**Search/Filter by:**|Channel, Campaign, Status|
|**Visual Design**|Tabular channel config panel with toggle + key input|

✅ **MVP Features**:

- SMS (e.g., Twilio or Indian gateway like Textlocal)
    
- Telegram Bot config for lead alerts or CRM pings
    
- Email provider integration (e.g., Mailgun, SendGrid)
    

🟡 **Good to Have**:

- WhatsApp Business API integration
    
- In-app push notifications
    
- Channel performance analytics
    

---

### 📊 **Analytics Tools Integration** — 🟡 **Good to Have**

|Attribute|Value|
|---|---|
|**UX Name**|Analytics Connect|
|**Internal Submodule**|`analytics_bridge`|
|**Roles with Access**|Admin, Product, Superadmin|
|**Functionality**|Connect Google Analytics, Mixpanel, Meta Pixel for user tracking & funnel visualization|
|**Search/Filter by:**|Tool name, Page ID, Last activity|
|**Visual Design**|Integration cards with toggle and settings|

✅ **MVP Features**:

- N/A
    

🟡 **Good to Have**:

- GA4 integration for tracking visitors
    
- Meta Pixel for retargeting
    
- Mixpanel/Firebase events for funnels
    

---

### ⚙️ **Webhook & API Management** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Developer Tools|
|**Internal Submodule**|`webhook_api_panel`|
|**Roles with Access**|Admin, Developer, Superadmin|
|**Functionality**|Manage outgoing webhooks and internal/external API endpoints|
|**Search/Filter by:**|API name, Webhook event, Method|
|**Visual Design**|Endpoint list with test payload and status indicator|

✅ **MVP Features**:

- Define webhook endpoints (e.g., lead_created, appointment_booked)
    
- Add internal API endpoints for fetching reports or data
    
- Monitor webhook failures
    

🟡 **Good to Have**:

- Retry failed webhook calls
    
- View usage stats per endpoint
    
- IP whitelisting and key rotation
    

---

### 🤝 **CRM/Calendar Sync Integrations** — 🟡 **Good to Have**

|Attribute|Value|
|---|---|
|**UX Name**|CRM + Calendar Sync|
|**Internal Submodule**|`calendar_crm_sync`|
|**Roles with Access**|Admin, Astrologer, Sales|
|**Functionality**|Sync client contacts & appointments with Google Calendar or external CRMs|
|**Search/Filter by:**|Service, Connected status|
|**Visual Design**|OAuth tile view + Sync button|

✅ **MVP Features**:

- N/A
    

🟡 **Good to Have**:

- Google Calendar bi-directional sync
    
- Pabbly/Zapier integration with other tools
    
- Auto-sync client details to HubSpot/Freshdesk
    
