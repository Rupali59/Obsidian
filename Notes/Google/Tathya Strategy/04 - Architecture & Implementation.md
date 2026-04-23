# Architecture & Implementation

> Where the assessment system lives in the existing stack. Maps to Motherboard, Tathya-portfolio, and the plugin ecosystem.

---

## Existing Stack

| Component | What | Where |
|-----------|------|-------|
| **Motherboard API** | Go/Gin gateway: CRM, plugin proxy, auth, entitlements, workflows | `motherboard-api` — `/api/clients`, `/api/plugins/tathya/*` |
| **Client CRM** | Full model: name, email, phone, status, personal/professional/billing, onboarding, metadata, source, tags, notes, assignedTo, pluginKey | `internal/models/client.go` |
| **Client workflows** | Transition endpoint: `POST /api/clients/:id/transition` | `routes_api.go` |
| **Plugin system** | Tathya proxied at `/api/plugins/tathya/*` with entitlement `tathya` | `plugin_tathya.go` → `TATHYA_PLUGIN_URL` |
| **Communication plugins** | Email, SMS, WhatsApp, Telegram | `routes_plugin.go` |
| **Inventory plugin** | Registered in Motherboard | `registerInventoryPlugin()` |
| **Astrology plugin** | Registered in Motherboard | `registerAstrologyRoutes()` |
| **Tathya-portfolio** | Next.js 16 on Vercel (tathya.dev), NextAuth, Motherboard OAuth | `Tathya-portfolio/src/app/` |
| **Dashboard** | `/dashboard` — currently placeholder "core vitals" | `src/app/dashboard/page.tsx` |
| **Analytics** | GTM + gtag on tathya.dev | `layout.tsx` |
| **Tathya-mb** | Express microservice (port 3120), MongoDB, JWT auth | `Tathya-mb/server/` |

---

## Architecture Decision

The assessment is NOT a separate app. It splits across two layers:

```
PUBLIC (no auth)                        PRIVATE (auth + workspace)
─────────────────                       ─────────────────────────
tathya.dev                              Motherboard
├── /assess (public form)               ├── /api/clients (CRM)
├── /assess/[id] (public report)        ├── /api/plugins/tathya/* (plugin API)
├── /api/assess (Next.js route)         ├── Client.metadata.assessment {}
│   ├── POST → create assessment        ├── Client.onboarding {}
│   ├── GET /[id] → fetch results       ├── Workflow transitions
│   └── POST /[id]/verify → run audit   └── Communication plugins
└── /dashboard/assessments (private)
    ├── list all submissions
    ├── per-assessment deep dive
    └── verification overlay
```

| Layer | Responsibility | Auth |
|-------|---------------|------|
| **tathya.dev `/assess`** | Public form + instant report | None (public) |
| **tathya.dev `/api/assess`** | Route handler: store, score, optionally create Motherboard client | None for POST, session for dashboard |
| **Tathya-mb or Tathya plugin** | Assessment data model, scoring engine, verification service | JWT / plugin proxy |
| **Motherboard CRM** | Prospect → client lifecycle. Assessment in `Client.metadata` | OAuth + workspace |
| **Motherboard comms** | Follow-up via WhatsApp/Email after assessment | Plugin proxy |

---

## Data Model

### Assessment Submission (New Collection: `assessments`)

Lives in Tathya-mb's MongoDB (or as a Tathya plugin collection proxied through Motherboard).

```javascript
{
  _id: ObjectId,

  profile: {
    businessType: "local" | "ecommerce" | "b2b" | "creator" | "nonprofit" | "other",
    industry: String,
    yearsOperating: "< 1" | "1-3" | "3-10" | "10+",
    teamSize: "solo" | "2-5" | "6-20" | "20+",
    revenueRange: String,
    language: "en" | "hi" | "kn",
    location: {
      city: String,
      state: String,
      country: String  // default "IN"
    }
  },

  assessmentPath: "starting" | "growing" | "scaling",

  answers: {
    "q1_1": 2,
    "q1_2": 3
    // keyed by question ID
  },

  scores: {
    dimensions: {
      strategy:      { raw: 2.5, scaled: 3.1, level: 3 },
      website:       { raw: 1.0, scaled: 1.25, level: 1 },
      analytics:     { raw: 0.5, scaled: 0.63, level: 0 },
      search:        { raw: 1.5, scaled: 1.88, level: 1 },
      content:       { raw: 2.0, scaled: 2.5, level: 2 },
      social:        { raw: 3.0, scaled: 3.75, level: 3 },
      whatsappEmail: { raw: 0.0, scaled: 0.0, level: 0 },
      paidAds:       { raw: 1.0, scaled: 1.25, level: 1 },
      conversion:    { raw: 1.5, scaled: 1.88, level: 1 },
      teamProcess:   { raw: 1.0, scaled: 1.25, level: 1 }
    },
    overall: 1.67,
    maturityLevel: 1,
    maturityLabel: "Present",
    topGaps: ["whatsappEmail", "analytics", "website"],
    pattern: "spiky"  // flat_low | spiky | plateau | high_with_holes | uniform_high
  },

  verification: {
    completedAt: Date,
    completedBy: ObjectId,
    checks: {
      googleSearch: {
        query: String,
        found: Boolean,
        position: Number,
        competitors: [String],
        screenshot: String
      },
      googleBusinessProfile: {
        exists: Boolean,
        claimed: Boolean,
        complete: Boolean,
        reviewCount: Number,
        rating: Number,
        missingFields: [String]
      },
      website: {
        exists: Boolean,
        url: String,
        mobileFriendly: Boolean,
        pageSpeedMobile: Number,
        pageSpeedDesktop: Number,
        coreWebVitals: { lcp: Number, inp: Number, cls: Number, pass: Boolean },
        hasAnalytics: Boolean,
        analyticsTool: String,
        hasMetaTags: Boolean,
        hasStructuredData: Boolean
      },
      socialMedia: {
        instagram: { exists: Boolean, handle: String, lastPost: String, followers: Number },
        facebook: { exists: Boolean, lastPost: String, followers: Number },
        youtube: { exists: Boolean },
        whatsapp: { type: "personal" | "business" | "none" }
      },
      directories: {
        justdial: { listed: Boolean, reviews: Number, rating: Number },
        practo: { listed: Boolean },
        sulekha: { listed: Boolean }
      },
      upiPayment: {
        hasQR: Boolean,
        onlinePayment: Boolean
      }
    },
    verificationScore: Number,  // 0-20
    estimatedLevel: Number,
    discrepancies: [{
      dimension: String,
      selfReported: Number,
      verified: Number,
      note: String
    }]
  },

  contact: {
    email: String,
    phone: String,
    name: String,
    websiteUrl: String,
    preferredLanguage: "en" | "hi" | "kn",
    consent: {
      saveReport: Boolean,
      emailFollowUp: Boolean,
      whatsappFollowUp: Boolean
    }
  },

  status: "completed" | "partial" | "verified" | "converted",
  motherboardClientId: ObjectId,

  source: String,    // "website" | "whatsapp_share" | "linkedin" | "direct" | "walk_in"
  referrer: String,
  completedAt: Date,
  createdAt: Date,
  updatedAt: Date
}
```

### Extending the Motherboard Client Model

When an assessment converts to a client, data flows into the existing Client model. No schema changes needed — `metadata` is already `map[string]interface{}`.

```go
metadata: {
  "assessment": {
    "assessmentId": "abc123",
    "maturityLevel": 1,
    "maturityLabel": "Present",
    "overallScore": 1.67,
    "topGaps": ["whatsappEmail", "analytics", "website"],
    "pattern": "spiky",
    "verificationScore": 6,
    "assessedAt": "2026-03-23T..."
  }
}

source: "assessment"

tags: ["level-1", "local-business", "hindi", "healthcare"]

onboarding: {
  stage: "assessed"
  // assessed → call_booked → proposal_sent → engaged → active
}
```

---

## API Endpoints

### Public (tathya.dev — Next.js Route Handlers)

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| `POST` | `/api/assess` | Submit answers, calculate scores, store, return report | None |
| `GET` | `/api/assess/[id]` | Fetch results by ID (shareable link) | None |
| `POST` | `/api/assess/[id]/contact` | Add contact info after report shown | None |
| `POST` | `/api/assess/[id]/book` | Booking intent; optionally create Motherboard client | None |

### Private (Tathya Plugin via Motherboard Proxy)

| Method | Path (via `/api/plugins/tathya/`) | Purpose | Auth |
|--------|-----------------------------------|---------|------|
| `GET` | `/assessments` | List all (dashboard) | Workspace + entitlement |
| `GET` | `/assessments/:id` | Full detail with verification | Workspace + entitlement |
| `POST` | `/assessments/:id/verify` | Run/update verification checks | Workspace + entitlement |
| `POST` | `/assessments/:id/convert` | Convert to Motherboard Client | Workspace + entitlement |
| `GET` | `/assessments/analytics` | Aggregate stats | Workspace + entitlement |
| `POST` | `/assessments/:id/followup` | Trigger WhatsApp/email via Motherboard plugins | Workspace + entitlement |

---

## UI Components

### Public: `/assess`

```
src/app/assess/
├── page.tsx                    # Landing: "Is your digital marketing working?"
├── form/
│   ├── page.tsx                # Assessment form (multi-step)
│   ├── gateway.tsx             # 3 gateway questions → route to path A/B/C
│   ├── path-a.tsx              # Starting Fresh (12 questions, Hindi/English)
│   ├── path-b.tsx              # Growing (standard 40 questions)
│   ├── path-c.tsx              # Scaling (full technical)
│   └── section.tsx             # Reusable section component
├── [id]/
│   └── page.tsx                # Public report page (shareable URL)
└── components/
    ├── radar-chart.tsx          # D3 radar chart
    ├── score-card.tsx           # Dimension breakdown card
    ├── gap-reveal.tsx           # Top 3 gaps with plain-language explanation
    ├── benchmark-comparison.tsx # Comparison to similar businesses
    ├── verification-overlay.tsx # Screenshot + data evidence (post-verify)
    ├── plain-report.tsx         # Path A simplified report (no radar, no jargon)
    └── cta-section.tsx          # Save report / Email breakdown / Book call
```

### Private: `/dashboard/assessments`

```
src/app/dashboard/assessments/
├── page.tsx                    # List: sortable, filterable
├── [id]/
│   └── page.tsx                # Deep dive: scores + answers + verification + actions
└── analytics/
    └── page.tsx                # Aggregate: submissions, avg maturity, conversion rates, gaps
```

Uses existing dashboard layout. The "core vitals" placeholder shows:
- Total assessments this month
- Average maturity level
- Top 3 gaps across all submissions
- Conversion rate (assessment → call → client)
- Revenue from assessment-sourced clients

---

## Prospect → Client Pipeline

```
Assessment Submitted
       │
       ▼
  assessments collection (status: "completed")
       │
  Contact info provided
       │
       ▼
  status: "contacted" → trigger WhatsApp/Email follow-up via Motherboard plugins
       │
  Call booked
       │
       ▼
  POST /api/clients → Create Client in Motherboard CRM
    source: "assessment"
    metadata.assessment: { scores, gaps, pattern }
    tags: ["level-1", "local", "hindi"]
    onboarding.stage: "call_booked"
       │
  Strategy call → you have all the data
       │
       ▼
  POST /clients/:id/transition → "proposal_sent"
       │
  Proposal accepted
       │
       ▼
  transition → "engaged" → Sprint 1 begins
    Plugins activate:
    ├── WhatsApp comms
    ├── Email updates
    ├── Inventory (if applicable)
    └── Astrology (if applicable)
```

Uses EXISTING `POST /api/clients/:id/transition`. No new workflow engine.

---

## Plugin Mapping to Client Types

| Client Type | Relevant Plugins | How They Connect |
|-------------|-----------------|-----------------|
| **Jyotish** | `astrology`, `whatsapp`, `telegram` | Astrology plugin exists. WhatsApp for comms. Assessment identifies Level 0. |
| **Ophthalmology** | `inventory`, `whatsapp`, `email`, `sms` | Inventory for lens/frame/medication. WhatsApp for reminders. Assessment identifies marketing + ops gaps. |
| **E-commerce** | `inventory`, `orders`, `email`, `whatsapp` | Inventory for stock. Orders for fulfilment. Assessment identifies which channels work. |
| **CRM Need** | `whatsapp`, `email`, core CRM | Motherboard CRM IS the solution. Assessment identifies they need structured lead management. |

The assessment qualifies which Motherboard plugins the client needs. Maturity gaps → plugin recommendations.

---

## Localisation (i18n)

### Approach

Use `next-intl` with JSON message files. Route-based or cookie-based language selection.

```
/messages/en.json    # Default
/messages/hi.json    # Hindi — build first
/messages/kn.json    # Kannada — second
```

All question text, answer options, report text, CTA text, and error messages need translation. Scoring logic is language-independent.

### Data Tracks Language

```javascript
profile.language       // which language the form was taken in
contact.preferredLanguage  // for follow-up messages
```

Feeds: WhatsApp messages in Hindi, email in Hindi, report PDF in Hindi.

---

## Verification Automation

`POST /api/plugins/tathya/assessments/:id/verify`

**Input:** Assessment ID (website URL and business name from the assessment)

**Process:**
1. Fetch website → status code, `<title>`, `<meta description>`, analytics scripts
2. PageSpeed Insights API → Core Web Vitals
3. Google Places API → GBP existence, rating, reviews
4. Social handles → public page fetch, existence, follower count, last post
5. Store in `verification.checks`
6. Flag manual checks (WhatsApp, in-person)

**Semi-Automated Workflow:**

```
Assessment submitted
       │
  Auto-verify runs immediately (website, speed, meta tags, GBP)
       │
  Results stored. Discrepancies flagged.
       │
  You review in dashboard. Add manual checks.
       │
  Full verified report available.
```

**Cost:** PageSpeed API free. Google Places API free tier (10K/month). Social checks via public page fetches.

---

## Implementation Priority

| # | What | Where | Why First |
|---|------|-------|-----------|
| 1 | Assessment data model + API | Tathya-mb or plugin service | Everything depends on storing and retrieving assessments |
| 2 | Public assessment form (`/assess`) | tathya.dev | The product prospects interact with |
| 3 | Scoring engine + instant report | tathya.dev + API | Form is worthless without the payoff |
| 4 | Hindi translation | `messages/hi.json` | First clients speak Hindi |
| 5 | Dashboard view (`/dashboard/assessments`) | tathya.dev | You need to see and manage submissions |
| 6 | Assessment → Client conversion | Motherboard API integration | Connects to existing CRM pipeline |
| 7 | Automated verification | Tathya plugin API | Replaces manual checks with API calls |
| 8 | WhatsApp follow-up | Motherboard WhatsApp plugin | Follow-up in the channel prospects use |
| 9 | Benchmarking engine | Tathya-mb | Needs real submission data before it's meaningful |
