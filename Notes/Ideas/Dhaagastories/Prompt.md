Act as a Senior Full Stack Engineer. We are building a high-performance, single-page "Micro-Site" for a Valentine's Day campaign. 

**Project Context:**
- Brand: "Dhaaga Stories" (Campaign Name: "The Date Night Edit").
- Goal: Sell Intimacy/Candle Bundles via Instagram Ads.
- Constraint: No database. No backend CMS. Zero fixed costs.
- Deployment: Vercel.

**Tech Stack:**
- Framework: Next.js 14 (App Router).
- Styling: Tailwind CSS (Mobile-first, "Dark Mode/Luxury" aesthetic).
- Payments: Razorpay Payment Buttons (Embedded Script method).
- Logistics: Delhivery API (triggered via Webhooks).
- Icons: Lucide-React.

**Design System:**
- Background: #0a0a0a (Almost Black).
- Accents: #881337 (Deep Rose Red) and #C0A062 (Muted Gold).
- Typography: Use a Serif font (Playfair Display) for Headings, Sans (Inter) for body.

**Deliverables & File Structure:**

1. **Config:**
   - Setup `tailwind.config.ts` with the custom colors.
   - Configure `next.config.js` to allow images from external sources if needed.

2. **Data (`lib/constants.ts`):**
   - Create a constant array `PRODUCTS` with 3 items:
     - Single Candle (₹999).
     - The Date Night Bundle (₹1499) [Highlight this].
     - The "Bulk/Party" Pack (₹2499).
   - Each item needs: title, description, price, image path, and `razorpay_button_id`.

3. **Components:**
   - `HeroSection`: Full screen, moody background, strong CTA "Get the Kit".
   - `ProductCard`: A premium card displaying the product details.
   - `RazorpayButton`: A client component that safely injects the Razorpay `<script>` tag. It must accept a `buttonId` prop. Use `useRef` to append the script to avoid hydration errors.
   - `WhatsAppFloat`: A sticky floating button bottom-right.
   - `DeliveryChecker`: A simple input to check pincode (Mock logic: if Pincode starts with '560' return "Same Day", else "5-7 Days").

4. **API Route (`app/api/webhooks/razorpay/route.ts`):**
   - Create a POST handler.
   - **Step 1:** Verify Razorpay Signature using `crypto` and `RAZORPAY_WEBHOOK_SECRET`.
   - **Step 2:** Parse the JSON body. Check if event is `payment.captured`.
   - **Step 3:** Extract user details (email, phone, notes.address) from the payload.
   - **Step 4:** Mock the call to Delhivery API (Comment out the actual fetch call but write the payload structure matching Delhivery Surface API requirements).

5. **Pages:**
   - `app/page.tsx`: The main landing page assembling the sections.
   - `app/success/page.tsx`: A simple "Order Confirmed" page that fires a Facebook Pixel "Purchase" event (mock the pixel call).

**Specific Constraints:**
- Do not use the Razorpay Node SDK. Use the Button Script injection method.
- Ensure the webhook route uses `NextResponse`.
- Make the UI responsive. The "Buy" buttons must be large and thumb-friendly on mobile.