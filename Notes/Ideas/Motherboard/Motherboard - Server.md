### 1. The Multi-Tenant Identity Provider (Authn/Authz)

This is the "Gatekeeper" that replaces traditional username/password logic with modern security.

- **WebAuthn RP (Relying Party) Handler:** Manages the registration and authentication ceremonies for passkeys.
    
- **Scoped JWT Engine:** A service that generates tokens containing the `Client_ID` and `User_Role`.
    
- **Double-RBAC Evaluator:** A middleware that checks permissions against two different databases: the **Global Registry** (for Super Admins) and the **Client Vault** (for team-specific roles).
    

### 2. The Dynamic Database Router (The "Switch")

This is the most critical piece of the Go backend. It ensures data isolation.

- **Connection Pool Manager:** Maintains active pipes to multiple MongoDB clusters/databases.
    
- **Context Injector:** A middleware that extracts the `Client_ID` from the incoming request and injects the corresponding database pointer into the Go `context.Context`.
    
- **Client Registry Cache:** A fast in-memory store (like Redis or a Go Map) to quickly look up where a client's data lives without hitting the Global DB for every single request.
    

### 3. The Job Orchestrator (Intent Engine)

This module manages the transition from "User Request" to "Cloud Action."

- **Intent Validator:** Ensures that when a Marketing user wants to change a setting, the new value is safe and within limits.
    
- **Audit Logger:** Automatically records every configuration change into a tamper-proof collection within the Client's DB.
    
- **Task Dispatcher:** Communicates with Layer 2 (Workers) by sending messages to a queue (like RabbitMQ, NATS, or Pub/Sub) to trigger the cloud synchronization.
    

### 4. The Telemetry & Ingestion Gateway

This is the "Receiver" that gathers information from your independent scrapers and websites.

- **HMAC Webhook Validator:** Verifies that incoming status reports are actually coming from _your_ scrapers and not an attacker.
    
- **Aggregator Service:** Collects raw logs and metrics from Layer 4 and stores them in a format that the Frontend can easily query for charts.
    
- **Uptime Poller:** A background routine that pings client websites and APIs to verify they are online.
    

### 5. The Plugin & Entitlement Manager

This handles the "App Store" logic and the modular extensions.

- **Entitlement Guard:** A logic layer that checks if a workspace is "subscribed" to a feature (like Gmail or Slack) before allowing the API calls to pass through.
    
- **OAuth Lifecycle Manager:** Handles the "Connect to Google" flow, including the secure exchange of authorization codes for refresh tokens.
    
- **Reverse Proxy / Gateway:** Acts as a bridge between the Frontend and your independent Plugin Microservices.
    

---

### Summary of Server Responsibilities

| **Component**         | **Technical Role** | **Purpose**                                                  |
| --------------------- | ------------------ | ------------------------------------------------------------ |
| **Identity Service**  | Auth & JWT         | Identifies the user and their "Home" client.                 |
| **Tenant Middleware** | Context Switching  | Guarantees that Client A never sees Client B's data.         |
| **Worker Client**     | Task Dispatch      | Triggers the asynchronous cloud config sync.                 |
| **Ingestion API**     | Data Collection    | Receives scrapings/analytics from independent apps.          |
| **Proxy Gateway**     | Plugin Routing     | Directs traffic to specialized microservices (Google/Slack). |



To implement the **Motherboard Server** in Go, you need to structure your project around these core technical components. These work together to ensure that the server remains a high-performance, stateless orchestrator.

### 1. The Multi-tenant Context Switcher (Database Router)

This is the most critical item. In Go, you use **Middleware** to intercept every incoming HTTP request.

- **Tenant Resolution:** The middleware extracts the `tenant_id` from the JWT claims.
    
- **Connection Factory:** It looks up the connection string for that tenant (cached in memory for speed).
    
- **Context Injection:** It uses `context.WithValue` to pass the specific database pointer down the call stack.
    
- **Safety:** This ensures that your business logic never "knows" which database it's talking to; it just receives a database handle that is already scoped to the correct client.
    

---

### 2. The WebAuthn Relying Party (RP) Service

Since you are avoiding passwords, the server must act as a FIDO2 Relying Party.

- **Session Management:** A service to store "Pending Challenges" (using Redis or an in-memory TTL map).
    
- **Credential Manager:** Logic to verify signatures from authenticators (TouchID, FaceID, YubiKeys) against the public keys stored in the **Global MongoDB**.
    
- **Identity Mapping:** After a successful login, this service maps the physical hardware key to a specific `user_id` and their allowed `client_id` list.
    

---

### 3. The Job Orchestrator (Intent API)

The server doesn't "do" the work; it "commands" the work.

- **Intent State Machine:** When a user changes a scraper's frequency, the server updates the **Client DB** to a `SYNC_PENDING` status.
    
- **The Dispatcher:** It pushes a JSON payload (containing the workspace ID and the new config) to a message queue or directly triggers a **Serverless Worker**.
    
- **Validation Layer:** A strict schema validator (using Go Struct tags) to ensure that only valid configuration data is sent to the cloud providers.
    

---

### 4. The Ingestion & Webhook Gateway

This component acts as the "Ear" of the Motherboard, listening to the independent scrapers and websites (Layer 4).

- **HMAC Signing Service:** It provides a unique "Secret Key" to every workspace. The workspaces use this key to sign their data packets.
    
- **Signature Validator:** The gateway checks the signature of incoming reports to prevent "Data Spoofing" (someone trying to send fake analytics to the dashboard).
    
- **Rate Limiter:** Protects the Motherboard from being overwhelmed if a scraper starts sending too much data too fast.
    

---

### 5. The Audit & Compliance Engine

Essential for your SMB clients who need to know "Who changed what?"

- **Interceptor Pattern:** A wrapper around your database calls that automatically logs every `Update` or `Delete` action.
    
- **Immutability:** These logs are written to a special "Append-Only" collection in the Client's MongoDB, so they cannot be deleted or altered.
    

---

### 6. The Plugin Proxy (Adapter Gateway)

This manages the communication between the Frontend and your independent Plugin Microservices (Gmail, Slack, etc.).

- **Entitlement Middleware:** Checks the `entitlements` table in the Client DB before allowing a request to reach a plugin.
    
- **Request Forwarder:** A Reverse Proxy that forwards authorized requests to the correct internal microservice URL.
    
- **OAuth Scripter:** Manages the secure redirection and token exchange logic for third-party integrations.
    

---

### Summary Table for the Dev Team

| **Feature**      | **Go Package/Library**    | **Purpose**                                         |
| ---------------- | ------------------------- | --------------------------------------------------- |
| **Auth**         | `go-webauthn`             | Handle biometric login ceremonies.                  |
| **Routing**      | `chi` or `gin`            | Fast, middleware-based request handling.            |
| **Multitenancy** | `mongo-driver`            | Dynamic connection pooling & context switching.     |
| **Validation**   | `go-playground/validator` | Ensure incoming config data is safe.                |
| **Queueing**     | `RabbitMQ` or `NATS`      | Decouple the server from long-running worker tasks. |