## 📘 ELI15 Summary

Instead of remembering a password, you just click a special link sent to your email. It's like showing your email inbox as proof of identity. The link works once and only for a short time.

---

## 🧠 How It Works

1. User enters their email address.
    
2. System generates a **one-time, time-bound tokenized link**.
    
3. The link is emailed to the user.
    
4. Clicking it logs the user in automatically.
    

---

## ✅ Pros

- No passwords to forget or leak.
    
- Reduces phishing and brute force risk.
    
- Smooth for users who check email frequently.
    

## ❌ Cons

- Depends on user’s email access.
    
- If email is compromised, account can be hijacked.
    
- Not great for users with delayed or unreliable email delivery.
    

---

## ⚠️ Common Threats

- **Stolen links** (from open inboxes or insecure email clients).
    
- **Expired tokens** not being invalidated.
    
- **Token reuse** if links aren’t one-time only.
    

---

## 🛡️ Best Practices

- Token should expire in 10–30 minutes.
    
- Invalidate token after use.
    
- Limit how many links can be sent per hour.
    
- Notify user when a login link is used.
    

---

## 🧪 Example (Simplified Flow)

```javascript
POST /send-magic-link
-> Generate token (JWT or UUID)
-> Store token hash in DB with expiration
-> Send email with URL like: /auth/confirm?token=abc123

GET /auth/confirm
-> Validate token
-> Log user in and redirect
```

---

## 📚 References

1. [Magic Link Overview - Auth0](https://auth0.com/docs/authenticate/passwordless/send-email)
    
2. [Netlify Identity Magic Links](https://docs.netlify.com/visitor-access/identity/#magic-links)
    
3. [UX Research on Passwordless](https://www.nngroup.com/articles/passwordless-login/)
    

---

> Magic links are great for reducing friction — but always assume the inbox could be compromised and log activity accordingly.