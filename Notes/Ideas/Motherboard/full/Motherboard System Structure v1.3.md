---

# 🛰️ Motherboard System Structure v1.3

**Status:** Active Development | **Architecture:** Hybrid (Local-First + SaaS) | **Control Plane:** Centralized

This document acts as the "Source of Truth" for the Motherboard Platform. It unifies the **Dockerized Microservices** architecture with the **Local-First Data Model** and details the **Polyglot Deployment Strategy**.

---

## 1. 🏗️ High-Level Architecture: The "Bridge" Concept

The platform operates as an **Internal Developer Platform (IDP)** that bridges your local development environment (MacBook) with cloud-native capabilities (SaaS).

### **The Two Planes of Existence**

1. **The Physical Plane (Localhost):**
    
    - **Source:** Your actual code lives in `/Users/rupali.b/Documents/GitHub`.
        
    - **Role:** Development, Coding, and Git Management.
        
    - **Sync:** The **Scheduler Service** scans this plane to auto-discover Workspaces and Assets.
        
2. **The Logical Plane (Motherboard UI):**
    
    - **Source:** MongoDB Atlas (Cloud).
        
    - **Role:** Management, Billing, Configuration, and Deployment triggering.
        
    - **Control:** You use the UI to assign "Assets" (found locally) to "Clients" (created in DB) and deploy them to the cloud.
        

---

## 2. 📁 Repository & Service Structure

The codebase is organized as a **Hybrid Monorepo**.

| **Layer**  | **Service**         | **Path**                  | **Port** | **Database Access** | **Responsibility**                   |
| ---------- | ------------------- | ------------------------- | -------- | ------------------- | ------------------------------------ |
| **CORE**   | **Frontend**        | `core/frontend`           | `3000`   | API Only            | The Visual Shell / Dashboard.        |
| **CORE**   | **Backend Gateway** | `core/motherboard-server` | `8080`   | **Primary (R/W)**   | Auth, Routing, Plugin Proxy.         |
| **MICRO**  | **Cloud Adapter**   | `services/cloud-adapter`  | `8093`   | N/A (API)           | **The Deployment Engine.**           |
| **MICRO**  | **Scheduler**       | `services/scheduler`      | `8084`   | `motherboard`       | **The Sync Engine** (File Scanning). |
| **MICRO**  | **Billing**         | `services/billing`        | `8090`   | `billing`           | Subscription & Invoicing.            |
| **MICRO**  | **Auth Service**    | `services/auth`           | `8088`   | `motherboard`       | Identity (WebAuthn/JWT).             |
| **PLUGIN** | **Communication**   | `plugins/*`               | `8081-4` | N/A                 | Email, SMS, WhatsApp, Telegram.      |
## 3. ⚙️ Polyglot Deployment & Configuration Engine

This is how Motherboard manages and deploys diverse assets (`Next.js`, `Python`, `Go`) found in your GitHub folder.

### **A. Asset Detection (The "What is this?")**

The **Scheduler Service** scans local folders and assigns a `tech_stack` tag based on file signatures:

- **Next.js/React:** Presence of `package.json` + `next.config.js`.
    
- **Python/Scraper:** Presence of `requirements.txt`, `Pipfile`, or `.py` files.
    
- **Go Service:** Presence of `go.mod`.
    
- **Static/Docs:** Presence of `.md` files or `index.html` only.
    

### **B. Configuration Management (The "Env Vars")**

Motherboard acts as a **Secret Vault**. You do not store `.env` files in production; you manage them via the UI.

1. **Input:** You enter secrets (e.g., `OPENAI_API_KEY`, `DATABASE_URL`) in the Motherboard Dashboard for a specific Asset.
    
2. **Storage:** Secrets are AES-256 encrypted and stored in the `assets` collection in MongoDB.
    
3. **Injection:**
    
    - **For Vercel:** Pushed via Vercel API during deployment.
        
    - **For Docker/VPS:** Injected as environment variables into the container at runtime.
        

### **C. Deployment Pipelines (The "How do I ship?")**

The **Cloud Adapter (Port 8093)** abstracts the underlying provider logic.

|**Tech Stack**|**Target Provider**|**Deployment Mechanism**|**Control Flow**|
|---|---|---|---|
|**Next.js Web App**|**Vercel**|**API Trigger**|Motherboard UI → Cloud Adapter → `vercel deploy` (via API) + Env Var Sync.|
|**Python Scraper**|**AWS ECS / DigitalOcean**|**Docker Build**|Motherboard UI → Cloud Adapter → Build Dockerfile → Push to Registry → Restart Container.|
|**Go Service**|**Cloud Run**|**Container**|Motherboard UI → Cloud Adapter → `gcloud run deploy`.|
|**Documentation**|**Vercel / Netlify**|**Static Build**|Motherboard UI → Cloud Adapter → Trigger Static Site Gen.|

---

## 4. 📊 The Data Model (v1.3)

The data model strictly separates **Physical Assets** (Code) from **Logical Clients** (People).

### **1. Workspace (The Container)**

- **Source:** Top-level Folder (e.g., `/GitHub/Vipin Kaushik`).
    
- **Purpose:** Organization / Business Identity.
    

```JavaScript
{
  _id: ObjectId("..."),
  name: "Vipin Kaushik",
  settings: {
    physicalPath: "/Users/rupali.b/Documents/GitHub/Vipin Kaushik",
    cloudProvider: "aws" // Default provider for this workspace
  }
}
```

### **2. Asset (The Code)**

- **Source:** Sub-folder (e.g., `/GitHub/Vipin Kaushik/astro-acharya`).
    
- **Purpose:** The deployable unit.

```JavaScript
{
  _id: ObjectId("..."),
  workspaceId: ObjectId("ws_vipin"),
  clientId: ObjectId("client_vipin_person"), // Assigned Billing Entity
  name: "astro-acharya",
  techStack: "nextjs",           // Auto-detected
  status: "active",
  config: {                      // Configuration Management
    envVars: [
      { key: "API_URL", value: "encrypted_string..." }
    ],
    deploymentId: "dpl_12345"    // Link to Vercel/AWS deployment
  }
}
```

### **3. Client (The Payer)**

- **Source:** Manual Creation.
    
- **Purpose:** Billing & Auth.
    

```JavaScript
{
  _id: ObjectId("client_vipin_person"),
  name: "Vipin Kaushik",
  email: "vipin@example.com",
  billing: { plan: "retainer_pro" }
}
```

---

## 5. 🐳 Infrastructure & Parity

### **Environment A: Local Development (Sync Mode)**

- **Docker Compose:** Mounts `/Users/rupali.b/Documents/GitHub` as a read-only volume to the Backend.
    
- **Sync:** Active. The Scheduler watches for file changes and updates MongoDB `Assets` in real-time.
    
- **Action:** You code locally; Motherboard "watches" you.
    

### **Environment B: Production (Control Mode)**

- **Docker Compose:** No local volume mounts.
    
- **Sync:** Disabled. Assets are "Locked" to their Git Repositories.
    
- **Action:** You use the Motherboard UI to trigger deployments (`Git Push` or `Manual Deploy`) via the **Cloud Adapter**.
    

---

## 6. 🔐 Security & Isolation

### **Plugin Proxy Pattern**

All communication assets (Whatsapp, SMS, Email) are proxied.

- **Frontend:** Calls `POST /api/plugins/email/send`.
    
- **Backend:**
    
    1. Checks `WorkspaceContext`.
        
    2. Checks `Entitlements` (Does this Client have email credits?).
        
    3. Decrypts the Provider Key (Resend API Key) from the Workspace Config.
        
    4. Forwards request to **Email Plugin (Port 8081)**.
        

### **Asset Isolation**

- **Secrets:** Env vars for _Client A's_ website are encrypted with a key unique to _Client A_.
    
- **Databases:** If an Asset requires a DB, Motherboard provisions a **Logical Database** (on Shared Cluster) or a **Dedicated Container**, depending on the Plan.
    

---

## 📝 Developer Workflow Summary

1. **Code:** Create a new project folder in `/GitHub/MyWorkspace/MyNewApp`.
    
2. **Sync:** Motherboard detects `MyNewApp`, identifies it as `Next.js`, and creates an **Asset** entry.
    
3. **Config:** In Motherboard UI, you add `DATABASE_URL` to the Asset's config.
    
4. **Assign:** You link this Asset to "Client John Doe" for billing.
    
5. **Deploy:** You click "Deploy". Motherboard's **Cloud Adapter** pushes the config to Vercel and triggers the build.