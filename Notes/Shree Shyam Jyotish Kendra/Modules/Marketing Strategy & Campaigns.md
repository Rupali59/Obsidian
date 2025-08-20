## 📈 **Marketing Strategy & Campaigns**

---

### 🗂️ **Campaign Dashboard** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Campaign Manager|
|**Internal Submodule**|`marketing_dashboard`|
|**Roles with Access**|Marketing, Admin, Founders|
|**Functionality**|Central hub to track all marketing campaigns, statuses, source, budget, ROI|
|**Search/Filter by:**|Channel, Campaign Status, Date Range, Target Audience|
|**Visual Design**|Card or tabular layout with status indicators (Running, Draft, Completed)|

✅ **MVP Features**:

- Create, view, and edit campaigns
    
- Track basic metrics: status, dates, assigned team
    
- Link campaign to lead sources (e.g., landing page, WhatsApp, Insta)
    

🟡 **Good to Have**:

- Campaign timeline and calendar view
    
- Budget vs spend graph
    
- ROI snapshot tile
    

---

### ✍️ **Campaign Creation & Targeting** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|New Campaign|
|**Internal Submodule**|`campaign_creation`|
|**Roles with Access**|Marketing, Admin|
|**Functionality**|Define campaign content, audience segments, goal, medium, and call-to-action|
|**Search/Filter by:**|Campaign Name, Created By, Goal|
|**Visual Design**|Guided form or wizard for setup|

✅ **MVP Features**:

- Name, channel, campaign brief, platform (e.g., WhatsApp, email)
    
- Goal selection (Awareness, Leads, Sales, Retargeting)
    
- CTA button/link integration
    

🟡 **Good to Have**:

- Auto-clone from past campaigns
    
- A/B variant setup
    
- Dynamic personalization tokens (e.g., {name}, {zodiac})
    

---

### 📢 **Campaign Execution & Scheduling** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Campaign Scheduler|
|**Internal Submodule**|`campaign_execution`|
|**Roles with Access**|Marketing|
|**Functionality**|Execute campaigns via configured channels; schedule date/time or send immediately|
|**Search/Filter by:**|Scheduled vs Sent, Medium, Channel|
|**Visual Design**|Timeline view with option to schedule/pause campaigns|

✅ **MVP Features**:

- Schedule SMS/email/WhatsApp broadcast
    
- Manual or automatic execution toggle
    
- Message templates support
    

🟡 **Good to Have**:

- Auto-pause on low engagement
    
- Multi-channel fallback (e.g., SMS if WhatsApp fails)
    
- Smart send-time recommendation
    

---

### 🧪 **Campaign Performance Analytics** — 🟡 **Good to Have**

|Attribute|Value|
|---|---|
|**UX Name**|Campaign Analytics|
|**Internal Submodule**|`campaign_analytics`|
|**Roles with Access**|Marketing, Admin, Founders|
|**Functionality**|Analyze reach, click-throughs, conversions per campaign|
|**Search/Filter by:**|Campaign, Medium, Source, Conversion %|
|**Visual Design**|Line/bar graphs and conversion funnels|

✅ **MVP Features**:

- N/A
    

🟡 **Good to Have**:

- CTR, open rate, response rate
    
- Per-platform effectiveness chart
    
- Cost per conversion analysis
    

---

### 🗃️ **Template Library** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Message Templates|
|**Internal Submodule**|`message_templates`|
|**Roles with Access**|Marketing|
|**Functionality**|Store and reuse predefined campaign message templates|
|**Search/Filter by:**|Template Name, Type (WhatsApp, SMS, Email), Last Used|
|**Visual Design**|List or tile view with preview option|

✅ **MVP Features**:

- Create/edit/delete templates
    
- WhatsApp/SMS format support
    
- Tag templates by theme (festive, zodiac-based, offers)
    

🟡 **Good to Have**:

- AI-assisted message draft
    
- Emoji and media suggestions
    
- Pre-approved WhatsApp API template status tracker
    

---

### 🔄 **UTM & Campaign Source Tracking** — 🟡 **Good to Have**

|Attribute|Value|
|---|---|
|**UX Name**|Source Attribution|
|**Internal Submodule**|`utm_tracking`|
|**Roles with Access**|Marketing, Admin|
|**Functionality**|Create and track UTM links or short links to attribute traffic and leads to campaigns|
|**Search/Filter by:**|Campaign Name, Medium, UTM Tag|
|**Visual Design**|Tag manager or table with click data|

✅ **MVP Features**:

- N/A
    

🟡 **Good to Have**:

- UTM link generator
    
- Short link generator (e.g., g.astrology.link)
    
- Auto-source tagging in CRM