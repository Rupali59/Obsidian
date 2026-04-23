# Get the Most from Your Business Data

> Data & Analytics · Module 5

← [[Notes/Google/Fundamentals of Digital Marketing - Google]]

---

## Index

| # | Section |
|---|---------|
| 1 | [[#1. Digital Marketing Strategy and Data]] |
| 2 | [[#2. The Data Cycle]] |
| 3 | [[#3. Top Tips for Gathering Data]] |
| 4 | [[#4. Analytics and the Customer Journey]] |
| 5 | [[#5. Managing and Presenting Data]] |
| 6 | [[#6. Checklists]] |

---

## 1. Digital Marketing Strategy and Data

Using data to inform and improve your digital marketing strategy in a structured way is essential.

### A Robust Digital Marketing Strategy

A strategy outlines how to get from where you are now to where you want to be. For long-term success:

| Principle | Description |
|-----------|-------------|
| **Set realistic expectations** | Goals can take time to achieve. |
| **Track your results** | Understand what's working and what's not; make changes and improve. |
| **Adapt to changes** | Stay current with technology, AI capabilities, privacy regulations, and industry shifts. |

### Performance Goals

Performance goals measure the actions customers take when they arrive at your website or store. They vary by business model.

| Business Type | Key Metrics |
|---------------|-------------|
| **E-commerce** | Add to cart, purchases, product page views, purchase value, return on ad spend (ROAS) |
| **App** | Installs, downloads, first opens, in-app events |
| **Lead gen** | Phone calls, form submissions; sales team follow-up; cost per lead (CPL) |
| **Content / media** | Page views, time on site, subscriber growth, ad revenue |

**Advice:** Understand how the client makes money first—profit margins, lead conversion—then give sound marketing advice. The data never lies when attribution is set up correctly.

### What is an Insight?

An **insight** is a deep understanding from analysing data or experiences. It reveals non-obvious patterns and guides decisions.

| Data | Insight |
|------|---------|
| Sales dropped 20% last quarter | Customer feedback shows a competitor's new feature is attracting users → need for innovation |

An **actionable insight** identifies what to do next to improve.

---

## 2. The Data Cycle

Collect, analyse, and use data to guide decisions. The cycle: **Plan → Do → Check → Act**.

| Stage | Description |
|-------|-------------|
| **1. Plan** | Identify a realistic goal (e.g. +10% social followers). Use existing data (visits, sales, GA4 analytics) to check achievability. Define campaign goals that support main goals. |
| **2. Do** | Implement: create and launch content across relevant channels. Design ads; target audience with engaging content. |
| **3. Check** | Review data relevant to the goal. E.g. one social site gains more followers. Evaluate metrics (clicks, visits). Compare to goals. *Give approaches 2–3 months before reviewing.* |
| **4. Act** | Adjust based on insights. E.g. change posting frequency, content type on underperforming channels. Optimise future campaigns. |

---

## 3. Top Tips for Gathering Data

| Tip | Description |
|-----|-------------|
| **Stay focused** | Don't collect everything. Focus on data relevant to your goals; capture the right information at the right time. |
| **Stay up-to-date** | Review data at regular intervals. Spot anomalies (seasonal spikes, drops). |
| **Use the right tools** | GA4 for web analytics, platform insights for social, Google Search Console for search performance. AI-powered dashboards (Looker Studio, Power BI) for automated reporting. |
| **Review past data** | Use historical data; compare similar datasets (apples to apples); watch for outliers. |
| **Prioritise first-party data** | With third-party cookies deprecated, your own data (email, purchase history, on-site behaviour) is your most valuable asset. |

### Using AI for Analysis

AI tools can analyse large datasets quickly—reviews, sentiment, market research—to identify trends and insights. For AI analysis fundamentals and the T-C-R-E-I prompting framework, see [[04 - Create Engaging Content#3. Using AI for Content Creation]].

| AI Use Case | Example |
|-------------|---------|
| **Anomaly detection** | GA4 AI insights automatically flag unusual traffic spikes or drops |
| **Predictive analytics** | GA4 predictive metrics estimate purchase probability and churn risk |
| **Sentiment analysis** | AI analyses customer reviews at scale to spot trends |
| **Report generation** | AI summarises key metrics into natural-language reports |

---

## 4. Analytics and the Customer Journey

### Types of Data

| Type | Description | Source |
|------|-------------|--------|
| **Quantitative** | Numerically measured (visits, sales) | GA4, social media analytics, ad platforms |
| **Qualitative** | Descriptive (opinions, sentiment, language) | Reviews, surveys, open-ended questions |
| **Online vs offline** | Combine in-store surveys with online reviews for a fuller picture | Both channels |

**Choose by goal:** Feelings → qualitative. Numbers (e.g. blog reads) → analytics. Combining both gives richer insights.

### GA4 (Google Analytics 4)

GA4 is the current Google analytics platform (Universal Analytics was sunset in July 2023). Key features:

| Feature | Description |
|---------|-------------|
| **Event-based tracking** | Every interaction is an event (page view, scroll, click, purchase) |
| **AI-powered insights** | Automated anomaly detection and trend identification |
| **Predictive metrics** | Purchase probability, churn probability, predicted revenue |
| **Cross-platform** | Tracks website and app in one property |
| **Privacy-centric** | Designed for a cookieless future; uses modelled data to fill gaps |
| **Explorations** | Freeform, funnel, path, and cohort analysis |

### Analytics by Journey Stage

| Stage | What You Can Measure |
|-------|----------------------|
| **Awareness** | How people find you; which search engines; which pages they land on; AI Overview appearances |
| **Engagement** | Do they browse, sign up, or leave? Scroll depth, video plays, time on page |
| **Conversion** | Reservations, add to basket, purchases |
| **Retention** | Repeat visits; advocates sharing content; customer lifetime value (CLV) |

### Getting Specific: Strategies

| Step | Action |
|------|--------|
| **Identify goals** | Set clear, quantifiable goals per stage. E.g. Awareness: click from social; Engagement: sign up for free consultation; Conversion: first purchase; Retention: voucher code from newsletter. Revisit SMART goals from [[02 - Build Your Digital Marketing Strategy]]. |
| **Configure tools** | Set up conversions in GA4. Configure events and mark key events as conversions. |
| **Find actionable insights** | Spot bottlenecks. E.g. only 2% of social visitors sign up; weekends see 6% vs 3% reservation rate; booking page visits but no appointments. |
| **Make changes** | Act on insights: offer 10% off for newsletter sign-up; boost weekend advertising; simplify booking. |

---

## 5. Managing and Presenting Data

### Organising and Analysing

| Tool | Use |
|------|-----|
| **Spreadsheets** | Google Sheets, Excel for manual data analysis. Functions, filters, pivot tables. |
| **Looker Studio (Google)** | Free dashboard tool. Connect GA4, Google Ads, Search Console, Sheets for automated reports. |
| **Power BI / Tableau** | Enterprise-level visualisation and reporting. |
| **AI-powered summaries** | Use ChatGPT, Claude, or Gemini to interpret data exports and generate narrative summaries. |

### Presenting Your Data

#### Know Your Audience

Your audience = those reviewing the data (colleagues, stakeholders, investors). Ask:

- What roles do they hold?
- What level of knowledge?
- What decisions will they make from this data?

#### Choose Your Format

| Format | Best For |
|--------|----------|
| **Tables** | Smaller datasets; quick comparisons |
| **Pie charts** | Percentages; proportional data |
| **Bar charts** | Comparing related items; bar length = value |
| **Line graphs** | Data over time (e.g. traffic trends) |
| **Heat maps** | Performance by area (e.g. click hotspots) |
| **Dashboards** | Live, updating views for ongoing monitoring (Looker Studio, Power BI) |

---

## 6. Checklists

### AI Data Analysis Checklist

- [ ] Identify a goal and relevant data
- [ ] Choose an AI tool (ChatGPT, Claude, Gemini, or platform-native AI)
- [ ] Check data isn't confidential; review tool's data usage policies
- [ ] Enter prompt using T-C-R-E-I framework; include the goal
- [ ] Verify AI output against raw data

### Data Collection Checklist

- [ ] What qualitative data do you collect?
- [ ] What quantitative data do you collect?
- [ ] How frequently do you collect it?
- [ ] Are you building first-party data assets (email, CRM, on-site behaviour)?

### Customer Journey Goals Checklist

- [ ] Identify one goal per stage: Awareness, Engagement, Conversion, Retention
- [ ] E.g. Conversion: 25% of basket-adders make a purchase
- [ ] E.g. Retention: Increase 4–5 star reviews over next 3 months
- [ ] Find insightful data for each goal
- [ ] Identify 1–2 bottlenecks preventing goal achievement

### Dashboard Planning Checklist

- [ ] Note important metrics to track (e.g. clicks to website, conversion rate, ROAS)
- [ ] Identify links between data (e.g. content topic and clicks; social origin and purchase %)
- [ ] Choose a visualisation tool (Looker Studio, Power BI, spreadsheet)
- [ ] Set up automated reporting cadence (weekly, monthly)

---

← [[04 - Create Engaging Content]] | [[Notes/Google/Fundamentals of Digital Marketing - Google]] | [[06 - Make Social Media Work for You]] →
