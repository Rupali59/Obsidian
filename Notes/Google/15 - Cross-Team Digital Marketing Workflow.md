# Cross-Team Digital Marketing Workflow

> Team Operations & Tool Stack · Module 15

← [[Notes/Google/Fundamentals of Digital Marketing - Google]]

---

## Index

| # | Section |
|---|---------|
| 1 | [[#1. Roles and Responsibilities]] |
| 2 | [[#2. Campaign Planning Process]] |
| 3 | [[#3. Weekly and Monthly Cadence]] |
| 4 | [[#4. Content-to-Launch Pipeline]] |
| 5 | [[#5. Shared Metrics and Dashboards]] |
| 6 | [[#6. Tool Stack]] |
| 7 | [[#7. AI Integration Across Teams]] |
| 8 | [[#8. Templates]] |

---

## 1. Roles and Responsibilities

Every team member doesn't need to do everything. Assign clear ownership so nothing falls through the cracks.

### Core Roles

| Role | Owns | Key Modules |
|------|------|-------------|
| **Strategy Lead** | Goals, personas, competitive analysis, budget allocation | [[02 - Build Your Digital Marketing Strategy]], [[03 - Know Your Digital Customers]] |
| **Content Creator** | Blog posts, social copy, email copy, video scripts, visual assets | [[04 - Create Engaging Content]], [[14 - Create Engaging Videos for Your Customers]] |
| **SEO Specialist** | Keyword research, on-page optimisation, technical SEO, Search Console | [[07 - Help Customers Find You Through Search]] |
| **Paid Media Manager** | Google Ads, Meta Ads, display, retargeting, budget management | [[11 - Choose the Right Marketing Channels for Your Budget]] |
| **Social Media Manager** | Organic social strategy, community engagement, influencer partnerships | [[06 - Make Social Media Work for You]] |
| **Email Marketer** | Email campaigns, automation flows, list management, deliverability | [[13 - Craft Effective Email Campaigns]] |
| **Analytics Lead** | GA4, reporting, dashboards, attribution, data-driven recommendations | [[05 - Get the Most from Your Business Data]] |
| **Web / Tech Lead** | Website, apps, chatbots, tracking implementation, site speed | [[08 - Improve Your Business with Websites and Apps]] |

> **Small teams:** One person may cover multiple roles. The important thing is that every responsibility has a named owner.

### RACI for Key Activities

| Activity | Responsible | Accountable | Consulted | Informed |
|----------|-------------|-------------|-----------|----------|
| Campaign strategy | Strategy Lead | Strategy Lead | All roles | Stakeholders |
| Content creation | Content Creator | Content Creator | SEO, Social | Strategy Lead |
| SEO review of content | SEO Specialist | SEO Specialist | Content Creator | Strategy Lead |
| Paid campaign setup | Paid Media Manager | Paid Media Manager | Strategy Lead | Analytics |
| Social posting | Social Media Manager | Social Media Manager | Content Creator | Strategy Lead |
| Email campaigns | Email Marketer | Email Marketer | Content Creator | Analytics |
| Performance reporting | Analytics Lead | Analytics Lead | All roles | Stakeholders |
| Website updates | Web / Tech Lead | Web / Tech Lead | SEO, Content | Strategy Lead |

---

## 2. Campaign Planning Process

### Campaign Brief Template

Before launching any campaign, complete a brief that aligns the team:

| Field | Description |
|-------|-------------|
| **Campaign name** | Clear, descriptive |
| **Objective** | SMART goal (from [[02 - Build Your Digital Marketing Strategy#SMART Goals Framework]]) |
| **Target persona** | Which persona? (from [[03 - Know Your Digital Customers#1. Customer Personas]]) |
| **Key message** | One sentence: what do we want them to know, feel, or do? |
| **Channels** | Which channels? Who owns each? |
| **Content needs** | List of assets needed (blog, video, email, social posts, ads) |
| **Budget** | Total and per-channel allocation |
| **Timeline** | Start, key milestones, end date |
| **Success metrics** | KPIs tied to the objective |
| **Owner** | Who is accountable for the campaign overall? |

### Planning Steps

```
1. Strategy Lead defines objective and persona
2. Team brainstorms themes and messaging (AI can assist)
3. Content Creator drafts content plan and asset list
4. SEO Specialist reviews keywords and optimisation opportunities
5. Paid Media Manager plans targeting and budget allocation
6. Social Media Manager plans organic distribution
7. Email Marketer plans supporting email sequences
8. Analytics Lead sets up tracking and baseline metrics
9. Strategy Lead reviews and approves brief
10. Execution begins
```

---

## 3. Weekly and Monthly Cadence

### Weekly Rhythm

| Day | Activity | Who |
|-----|----------|-----|
| **Monday** | Weekly standup: review last week's metrics, this week's priorities | All |
| **Tuesday–Thursday** | Content creation, campaign execution, ad optimisation | Respective owners |
| **Friday** | Content review and scheduling for next week; SEO check on new content | Content + SEO |

### Weekly Standup Agenda (30 min)

1. **Wins:** What performed well? (2 min per person)
2. **Metrics snapshot:** Key numbers vs targets (Analytics Lead, 5 min)
3. **Blockers:** What's stuck? Who needs help? (5 min)
4. **This week's priorities:** What's each person focused on? (10 min)
5. **Decisions needed:** Anything requiring group input (5 min)

### Monthly Rhythm

| When | Activity | Who |
|------|----------|-----|
| **Month start** | Review previous month's performance; publish monthly report | Analytics Lead → All |
| **First week** | Adjust strategy based on data; plan next month's content calendar | Strategy Lead + Content |
| **Mid-month** | Campaign health check; budget reallocation if needed | Paid Media + Strategy Lead |
| **Month end** | Content audit; review what to repurpose; prep next month | Content + Social |

### Quarterly Review

| Focus | Questions |
|-------|----------|
| **Strategy** | Are goals still relevant? Do personas need updating? |
| **Channels** | Which are performing? Where should we invest more/less? |
| **Competitors** | What have they changed? Any new threats or opportunities? |
| **Tools** | Are our tools still the right fit? Any new options? |
| **AI** | What new AI capabilities should we adopt? |

---

## 4. Content-to-Launch Pipeline

A clear pipeline ensures content is reviewed, optimised, and published consistently.

### Pipeline Stages

```
IDEA → BRIEF → DRAFT → REVIEW → OPTIMISE → SCHEDULE → PUBLISH → MEASURE
```

| Stage | Owner | Action | Tool |
|-------|-------|--------|------|
| **Idea** | Anyone | Log idea with topic, persona, purpose, channel | Notion, Trello, Asana |
| **Brief** | Content Creator | Fill out content brief (topic, keywords, persona, CTA, format) | Shared doc |
| **Draft** | Content Creator | Write/produce first draft. Use AI for brainstorming and first drafts. | Google Docs, Notion |
| **Review** | SEO + Strategy Lead | Check keywords, brand voice, accuracy, messaging | Comments in doc |
| **Optimise** | SEO Specialist | Meta titles, descriptions, headings, internal links, structured data | CMS + SEO tools |
| **Schedule** | Social / Email / Web Lead | Schedule across relevant channels with correct timing | Buffer, Hootsuite, CMS, email platform |
| **Publish** | Respective channel owner | Go live; verify links, tracking, formatting | — |
| **Measure** | Analytics Lead | Track performance at 24h, 7 days, 30 days; report back | GA4, Looker Studio |

### Handoff Rules

- Content moves forward only when the current stage owner marks it "ready"
- SEO review must happen before any blog or web page is published
- All paid campaigns require tracking verification before launch
- Email campaigns require a test send to at least 2 team members before launch

---

## 5. Shared Metrics and Dashboards

### North Star Metrics (Company Level)

| Metric | Source | Review Cadence |
|--------|--------|----------------|
| **Revenue from digital** | GA4 + CRM | Monthly |
| **Customer acquisition cost (CAC)** | Ad spend ÷ new customers | Monthly |
| **Customer lifetime value (CLV)** | CRM / analytics | Quarterly |
| **Return on ad spend (ROAS)** | Ad platforms + GA4 | Weekly |

### Channel Metrics

| Channel | Key Metrics | Tool |
|---------|-------------|------|
| **Organic search** | Impressions, clicks, CTR, avg. position, organic conversions | Search Console + GA4 |
| **Paid search** | Impressions, clicks, CPC, conversions, ROAS, quality score | Google Ads |
| **Social (organic)** | Followers, reach, engagement rate, top posts | Platform analytics |
| **Social (paid)** | Reach, CTR, CPA, ROAS | Meta Ads Manager, TikTok Ads, etc. |
| **Email** | Open rate, CTR, CTOR, conversion rate, unsubscribe rate, revenue per email | Email platform |
| **Website** | Sessions, bounce rate, pages/session, conversion rate, Core Web Vitals | GA4 + PageSpeed Insights |
| **Video** | Views, watch time, avg. view duration, engagement, CTR | YouTube Studio, TikTok Analytics |

### Dashboard Setup

Build a shared dashboard (Looker Studio recommended—free, connects to GA4, Ads, Search Console, Sheets):

| Dashboard Section | Contains |
|-------------------|----------|
| **Overview** | North star metrics; month-over-month trends |
| **Acquisition** | Traffic by channel; new vs returning users |
| **Engagement** | Top pages, avg. session duration, events |
| **Conversion** | Funnel visualisation; conversion rate by channel |
| **Campaigns** | Active campaign performance; spend vs results |
| **Channel deep-dives** | One tab per channel with detailed metrics |

---

## 6. Tool Stack

### Recommended Tools by Function

| Function | Free / Budget | Mid-Range | Enterprise |
|----------|---------------|-----------|------------|
| **Analytics** | GA4, Search Console | GA4 + Looker Studio | Adobe Analytics, Amplitude |
| **SEO** | Search Console, Google Keyword Planner | Ahrefs Lite, SE Ranking | Ahrefs, SEMrush |
| **Social management** | Buffer (free tier), Meta Business Suite | Buffer, Later, Hootsuite | Sprout Social |
| **Email** | Mailchimp (free tier), Brevo | Klaviyo, ConvertKit | HubSpot, ActiveCampaign |
| **Paid ads** | Google Ads, Meta Ads Manager | + TikTok Ads, LinkedIn Ads | + DV360, The Trade Desk |
| **Content / design** | Canva (free), Google Docs | Canva Pro, Figma | Adobe Creative Suite |
| **Video editing** | CapCut, iMovie | Descript, DaVinci Resolve | Adobe Premiere, Final Cut |
| **Project management** | Trello, Google Sheets | Notion, Asana | Monday.com, Jira |
| **AI assistants** | ChatGPT (free), Gemini | ChatGPT Plus, Claude Pro | Enterprise AI (Azure OpenAI, etc.) |
| **CRM** | HubSpot (free CRM) | HubSpot Starter | Salesforce, HubSpot Enterprise |

### Integration Priorities

1. **GA4 ↔ Google Ads ↔ Search Console** — link these first for unified reporting
2. **Email platform ↔ CRM / E-commerce** — sync customer data for segmentation
3. **Social management tool ↔ All social accounts** — centralised publishing and analytics
4. **Looker Studio ↔ All data sources** — single reporting dashboard

---

## 7. AI Integration Across Teams

### Where AI Fits in Each Role

| Role | AI Use Cases | Tools |
|------|-------------|-------|
| **Strategy Lead** | Competitive analysis, persona drafting, SWOT generation, market research | ChatGPT, Claude, Gemini, Perplexity |
| **Content Creator** | First drafts, headline variations, repurposing, image generation | ChatGPT, Claude, Midjourney, Canva AI, CapCut |
| **SEO Specialist** | Keyword clustering, content briefs, schema markup, meta description drafts | Clearscope, Surfer SEO, ChatGPT |
| **Paid Media Manager** | Ad copy variations, audience insights, bid strategy recommendations | Google Ads AI, Meta Advantage+, ChatGPT |
| **Social Media Manager** | Caption writing, trend research, hashtag suggestions, scheduling optimisation | ChatGPT, Buffer AI, Later AI |
| **Email Marketer** | Subject line testing, copy drafts, send-time optimisation, segmentation ideas | Klaviyo AI, Mailchimp AI, ChatGPT |
| **Analytics Lead** | Data interpretation, anomaly explanation, report narratives | GA4 AI insights, ChatGPT, Claude |
| **Web / Tech Lead** | Chatbot training, copy generation, accessibility audits | ChatGPT, Lighthouse, axe DevTools |

### AI Governance Rules

| Rule | Why |
|------|-----|
| **Human reviews all AI output before publishing** | Accuracy, brand voice, legal compliance |
| **No confidential data in public AI tools** | Data security; use enterprise versions for sensitive data |
| **Disclose AI content where required** | Platform policies, regional regulations (EU AI Act) |
| **Document AI prompts that work well** | Build a shared prompt library for consistency across the team |
| **Re-evaluate tools quarterly** | AI landscape changes fast; stay current |

### Shared Prompt Library

Maintain a shared document with proven prompts for common tasks:

| Task | Prompt Pattern |
|------|---------------|
| **Blog outline** | "Act as a [industry] content strategist. Create a detailed outline for a blog post about [topic] targeting [persona]. Include H2/H3 structure, key points per section, and a compelling intro hook." |
| **Social caption** | "Write 3 Instagram caption variations for [product/topic]. Tone: [brand voice]. Include a CTA and 5 relevant hashtags. Max 150 words." |
| **Email subject lines** | "Generate 10 subject line variations for an email about [topic/offer]. Target: [persona]. Goal: [open rate / urgency / curiosity]. Max 50 characters each." |
| **Ad copy** | "Write 5 Google Ads RSA headlines (max 30 chars) and 3 descriptions (max 90 chars) for [product/service]. USP: [value prop]. CTA: [desired action]." |
| **Competitor analysis** | "Analyse [competitor URL]. Summarise their USP, target audience, content strategy, and social presence. Identify 3 gaps or opportunities for [my business]." |

---

## 8. Templates

### Campaign Brief

```
Campaign Name: _______________
Objective (SMART): _______________
Target Persona: _______________
Key Message: _______________
Channels: _______________
Content Needs: _______________
Budget: _______________
Timeline: Start ___ → End ___
Success Metrics: _______________
Owner: _______________
```

### Content Brief

```
Title/Topic: _______________
Target Keyword: _______________
Secondary Keywords: _______________
Persona: _______________
Purpose: Entertain / Inspire / Educate / Convince
Format: Blog / Video / Social / Email / Infographic
CTA: _______________
Publish Date: _______________
Channel(s): _______________
Notes: _______________
```

### Weekly Report Template

```
Week of: _______________

## Key Metrics vs Targets
| Metric | Target | Actual | Trend |
|--------|--------|--------|-------|
| Website sessions | ___ | ___ | ↑↓→ |
| Organic traffic | ___ | ___ | ↑↓→ |
| Social engagement rate | ___ | ___ | ↑↓→ |
| Email open rate | ___ | ___ | ↑↓→ |
| Conversions | ___ | ___ | ↑↓→ |
| Ad spend / ROAS | ___ | ___ | ↑↓→ |

## Wins
- 

## Issues / Blockers
- 

## Next Week Priorities
- 
```

### Monthly Performance Report

```
Month: _______________

## Executive Summary
[2–3 sentences on overall performance]

## Channel Performance
[Table with each channel's key metrics]

## Campaign Results
[Summary of active/completed campaigns]

## Insights & Recommendations
[3–5 actionable insights from the data]

## Next Month Focus
[Top 3 priorities]
```

---

← [[14 - Create Engaging Videos for Your Customers]] | [[Notes/Google/Fundamentals of Digital Marketing - Google]]
