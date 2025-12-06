Cybersecurity-Vulnerable/
│
├── 📁 .venv/                                     # Virtual environment (not in git)
│
├── 📁 app/                                       # 🌐 MAIN APPLICATION
│   │
│   ├── 📄 __init__.py                           # Flask app factory
│   │   # Config:
│   │   # - SECRET_KEY = 'dev-vulnerable'
│   │   # - DATABASE = 'app-vulnerable.sqlite'
│   │   # - SECURITY_MODE = 'vulnerable'
│   │
│   ├── 📄 db.py                                 # 📊 DATABASE CONNECTION
│   │   # Functions:
│   │   # - get_db() - Connect to SQLite
│   │   # - close_db() - Close connection
│   │   # - init_db() - Initialize tables
│   │   # - init_app() - Register with Flask
│   │
│   ├── 📄 schema.sql                            # 📊 DATABASE SCHEMA
│   │   # Tables:
│   │   # - users (id, username, password, email, full_name, bio)
│   │   # - accounts (id, user_id, account_number, balance)
│   │   # - transactions (id, from_account, to_account, amount, timestamp)
│   │
│   ├── 📄 models.py                             # 📊 DATA MODELS (optional)
│   │   # Classes:
│   │   # - User
│   │   # - Account
│   │   # - Transaction
│   │
│   ├── 📄 auth.py                               # 🔧 AUTHENTICATION (VULNERABLE)
│   │   # Routes:
│   │   # - /register (GET, POST)
│   │   # - /login (GET, POST) ← 🔴 SQL Injection vulnerable
│   │   # - /logout
│   │   # 
│   │   # Vulnerabilities:
│   │   # - Direct string concatenation in SQL
│   │   # - No input validation
│   │   # - Plain text password storage
│   │
│   ├── 📄 views.py                              # 🔧 MAIN VIEWS (VULNERABLE)
│   │   # Routes:
│   │   # - / (index)
│   │   # - /dashboard
│   │   # - /profile ← 🔴 XSS vulnerable
│   │   # - /transfer (POST) ← 🔴 CSRF vulnerable
│   │   # - /transactions
│   │   # - /download/<filename> ← 🔴 Path Traversal vulnerable
│   │   #
│   │   # Vulnerabilities:
│   │   # - No HTML escaping for user input (XSS)
│   │   # - No CSRF tokens
│   │   # - No path validation (Path Traversal)
│   │
│   ├── 📁 templates/                            # 🎨 HTML TEMPLATES
│   │   │
│   │   ├── 📄 base.html                        # Base layout
│   │   │   # Contains:
│   │   │   # - Header with navigation
│   │   │   # - Flash messages
│   │   │   # - Content block
│   │   │   # - Footer
│   │   │
│   │   ├── 📄 index.html                       # Homepage
│   │   │   # - Welcome message
│   │   │   # - Login/Register links
│   │   │
│   │   ├── 📁 auth/
│   │   │   ├── 📄 login.html                   # Login form
│   │   │   │   # - Username input
│   │   │   │   # - Password input
│   │   │   │   # - Submit button
│   │   │   │
│   │   │   └── 📄 register.html                # Register form
│   │   │       # - Username, email, password inputs
│   │   │       # - Submit button
│   │   │
│   │   └── 📁 banking/
│   │       ├── 📄 dashboard.html               # User dashboard
│   │       │   # - Account balance
│   │       │   # - Quick actions
│   │       │   # - Recent transactions
│   │       │
│   │       ├── 📄 profile.html                 # User profile (XSS vulnerable)
│   │       │   # - Display user bio (NOT escaped)
│   │       │   # - Edit profile form
│   │       │
│   │       ├── 📄 transfer.html                # Money transfer (CSRF vulnerable)
│   │       │   # - To account input
│   │       │   # - Amount input
│   │       │   # - NO CSRF token
│   │       │
│   │       └── 📄 transactions.html            # Transaction history
│   │           # - List all transactions
│   │           # - Download statement link
│   │
│   └── 📁 static/                               # 🎨 STATIC FILES
│       │
│       ├── 📁 css/
│       │   └── 📄 style.css                    # Main stylesheet
│       │       # - Layout styles
│       │       # - Form styles
│       │       # - Table styles
│       │
│       ├── 📁 js/
│       │   └── 📄 main.js                      # Main JavaScript
│       │       # - Form validation (client-side only)
│       │       # - UI interactions
│       │
│       └── 📁 images/
│           ├── 📄 logo.png                     # Bank logo
│           └── 📄 icon.png                     # Favicon
│
├── 📁 attacks/                                   # 🔴 ATTACK SCRIPTS
│   │
│   ├── 📄 __init__.py
│   │
│   ├── 📄 sql_injection.py                      # SQL Injection attack
│   │   # Target: http://localhost:5000/login
│   │   # Payload: admin' OR '1'='1
│   │   # Expected: Login success without valid password
│   │
│   ├── 📄 xss_attack.py                         # XSS attack
│   │   # Target: http://localhost:5000/profile
│   │   # Payload: <script>alert('XSS')</script>
│   │   # Expected: Script executes in browser
│   │
│   ├── 📄 csrf_attack.py                        # CSRF attack
│   │   # Creates malicious HTML page
│   │   # Target: http://localhost:5000/transfer
│   │   # Expected: Unauthorized transfer when victim clicks
│   │
│   ├── 📄 path_traversal.py                     # Path Traversal attack
│   │   # Target: http://localhost:5000/download/../../etc/passwd
│   │   # Expected: Access to unauthorized files
│   │
│   └── 📄 run_all_attacks.py                    # Run all attacks at once
│       # Execute all 4 attacks and generate report
│
├── 📁 screenshots/                               # 📸 ATTACK EVIDENCE
│   ├── 📄 sql-injection-success.png
│   ├── 📄 xss-popup.png
│   ├── 📄 csrf-transfer.png
│   └── 📄 path-traversal-file.png
│
├── 📁 instance/                                  # Instance-specific files
│   └── 📄 app-vulnerable.sqlite                 # Database file (auto-generated)
│
├── 📁 tests/                                     # 🧪 TESTS
│   ├── 📄 conftest.py                           # Test configuration
│   ├── 📄 test_db.py                            # Database tests
│   ├── 📄 test_auth.py                          # Auth tests
│   └── 📄 test_attacks.py                       # Verify attacks work
│
├── 📄 .gitignore                                # Git ignore
│   # Ignore:
│   # - .venv/
│   # - instance/
│   # - __pycache__/
│   # - *.pyc
│
├── 📄 requirements.txt                          # Python dependencies
│   # Flask==3.0.0
│   # Werkzeug==3.0.1
│   # requests==2.31.0
│
├── 📄 pyproject.toml                            # Project metadata
│
└── 📄 README.md                                 # Project README
    # - Setup instructions
    # - How to run vulnerable version
    # - How to run attacks
    # - Port: 5000