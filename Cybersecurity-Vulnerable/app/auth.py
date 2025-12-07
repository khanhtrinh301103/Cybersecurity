import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    User registration endpoint.
    Creates new user account with username, email, password.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        full_name = request.form.get('full_name', '')
        
        db = get_db()
        error = None

        # Basic validation
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'

        if error is None:
            try:
                # ⚠️ VULNERABLE: Plain text password storage (no hashing)
                # ⚠️ VULNERABLE: No input validation (allows XSS in full_name)
                db.execute(
                    "INSERT INTO users (username, password, email, full_name) VALUES (?, ?, ?, ?)",
                    (username, password, email, full_name),
                )
                db.commit()
                
                # Auto-create bank account for new user
                user_id = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()['id']
                account_number = f'ACC-{1000 + user_id}'
                db.execute(
                    "INSERT INTO accounts (user_id, account_number, balance) VALUES (?, ?, ?)",
                    (user_id, account_number, 1000.00)
                )
                db.commit()
                
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('auth.login'))
                
            except db.IntegrityError:
                error = f"Username '{username}' or email '{email}' is already registered."
        
        flash(error, 'error')

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    User login endpoint.
    
    ⚠️ SECURITY WARNING: This function is INTENTIONALLY VULNERABLE to SQL Injection!
    
    Vulnerable code for demonstration purposes:
    - Direct string concatenation in SQL query
    - No input validation or sanitization
    - Allows SQL injection attacks like: admin' OR '1'='1
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        error = None
        
        # 🔴 VULNERABLE: SQL Injection vulnerability
        # Direct string concatenation allows SQL injection
        # Attack example: username = "admin' OR '1'='1" bypasses authentication
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        
        try:
            user = db.execute(query).fetchone()
        except db.Error as e:
            # ⚠️ VULNERABLE: Verbose error messages leak database info
            error = f'Database error: {str(e)}'
            user = None

        if user is None and error is None:
            error = 'Invalid username or password.'

        if error is None:
            # Login successful
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('index'))

        flash(error, 'error')

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    """
    User logout endpoint.
    Clears the session and redirects to login page.
    """
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@bp.before_app_request
def load_logged_in_user():
    """
    Load user information before each request if user is logged in.
    Makes user data available in g.user for all views.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    """
    Decorator to require login for protected views.
    
    Usage:
        @login_required
        def dashboard():
            return render_template('dashboard.html')
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view