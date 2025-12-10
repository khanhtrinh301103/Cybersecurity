import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    User registration endpoint.
    Creates new user account with username, email, password.
    
    ✅ SECURE: Password hashing and input validation implemented
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()
        
        db = get_db()
        error = None

        # ✅ SECURE: Input validation
        if not username:
            error = 'Username is required.'
        elif len(username) < 3:
            error = 'Username must be at least 3 characters.'
        elif not password:
            error = 'Password is required.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        elif not email:
            error = 'Email is required.'
        elif '@' not in email:
            error = 'Invalid email format.'

        if error is None:
            try:
                # ✅ SECURE: Password hashing using werkzeug.security
                password_hash = generate_password_hash(password)
                
                # ✅ SECURE: Parameterized query prevents SQL injection
                db.execute(
                    "INSERT INTO users (username, password, email, full_name) VALUES (?, ?, ?, ?)",
                    (username, password_hash, email, full_name),
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
    
    ✅ SECURE: SQL Injection protection implemented
    - Parameterized queries (using ? placeholders)
    - Input validation
    - Password verification using werkzeug.security
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        db = get_db()
        error = None
        
        # ✅ SECURE: Input validation
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            # ✅ SECURE: Parameterized query prevents SQL injection
            # Using ? placeholder instead of string concatenation
            user = db.execute(
                'SELECT * FROM users WHERE username = ?',
                (username,)
            ).fetchone()
            
            if user is None:
                error = 'Invalid username or password.'
            else:
                # ✅ SECURE: Verify password using werkzeug.security
                # This compares the hashed password, not plain text
                if not check_password_hash(user['password'], password):
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
        # ✅ SECURE: Parameterized query
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

