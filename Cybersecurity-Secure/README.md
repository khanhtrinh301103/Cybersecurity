# Cybersecurity-Secure

This is the **SECURE VERSION** of the banking application. All security vulnerabilities from the vulnerable version have been fixed and protected.

## Security Features Implemented

### ✅ 1. SQL Injection Protection
- **Fixed in**: `app/auth.py` - Login function
- **Protection**: Parameterized queries using `?` placeholders
- **Before**: Direct string concatenation allowed SQL injection
- **After**: All database queries use parameterized statements

### ✅ 2. XSS (Cross-Site Scripting) Protection
- **Fixed in**: `app/__init__.py` - Profile route and templates
- **Protection**: HTML escaping via Jinja2 autoescape and `markupsafe.escape()`
- **Before**: User input displayed with `|safe` filter, allowing script execution
- **After**: All user input is automatically escaped before display

### ✅ 3. CSRF (Cross-Site Request Forgery) Protection
- **Fixed in**: `app/__init__.py` - Transfer route and all forms
- **Protection**: Flask-WTF CSRF tokens and SameSite cookie attribute
- **Before**: Forms could be submitted from external websites
- **After**: All POST requests require valid CSRF token

### ✅ 4. Path Traversal Protection
- **Fixed in**: `app/__init__.py` - Download route
- **Protection**: Path normalization, whitelist-based access, absolute path verification
- **Before**: Direct file path construction allowed `../` traversal
- **After**: Only files in whitelisted directory are accessible

### ✅ 5. IDOR (Insecure Direct Object Reference) Protection
- **Fixed in**: `app/__init__.py` - Account details route
- **Protection**: Authorization check to verify account belongs to logged-in user
- **Before**: Users could view any account by changing account_id in URL
- **After**: Users can only view their own account; access denied for others

### ✅ Additional Security Measures
- Password hashing using `werkzeug.security` (PBKDF2)
- Input validation and sanitization
- Secure session cookies (HttpOnly, SameSite)
- User-specific file access control

## Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the database**:
   ```bash
   flask init-db
   ```

3. **Run the application**:
   ```bash
   flask run --port 5001
   ```

4. **Access the application**:
   - Open browser: http://localhost:5001
   - Register a new account or use existing test accounts

## Testing Security Defenses

### Test SQL Injection Protection
1. Go to login page: http://localhost:5001/auth/login
2. Try SQL injection payload: `admin' OR '1'='1`
3. **Expected**: Login fails - SQL injection blocked

### Test XSS Protection
1. Login and go to profile page
2. Try XSS payload in bio: `<script>alert('XSS')</script>`
3. **Expected**: Script displays as text, does not execute

### Test CSRF Protection
1. Login to the application
2. Try to submit transfer form from external website (like `csrf_attack.html`)
3. **Expected**: Request rejected - CSRF token missing/invalid

### Test Path Traversal Protection
1. Login and go to statements page
2. Try accessing: http://localhost:5001/download?file=../schema.sql
3. **Expected**: Access denied - path traversal blocked

### Test IDOR Protection
1. Login as admin (account ID 1)
2. Try accessing: http://localhost:5001/account/2 (Alice's account)
3. **Expected**: Access denied - "You can only view your own account"
4. Try accessing: http://localhost:5001/account/1 (your own account)
5. **Expected**: Account details displayed successfully

## Port Configuration

- **Secure Version**: Port 5001
- **Vulnerable Version**: Port 5000

Run both versions simultaneously to compare security implementations.

## Security Comparison

| Vulnerability | Vulnerable Version | Secure Version |
|--------------|-------------------|----------------|
| SQL Injection | ❌ Vulnerable | ✅ Protected |
| XSS | ❌ Vulnerable | ✅ Protected |
| CSRF | ❌ Vulnerable | ✅ Protected |
| Path Traversal | ❌ Vulnerable | ✅ Protected |
| IDOR | ❌ Vulnerable | ✅ Protected |
| Password Storage | ❌ Plain text | ✅ Hashed |

## Notes

- This is an educational project demonstrating security best practices
- All security measures are implemented according to OWASP guidelines
- For production use, additional security measures should be considered:
  - HTTPS/TLS encryption
  - Rate limiting
  - Account lockout after failed attempts
  - Two-factor authentication
  - Security headers (CSP, HSTS, etc.)
