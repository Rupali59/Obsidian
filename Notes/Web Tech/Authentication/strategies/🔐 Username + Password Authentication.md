## 📘 ELI15 Summary

This is the classic way to log in. You enter a username (like your email) and a password (something only you know). The system checks its records, and if they match, you’re in.

It's like a secret handshake – if you get it right, the door opens.

---

## 🧠 How It Works

1. User enters username and password.
    
2. System compares it with stored hash in database.
    
3. If it matches:
    
    - Success: login allowed.
        
    - Failure: show error message.
        

### 🔐 Behind the Scenes

- Passwords are never stored directly.
    
- They are **hashed** using algorithms like `bcrypt`, `argon2`, or `scrypt`.
    
- Salts are added to hashes to prevent dictionary attacks.
    

---

## ✅ Pros

- Simple, widely supported.
    
- Easy to implement and test.
    

## ❌ Cons

- Users often reuse weak passwords.
    
- Vulnerable to brute force, phishing, leaks.
    
- Needs frequent resets and user education.
    

---

## ⚠️ Common Threats

- **Password reuse** across sites.
    
- **Phishing** to steal credentials.
    
- **Brute-force attacks** with bots.
    
- **Database leaks** if hashing is weak.
    

---

## 🛡️ Hardening Tips

- Enforce strong password policies.
    
- Use 2FA or MFA.
    
- Rate-limit login attempts.
    
- Use modern hashing algorithms.
    

---

## 🧪 Example (Pseudo-Code)

```python
# Registration
hashed = bcrypt.hash(password + salt)
db.save(user, hashed)

# Login
hashed_input = bcrypt.hash(input_password + salt)
if hashed_input == db.get(user):
    login_success()
```

---

## 📚 References

1. [OWASP Authentication Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
    
2. [NIST SP 800-63B: Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
    
3. [Understanding Bcrypt](https://auth0.com/blog/hashing-in-action-understanding-bcrypt/)
    

---

> Use this method as a base, but never rely on it alone. Always combine with smarter security practices (MFA, password managers, etc).