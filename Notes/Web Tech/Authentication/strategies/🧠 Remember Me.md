## 📘 ELI15 Summary

If you forget your password, the system sends you a secret link to reset it — like getting a spare key from a trusted friend who checks your ID first.

---

## 🧠 How It Works

1. User clicks “Forgot Password”
    
2. Enters email/username
    
3. Server sends a **one-time link** with a token to email
    
4. User clicks the link → verifies → sets new password
    
5. Token is invalidated
    

---

## 📩 Email Link Token

- **One-time use only**
    
- **Short expiry** (usually 15–30 minutes)
    
- **Cryptographically random**
    
- Bound to user and time
    

---

## ✅ Pros

- Easy and familiar for users
    
- Works even if user is logged out
    

## ❌ Cons

- Email delivery can fail
    
- Link can be stolen if email compromised
    

---

## ⚠️ Common Threats

- **Phishing links** pretending to be reset emails
    
- **Token leakage** from shared devices or URLs
    
- **Replay attacks** using old links
    

---

## 🛡️ Best Practices

- Token stored **server-side with expiration**
    
- Invalidate token after use
    
- Invalidate all sessions post-reset
    
- Log IP and browser used for reset
    
- Rate-limit reset attempts
    
- Require CAPTCHA or MFA for added protection
    

---

## 🧪 Flow Example

```text
POST /forgot → send email
GET /reset?token=abc123 → show form
POST /reset-password → validate and set new password
```

---

## 📚 References

1. [OWASP Forgot Password Guidelines](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)
    
2. [NIST SP 800-63B Password Recovery](https://pages.nist.gov/800-63-3/sp800-63b.html)
    
3. [Django Password Reset Docs](https://docs.djangoproject.com/en/stable/topics/auth/default/#using-the-views)
    
4. [Auth0 Forgot Password](https://auth0.com/docs/authenticate/login/forgot-password)
    

---

> Forgot password flows are **entry points for attackers** — secure them like a front door with a camera and locks.