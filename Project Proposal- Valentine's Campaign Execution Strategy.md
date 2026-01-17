
## 1. Summary

This document outlines the operational blueprint for the "Date Night Edit" campaign. To mitigate ad-policy risks associated with the "Intimacy" category and maximize conversion within the 18-day window (Jan 27 – Feb 14), we will deploy a **High-Velocity Micro-Site** on a dedicated domain.

Primary Objective: Maximize Net Profit via a two-phase logistics strategy (National + Hyper-local).

Secondary Objective: Protect the primary Dhaaga Stories domain reputation.

---

## 2. Unit Economics & Pricing Strategy

To ensure campaign profitability, the Average Order Value (AOV) must absorb Customer Acquisition Cost (CAC) and Shipping.

**Strategic Recommendation:** We strictly advertise **The Bundle (₹1,499)**.

|**Component**|**Single Candle (₹999)**|**The Bundle (₹1,499)**|
|---|---|---|
|**Gross Revenue**|**₹999.00**|**₹1,499.00**|
|Payment Gateway (2.36%)|- ₹23.60|- ₹35.40|
|COGS (Est. Product Cost)|- ₹250.00|- ₹300.00|
|Shipping (Delhivery Surface)|- ₹90.00|- ₹90.00|
|**Gross Margin (Pre-Ads)**|**₹635.40**|**₹1,073.60**|
|_Est. Ad Spend (CAC)_|_- ₹450.00_|_- ₹450.00_|
|**Net Profit Per Unit**|**₹185.40**|**₹623.60**|
|**Net Margin %**|**18% (High Risk)**|**41% (Healthy)**|

**Analysis:** The Single Candle offers insufficient buffer against ad cost volatility. The Bundle maintains profitability even if CAC spikes to ₹700 during Valentine's peak week.

---

## 3. Marketing & Revenue Projections

Proposed Budget: ₹15,000 (Scalable based on ROAS).

Launch Timeline: Jan 27 – Feb 14.

Based on industry benchmarks for Indian D2C Gifting, here are the projected outcomes:

|**Metric**|**Conservative Scenario**|**Target Scenario**|
|---|---|---|
|**Ad Budget**|₹15,000|₹15,000|
|**Cost Per Acquisition (CPA)**|₹500|₹350|
|**Total Orders**|30|43|
|**Gross Revenue**|**₹44,970**|**₹64,457**|
|**Total Net Profit**|**~₹18,700**|**~₹26,800**|

_Note: These projections exclude organic sales from existing followers, which would be 100% margin accretive._

---

## 4. Technical Deliverables

To support this volume without operational burnout, the following infrastructure will be deployed:

1. **Custom Next.js Frontend:** A dark-mode, high-performance landing page (0.8s load time) to maximize conversion from Instagram traffic.
    
2. **Serverless Logistics:** Automated Delhivery integration.
    
    - _Current Workflow:_ Manual Entry (5 mins/order).
        
    - _New Workflow:_ Auto-generated Waybill (0 mins/order).
        
3. **Risk Isolation:** Deployment on a separate domain (e.g., `DateNightKit.in`) to insulate the main brand from Meta ad flags.
    

---

## 5. Commercials & Partnership Model

Given the scope involves Development, Systems Automation, and Strategy, I have structured the fees to minimize upfront cash flow impact for the business while aligning incentives.

### A. Development Sprint Fee: ₹10,000 (Fixed)

- **Inclusions:** Full Codebase, Vercel Deployment, Domain Configuration, Payment & Logistics API Integration.
    
- **Payment Terms:** 100% Upfront to commence the sprint.
    

### B. Success Fee: 10% of Net Profit

- **Definition:** Calculated on _Net Profit_ (Revenue - COGS - Shipping - Ad Spend).
    
- **Payment Terms:** Post-Campaign (February 15, 2026).
    
- **Rationale:** This aligns my efforts with your profitability. I will actively monitor ad performance and technical stability throughout the campaign to ensure the "Target Scenario" is met.