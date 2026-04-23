# Tathya Assessment System

> Assess, prove you understand, earn the call. No "book a consultation" button.

---

## What This Is

Prospects take a Digital Marketing Maturity Assessment on tathya.dev. They answer factual questions about their business, get an instant scorecard across 10 dimensions, see where they compare to benchmarks — and only then decide whether to book a strategy call. You walk into that call already knowing their business.

---

## The Journey

```
DISCOVER ──→ ASSESS ──→ REPORT ──→ CONSIDER ──→ CALL ──→ PROPOSE ──→ ENGAGE
```

### 1. Discover

| Source | How | Priority |
|--------|-----|----------|
| **LinkedIn** | Posts about maturity, case studies, common gaps | High — builds personal brand |
| **Organic search** | Blog content: "digital marketing audit", "is my marketing working" | High — long-term |
| **Local outreach** | Run the 10-min audit on businesses around you, DM/WhatsApp them results | High — immediate pipeline |
| **Social media** | Reels/Shorts showing quick audits, before/after, common gaps | Medium |
| **Referrals** | Past clients, industry contacts | Medium — grows naturally |

The homepage funnels to one action: **take the assessment.** Not a services page, not pricing, not "book a call."

**Above the fold:**

```
Is your digital marketing actually working?
Find out in 5 minutes. Free. No login.
[ Take the Assessment → ]
```

**Below the fold:** What you'll learn → How it works (3-step visual) → Sample report preview → Who this is for → Social proof → FAQ.

### 2. Assess

Three gateway questions route the prospect to one of three paths:

| If... | Then... |
|-------|---------|
| No website + can't be found online + word-of-mouth only | **Path A: Starting Fresh** — 12 plain-English questions, 3 min |
| Has website + mixed visibility + mix of channels | **Path B: Growing** — standard 40 questions with tooltips, 5–7 min |
| Has website + ranks on Google + multiple active channels | **Path C: Scaling** — full technical assessment, 5–7 min |

See [[02 - Maturity Model & Assessment]] for the complete question bank.

**UX:**
- Progress bar ("Section 3 of 10")
- One section per screen, tap-to-select, mobile-first
- No login, no email gate — results shown first
- "What's that?" is always a valid answer
- Micro-feedback after each section (subtle dimension badge)

### 3. Report

Instant. No "we'll email you in 24 hours."

Path A prospects get a **plain-language health check** — no radar chart, no jargon, no "Level 0" label. Outcome-oriented ("People can't find you online yet").

Path B/C prospects get the **full scorecard** — radar chart, dimension breakdown, top 3 gaps, benchmark comparison.

Both get: what the gap IS, not how to fix it. That's the strategy call.

See [[03 - Report, Verification & Engagement]] for full report design.

### 4. Consider

Three paths after the report:

| Path | What Happens |
|------|-------------|
| **Leave** | Report URL lives forever. If they gave email, they enter the follow-up sequence. |
| **Save report** | Email capture → PDF report → nurture sequence (gap-specific content, not generic blasts). |
| **Book call** | Calendar booking. Confirmation: "We've reviewed your assessment. We'll come prepared." |

### 5. Strategy Call (30 min)

| Time | What |
|------|------|
| 0–5 min | Confirm context: "You're a [type] at Level [X]. Strengths: [social, website]. Gaps: [analytics, email]. Does that match?" |
| 5–15 min | Dive into 3 lowest dimensions. What the gap costs them. Specific examples for their business type. |
| 15–25 min | Roadmap preview: 90-day sprint approach. Enough to be credible, not enough to DIY. |
| 25–30 min | "I'll send a custom proposal with POA&M, timeline, pricing within 48 hours." |

### 6. Proposal (48 hrs after call)

```
1. YOUR CURRENT STATE         (summary from assessment)
2. WHERE YOU NEED TO BE       (target maturity per dimension, 90-day)
3. THE 90-DAY PLAN            (sprints based on their gaps)
4. WHAT WE'LL DELIVER         (deliverables per sprint)
5. WHAT WE NEED FROM YOU      (access, approvals, time)
6. INVESTMENT                 (priced by scope, not time)
7. HOW WE'LL MEASURE SUCCESS  (KPIs tied to their goals)
```

### 7. Engagement

Assessment data flows into Motherboard CRM. Sprint 1 begins. Discovery phase is already done.

See [[03 - Report, Verification & Engagement]] for sprint planning and [[04 - Architecture & Implementation]] for the technical pipeline.

---

## Design Principles

| Principle | Why |
|-----------|-----|
| **Evidence over opinion** | Form asks factual questions ("Do you have GA4?" not "How good is your analytics?"). Builds trust, gives real data. |
| **Value before ask** | Prospect gets their scorecard before you ask for anything. The call becomes their idea. |
| **No black box** | They see scores, understand why they scored low. Transparency creates trust. |
| **Data does double duty** | Assessment responses = your diagnosis. Skip Stage 1 of the client workflow. Saves a week of discovery. |
| **Segmentation by maturity** | Level 1 needs different work than Level 4. Proposal and pricing are tailored. |
| **The report is proof** | When they share their report internally, they're pre-selling your service to their team. |

---

## Design & SMART goals — on tathya.dev itself

There are **two different things** people mix up: (1) what you **measure and teach clients** (SMART goals, mature UX), and (2) how the **Tathya product** should look and what **you** commit to. They stay aligned when the site *embodies* the same standards you score others on.

### How product design maps to the maturity model

You assess others on **Website & Technical Foundation** (fast, mobile-first, clear CTAs, accessibility). tathya.dev should score well on the same bar: one obvious primary CTA (assessment), readable type, fast LCP, no clutter before the ask, accessible forms and charts, and report pages that work on a ₹10k phone on 4G. Visual identity (colour, typography, motion) is secondary to **clarity and speed** — the design *is* "we practise what we measure."

| Site surface | Design job | Tie to strategy |
|--------------|------------|-----------------|
| **Home / `/assess` landing** | Single funnel, trust, no bait-and-switch | Value before ask; evidence-led copy |
| **Gateway + paths A/B/C** | Plain language vs technical tone by path | Same segmentation as maturity paths |
| **Report (Path A vs B/C)** | Outcome language vs radar + benchmarks | No black box; top gaps without prescriptions |
| **Post-report CTAs** | Save / WhatsApp / book — equal visual weight until user chooses | No forced call |
| **Hindi / Kannada** | Same layout, not a shrunken afterthought | Local-first from [[03 - Report, Verification & Engagement]] |
| **Dashboard** (you) | Dense but scannable: verification + scores + next action | Your operational view of the same data model |

Implementation detail (routes, components): [[04 - Architecture & Implementation]].

### SMART goals: clients vs Tathya

**Clients (assessment + engagement):** Dimension 1 (*Strategy & Goals*) asks whether *they* have documented goals, SMART cadence, and KPIs ([[02 - Maturity Model & Assessment]]). After they engage, the proposal ends with **"How we'll measure success"** — that section should be **their** SMART or SMART-like targets (specific metric, number, deadline), not vague "more leads."

**Tathya (your site and business):** You use the **same discipline** on yourself. The funnel metrics below are already **M**easurable and **T**ime-bound; you make them **S**pecific and **R**elevant by choosing targets per quarter, and **A**chievable by grounding them in traffic you actually have.

| SMART letter | On tathya.dev |
|--------------|----------------|
| **S** | e.g. "Grow assessment *completions* from organic + referral" not "get famous" |
| **M** | Same events you’d expect a Level 3 client to track: starts, completions, save-report, book-call (GA4 + Motherboard where applicable) |
| **A** | Targets tied to current baseline (see Conversion Targets) |
| **R** | Every goal ties to revenue or pipeline (calls → proposals → clients) |
| **T** | Review weekly/monthly in dashboard; reset quarterly |

So: **SMART is what you score clients on in the form; it’s also how you run the product.** The website doesn’t need a page titled "SMART goals" — it needs **instrumentation and reviews** that match what you sell.

### One-line alignment check

> If a prospect ran your own methodology on tathya.dev, would the site pass the same bar you set for their UX, clarity, and measurement?

---

## Course Concepts → Product Integration Map

The Google Digital Marketing course (modules 01–15) contains ~60 frameworks, 30+ checklists, and 20+ templates. They don't all go in one place. They integrate across **four layers** of the Tathya product.

### Layer 1: Assessment (what we score)

These concepts are embedded in assessment questions. The prospect doesn't see the framework name — they answer factual questions that map to it.

| Course Concept | Module | Where in Assessment | Dimension |
|---------------|--------|-------------------|-----------|
| **SMART Goals** | 02 | Q1.1 (documented goals), Q1.4 (review cadence) | Strategy |
| **USP** | 02 | Q1.3 (differentiation) | Strategy |
| **Persona / Segmentation** | 03 | Q1.2 (ideal customer defined) | Strategy |
| **Core Web Vitals** (LCP, INP, CLS) | 08 | Q2.2 (mobile), Q2.1 (speed); also verification auto-check | Website |
| **GA4** | 05 | Q3.1 (installed), Q3.2 (conversions), Q3.4 (traffic knowledge) | Analytics |
| **Conversion tracking** | 05, 11 | Q3.2, Q8.4 | Analytics, Paid Ads |
| **Keyword research** | 07 | Q4.3 (documented keywords) | Search |
| **Meta tags / titles** | 07 | Q4.4 (unique per page) | Search |
| **Search Console** | 07 | Q4.2 (set up and used) | Search |
| **Content calendar** | 04 | Q5.2 (documented, planned) | Content |
| **Content repurposing** | 04 | Q5.3 (pipeline exists) | Content |
| **AI content tools** (T-C-R-E-I) | 04 | Q5.4 (AI in workflow with guidelines) | Content |
| **Brand guidelines** | 04 | Q5.4 (prompt library, quality checks) | Content |
| **Platform-specific content** | 06 | Q6.1 (platforms), Q6.2 (frequency), Q6.4 (analytics) | Social |
| **Engagement / community** | 06 | Q6.3 (responds to DMs/comments) | Social |
| **Email list / segmentation** | 13 | Q7.1 (list size), Q7.2 (frequency) | WhatsApp+Email |
| **Automation flows** (welcome, cart abandon, win-back) | 13 | Q7.3 (which automations exist) | WhatsApp+Email |
| **Email deliverability** (SPF, DKIM, DMARC) | 13 | Q7.4 (knows metrics) | WhatsApp+Email |
| **ROAS / conversion tracking** | 11 | Q8.2 (knows ROAS), Q8.4 (tracking works) | Paid Ads |
| **Retargeting** | 11 | Q8.3 (retargeting active) | Paid Ads |
| **Smart Bidding / Performance Max** | 11 | Q8.1 (multi-platform sophistication) | Paid Ads |
| **Checkout optimisation** (BNPL, one-click, UPI) | 09 | Q9.1 (payment options, friction) | Conversion |
| **Reviews / social proof** | 09, 12 | Q9.2 (systematic collection) | Conversion |
| **RACI / team structure** | 15 | Q10.1 (who handles marketing), Q10.4 (process maturity) | Team |
| **Tool adoption** | 15 | Q10.3 (which tools in use) | Team |

**Not scored but used for routing:** Business type (Q0.1) → determines benchmarks, Path A/B/C routing, and India-adjusted dimensions.

### Layer 2: Report & Follow-Up (what we teach)

These concepts don't appear in the assessment but **explain the gaps**. They power the follow-up emails, the strategy call, and the educational content that nurtures prospects.

| Course Concept | Module | Where It Goes | Triggered By |
|---------------|--------|--------------|-------------|
| **SWOT Analysis** | 02 | Strategy call prep (your internal framework for analysing client position) | Any engagement |
| **See / Think / Do / Care** | 03, 06 | Follow-up emails explaining customer journey gaps; strategy call framing | Low Strategy or Content scores |
| **Customer journey mapping** (Awareness → Retention) | 03 | Follow-up email #2 (gap deep-dive): "Your customers go through these stages — here's where you lose them" | Low Analytics or Conversion scores |
| **E-E-A-T** | 07 | Report gap explanation for Search dimension: "Google evaluates your Experience, Expertise, Authority, Trust" | Low Search score |
| **Data Cycle** (Plan → Do → Check → Act) | 05 | Follow-up for Analytics gap: "Data only works if you close the loop" | Low Analytics score |
| **Sales funnel** (Awareness → Conversion) | 11 | Strategy call: frame their paid ads within the funnel; explain why retargeting matters | Low Paid Ads score |
| **Quality Score** (Google Ads) | 11 | Strategy call or proposal: "Your ads cost more because Quality Score is low" | Low Paid Ads + has Google Ads |
| **Keyword match types** (broad, phrase, exact) | 11 | Proposal detail for SEM work | Paid Ads engagement includes Google Ads |
| **Nano/Micro/Macro influencer tiers** | 06 | Proposal for social strategy: which tier fits their budget | Social engagement, Level 2+ |
| **Social commerce** (Instagram Shop, TikTok Shop) | 09 | Follow-up content for e-commerce clients: "You're selling but not where your customers browse" | E-commerce + low Social or Conversion |
| **A/B testing** | 11, 13 | Sprint 2–3 activities in proposal | Level 2+ engagement |
| **Email metrics** (open rate, CTOR, revenue per email) | 13 | Follow-up email for WhatsApp+Email gap: "Here's what good looks like" | Low WhatsApp+Email score |
| **Double opt-in / one-click unsubscribe** | 13 | Deliverable: set these up in Sprint 1 if building email | Email setup in engagement |
| **SPF / DKIM / DMARC** | 13 | Deliverable: configure during Sprint 1 for deliverability | Email setup in engagement |
| **Video types & metrics** | 14 | Follow-up for Content gap: "Short-form video is the fastest way to grow" | Low Content + low Social |
| **PESTEL** | 10 | Only for clients expanding internationally — not default | Rare: international client |
| **hreflang / localisation** | 10 | Only for multi-market clients | Rare: international client |
| **WCAG accessibility** | 08 | Verification overlay: "Your site isn't accessible" with specific failures | Website verification |
| **Structured data / schema** | 07, 12 | Verification: does the site have LocalBusiness, Product, FAQ schema? | Website + Search verification |
| **NAP consistency** | 12 | Verification: name/address/phone match across directories | Local business verification |

### Layer 3: Engagement Deliverables (what we build for clients)

These are **templates and tools** from the course that become tangible deliverables during client sprints. They live in the Motherboard dashboard or are delivered as shared docs.

| Deliverable | Source Concept | Module | When Delivered | Sprint |
|------------|---------------|--------|---------------|--------|
| **SMART goals document** | SMART framework | 02 | Sprint 1: foundation | 1 |
| **Persona document** | Persona template | 03 | Sprint 1: strategy work | 1 |
| **Digital presence audit** | Audit framework + verification | 02 | Pre-engagement (assessment + verification = this) | 0 |
| **Competitive analysis** (3–5 competitors) | Research framework | 02 | Sprint 1 | 1 |
| **Content calendar** | Calendar template | 04 | Sprint 2: build the engine | 2 |
| **Content brief template** | Content brief | 15 | Sprint 2: for each content piece | 2 |
| **Brand guidelines doc** | Brand attributes | 04 | Sprint 1 or 2 depending on maturity | 1–2 |
| **AI prompt library** | T-C-R-E-I + shared prompts | 04, 15 | Sprint 2–3: team enablement | 2–3 |
| **Campaign brief** | Campaign brief template | 15 | Every campaign from Sprint 2 onward | 2+ |
| **RACI matrix** | RACI framework | 15 | Sprint 1: who does what | 1 |
| **Email automation flows** | Welcome, cart abandon, win-back | 13 | Sprint 1–2 depending on maturity | 1–2 |
| **GA4 dashboard** (Looker Studio) | Dashboard template | 05, 15 | Sprint 1: measurement foundation | 1 |
| **Monthly report** | Report template | 15 | Every month from Sprint 1 | 1+ |
| **Weekly standup agenda** | Standup template | 15 | Sprint 1: process setup | 1 |
| **Quarterly review** | Review framework | 15 | End of 90-day engagement | 3 |
| **Google Business Profile setup** | GBP checklist | 12 | Sprint 1 for local businesses | 1 |
| **SEO keyword map** | Keyword research process | 07 | Sprint 1–2 | 1–2 |
| **Retargeting setup** | Retargeting steps | 11 | Sprint 2–3 | 2–3 |
| **Email deliverability config** | SPF/DKIM/DMARC | 13 | Sprint 1 when setting up email | 1 |
| **Checkout optimisation** | E-commerce checklist | 09 | Sprint 2 for e-commerce clients | 2 |

### Layer 4: Content Engine (what powers tathya.dev blog/social)

These concepts become **published content** on tathya.dev — blog posts, LinkedIn posts, newsletter issues, and assessment-related educational material. Each one is tied to a dimension so it feeds the right nurture segment.

| Content Topic | Source | Targets Dimension | Format |
|--------------|--------|------------------|--------|
| "What are SMART goals and why your business needs them" | 02 | Strategy gap | Blog + LinkedIn |
| "The 10-minute digital audit you can run on any business" | Verification toolkit | All | Blog (hero content) |
| "What Google actually looks for: E-E-A-T explained" | 07 | Search gap | Blog |
| "Your website is slow and it's costing you customers" | 08 (Core Web Vitals) | Website gap | Blog + follow-up email |
| "GA4 in 10 minutes: what to set up and what to ignore" | 05 | Analytics gap | Blog + YouTube |
| "The content repurposing pipeline: 1 piece → 5 formats" | 04 | Content gap | Blog + Instagram carousel |
| "Why you need a content calendar (and a free template)" | 04 | Content gap | Blog (lead magnet) |
| "Email is not dead: why it's still the highest-ROI channel" | 13 | WhatsApp+Email gap | Newsletter + blog |
| "WhatsApp Business vs personal: what you're missing" | India playbook | WhatsApp+Email gap | Blog (Hindi) |
| "Retargeting for beginners: stop losing visitors" | 11 | Paid Ads gap | Blog |
| "How to get Google reviews (and why 15 changes everything)" | 12 | Conversion/Search gap | Blog (Hindi) |
| "See-Think-Do-Care: the customer journey you're ignoring" | 03 | Strategy gap | LinkedIn |
| "We assessed [N] businesses — here's the #1 gap" | Assessment aggregate data | All | Yearly report |
| "Month [X]: my own maturity score and what I did" | Self-assessment | All | LinkedIn + newsletter |
| "The tool stack at every budget level" | 15 | Team gap | Blog |
| "AI for marketing: what works, what's hype" | 04 (T-C-R-E-I) | Team gap | Blog + LinkedIn |
| "How to read your website's PageSpeed score" | 08 | Website gap | YouTube (Hindi) |
| "Social commerce in India: Instagram Shop, WhatsApp Catalogue" | 09 | Conversion gap | Blog (Hindi) |

### Checklists: Where They Live

Every module has checklists. They integrate at **two levels**:

**1. Internal (your process):** Checklists become your Sprint 1/2/3 task lists during client engagement. They don't need to be visible to the prospect — they're your operational playbook.

| Checklist Category | Modules | Your Use |
|-------------------|---------|----------|
| Strategy (SMART, audit, research, USP) | 02 | Sprint 1 discovery and planning |
| Persona + journey | 03 | Sprint 1 persona workshop |
| Content (planning, calendar, AI prompting) | 04 | Sprint 2 content setup |
| Data (collection, dashboard, journey goals) | 05 | Sprint 1 analytics foundation |
| Social (platform selection, content plan) | 06 | Sprint 2 social setup |
| SEO (website refinement, keywords, goals) | 07 | Sprint 1–2 SEO work |
| Website (planning, design, accessibility, chatbot) | 08 | Sprint 1 website fixes |
| E-commerce (goals, payments, promotion, social commerce) | 09 | Sprint 2 for e-commerce clients |
| International (SEO, expansion readiness) | 10 | Only for international clients |
| Paid (goals, SEM, retargeting, social ads, video) | 11 | Sprint 2–3 paid setup |
| Local (GBP, NAP, reviews, schema) | 12 | Sprint 1 for local businesses |
| Email (audit, creation, automation, deliverability) | 13 | Sprint 1–2 email setup |
| Video (strategy, content plan, promotion) | 14 | Sprint 2–3 content expansion |
| Team (RACI, campaign brief, standup, report) | 15 | Sprint 1 process setup |

**2. Client-facing (optional):** Selected checklists can be surfaced in the Motherboard dashboard as "next steps" tied to the client's maturity level — but only after engagement begins. Not in the free report.

### What Does NOT Go Into tathya.dev

Some course material is **reference knowledge** you carry in your head, not product surface:

- **PESTEL** — too academic for most Indian SMB clients; use when relevant in proposal
- **Four Ps** — foundational but not actionable as a deliverable
- **Owned / Earned / Paid** taxonomy — framing tool for your strategy thinking, not client-facing
- **SEM auction mechanics / Ad Rank formula** — you need to know this, the client doesn't
- **Programmatic display / DV360 / The Trade Desk** — enterprise tools; not your first market
- **International payments** (iDEAL, Bancontact, Alipay) — only relevant for specific clients
- **Video production details** (storyboards, batching) — operational, not product

---

## Conversion Targets

| Metric | Target | Measures |
|--------|--------|----------|
| Assessment completions | 70%+ of starts | Form UX |
| Email captures | 40%+ of completions | Report value |
| Strategy calls booked | 10–15% of completions | Report persuasiveness |
| Proposals sent | 90%+ of calls | Call quality |
| Proposals accepted | 50%+ of proposals | Pricing fit |
| **Assessment → Paying Client** | **5–8% overall** | **System effectiveness** |

---

## What the Prospect Gets (Free) vs Doesn't Get (Until Engagement)

| Free | Paid |
|------|------|
| Maturity score (overall + per dimension) | Custom recommendations ("do X, then Y") |
| Radar chart showing strengths and gaps | Implementation support |
| Benchmark comparison for their business type | Tool configuration |
| Shareable report | Strategy roadmap |
| Clear label: "Level 2: Active — here's what that means" | Ongoing management |
