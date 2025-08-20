## 📘 ELI15 Summary

MFA means using **more than one way** to prove who you are when logging in.

Instead of just a password, you need something **you know** (like a password) _and_ something **you have** (like an OTP code or a phone).

---

## 🧠 How It Works

1. Enter your password (something you know).
    
2. Enter a second factor:
    
    - OTP (via SMS, email, or authenticator app)
        
    - Fingerprint (biometric)
        
    - Hardware key (e.g., YubiKey)
        
3. If both checks pass, you’re in.
    

---

## 🧩 Types of Factors

- **Knowledge** (password, PIN)
    
- **Possession** (phone, app, security key)
    
- **Inherence** (biometric: face, fingerprint)
    

---

## ✅ Pros

- Blocks most account takeovers
    
- Great protection if password is leaked
    
- Easy to add on top of existing systems
    

## ❌ Cons

- Adds friction (extra steps)
    
- OTPs can be phished or intercepted
    
- Device loss can lock users out
    

---

## ⚠️ Common Threats

- **Man-in-the-middle phishing**
    
- **SIM swap** to hijack OTP
    
- **Fatigue attacks** (users spammed with MFA prompts)
    

---

## 🛡️ Best Practices

- Use app-based OTP (TOTP) instead of SMS
    
- Add fallback methods (backup codes, email recovery)
    
- Notify users on new device logins
    
- Rotate OTP secrets occasionally
    

---

## 🧪 Example Flow

```text
User logs in → Enters password → Prompted for OTP → Validates → Access granted
```

---

## 📚 References

1. [Google Research on MFA Effectiveness](https://security.googleblog.com/2019/05/new-research-how-effective-is-basic.html)
    
2. [NIST 800-63B Section 5.1.2](https://pages.nist.gov/800-63-3/sp800-63b.html)
    
3. [Auth0 MFA Guide](https://auth0.com/docs/multifactor-authentication)
    
4. [OWASP MFA Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html)
    

---

> MFA is one of the best upgrades you can make to your login system. It’s like using a deadbolt _and_ a security code.