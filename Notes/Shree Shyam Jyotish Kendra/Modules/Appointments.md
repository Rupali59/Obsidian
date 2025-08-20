📌 _The core of daily operations—handles all bookings, schedules, availability, and session histories._

**Accessible To:**  
🧙‍♂️ Astrologers | 🧾 Admin | 📞 Sales

---

### 1. 📅 **Calendar View**— ✅ **MVP**
|Attribute|Value|
|---|---|
|**UX Name**|Calendar|
|**Internal Submodule**|`calendar_view`|
|**Roles with Access**|Astrologers, Admin|
|**Functionality**|View, manage and filter all appointments in a calendar format|
|**Search/Filter by:**|Date, Status, Astrologer|
|**Visual Design**|Grid calendar layout with color-coded status tags, view toggles (Day/Week/Month), quick preview modal on click|✅ **MVP Features**:

- View Day/Week/Month/List calendar
    
- Color-coded slots (Booked, Available, Cancelled)
    
- Filter by astrologer or appointment status
    

🟡 **Good to Have**:

- Drag-to-reschedule appointments
    
- Notification/reminder integration (email/SMS)        

---

### 📝 **Booking Requests** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Booking Requests|
|**Internal Submodule**|`booking_queue`|
|**Roles with Access**|Admin, Sales|
|**Functionality**|Handle and assign new appointment requests from clients|
|**Search/Filter by:**|Date, Client, Source, Status|
|**Visual Design**|Table of pending requests with Accept/Reject/Assign buttons, status badges, and client information|

✅ **MVP Features**:

- View all pending appointment requests
    
- Accept, reject, or assign astrologer
    
- Sync confirmed bookings to calendar
    

🟡 **Good to Have**:

- AI-based astrologer recommendation
    
- Tag requests with urgency or topic
    

---

### 🔄 **Reschedule & Cancellation Manager** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Reschedule & Cancellations|
|**Internal Submodule**|`appointment_modifications`|
|**Roles with Access**|Astrologers, Admin|
|**Functionality**|Track and manage all changes to appointments, along with reasons and timestamps|
|**Search/Filter by:**|Astrologer, Client, Status, Date|
|**Visual Design**|List view with old/new times, reason tags, initiator, and status icons|

✅ **MVP Features**:

- Log reschedule/cancellation events with reasons
    
- Show initiator and current status
    
- Option to update or confirm changes
    

🟡 **Good to Have**:

- Smart slot suggestions for reschedule
    
- Reschedule/cancellation history dashboard
    

---

### 🧘 **Astrologer Availability Settings** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Availability Manager|
|**Internal Submodule**|`availability_settings`|
|**Roles with Access**|Astrologers, Admin|
|**Functionality**|Define and edit astrologer work hours, breaks, off-days, and session caps|
|**Search/Filter by:**|Astrologer, Date, Availability Status|
|**Visual Design**|Drag-and-drop week scheduler with toggles for off days and break hours, editable limit settings|

✅ **MVP Features**:

- Set weekly availability and working hours
    
- Block off holidays/custom dates
    
- Limit number of sessions per day
    

🟡 **Good to Have**:

- Google Calendar sync
    
- Auto-adjustment for timezone or DST
    

---

### 📞 **Session History & Recordings** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Session Logs|
|**Internal Submodule**|`appointment_logs`|
|**Roles with Access**|Astrologers, Admin|
|**Functionality**|Access complete history of past client-astrologer sessions|
|**Search/Filter by:**|Client, Astrologer, Topic Tag, Date|
|**Visual Design**|Timeline or List view with expandable cards showing session summary, time, and links to files or notes|

✅ **MVP Features**:

- List all past sessions by astrologer or client
    
- Display timestamps, durations, and basic notes
    
- Filter by client/date
    

🟡 **Good to Have**:

- Audio/video session recording archive
    
- Topic tagging and exportable session summaries
    

---

### 🧾 **Appointment Payments** — ✅ **MVP**

|Attribute|Value|
|---|---|
|**UX Name**|Booking Payments|
|**Internal Submodule**|`booking_payments`|
|**Roles with Access**|Admin, Sales|
|**Functionality**|Manage all appointment-related payments and sync with orders|
|**Search/Filter by:**|Client, Payment Status, Date|
|**Visual Design**|Payment table with filters, color-coded status, linked appointment references, and CTAs for invoice/refund|

✅ **MVP Features**:

- View and update payment status for bookings
    
- Link appointment to transaction ID
    
- Manual marking of payment received
    

🟡 **Good to Have**:

- Auto-invoice and receipt generation
    
- Coupon/promo/refund management interface