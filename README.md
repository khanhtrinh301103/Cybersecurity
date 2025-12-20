# Cybersecurity Banking Application - Security Analysis Project

This project contains two versions of a Flask banking application:
- **Cybersecurity-Vulnerable**: Intentionally vulnerable version for attack simulation
- **Cybersecurity-Secure**: Secure version with Defense in Depth protections

## Quick Start - Running Both Projects Simultaneously

To test and compare both versions, you need to run them in separate terminal windows.

### Method 1: Using Two PowerShell Windows (Recommended)

**Terminal 1 - Vulnerable Version:**
```powershell
cd "Cybersecurity-Vulnerable"
.venv\Scripts\activate
flask init-db
flask run --port 5000
```

**Terminal 2 - Secure Version:**
```powershell
cd "Cybersecurity-Secure"
.venv\Scripts\activate
flask init-db
flask run --port 5001
```

### Method 2: Using Background Jobs (PowerShell)

Run both in the same PowerShell window:
```powershell
# Start Vulnerable version in background
cd "Cybersecurity-Vulnerable"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .venv\Scripts\activate; flask run --port 5000"

# Start Secure version in background
cd "Cybersecurity-Secure"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .venv\Scripts\activate; flask run --port 5001"
```

### Method 3: Using Batch Script

Create a file `run_both.bat` in the Cybersecurity folder:
```batch
@echo off
start "Vulnerable App" cmd /k "cd Cybersecurity-Vulnerable && .venv\Scripts\activate && flask run --port 5000"
start "Secure App" cmd /k "cd Cybersecurity-Secure && .venv\Scripts\activate && flask run --port 5001"
```

Then simply double-click `run_both.bat` to start both applications.

## Access URLs

Once both applications are running:

- **Vulnerable Version**: http://localhost:5000
- **Secure Version**: http://localhost:5001

## Test Accounts

### Vulnerable Version:
- Username: `admin`
- Password: `admin123`

### Secure Version:
- Username: `admin`
- Password: `admin123`

## Testing Attacks

### 1. SQL Injection Test
- **Vulnerable**: http://localhost:5000/auth/login
  - Try: `admin' OR '1'='1` in username field
  - **Expected**: Login succeeds (vulnerable)
  
- **Secure**: http://localhost:5001/auth/login
  - Try: `admin' OR '1'='1` in username field
  - **Expected**: Login fails (protected)

### 2. XSS Test
- **Vulnerable**: http://localhost:5000/profile
  - Enter: `<script>alert('XSS')</script>` in bio field
  - **Expected**: Script executes (vulnerable)
  
- **Secure**: http://localhost:5001/profile
  - Enter: `<script>alert('XSS')</script>` in bio field
  - **Expected**: Script displayed as text (protected)

### 3. CSRF Test

**Step-by-Step Instructions to Open `csrf_attack.html`:**

**Method 1: Double-Click (Easiest)**
1. Open **File Explorer** (Windows key + E)
2. Navigate to: `D:\security in computing information technology\a2\Cybersecurity\`
3. Look for the file named `csrf_attack.html`
4. **Double-click** the file
5. It will automatically open in your default web browser (Chrome, Edge, Firefox, etc.)

**Method 2: Right-Click Menu**
1. Navigate to the `Cybersecurity` folder in File Explorer
2. **Right-click** on `csrf_attack.html`
3. Select **"Open with"** → Choose your browser (Chrome, Edge, Firefox, etc.)

**Method 3: Drag and Drop**
1. Open your web browser (Chrome, Edge, Firefox, etc.)
2. Open File Explorer and navigate to the `Cybersecurity` folder
3. **Drag** the `csrf_attack.html` file and **drop** it into the browser window

**Method 4: From Browser**
1. Open your web browser
2. Press **Ctrl + O** (or go to File → Open)
3. Navigate to: `D:\security in computing information technology\a2\Cybersecurity\`
4. Select `csrf_attack.html` and click **Open**

---

**Complete CSRF Testing Procedure:**

#### **Test A: Vulnerable Version (Port 5000)**

1. **Start the Vulnerable Application:**
   - Make sure the vulnerable app is running on http://localhost:5000
   - If not running, follow the "Quick Start" instructions above

2. **Login to Vulnerable App:**
   - Open browser and go to: http://localhost:5000
   - Login with:
     - Username: `admin`
     - Password: `admin123`
   - **Important**: Stay logged in (do NOT close this tab/window)

3. **Open the CSRF Attack File:**
   - Use one of the methods above to open `csrf_attack.html`
   - The file will open in a **new tab** or **new window**
   - You should see a webpage with title "Win a Free iPhone!" and a button "Claim My iPhone!"

4. **Execute the Attack:**
   - Click the **"Claim My iPhone!"** button
   - The page will show "Processing your claim..."

5. **Check the Result:**
   - Go back to the vulnerable app tab (http://localhost:5000)
   - Check your account balance or transaction history
   - **Expected Result**: $500 was transferred to account ACC-1004 (CSRF attack succeeded - vulnerable)

---

#### **Test B: Secure Version (Port 5001)**

1. **Start the Secure Application:**
   - Make sure the secure app is running on http://localhost:5001
   - If not running, follow the "Quick Start" instructions above

2. **Modify the Attack File (Required):**
   - The `csrf_attack.html` file currently targets port 5000
   - You need to change it to target port 5001:
     - Open `csrf_attack.html` in a text editor (Notepad, VS Code, etc.)
     - Find line 45: `action="http://127.0.0.1:5000/transfer"`
     - Change it to: `action="http://127.0.0.1:5001/transfer"`
     - Save the file

3. **Login to Secure App:**
   - Open browser and go to: http://localhost:5001
   - Login with:
     - Username: `admin`
     - Password: `admin123`
   - **Important**: Stay logged in (do NOT close this tab/window)

4. **Open the CSRF Attack File:**
   - Use one of the methods above to open `csrf_attack.html`
   - The file will open in a **new tab** or **new window**

5. **Execute the Attack:**
   - Click the **"Claim My iPhone!"** button

6. **Check the Result:**
   - You should see an **error message** in the browser
   - Common errors:
     - "Bad Request - CSRF token missing"
     - "400 Bad Request"
     - "CSRF token is missing"
   - Go back to the secure app tab (http://localhost:5001)
   - Check your account balance
   - **Expected Result**: No money was transferred (CSRF attack blocked - protected)

---

**Visual Guide:**
```
Step 1: Login to Banking App          Step 2: Open csrf_attack.html
┌─────────────────────┐              ┌─────────────────────┐
│ Banking App          │              │ Win a Free iPhone!   │
│ (Stay logged in)     │              │ [Claim My iPhone!]  │
│                      │              │                      │
│ Port 5000 or 5001    │              │ (Hidden form)       │
└─────────────────────┘              └─────────────────────┘
         │                                      │
         │                                      │
         └────────── Click Button ──────────────┘
                      │
                      ▼
         ┌─────────────────────┐
         │ Check Result:       │
         │ - Vulnerable: ✅    │
         │   Transfer works    │
         │ - Secure: ❌        │
         │   Transfer blocked  │
         └─────────────────────┘
```

**Troubleshooting:**

- **File won't open?**
  - Make sure you're in the correct folder: `Cybersecurity` (not inside `Cybersecurity-Vulnerable` or `Cybersecurity-Secure`)
  - Try right-click → Properties → Check if file extension is `.html`

- **Attack doesn't work on vulnerable version?**
  - Make sure you're logged into http://localhost:5000
  - Make sure the vulnerable app is running
  - Check browser console (F12) for errors

- **Attack works on secure version?**
  - Make sure you changed port 5000 to 5001 in the file
  - Make sure you're logged into http://localhost:5001
  - Check that CSRF protection is enabled in the secure app

### 4. Path Traversal Test
check carefully the code of csrf_attack.html when testing isn't it look forward to vulnerable port or secure port before testing
- **Vulnerable**: http://localhost:5000/download?file=../app/schema.sql
  - **Expected**: File downloaded (vulnerable)
  
- **Secure**: http://localhost:5001/download?file=../app/schema.sql
  - **Expected**: Access denied (protected)

### 5. IDOR Test
- **Vulnerable**: http://localhost:5000/account/2 (while logged in as admin)
  - **Expected**: Can view other user's account (vulnerable)
  
- **Secure**: http://localhost:5001/account/2 (while logged in as admin)
  - **Expected**: Access denied (protected)

## Project Structure

```
Cybersecurity/
├── Cybersecurity-Vulnerable/    # Vulnerable version (Port 5000)
│   ├── app/
│   ├── instance/
│   └── README.md
├── Cybersecurity-Secure/        # Secure version (Port 5001)
│   ├── app/
│   ├── instance/
│   └── README.md
├── AttackSimulation.md          # Attack simulation guide
├── csrf_attack.html            # CSRF attack test file
└── README.md                   # This file
```

## Prerequisites

- Python 3.8 or higher
- Virtual environments for both projects (`.venv` folders)
- Flask installed in both virtual environments

## Initial Setup (First Time Only)

### Vulnerable Version:
```powershell
cd "Cybersecurity-Vulnerable"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
flask init-db
```

### Secure Version:
```powershell
cd "Cybersecurity-Secure"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
flask init-db
```

## Troubleshooting

### Port Already in Use
If you get "Address already in use" error:
- Check if another Flask app is running on ports 5000 or 5001
- Kill the process: `netstat -ano | findstr :5000` then `taskkill /PID <PID> /F`
- Or change ports in the commands above

### Virtual Environment Not Found
If `.venv` folder doesn't exist:
- Run the Initial Setup commands above
- Make sure you're in the correct directory

### Database Not Initialized
If you get database errors:
- Run `flask init-db` in each project directory
- Make sure you're in the project root directory when running the command

## Notes

- This is an educational project for security analysis
- Both versions should be run simultaneously for comparison testing
- The vulnerable version is intentionally insecure for demonstration purposes
- Never use the vulnerable version in production environments

account: 
admin admin123
alice alice123
bob bob123