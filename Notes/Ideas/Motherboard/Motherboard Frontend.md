### 1. The Interface Definition (The "Props")

The Motherboard Shell uses **Module Federation** to inject the wrapper. When it mounts the component, it passes a standardized `props` object. Every wrapper, regardless of the client, must expect this exact structure:

|**Prop Name**|**Data Type**|**Description**|
|---|---|---|
|`user`|`Object`|Contains `id`, `name`, and `role` (e.g., "Marketing", "Dev").|
|`workspace`|`Object`|Metadata for the current app (e.g., Scraper ID, Vercel URL).|
|`data`|`Array/Obj`|The raw telemetry/analytics pulled from the Client MongoDB.|
|`entitlements`|`Array`|List of active plugins (e.g., `['google_cal', 'slack_notify']`).|
|`actions`|`Object`|Pre-bound functions to trigger Motherboard events (e.g., `redeploy()`).|

---

### 2. The Communication Bridge (`apiBridge`)

To maintain the **Independence Principle**, the wrapper shouldn't make direct calls to the Motherboard API. Instead, the Shell provides a "Bridge" function.

- **The Shell Side:** Provides a secure, authenticated fetcher that already knows the `Tenant_ID`.
    
- **The Wrapper Side:** Calls `apiBridge.get('/logs')`.
    
- **Security:** This prevents the wrapper from accidentally (or maliciously) trying to access another client's data, as the bridge is hard-coded to the current session.
    

---

### 3. The Design System (Visual Contract)

To ensure the "Marketing Wrapper" looks like it belongs in the Motherboard, you must provide a **Shared Style Guide**.

- **CSS Variables:** The Motherboard defines a theme (colors, spacing, font-sizes) as CSS variables (e.g., `--color-primary`). The wrapper must use these variables instead of hardcoded hex codes.
    
- **Component Library:** You provide a lightweight NPM package (e.g., `@motherboard/ui-kit`) containing standard buttons, cards, and charts.
    
- **Benefit:** When you change the Motherboard's brand color from blue to purple, every client wrapper updates automatically.
    

---

### 4. The Manifest File (`motherboard.json`)

Every custom wrapper repo must include a manifest file. This is what the Motherboard Server reads to understand how to load the UI.

JSON

```
{
  "name": "Reddit Scraper Analytics",
  "version": "1.2.0",
  "entry": "remoteEntry.js",
  "permissions_required": ["read_logs", "view_marketing"],
  "supported_roles": ["marketing", "technical_ops"]
}
```

---

### 5. The Development Sandbox

Your team cannot build wrappers if they have to run the entire Motherboard server locally. You must provide a **Sandbox Tool**.

1. **Mock Shell:** A tiny React/Next.js app that mimics the Motherboard.
    
2. **Hot Reloading:** The developer works in the Client Repo, and the Mock Shell reflects changes instantly.
    
3. **Production Flow:** Once the developer is happy, they push to the Client Repo (Vercel/S3). The Motherboard points its "Remote URL" to that new build.
    

---

### Summary: What your Team needs to do

- **Design Team:** Create the `@motherboard/ui-kit` (The visual contract).
    
- **Frontend Team:** Build the `RemoteLoader` component in Next.js using **Module Federation**.
    
- **DevOps:** Set up the CDN/S3 buckets where client wrappers will be hosted.