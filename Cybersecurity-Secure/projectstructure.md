Cybersecurity-Secure/
│
├── 📁 .venv/                                     # Virtual environment (not in git)
│
├── 📁 app/                                       # 🌐 MAIN APPLICATION
│   │
│   ├── 📄 __init__.py                           # Flask app factory
│   │   # Config:
│   │   # - SECRET_KEY = 'dev-secure' (stronger key)
│   │   # - DATABASE = 'app-secure.sqlite'
│   │   # - SECURITY_MODE = 'secure'
│   │   # - WTF_CSRF_ENABLED = True
│   │   # - SESSION_COOKIE_SECURE = True
│   │   # - SESSION_COOKIE_HTTPONLY = True
│   │   # - SESSION_COOKIE_SAMESITE = 'Lax'
│   │
│   ├── 📄 db.py                                 # 📊 DATABASE CONNECTION
│   │   # Same as vulnerable but with:
│   │   # - Connection pooling
│   │   # - Query logging
│   │   # - Error handling
│   │
│   ├── 📄 schema.sql                            # 📊 DATABASE SCHEMA
│   │   # Same tables as vulnerable but with:
│   │   # - Constraints (NOT NULL, UNIQUE)
│   │   # - Indexes for performance
│   │   # - Audit log table
│   │
│   ├── 📄 models.py                             # 📊 DATA MODELS
│   │   # Enhanced with validation methods
│   │
│   ├── 📄 auth.py                               # 🔧 AUTHENTICATION (SECURE)
│   │   # Routes:
│   │   # - /register (GET, POST)
│   │   # - /login (GET, POST) ← 🟢 SQL Injection FIXED
│   │   # - /logout
│   │   #
│   │   # Security improvements:
│   │   # ✅ Parameterized queries
│   │   # ✅ Input validation
│   │   # ✅ Password hashing (werkzeug.security)
│   │   # ✅ Rate limiting
│   │   # ✅ Account lockout after failed attempts
│   │
│   ├── 📄 views.py                              # 🔧 MAIN VIEWS (SECURE)
│   │   # Routes:
│   │   # - / (index)
│   │   # - /dashboard
│   │   # - /profile ← 🟢 XSS FIXED
│   │   # - /transfer (POST) ← 🟢 CSRF FIXED
│   │   # - /transactions
│   │   # - /download/<filename> ← 🟢 Path Traversal FIXED
│   │   #
│   │   # Security improvements:
│   │   # ✅ HTML escaping (Jinja2 autoescape)
│   │   # ✅ CSRF tokens (Flask-WTF)
│   │   # ✅ Path validation & whitelist
│   │   # ✅ Authorization checks
│   │   # ✅ Audit logging
│   │
│   ├── 📁 security/                             # 🛡️ SECURITY MODULES
│   │   │
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📄 input_validation.py              # Input validation functions
│   │   │   # Functions:
│   │   │   # - validate_username()
│   │   │   # - validate_email()
│   │   │   # - validate_amount()
│   │   │   # - sanitize_input()
│   │   │
│   │   ├── 📄 sql_protection.py                # SQL Injection protection
│   │   │   # Functions:
│   │   │   # - safe_query() - Parameterized queries wrapper
│   │   │   # - validate_sql_input()
│   │   │
│   │   ├── 📄 xss_protection.py                # XSS protection
│   │   │   # Functions:
│   │   │   # - escape_html()
│   │   │   # - sanitize_output()
│   │   │   # - csp_header() - Content Security Policy
│   │   │
│   │   ├── 📄 csrf_protection.py               # CSRF protection
│   │   │   # Functions:
│   │   │   # - generate_csrf_token()
│   │   │   # - validate_csrf_token()
│   │   │   # Integrated with Flask-WTF
│   │   │
│   │   ├── 📄 path_protection.py               # Path Traversal protection
│   │   │   # Functions:
│   │   │   # - validate_path()
│   │   │   # - get_safe_path()
│   │   │   # - whitelist_check()
│   │   │
│   │   ├── 📄 auth_protection.py               # Authentication security
│   │   │   # Functions:
│   │   │   # - hash_password()
│   │   │   # - verify_password()
│   │   │   # - generate_session_token()
│   │   │
│   │   └── 📄 logging_config.py                # Security logging
│   │       # Functions:
│   │       # - log_security_event()
│   │       # - log_failed_login()
│   │       # - log_suspicious_activity()
│   │
│   ├── 📁 templates/                            # 🎨 HTML TEMPLATES
│   │   │
│   │   ├── 📄 base.html                        # Base layout (with CSP headers)
│   │   │
│   │   ├── 📄 index.html                       # Homepage
│   │   │
│   │   ├── 📁 auth/
│   │   │   ├── 📄 login.html                   # Login form (with CSRF token)
│   │   │   └── 📄 register.html                # Register form (with validation)
│   │   │
│   │   └── 📁 banking/
│   │       ├── 📄 dashboard.html               # User dashboard
│   │       ├── 📄 profile.html                 # Profile (HTML escaped)
│   │       ├── 📄 transfer.html                # Transfer (with CSRF token)
│   │       └── 📄 transactions.html            # Transaction history
│   │
│   └── 📁 static/                               # 🎨 STATIC FILES (same as vulnerable)
│       ├── 📁 css/
│       │   └── 📄 style.css
│       ├── 📁 js/
│       │   └── 📄 main.js
│       └── 📁 images/
│
├── 📁 defense/                                   # 🛡️ DEFENSE DOCUMENTATION
│   │
│   ├── 📄 defense_architecture.md               # Defense in Depth explanation
│   │   # Layer 1: Input Validation
│   │   # Layer 2: Output Encoding
│   │   # Layer 3: Authentication & Authorization
│   │   # Layer 4: Secure Configuration
│   │   # Layer 5: Logging & Monitoring
│   │
│   ├── 📄 sql_injection_defense.md              # SQL Injection mitigation
│   ├── 📄 xss_defense.md                        # XSS mitigation
│   ├── 📄 csrf_defense.md                       # CSRF mitigation
│   └── 📄 path_traversal_defense.md             # Path Traversal mitigation
│
├── 📁 screenshots/                               # 📸 DEFENSE EVIDENCE
│   ├── 📄 sql-injection-blocked.png
│   ├── 📄 xss-blocked.png
│   ├── 📄 csrf-blocked.png
│   └── 📄 path-traversal-blocked.png
│
├── 📁 instance/                                  # Instance files
│   ├── 📄 app-secure.sqlite                     # Database
│   └── 📁 logs/                                 # Security logs
│       └── 📄 security.log
│
├── 📁 tests/                                     # 🧪 TESTS
│   ├── 📄 conftest.py
│   ├── 📄 test_db.py
│   ├── 📄 test_auth.py
│   ├── 📄 test_security.py                      # Security feature tests
│   └── 📄 test_defense.py                       # Verify attacks blocked
│
├── 📄 .gitignore
├── 📄 requirements.txt
│   # Flask==3.0.0
│   # Werkzeug==3.0.1
│   # Flask-WTF==1.2.1        ← CSRF protection
│   # email-validator==2.1.0  ← Email validation
│   # requests==2.31.0
│
├── 📄 pyproject.toml
│
└── 📄 README.md
    # - Setup instructions
    # - Security features overview
    # - How to test defense
    # - Port: 5001