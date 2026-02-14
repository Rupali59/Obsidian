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

## 2. 📁 Repository & Service Structure

The codebase is organized as a **Monorepo** containing the Core Gateway, Microservices, and Plugins.

|**Layer**|**Service**|**Path**|**Port**|**Database Access**|
|---|---|---|---|---|
|**CORE**|**Frontend**|`core/frontend`|`3000`|API Only|
|**CORE**|**Backend Gateway**|`core/motherboard-server`|`8080`|**Primary (R/W)**|
|**MICRO**|**Auth Service**|`services/auth`|`8088`|`motherboard` DB|
|**MICRO**|**Billing**|`services/billing`|`8090`|`billing` DB|
|**MICRO**|**Scheduler**|`services/scheduler`|`8084`|`motherboard` DB|
|**MICRO**|**Notification**|`services/notification-service`|`8094`|`motherboard` DB|
|**MICRO**|**Cloud Adapter**|`services/cloud-adapter`|`8093`|N/A (API)|
|**PLUGIN**|**Email (Resend)**|`plugins/email`|`8081`|N/A|
|**PLUGIN**|**WhatsApp**|`plugins/telephony/whatsapp`|`8083`|N/A|

## 3. 📊 The Data Model (Updated)

This is the critical mapping logic. The system distinguishes between **where code lives** (Assets) and **who pays for it** (Clients).

### **A. Workspace (The Business Entity)**

- **Source:** Top-level folders in `/GitHub/`.
    
- **Definition:** A container for related projects, usually representing a Business Identity or Persona.
    
- **Sync Logic:** Automated via `sync-github-folders-to-workspaces.go`.

```javascript
// Collection: workspaces
{
  _id: ObjectId("..."),
  name: "Vipin Kaushik",       // From Folder Name
  slug: "vipin-kaushik",       // URL-safe
  settings: {
    physicalPath: "/Users/rupali.b/Documents/GitHub/Vipin Kaushik",
    syncEnabled: true
  }
}
```
### **B. Asset (The Product)**

- **Source:** Sub-folders within a Workspace.
    
- **Definition:** An actual deliverable (Web App, iOS App, Scraper, Documentation).
    
- **Sync Logic:** Automated. Detected by presence of `.git`, `package.json`, or content.

```javascript
// Collection: assets
{
  _id: ObjectId("..."),
  workspaceId: ObjectId("ws_vipin"),
  clientId: ObjectId("client_vipin_person"), // Linked to a Person
  name: "astro-acharya",       // From Sub-folder Name
  type: "application",         // Detected (e.g., contains package.json)
  location: {
    path: "/Users/rupali.b/Documents/GitHub/Vipin Kaushik/astro-acharya",
    repoUrl: "github.com/VipinKaushik/astro-acharya"
  }
}
```
### **C. Client (The Customer)**

- **Source:** **Manual Creation / API** (NOT a folder).
    
- **Definition:** The human being or legal entity that owns the Assets.
    
- **Role:** Billing contact, Auth credentials, Communication target.

```javascript
// Collection: clients
{
  _id: ObjectId("client_vipin_person"),
  workspaceId: ObjectId("ws_vipin"),
  name: "Vipin Kaushik",       // The Person
  email: "vipin@astro-clarity.com",
  phone: "+919876543210",
  billing: {
    status: "active",
    plan: "retainer"
  }
}
```

## . 🔄 The Sync Engine

The **Scheduler Service** (`services/scheduler`) runs the bridge logic that keeps MongoDB in sync with your Disk.

### **Sync Workflow (`github_sync` Job)**

1. **Scan Phase:**
    
    - Reads `/Users/rupali.b/Documents/GitHub/`.
        
    - Ignores exclusions (`Motherboard`, `.DS_Store`).
        
2. **Workspace Upsert:**
    
    - Found folder `Tathya` → Check if Workspace `Tathya` exists. If not, Create.
        
3. **Asset Discovery:**
    
    - Scans sub-folders of `Tathya` (e.g., `Obsidian`, `WorkTracker`).
        
    - Determines `type` (Is it a React app? A Python script? A Markdown doc?).
        
    - Upserts into `assets` collection linked to the Workspace.
        
4. **Orphan Check:**
    
    - If a folder is deleted from Disk, mark the Asset as `status: "missing"` in DB (Soft Delete).
        

---

## 5. 🐳 Deployment Strategy

### **Environment A: Local Development (The "Brain")**

- **Context:** Running on your MacBook.
    
- **Docker Compose:** Mounts local source code.
    
- **Data Access:** The Backend has **direct read access** to `/Users/rupali.b/Documents/GitHub` via Docker Volume binds.
    
- **Role:** This is where Sync happens.

```yaml

# docker-compose.yml snippet
services:
  backend:
    volumes:
      - /Users/rupali.b/Documents/GitHub:/data/github_root:ro
    environment:
      - GITHUB_ROOT=/data/github_root
        
```
### **Environment B: Cloud Production (The "Control Plane")**

- **Context:** Running on AWS/DigitalOcean.
    
- **Limitation:** **Cannot see your local files.**
    
- **Strategy:**
    
    - Production database only holds the **Metadata** (links to GitHub Repos).
        
    - It uses the **Cloud Adapter** to interact with assets via APIs (Vercel/AWS) rather than local file manipulation.
        
    - The `sync-github-folders` job is **DISABLED** in production.
        

---

## 6. 🔐 Security & Multi-Tenancy

### **Logical Isolation**

Every query in the system is scoped by `WorkspaceID`.

- **User Access:** `rupali` (Super Admin) sees All Workspaces.
    
- **Client Access:** `vipin` (Client User) sees **Only** `workspaceId: "ws_vipin"`.
    

### **Asset Assignment**

Assets are loosely coupled.

- An Asset belongs to a **Workspace** (System organization).
    
- An Asset is assigned to a **Client** (Billing/Ownership).
    
- _Example:_ The `gemstone` asset belongs to the `SSJK` Workspace but is assigned to the `Panditji` Client.
    

---

## 📝 Summary for Developers

1. **To Add a New Project:**
    
    - Create a folder: `/GitHub/{Workspace}/{ProjectName}`.
        
    - Wait for the Sync Job (or run `go run sync.go`).
        
    - The Asset appears in the Dashboard.
        
2. **To Bill a Customer:**
    
    - Create a **Client** in the Dashboard (e.g., "Mr. Client").
        
    - Go to the Asset and select "Assign to Mr. Client".
        
    - The Billing Service now knows who to invoice for that asset's usage.
        
3. **To Deploy:**
    
    - Click "Deploy" on the Asset.
        
    - **Cloud Adapter** reads the `repoUrl` from the Asset metadata and triggers a Vercel build.# 🛰️ Motherboard System Structure v1.2

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

## 2. 📁 Repository & Service Structure

The codebase is organized as a **Monorepo** containing the Core Gateway, Microservices, and Plugins.

|**Layer**|**Service**|**Path**|**Port**|**Database Access**|
|---|---|---|---|---|
|**CORE**|**Frontend**|`core/frontend`|`3000`|API Only|
|**CORE**|**Backend Gateway**|`core/motherboard-server`|`8080`|**Primary (R/W)**|
|**MICRO**|**Auth Service**|`services/auth`|`8088`|`motherboard` DB|
|**MICRO**|**Billing**|`services/billing`|`8090`|`billing` DB|
|**MICRO**|**Scheduler**|`services/scheduler`|`8084`|`motherboard` DB|
|**MICRO**|**Notification**|`services/notification-service`|`8094`|`motherboard` DB|
|**MICRO**|**Cloud Adapter**|`services/cloud-adapter`|`8093`|N/A (API)|
|**PLUGIN**|**Email (Resend)**|`plugins/email`|`8081`|N/A|
|**PLUGIN**|**WhatsApp**|`plugins/telephony/whatsapp`|`8083`|N/A|

## 3. 📊 The Data Model (Updated)

This is the critical mapping logic. The system distinguishes between **where code lives** (Assets) and **who pays for it** (Clients).

### **A. Workspace (The Business Entity)**

- **Source:** Top-level folders in `/GitHub/`.
    
- **Definition:** A container for related projects, usually representing a Business Identity or Persona.
    
- **Sync Logic:** Automated via `sync-github-folders-to-workspaces.go`.

```javascript
// Collection: workspaces
{
  _id: ObjectId("..."),
  name: "Vipin Kaushik",       // From Folder Name
  slug: "vipin-kaushik",       // URL-safe
  settings: {
    physicalPath: "/Users/rupali.b/Documents/GitHub/Vipin Kaushik",
    syncEnabled: true
  }
}
```
### **B. Asset (The Product)**

- **Source:** Sub-folders within a Workspace.
    
- **Definition:** An actual deliverable (Web App, iOS App, Scraper, Documentation).
    
- **Sync Logic:** Automated. Detected by presence of `.git`, `package.json`, or content.

```javascript
// Collection: assets
{
  _id: ObjectId("..."),
  workspaceId: ObjectId("ws_vipin"),
  clientId: ObjectId("client_vipin_person"), // Linked to a Person
  name: "astro-acharya",       // From Sub-folder Name
  type: "application",         // Detected (e.g., contains package.json)
  location: {
    path: "/Users/rupali.b/Documents/GitHub/Vipin Kaushik/astro-acharya",
    repoUrl: "github.com/VipinKaushik/astro-acharya"
  }
}
```
### **C. Client (The Customer)**

- **Source:** **Manual Creation / API** (NOT a folder).
    
- **Definition:** The human being or legal entity that owns the Assets.
    
- **Role:** Billing contact, Auth credentials, Communication target.

```javascript
// Collection: clients
{
  _id: ObjectId("client_vipin_person"),
  workspaceId: ObjectId("ws_vipin"),
  name: "Vipin Kaushik",       // The Person
  email: "vipin@astro-clarity.com",
  phone: "+919876543210",
  billing: {
    status: "active",
    plan: "retainer"
  }
}
```

## . 🔄 The Sync Engine

The **Scheduler Service** (`services/scheduler`) runs the bridge logic that keeps MongoDB in sync with your Disk.

### **Sync Workflow (`github_sync` Job)**

1. **Scan Phase:**
    
    - Reads `/Users/rupali.b/Documents/GitHub/`.
        
    - Ignores exclusions (`Motherboard`, `.DS_Store`).
        
2. **Workspace Upsert:**
    
    - Found folder `Tathya` → Check if Workspace `Tathya` exists. If not, Create.
        
3. **Asset Discovery:**
    
    - Scans sub-folders of `Tathya` (e.g., `Obsidian`, `WorkTracker`).
        
    - Determines `type` (Is it a React app? A Python script? A Markdown doc?).
        
    - Upserts into `assets` collection linked to the Workspace.
        
4. **Orphan Check:**
    
    - If a folder is deleted from Disk, mark the Asset as `status: "missing"` in DB (Soft Delete).
        

---

## 5. 🐳 Deployment Strategy

### **Environment A: Local Development (The "Brain")**

- **Context:** Running on your MacBook.
    
- **Docker Compose:** Mounts local source code.
    
- **Data Access:** The Backend has **direct read access** to `/Users/rupali.b/Documents/GitHub` via Docker Volume binds.
    
- **Role:** This is where Sync happens.

```yaml

# docker-compose.yml snippet
services:
  backend:
    volumes:
      - /Users/rupali.b/Documents/GitHub:/data/github_root:ro
    environment:
      - GITHUB_ROOT=/data/github_root
        
```
### **Environment B: Cloud Production (The "Control Plane")**

- **Context:** Running on AWS/DigitalOcean.
    
- **Limitation:** **Cannot see your local files.**
    
- **Strategy:**
    
    - Production database only holds the **Metadata** (links to GitHub Repos).
        
    - It uses the **Cloud Adapter** to interact with assets via APIs (Vercel/AWS) rather than local file manipulation.
        
    - The `sync-github-folders` job is **DISABLED** in production.
        

---

## 6. 🔐 Security & Multi-Tenancy

### **Logical Isolation**

Every query in the system is scoped by `WorkspaceID`.

- **User Access:** `rupali` (Super Admin) sees All Workspaces.
    
- **Client Access:** `vipin` (Client User) sees **Only** `workspaceId: "ws_vipin"`.
    

### **Asset Assignment**

Assets are loosely coupled.

- An Asset belongs to a **Workspace** (System organization).
    
- An Asset is assigned to a **Client** (Billing/Ownership).
    
- _Example:_ The `gemstone` asset belongs to the `SSJK` Workspace but is assigned to the `Panditji` Client.
    

---

## 📝 Summary for Developers

1. **To Add a New Project:**
    
    - Create a folder: `/GitHub/{Workspace}/{ProjectName}`.
        
    - Wait for the Sync Job (or run `go run sync.go`).
        
    - The Asset appears in the Dashboard.
        
2. **To Bill a Customer:**
    
    - Create a **Client** in the Dashboard (e.g., "Mr. Client").
        
    - Go to the Asset and select "Assign to Mr. Client".
        
    - The Billing Service now knows who to invoice for that asset's usage.
        
3. **To Deploy:**
    
    - Click "Deploy" on the Asset.
        
    - **Cloud Adapter** reads the `repoUrl` from the Asset metadata and triggers a Vercel build.document serves as the master reference, integrating your **Microservices Architecture** with your **Local-First Data Model**.

---

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

## 2. 📁 Repository & Service Structure

The codebase is organized as a **Monorepo** containing the Core Gateway, Microservices, and Plugins.

|**Layer**|**Service**|**Path**|**Port**|**Database Access**|
|---|---|---|---|---|
|**CORE**|**Frontend**|`core/frontend`|`3000`|API Only|
|**CORE**|**Backend Gateway**|`core/motherboard-server`|`8080`|**Primary (R/W)**|
|**MICRO**|**Auth Service**|`services/auth`|`8088`|`motherboard` DB|
|**MICRO**|**Billing**|`services/billing`|`8090`|`billing` DB|
|**MICRO**|**Scheduler**|`services/scheduler`|`8084`|`motherboard` DB|
|**MICRO**|**Notification**|`services/notification-service`|`8094`|`motherboard` DB|
|**MICRO**|**Cloud Adapter**|`services/cloud-adapter`|`8093`|N/A (API)|
|**PLUGIN**|**Email (Resend)**|`plugins/email`|`8081`|N/A|
|**PLUGIN**|**WhatsApp**|`plugins/telephony/whatsapp`|`8083`|N/A|

## 3. 📊 The Data Model (Updated)

This is the critical mapping logic. The system distinguishes between **where code lives** (Assets) and **who pays for it** (Clients).

### **A. Workspace (The Business Entity)**

- **Source:** Top-level folders in `/GitHub/`.
    
- **Definition:** A container for related projects, usually representing a Business Identity or Persona.
    
- **Sync Logic:** Automated via `sync-github-folders-to-workspaces.go`.

```javascript
// Collection: workspaces
{
  _id: ObjectId("..."),
  name: "Vipin Kaushik",       // From Folder Name
  slug: "vipin-kaushik",       // URL-safe
  settings: {
    physicalPath: "/Users/rupali.b/Documents/GitHub/Vipin Kaushik",
    syncEnabled: true
  }
}
```
### **B. Asset (The Product)**

- **Source:** Sub-folders within a Workspace.
    
- **Definition:** An actual deliverable (Web App, iOS App, Scraper, Documentation).
    
- **Sync Logic:** Automated. Detected by presence of `.git`, `package.json`, or content.

```javascript
// Collection: assets
{
  _id: ObjectId("..."),
  workspaceId: ObjectId("ws_vipin"),
  clientId: ObjectId("client_vipin_person"), // Linked to a Person
  name: "astro-acharya",       // From Sub-folder Name
  type: "application",         // Detected (e.g., contains package.json)
  location: {
    path: "/Users/rupali.b/Documents/GitHub/Vipin Kaushik/astro-acharya",
    repoUrl: "github.com/VipinKaushik/astro-acharya"
  }
}
```
### **C. Client (The Customer)**

- **Source:** **Manual Creation / API** (NOT a folder).
    
- **Definition:** The human being or legal entity that owns the Assets.
    
- **Role:** Billing contact, Auth credentials, Communication target.

```javascript
// Collection: clients
{
  _id: ObjectId("client_vipin_person"),
  workspaceId: ObjectId("ws_vipin"),
  name: "Vipin Kaushik",       // The Person
  email: "vipin@astro-clarity.com",
  phone: "+919876543210",
  billing: {
    status: "active",
    plan: "retainer"
  }
}
```

## . 🔄 The Sync Engine

The **Scheduler Service** (`services/scheduler`) runs the bridge logic that keeps MongoDB in sync with your Disk.

### **Sync Workflow (`github_sync` Job)**

1. **Scan Phase:**
    
    - Reads `/Users/rupali.b/Documents/GitHub/`.
        
    - Ignores exclusions (`Motherboard`, `.DS_Store`).
        
2. **Workspace Upsert:**
    
    - Found folder `Tathya` → Check if Workspace `Tathya` exists. If not, Create.
        
3. **Asset Discovery:**
    
    - Scans sub-folders of `Tathya` (e.g., `Obsidian`, `WorkTracker`).
        
    - Determines `type` (Is it a React app? A Python script? A Markdown doc?).
        
    - Upserts into `assets` collection linked to the Workspace.
        
4. **Orphan Check:**
    
    - If a folder is deleted from Disk, mark the Asset as `status: "missing"` in DB (Soft Delete).
        

---

## 5. 🐳 Deployment Strategy

### **Environment A: Local Development (The "Brain")**

- **Context:** Running on your MacBook.
    
- **Docker Compose:** Mounts local source code.
    
- **Data Access:** The Backend has **direct read access** to `/Users/rupali.b/Documents/GitHub` via Docker Volume binds.
    
- **Role:** This is where Sync happens.

```yaml

# docker-compose.yml snippet
services:
  backend:
    volumes:
      - /Users/rupali.b/Documents/GitHub:/data/github_root:ro
    environment:
      - GITHUB_ROOT=/data/github_root
        
```
### **Environment B: Cloud Production (The "Control Plane")**

- **Context:** Running on AWS/DigitalOcean.
    
- **Limitation:** **Cannot see your local files.**
    
- **Strategy:**
    
    - Production database only holds the **Metadata** (links to GitHub Repos).
        
    - It uses the **Cloud Adapter** to interact with assets via APIs (Vercel/AWS) rather than local file manipulation.
        
    - The `sync-github-folders` job is **DISABLED** in production.
        

---

## 6. 🔐 Security & Multi-Tenancy

### **Logical Isolation**

Every query in the system is scoped by `WorkspaceID`.

- **User Access:** `rupali` (Super Admin) sees All Workspaces.
    
- **Client Access:** `vipin` (Client User) sees **Only** `workspaceId: "ws_vipin"`.
    

### **Asset Assignment**

Assets are loosely coupled.

- An Asset belongs to a **Workspace** (System organization).
    
- An Asset is assigned to a **Client** (Billing/Ownership).
    
- _Example:_ The `gemstone` asset belongs to the `SSJK` Workspace but is assigned to the `Panditji` Client.
    

---

## 📝 Summary for Developers

1. **To Add a New Project:**
    
    - Create a folder: `/GitHub/{Workspace}/{ProjectName}`.
        
    - Wait for the Sync Job (or run `go run sync.go`).
        
    - The Asset appears in the Dashboard.
        
2. **To Bill a Customer:**
    
    - Create a **Client** in the Dashboard (e.g., "Mr. Client").
        
    - Go to the Asset and select "Assign to Mr. Client".
        
    - The Billing Service now knows who to invoice for that asset's usage.
        
3. **To Deploy:**
    
    - Click "Deploy" on the Asset.
        
    - **Cloud Adapter** reads the `repoUrl` from the Asset metadata and triggers a Vercel build.