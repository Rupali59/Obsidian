## 📘 ELI15 Summary

- **Basic Auth** is like showing your ID every time.
    
- **OAuth** is like giving a valet a **permission slip** to get your car but not your house keys.
    
- **Session-based Auth** is like getting a visitor badge that works till logout.
    
- **JWT** is a **signed badge** you carry around.
    

---

## 📋 Quick Comparison

|Strategy|Type|Storage|Good For|Weakness|
|---|---|---|---|---|
|Basic Auth|Credential|None|Internal tools|Sends password every time|
|Session Auth|Token|Server + Cookie|Websites|CSRF, server state needed|
|JWT|Token|Client|APIs, microservices|Can’t revoke easily|
|OAuth 2.0|Delegation|Server + Client|Third-party login|Complex, token leakage|
|SSO (SAML, OIDC)|Federation|Centralized|Enterprise/organizations|Setup overhead|

---

## 🔐 In-Depth: Basic Auth

- Sends username + password in every request (usually via header)
    
- Not secure unless used over HTTPS
    
- Very simple, no session state
    
- Good for quick internal scripts/APIs
    

## 🔐 In-Depth: Session Auth

- Server creates a session + stores it (DB or memory)
    
- Sends session ID via **cookie**
    
- Validates on each request
    
- Allows logout, expiration
    
- Used in most classic web apps
    

## 🔐 In-Depth: JWT

- Encoded + signed data in one token
    
- Stateless: no session server needed
    
- Token contains user data, scopes, expiry
    
- Stored in localStorage or secure cookies
    
- Issue: revocation is hard unless using blacklists
    

## 🔐 In-Depth: OAuth 2.0

- Allows a user to grant limited access to a 3rd party
    
- Used by Google/Facebook login, and APIs
    
- Supports access + refresh tokens
    
- Flow types:
    
    - Authorization Code
        
    - Implicit (legacy)
        
    - Client Credentials (for server apps)
        
    - Device Code (TVs)
        

---

## 🛡️ Security Considerations

- Always use HTTPS
    
- Avoid storing tokens in localStorage
    
- Use short-lived tokens + refresh mechanisms
    
- Rotate credentials regularly
    
- Log unusual activity
    

---

## 📚 References

1. [OAuth 2.0 Spec](https://datatracker.ietf.org/doc/html/rfc6749)
    
2. [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
    
3. [JWT RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519)
    
4. [AuthN vs AuthZ](https://auth0.com/docs/get-started/authentication-and-authorization-flow)
    
5. [OAuth vs OIDC vs SAML](https://www.okta.com/identity-101/)
    

---

> The strategy you choose depends on **who’s logging in**, **what they can access**, and **how much control you want over the session**.