### 📤 **Content Approvals** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Content Approvals|
|**Internal Submodule**|`content_approvals`|
|**Roles with Access**|Admin, Editor, Compliance Officer|
|**Functionality**|Review and approve blogs, newsletters, and static page updates before they go live|
|**Search/Filter by:**|Type (Blog, Page, Email), Submitted by, Status, Date|
|**Visual Design**|Kanban-style approval pipeline or list with quick-approve and comment fields|

✅ **MVP Features**:

- Mark content as "Pending Approval"
    
- Reviewer can approve/reject with comments
    
- Notify creator of status update
    

🟡 **Good to Have**:

- Multi-level approval chains
    
- Highlight compliance violations (e.g., missing disclaimers)
    
- Suggest inline edits or send back for revision
    

---

### 📑 **Astrological Report Review** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Report Checks|
|**Internal Submodule**|`report_approvals`|
|**Roles with Access**|Senior Astrologer, Admin, QA Analyst|
|**Functionality**|Review astrologer reports (manual or AI-generated) for quality and tone|
|**Search/Filter by:**|Report type, Astrologer, Date, Client Name|
|**Visual Design**|List of reports with “flag” options, inline comment or accept buttons|

✅ **MVP Features**:

- Manual report flagging for review
    
- Reviewer comments before sending to client
    
- Approve or send back for correction
    

🟡 **Good to Have**:

- Automated red flag detection (e.g., negative language, missing remedies)
    
- Audit trail of revisions
    
- Assign reviewers by seniority
    

---

### 📄 **Document/ID Verification** — 🟡 **Good to Have**

|Attribute|Value|
|---|---|
|**UX Name**|ID Verification|
|**Internal Submodule**|`kyc_documents`|
|**Roles with Access**|Admin, Compliance Officer|
|**Functionality**|Upload, verify, and store astrologer KYC documents|
|**Search/Filter by:**|Astrologer name, Status, Type (ID, Address), Date|
|**Visual Design**|Document viewer with approve/reject CTA and comments|

✅ **MVP Features**:

- N/A
    

🟡 **Good to Have**:

- Expiry-based alerts for document renewals
    
- KYC verification status on astrologer profile
    
- Integration with DigiLocker or manual upload
    

---

### 📜 **Legal & Consent Tracking** — 🟡 **Good to Have**

|Attribute|Value|
|---|---|
|**UX Name**|Consent Logs|
|**Internal Submodule**|`legal_compliance`|
|**Roles with Access**|Admin, Legal Officer|
|**Functionality**|Store user consent logs, track terms acceptance and privacy compliance|
|**Search/Filter by:**|User ID, Consent Type, Version, Date|
|**Visual Design**|Tabular view with legal text version, timestamp, and IP data|

✅ **MVP Features**:

- N/A
    

🟡 **Good to Have**:

- View/download consent history
    
- Auto-prompt re-consent on policy changes
    
- Highlight users who haven’t accepted latest policy