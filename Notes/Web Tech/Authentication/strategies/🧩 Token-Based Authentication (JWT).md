## 📘 ELI15 Summary

After you log in, the system gives you a digital “hall pass” called a **token** (usually a JWT – JSON Web Token). Every time you do something, you show the token instead of logging in again.

It’s like getting a wristband at a concert after you show your ticket once.

---

## 🧠 How It Works

1. You log in with username/password
    
2. Server sends back a JWT (a signed string that says who you are)
    
3. You store the token in your browser (localStorage or cookie)
    
4. Every request you make includes the token
    
5. Server checks the token’s validity and grants access
    

---

## 🧩 Token Contents (JWT)

```json
{
  "sub": "user123",
  "exp": 1721317200,
  "role": "admin"
}
```

- `sub`: subject (user ID)
    
- `exp`: expiration
    
- `role`: user role
    

---

## ✅ Pros

- Stateless (no need to store sessions on server)
    
- Scalable for APIs and SPAs
    
- Easy to inspect and debug
    

## ❌ Cons

- If token is stolen, attacker can impersonate user
    
- Can’t be easily revoked unless short-lived
    
- Must be stored securely (avoid XSS)
    

---

## ⚠️ Common Threats

- **Token theft** via XSS
    
- **Replay attacks** if token reused
    
- **Unvalidated tokens** being accepted
    

---

## 🛡️ Best Practices

- Use **HTTPS** always
    
- Store in **httpOnly cookies** (avoid localStorage if possible)
    
- Set short expiry (e.g., 15 minutes) + use refresh tokens
    
- Validate **signature, expiry, issuer, audience**
    

---

## 🧪 Sample Flow

```http
POST /login → Get JWT
Authorization: Bearer eyJhbGciOiJIUzI1...
→ Access protected routes
```

---

## 📚 References

1. [RFC 7519 - JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
    
2. [JWT.io Debugger](https://jwt.io/)
    
3. [OWASP Token Auth Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
    
4. [Auth0 JWT Guide](https://auth0.com/docs/secure/tokens/json-web-tokens)
    

---

> Tokens are lightweight, powerful tools — but they must be treated like passwords. Don’t expose them, don’t store them carelessly.