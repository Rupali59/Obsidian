This document explains how modern systems let people in (login) and check if they are really who they say they are (authentication). We explain this like you're 15, with detailed breakdowns, examples, pros/cons, and references.

---

## 📘 1. What is Authentication? (Explain Like I'm 15)

Authentication is like your system asking, "Hey, who are you? Can you prove it?"

- Think of logging into Instagram. You type your username and password – you're telling the system: "I'm this person, and here's proof."
    
- The system checks this info against its memory (like a bouncer checking a guest list).
    

Once you're authenticated, **authorization** kicks in – it decides what you're allowed to do inside the system (like entering VIP vs general lounge).

---

## 🔑 2. Common Login/Auth Strategies

Each method has pros and cons. We'll list them here, and go deeper in separate pages.

### 2.1 Username + Password

- **Summary**: Most basic method. User enters credentials.
    
- ✅ Easy to use, well understood.
    
- ❌ Weak if passwords are reused, stolen, or guessed.
    
- 📄 See: [[ Username Password Authentication]]
    

### 2.2 Email Link Login (Magic Link)

- **Summary**: System sends a login link to your email.
    
- ✅ No passwords to remember.
    
- ❌ Depends on email access/security.
    
- 📄 See: [[🔢 One-Time Link]]
    

### 2.3 OTP (One-Time Password)

- **Summary**: A short code is sent (via SMS/email/app) to confirm login.
    
- ✅ Temporary, good for verifying identity.
    
- ❌ Can be intercepted (especially SMS).
    
- 📄 See: [[🌐 OTP (One-Time Password)]]
    

### 2.4 OAuth 2.0 / OpenID Connect (Social Login)

- **Summary**: Login using Google, Facebook, etc.
    
- ✅ Fast and convenient.
    
- ❌ Privacy tradeoff, relies on third parties.
    
- 📄 See: [[OAuth 2.0  OpenID Connect (Social Login)]]
    

### 2.5 Biometric Authentication

- **Summary**: Uses your fingerprint, face, or iris.
    
- ✅ Highly personal.
    
- ❌ Needs special hardware, privacy concerns.
    
- 📄 See: [[👁️ Biometric Authentication]]
    

### 2.6 Multi-Factor Authentication (MFA)

- **Summary**: Combines two or more methods (e.g., password + OTP).
    
- ✅ Very secure.
    
- ❌ More steps = more friction.
    
- 📄 See: [[🧾 Token-Based Authentication (JWT)]]
    

### 2.7 Token-Based Authentication (JWT)

- **Summary**: After login, a signed token proves your identity.
    
- ✅ Stateless and fast.
    
- ❌ Token theft can lead to impersonation.
    
- 📄 See: [[🧩 Token-Based Authentication (JWT)]]
    

### 2.8 Session-Based Authentication

- **Summary**: Server tracks sessions using cookies.
    
- ✅ Simple, secure if HTTPS is used.
    
- ❌ Doesn’t scale well.
    
- 📄 See: [`strategies/session.md`](https://chatgpt.com/c/strategies/session.md)
    

### 2.9 Certificate-Based Authentication

- **Summary**: Digital certificates are used instead of passwords.
    
- ✅ Very secure.
    
- ❌ Complex setup and management.
    
- 📄 See: [`strategies/cert-based.md`](https://chatgpt.com/c/strategies/cert-based.md)
    

---

## 🧠 3. What We Are Doing in Our System (ELI15)

We're using **Username + Password Login**:

- User enters credentials → backend verifies.
    
- If correct, a **token** (digital hall pass) is generated.
    
- This token is sent with each API call to ServiceNow, proving identity.
    

### Additional Features:

- **[[🔐 Forgot Password Flow]]** → Saves token in browser securely (localStorage/cookies).
    
- **[[🧠 Remember Me]]** → We allow email/OTP-based reset.
    
- **Register** → New users can sign up and verify email.
    

### Why no ServiceNow redirect?

Because we want a smooth experience. We use backend logic to get the ServiceNow token after verifying the user. You stay in our app.

---

## 📚 4. References & Research Papers

1. **OAuth 2.0 and OpenID Connect**
    
    - RFC 6749: [https://datatracker.ietf.org/doc/html/rfc6749](https://datatracker.ietf.org/doc/html/rfc6749)
        
    - OpenID Connect: [https://openid.net/specs/openid-connect-core-1_0.html](https://openid.net/specs/openid-connect-core-1_0.html)
        
2. **JWT (JSON Web Token)**
    
    - RFC 7519: [https://datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519)
        
3. **Password Best Practices**
    
    - NIST Guidelines: [https://pages.nist.gov/800-63-3/sp800-63b.html](https://pages.nist.gov/800-63-3/sp800-63b.html)
        
4. **Magic Link Auth**
    
    - Okta on Passwordless: [https://www.okta.com/identity-101/passwordless-authentication/](https://www.okta.com/identity-101/passwordless-authentication/)
        
5. **MFA Effectiveness**
    
    - Google Research Blog: [https://security.googleblog.com/2019/05/new-research-how-effective-is-basic.html](https://security.googleblog.com/2019/05/new-research-how-effective-is-basic.html)
        
6. **Biometric Authentication Security**
    
    - MIT Review on biometrics: [https://www.technologyreview.com/2020/01/16/130983/biometrics-fingerprint-face-security/](https://www.technologyreview.com/2020/01/16/130983/biometrics-fingerprint-face-security/)
        
7. **Session vs Token Auth**
    
    - Auth0 Guide: [https://auth0.com/docs/secure/tokens/session-tokens-vs-jwt](https://auth0.com/docs/secure/tokens/session-tokens-vs-jwt)
        

---

## 🛠️ Supplemental Docs (Coming Soon)

- [`login-flow.md`](https://chatgpt.com/c/login-flow.md): Visual/text flow of login and token issuance.
    
- [`api-auth-integration.md`](https://chatgpt.com/c/api-auth-integration.md): Using Bearer tokens with ServiceNow.
    
- [`remember-me.md`](https://chatgpt.com/c/remember-me.md): Secure local/session storage strategies.
    
- [`strategies/`](https://chatgpt.com/c/strategies/): In-depth explanations of each method, use cases, attack vectors, and references.
    

---

Would you like me to populate each strategy file next?