
```
User Agent → DNS → TCP/QUIC → TLS → HTTP → App Logic → DB/Cache
                          ↘ WebSocket/gRPC/GraphQL/SOAP (as needed)
```

### DNS & URLs

- **DNS:** Resolves names (e.g., `api.example.com`) to IPs via recursive queries and authoritative name servers.
    
- **URL:** Structured identifier (`scheme://user:pass@host:port/path?query#fragment`). Modern parsing follows the WHATWG URL Standard.
    

### Transports & security

- **TCP vs QUIC:** HTTP/1.1 & HTTP/2 use TCP; **HTTP/3** uses QUIC (UDP‑based) for multiplexing without head‑of‑line blocking.
    
- **TLS 1.3:** Encrypts transport; fewer round‑trips, simpler ciphers; ALPN negotiates HTTP version.
    

### HTTP — core concepts

- **Methods:** GET (safe/idempotent), HEAD, POST, PUT (idempotent), PATCH, DELETE, OPTIONS.
    
- **Status codes:** 2xx success; 3xx redirects; 4xx client errors; 5xx server errors.
    
- **Headers:** `Content-Type`, `Accept` (content negotiation), `Authorization`, `Cache-Control`, `ETag`/`If-*`, `Set-Cookie`, `Location`, `Range`.
    
- **Caching:** Freshness (`max-age`, `s-maxage`), validation (ETag/Last‑Modified), `Vary`, CDN behavior, `stale-while-revalidate`.
    
- **Compression:** `gzip`, `br` (Brotli); negotiate via `Accept-Encoding`.
    
- **HTTP/2 & HTTP/3:** Binary framing, multiplexing; server push deprecated; H3 over QUIC reduces HOL blocking.
    
- **CORS & Same‑Origin:** Preflight (`OPTIONS`), `Access-Control-*` headers; understand origin tuple (scheme+host+port).
    
- **Auth:** Basic, Bearer tokens (JWT), OAuth 2.0, OIDC; mTLS for service‑to‑service.
    
- **Reliability patterns:** Retries w/ idempotency, exponential backoff + jitter, circuit breakers, timeouts, pagination (cursor), idempotency keys for POST, conditional requests.
    

### Real‑time & streaming choices

- **WebSockets:** Full‑duplex over an HTTP Upgrade handshake; great for chat, live dashboards.
    
- **Server‑Sent Events (SSE):** One‑way server→client stream; simple over HTTP.
    
- **gRPC:** HTTP/2 framing + protobuf; supports unary, server/client/bidirectional streaming; excellent for microservices.
    

### API styles — REST vs RPC vs GraphQL vs SOAP

- **REST:** Resource‑oriented; stateless; leverage HTTP semantics (methods, status codes, caching, HATEOAS optional in practice).
    
- **RPC/gRPC:** Procedure calls with a strict IDL; strong types; faster on the wire; coupled clients/servers.
    
- **GraphQL:** Client‑specified shapes; single endpoint; solves over/under‑fetching; needs caching strategy and query cost control.
    
- **SOAP:** XML envelope + WSDL contracts; strong tooling, WS-* extensions (security, transactions); common in legacy/enterprise/B2B.
    

### Web security essentials (brief)

- **TLS everywhere**; HSTS; secure cookies (`HttpOnly`, `Secure`, `SameSite`).
    
- **CSRF:** use same‑site cookies or CSRF tokens for cookie‑bound auth.
    
- **CSP:** mitigate XSS; sanitize untrusted input; avoid `eval`.
    
- **Rate limiting** and abuse prevention; input validation at boundaries.
    

### Designing pragmatic HTTP APIs

- Consistent resource nouns; verbs via methods.
    
- Use correct status codes; include `problem+json` error bodies.
    
- Pagination (cursor), filtering, sorting; `Prefer: return=minimal` for heavy writes.
    
- Versioning via media types or URIs; deprecation headers + sunset policy.
    
- Idempotency keys for writes; ETags for concurrency control (optimistic locking).
    
- Observability: correlation IDs, structured logs, metrics, traces (OpenTelemetry).
    

---

## References & Specs (curated)

**HTTP & Web core**

- IETF RFC 9110 (HTTP Semantics)
    
- IETF RFC 9112 (HTTP/1.1), RFC 9113 (HTTP/2), RFC 9114 (HTTP/3)
    
- MDN: HTTP Overview, Guides, and Specs Index
    
- WebSocket protocol — RFC 6455; MDN WebSocket API
    
- TLS 1.3 — RFC 8446
    
- DNS — RFC 1034/1035
    
- WHATWG URL Standard
    

**API Styles**

- REST — Fielding Dissertation (Ch. 5)
    
- gRPC — grpc.io (Introduction, Core Concepts)
    
- GraphQL — GraphQL Specification (latest release & drafts)
    

**SOAP & WSDL**

- SOAP 1.2 (Parts 0/1/2) — W3C Recommendations
    
- WSDL 1.1 — W3C Note; history
    

**Language docs (entry points)**

- Python, JavaScript/TypeScript, Go, Java, C#, Rust, Kotlin, Swift, Ruby, PHP, Scala, Elixir, Haskell — official docs and package managers.
    

> Tip: Keep RFC/MDN links handy in your team wiki; they’re the source of truth for protocol behavior and edge cases.

---

## Appendix — Handy checklists

**Backend service readiness (ship list):** health checks, graceful shutdown, timeouts, retries, idempotency, structured logs, metrics, tracing, dashboards, runbooks.

**HTTP caching quick guide:** choose `Cache-Control`, set `ETag`, support conditional GET, respect `Vary`, enable CDN `stale-while-revalidate` when safe.

**Security headers starter pack:** `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`.
