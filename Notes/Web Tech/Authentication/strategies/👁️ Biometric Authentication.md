## 📘 ELI15 Summary

Biometric authentication uses _something you are_ — like your fingerprint, face, voice, or eye — to log you in. It’s like your phone recognizing your face to unlock.

---

## 🧠 How It Works

1. You enroll a biometric: face scan, fingerprint, etc.
    
2. System stores a mathematical template (not the actual image).
    
3. On login, it captures a new scan.
    
4. Compares the scan to the stored template.
    
5. If it’s close enough → access granted.
    

---

## 🔍 Examples

- Face ID (Apple)
    
- Fingerprint (Android, Windows Hello)
    
- Retina/Iris scan (high-security)
    
- Voice recognition (e.g., call centers)
    

---

## ✅ Pros

- Fast and convenient
    
- Unique to each person
    
- Hard to guess or steal (in theory)
    

## ❌ Cons

- Can’t be changed if compromised
    
- Needs hardware support
    
- Privacy and data storage concerns
    

---

## ⚠️ Common Threats

- **Spoofing** (face masks, lifted fingerprints)
    
- **Template theft** (stored biometric data breaches)
    
- **False positives/negatives**
    

---

## 🛡️ Best Practices

- Store biometric templates securely (encrypted, isolated)
    
- Never store actual images
    
- Combine with another factor (e.g., PIN)
    
- Use local device validation (e.g., on-phone matching)
    

---

## 🧪 Example Use (Device-Based)

```javascript
navigator.credentials.get({
  publicKey: {
    challenge: ...,
    userVerification: "required"
  }
});
```

---

## 📚 References

1. [NIST SP 800-63A on Biometrics](https://pages.nist.gov/800-63-3/sp800-63a.html)
    
2. [MIT Tech Review on Biometric Risks](https://www.technologyreview.com/2020/01/16/130983/biometrics-fingerprint-face-security/)
    
3. [OWASP Biometrics Project](https://owasp.org/www-project-biometric-authentication/)
    
4. [Apple Face ID Security Whitepaper](https://www.apple.com/business/docs/site/FaceID_Security_Guide.pdf)
    

---

> Biometrics = powerful, but risky. Think of it like a key you can’t change. Use it with care and never as your only defense.