## 📘 ELI15 Summary

An OTP is like a temporary code you get via SMS, email, or an app (like Google Authenticator). It's only good for a short time or one use. It proves you're you _right now_.

---

## 🧠 How It Works

1. User enters phone number or email.
    
2. Server generates a random short code (e.g. 6 digits).
    
3. The code is sent via:
    
    - SMS
        
    - Email
        
    - Authenticator app (TOTP)
        
4. User enters the code in the app.
    
5. If correct and within time limit, login is allowed.
    

---

## ✅ Pros

- Temporary = safer than static passwords.
    
- Works with other auth methods (as MFA).
    
- Familiar to most users.
    

## ❌ Cons

- SMS can be intercepted (SIM swapping).
    
- Email delivery delays or spam filters.
    
- Some users find it tedious.
    

---

## 🔧 Types of OTP

### 🔹 HOTP (HMAC-based OTP)

- One-time use
    
- Increases counter on each use
    

### 🔹 TOTP (Time-based OTP)

- Expires every 30-60 seconds
    
- Used in apps like Google Authenticator
    

---

## ⚠️ Common Threats

- **SIM swap** attacks
    
- **Phishing** to steal OTPs in real time
    
- **Replay attacks** (if OTP isn't verified quickly)
    

---

## 🛡️ Best Practices

- Use TOTP over SMS for sensitive systems.
    
- Expire OTPs quickly (e.g. 60 seconds).
    
- Alert user if OTP is used.
    
- Limit resend and retry attempts.
    

---

## 🧪 Example Flow (Pseudo-code)

```python
# Generate
otp = random_6_digit()
store_in_cache(user_id, otp, 2_minutes)
send_sms(phone_number, otp)

# Validate
if entered_otp == stored_otp:
    login_success()
```

---

## 📚 References

1. [RFC 6238 - TOTP Algorithm](https://datatracker.ietf.org/doc/html/rfc6238)
    
2. [NIST 800-63 Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
    
3. [SIM Swap Risks - FTC](https://consumer.ftc.gov/articles/protecting-against-sim-swap-scams)
    
4. [Google Research on 2FA](https://security.googleblog.com/2019/05/new-research-how-effective-is-basic.html)
    

---

> OTP is a step up from plain passwords but should ideally be used with another factor (like something you know or something you are).