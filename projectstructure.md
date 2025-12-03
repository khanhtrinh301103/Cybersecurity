Cybersecurity/
├── .venv/                      # Virtual environment (không commit lên Git)
├── app/                        # THƯ MỤC CHÍNH CỦA ỨNG DỤNG
│   ├── __init__.py            # Application factory, cấu hình app
│   │
│   ├── models.py              # 📊 DATABASE MODELS (SQLAlchemy/SQL)
│   ├── db.py                  # 📊 DATABASE: Kết nối & khởi tạo database
│   ├── schema.sql             # 📊 DATABASE: SQL schema để tạo tables
│   │
│   ├── auth.py                # 🔧 BACKEND: Authentication logic (đăng nhập, đăng ký)
│   ├── blog.py                # 🔧 BACKEND: Blog logic (CRUD operations)
│   ├── api.py                 # 🔧 BACKEND: API endpoints (nếu có)
│   │
│   ├── templates/             # 🎨 FRONTEND/UI: HTML templates
│   │   ├── base.html          # Layout chính (header, footer, navigation)
│   │   ├── index.html         # Trang chủ
│   │   │
│   │   ├── auth/              # 🎨 UI: Authentication pages
│   │   │   ├── login.html     # Form đăng nhập
│   │   │   └── register.html  # Form đăng ký
│   │   │
│   │   └── blog/              # 🎨 UI: Blog pages
│   │       ├── create.html    # Form tạo bài viết
│   │       ├── index.html     # Danh sách bài viết
│   │       └── update.html    # Form chỉnh sửa bài viết
│   │
│   └── static/                # 🎨 FRONTEND: Static files (CSS, JS, images)
│       ├── css/
│       │   └── style.css      # Styling cho UI
│       ├── js/
│       │   └── main.js        # JavaScript cho tương tác frontend
│       └── images/
│           └── logo.png       # Hình ảnh, icons
│
├── tests/                     # 🧪 TEST: Unit tests và integration tests
│   ├── conftest.py
│   ├── test_db.py             # Test database
│   ├── test_auth.py           # Test authentication
│   └── test_blog.py           # Test blog features
│
├── instance/                  # Dữ liệu instance-specific (database file, config)
│   └── app.sqlite             # SQLite database file (tự động tạo)
│
├── .gitignore                 # Ignore files cho Git
├── README.md                  # Mô tả project
├── pyproject.toml             # Project metadata và dependencies
└── requirements.txt           # Python dependencies