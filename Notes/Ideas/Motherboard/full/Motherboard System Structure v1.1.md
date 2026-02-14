
**Version:** 1.1 | **Status:** Active Development | **Architecture:** Core + Satellite Hybrid

This document provides a complete structural overview of the **Motherboard Platform**, acting as the "Source of Truth" for repository organization, deployment architecture, and the multi-tenant data model.

---

## 📁 Repository Structure

The platform follows a **hybrid monorepo** structure. The "Core" components act as the central command center, while "Satellites" (Services/Plugins) are modular and can be deployed independently or orchestrated together.
```bash
Motherboard/                          # Root Monorepo
├── core/                             # 🎯 The "Control Plane"
│   ├── frontend/                     # Next.js 15.5+ App Router (Dashboard)
│   └── motherboard-server/           # Go Gin API Gateway (Port 8080)
├── services/                         # ⚙️ Domain Microservices
│   ├── auth/                         # Centralized Identity (WebAuthn/JWT)
│   ├── billing/                      # SaaS Subscription Engine (Stripe)
│   ├── scheduler/                    # Job Cron (GitHub/Jira Sync)
│   ├── notification-service/         # Action Engine (Email/SMS/WA Routing)
│   ├── task-tracker/                 # Python/FastAPI Task Manager
│   ├── health/                       # Observability & Metrics
│   ├── marketing/                    # ROI/Campaign Logic
│   └── cloud-adapter/                # Vercel/AWS/GCP Abstraction Layer
├── plugins/                          # 🔌 Communication Plugins (Standardized HTTP)
│   ├── email/                        # Resend Wrapper
│   ├── sms/                          # Twilio/Exotel Wrapper
│   └── telephony/                    # Voice & Chat
│       ├── whatsapp/                 # WhatsApp Business API
│       └── telegram/                 # Telegram Bot API
├── clients/                          # 🛒 Tenant-Specific Business Logic
│   ├── inventory-management/         # Stock & SKU Tracking
│   └── order-management/             # Order Processing Engine
├── tools/                            # 🛠️ DevOps Utilities
│   ├── seeds/                        # MongoDB Development Fixtures
│   └── docker/                       # Shared Docker Configurations
├── deploy.sh                         # Unified Deployment Script
├── docker-compose.yml                # Local Development Orchestrator
└── README.md                         # Project Entry Point
```

## 🏗️ Architecture Layers

### **Layer 1: The Control Plane (Core)**

#### **Frontend (`core/frontend`)**

- **Tech:** Next.js 15, TanStack Query, Tailwind CSS.
    
- **Role:** The visual "Shell" that aggregates remote UI wrappers.
    
- **Key Feature:** Does not store business logic. Communicates exclusively with the Backend Gateway via secure HttpOnly cookies.
    

#### **Backend Gateway (`core/motherboard-server`)**

- **Tech:** Go (Gin Framework), MongoDB Driver.
    
- **Role:** The "Switchboard." It intercepts every request to inject the correct `WorkspaceContext` before forwarding it to microservices.
    
- **Key Responsibilities:**
    
    - **Plugin Proxy:** Hides third-party API keys (e.g., Twilio) from the client.
        
    - **Rate Limiting:** Enforces SaaS tier quotas (e.g., "100 Emails/Month").
        

### **Layer 2: The Service Mesh (Microservices)**

Services are containerized and communicate via internal REST APIs on the Docker bridge network.

|**Service**|**Port**|**Database Access**|**Responsibility**|
|---|---|---|---|
|**Auth**|`8088`|`motherboard.users`|Handles WebAuthn (Passkeys) & JWT issuance.|
|**Billing**|`8090`|`billing` DB|Manages Stripe subscriptions & generates invoices.|
|**Cloud Adapter**|`8093`|N/A (API Only)|Provisions remote assets on Vercel/AWS for clients.|
|**Notification**|`8094`|`motherboard` (Shared)|Event-driven pipeline (Ingest → Template → Dispatch).|
|**Scheduler**|`8084`|`motherboard.jobs`|Syncs GitHub Repos & Jira Boards every 15/30 mins.|
|**Task Tracker**|`8095`|`motherboard.tasks`|Python-based project management engine.|

### **Layer 3: The Integration Layer (Plugins)**

Plugins are **stateless** wrappers around external APIs. They never access the database directly; they receive payload data from the Backend Gateway.

- **Email (`8081`):** Uses Resend API.
    
- **SMS (`8082`):** Multi-provider (Twilio failover to Exotel).
    
- **WhatsApp (`8083`):** Supports interactive buttons and templates.
    
- **Telegram (`8084`):** Bot API with webhook callback support.
---
## 🐳 Docker & Deployment Architecture

### **Environment Strategy**

The platform uses a **"Parity" strategy** where Staging mirrors Production using Docker Compose overrides.

#### **1. Local Development (`docker-compose.yml`)**

- **Volume Mounts:** Live code reloading for Go and Next.js.
    
- **Network:** `motherboard-network` (Bridge).
    
- **Database:** Local MongoDB container with `scripts/seed` data pre-loaded.
    
- **Access:** Direct access to all microservice ports for debugging.
    

#### **2. Production / Staging (`docker-compose.prod.yml`)**

- **Images:** Optimized multi-stage builds (no source code included).
    
- **Security:** Only Ports `80` (HTTP) and `443` (HTTPS) are exposed via a Reverse Proxy (Traefik/Nginx).
    
- **Secrets:** Injected via Docker Secrets or Environment Variables (never checked into Git).
    

### **Service Communication Map**

```graph TD
    Client[User Browser] -->|HTTPS| Gateway[Go Backend :8080]
    
    subgraph "Internal Docker Network"
        Gateway -->|Proxy| Auth[Auth Service :8088]
        Gateway -->|Proxy| Bill[Billing Service :8090]
        Gateway -->|Proxy| Cloud[Cloud Adapter :8093]
        
        Gateway -->|Event| Notif[Notification Engine :8094]
        Notif -->|Dispatch| Email[Email Plugin :8081]
        Notif -->|Dispatch| WA[WhatsApp Plugin :8083]
        
        Gateway -->|Data| Mongo[(MongoDB Cluster)]
    end
    
    Cloud -->|API| Vercel[Vercel / AWS]
```

## 🗄️ MongoDB Data Model (v1.1)

The database strategy uses **logical isolation** via `workspaceId` discriminators to remain within MongoDB Atlas collection limits (~10k) while scaling to thousands of tenants.

### **1. Core Registry (`motherboard` Database)**

#### **Workspaces (Tenants)**
```javascript
{
  _id: ObjectId,
  slug: String,              // Unique URL identifier (e.g., "acme-corp")
  tier: String,              // "free", "pro", "enterprise"
  branding: {
    logoUrl: String,
    primaryColor: String
  },
  createdAt: ISODate
}
```

#### **Clients (The "Registry")**

Formerly "folders," these represent the external entities a workspace manages.
```javascript
{
  _id: ObjectId,
  workspaceId: ObjectId,     // Link to Tenant
  name: String,              // "Client X Website"
  status: String,            // "active", "archived"
  externalId: String         // Reference to external CRM ID
}
```

#### **Assets (Remote Resources)**

Represents the actual deployed infrastructure managed via the **Cloud Adapter**.
```javascript
{
  _id: ObjectId,
  workspaceId: ObjectId,
  clientId: ObjectId,
  type: String,              // "vercel_deployment", "aws_s3", "github_repo"
  providerConfig: {
    provider: String,        // "vercel"
    projectId: String,       // External Provider ID
    deploymentUrl: String
  },
  syncStatus: String,        // "synced", "pending", "failed"
  lastSyncedAt: ISODate
}
```


### **2. Identity & Security**

#### **Users & RBAC**

```javascript
{
  _id: ObjectId,
  email: String,
  mobile: String,            // Primary Identity Key
  workspaces: [              // User belongs to multiple tenants
    {
      workspaceId: ObjectId,
      role: String           // "owner", "admin", "member"
    }
  ],
  webauthnCredentials: [     // Passkeys
    {
      credentialId: String,
      publicKey: String,
      counter: Number
    }
  ]
}
```

#### **Entitlements (SaaS Limits)**
```javascript
{
  _id: ObjectId,
  workspaceId: ObjectId,
  usage: {
    emailsSent: Number,
    storageUsedMB: Number
  },
  limits: {
    emailsMax: Number,
    storageMaxMB: Number
  },
  billingPeriod: String      // "2026-01"
}
```
### **3. Operational Data (Shared Collections)**

High-volume data uses a shared collection strategy with heavy indexing on `workspaceId`.

- **`audit_logs`:** Records every API action (Who, What, When).
    
- **`notifications`:** Stores state (`unread`, `sent`, `resolved`) for the Action Engine.
    
- **`jobs`:** Tracks Scheduler sync status (GitHub/Jira).


|**Service**|**Type**|**Language**|**Public Access?**|**Key Role**|
|---|---|---|---|---|
|**Frontend**|Core|TypeScript|✅ Yes|UI Dashboard|
|**Backend**|Core|Go|✅ Yes|API Gateway & Security|
|**Auth**|Micro|Go|❌ Internal|Identity Provider|
|**Billing**|Micro|Go|❌ Internal|Payments & Invoices|
|**Scheduler**|Micro|Go|❌ Internal|Background Sync|
|**Notification**|Micro|Go|❌ Internal|Alert Routing|
|**Task Tracker**|Micro|Python|❌ Internal|Project Management|
|**Cloud Adapter**|Micro|Go|❌ Internal|Remote Asset Provisioning|
|**Plugins**|Plugin|Go|❌ Internal|External API Wrappers|





-----
# 🛰️ Motherboard System Structure v1.2

**Status:** Active Development | **Architecture:** Hybrid (Local-First + SaaS)

**Core Logic:** Physical Folders = Assets; Database Entities = Clients.

This document outlines the complete technical structure of the Motherboard platform, unifying the **Dockerized Microservices** layer with the **Local Filesystem** data model.

---

## 1. 🏗️ High-Level Architecture

The platform operates as an **Internal Developer Platform (IDP)** that bridges your local development environment (MacBook) with cloud-native capabilities (SaaS).

### **The "Bridge" Concept**

- **The Physical Plane (Your Disk):** Your actual code, Git repositories, and project files live in `/Users/rupali.b/Documents/GitHub`.
    
- **The Logical Plane (MongoDB):** Motherboard maps these physical folders into structured `Assets` and assigns them to `Clients` (People) for management, billing, and deployment.
    

---

Based on the new documentation provided, I have updated the **Motherboard System Structure** to reflect the crucial distinction between **Physical Assets** (Filesystem) and **Logical Clients** (People/Entities).

This updated technical # 🛰️ Motherboard System Structure v1.2

**Status:** Active Development | **Architecture:** Hybrid (Local-First + SaaS)

**Core Logic:** Physical Folders = Assets; Database Entities = Clients.

This document outlines the complete technical structure of the Motherboard platform, unifying the **Dockerized Microservices** layer with the **Local Filesystem** data model.

---

## 1. 🏗️ High-Level Architecture

The platform operates as an **Internal Developer Platform (IDP)** that bridges your local development environment (MacBook) with cloud-native capabilities (SaaS).

### **The "Bridge" Concept**

- **The Physical Plane (Your Disk):** Your actual code, Git repositories, and project files live in `/Users/rupali.b/Documents/GitHub`.
    
- **The Logical Plane (MongoDB):** Motherboard maps these physical folders into structured `Assets` and assigns them to `Clients` (People) for management, billing, and deployment.
    

---

Based on the new documentation provided, I have updated the **Motherboard System Structure** to reflect the crucial distinction between **Physical Assets** (Filesystem) and **Logical Clients** (People/Entities).

This updated technical document serves as the master reference, integrating your **Microservices Architecture** with your **Local-First Data Model**.

---

