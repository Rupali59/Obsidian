

- **SOAP 1.2:** XML envelope with headers/body; transport‑agnostic (commonly HTTP).
    
- **WSDL:** Contract describing endpoints, operations, bindings, and messages.
    
- **MTOM/XOP:** Efficient binary content; WS‑Security, WS‑Addressing for enterprise needs.
    
- **Tooling:** Java (JAX‑WS), .NET (WCF, Core WCF), enterprise ESBs; use codegen from WSDL; strict schema evolution discipline.
    

---

## Part D — Practical recipes

- **Pick a stack quickly:** TS (Next.js) + Go API + Postgres + Redis + OpenAPI + k8s → scalable baseline.
    
- **Data/ML service:** Python + FastAPI + Pydantic + ONNX/TorchServe + Redis + Celery; offload hot loops to NumPy/Rust.
    
- **Legacy SOAP integration:** Generate client from WSDL, wrap in modern REST/gRPC façade; translate auth and errors.
    
- **Realtime dashboard:** WebSocket or SSE; backpressure and fan‑out via Redis pub/sub or NATS.
