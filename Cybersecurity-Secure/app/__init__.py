import os
from flask import Flask, render_template, g, request, redirect, url_for, flash, send_file
from flask_wtf.csrf import CSRFProtect

def create_app(test_config=None):
    """
    Application factory function.
    Creates and configures the Flask application with SECURE configurations.
    """
    # Create Flask app
    app = Flask(__name__, instance_relative_config=True)
    
    # Default configuration - SECURE VERSION
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secure-key-change-in-production'),
        DATABASE=os.path.join(app.instance_path, 'banking-secure.sqlite'),
        # CSRF Protection enabled
        WTF_CSRF_ENABLED=True,
        WTF_CSRF_TIME_LIMIT=None,  # No time limit for CSRF tokens
        # Secure session cookies
        SESSION_COOKIE_SECURE=False,  # Set to True in production with HTTPS
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )

    if test_config is None:
        # Load instance config if it exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load test config
        app.config.from_mapping(test_config)

    # Initialize CSRF protection
    csrf = CSRFProtect(app)
    
    # Make CSRF token available in all templates
    @app.context_processor
    def inject_csrf_token():
        from flask_wtf.csrf import generate_csrf
        return dict(csrf_token=lambda: generate_csrf())

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize database
    from . import db
    db.init_app(app)

    # Register authentication blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # Home page route
    @app.route('/')
    def index():
        """Homepage"""
        return render_template('index.html')

    # Dashboard route (protected)
    @app.route('/dashboard')
    @auth.login_required
    def dashboard():
        """User dashboard - requires login"""
        from app.db import get_db
        
        # Get user's account info
        account = get_db().execute(
            'SELECT * FROM accounts WHERE user_id = ?',
            (g.user['id'],)
        ).fetchone()
        
        # Get recent transactions
        transactions = get_db().execute(
            '''SELECT t.*, 
                      a1.account_number as from_account, 
                      a2.account_number as to_account
               FROM transactions t
               JOIN accounts a1 ON t.from_account_id = a1.id
               JOIN accounts a2 ON t.to_account_id = a2.id
               WHERE t.from_account_id = ? OR t.to_account_id = ?
               ORDER BY t.transaction_date DESC
               LIMIT 10''',
            (account['id'], account['id'])
        ).fetchall()
        
        return render_template('dashboard.html', account=account, transactions=transactions)
    
    # Profile route - XSS PROTECTED
    @app.route('/profile', methods=['GET', 'POST'])
    @auth.login_required
    def profile():
        """
        User profile page
        
        ✅ SECURE: XSS protection implemented
        - HTML escaping via Jinja2 autoescape (default)
        - Input validation and sanitization
        """
        from app.db import get_db
        from markupsafe import escape
        
        if request.method == 'POST':
            bio = request.form.get('bio', '')
            
            # ✅ SECURE: Input validation and sanitization
            # Remove potentially dangerous HTML tags while allowing safe formatting
            # In production, use a proper HTML sanitizer like bleach
            bio = escape(bio)  # Escape HTML entities
            
            db = get_db()
            db.execute(
                'UPDATE users SET bio = ? WHERE id = ?',
                (bio, g.user['id'])
            )
            db.commit()
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
        
        # Get current user info
        return render_template('profile.html')
    
    
    
    # Transfer route - CSRF PROTECTED
    @app.route('/transfer', methods=['GET', 'POST'])
    @auth.login_required
    def transfer():
        """
        Money transfer page
        
        ✅ SECURE: CSRF protection implemented
        - Flask-WTF CSRF tokens required
        - SameSite cookie attribute
        """
        from app.db import get_db
        
        if request.method == 'POST':
            # ✅ SECURE: CSRF token is automatically validated by Flask-WTF
            # If CSRF token is missing or invalid, Flask-WTF will raise CSRFError
            
            to_account_number = request.form.get('to_account')
            amount = request.form.get('amount')
            description = request.form.get('description', '')
            
            db = get_db()
            error = None
            
            # ✅ SECURE: Input validation
            if not to_account_number or not to_account_number.strip():
                error = 'Recipient account is required'
            elif not amount:
                error = 'Amount is required'
            
            if error is None:
                # Get user's account
                from_account = db.execute(
                    'SELECT * FROM accounts WHERE user_id = ?',
                    (g.user['id'],)
                ).fetchone()
                
                # Get recipient's account
                to_account = db.execute(
                    'SELECT * FROM accounts WHERE account_number = ?',
                    (to_account_number.strip(),)
                ).fetchone()
                
                # Basic validation
                try:
                    amount = float(amount)
                except (ValueError, TypeError):
                    error = 'Invalid amount'
                
                if not to_account:
                    error = f'Account {to_account_number} not found'
                elif amount <= 0:
                    error = 'Amount must be greater than 0'
                elif amount > from_account['balance']:
                    error = 'Insufficient balance'
                elif from_account['account_number'] == to_account_number:
                    error = 'Cannot transfer to your own account'
                
                if error is None:
                    # ✅ SECURE: All validations passed, CSRF token already validated
                    
                    # Deduct from sender
                    db.execute(
                        'UPDATE accounts SET balance = balance - ? WHERE id = ?',
                        (amount, from_account['id'])
                    )
                    
                    # Add to recipient
                    db.execute(
                        'UPDATE accounts SET balance = balance + ? WHERE id = ?',
                        (amount, to_account['id'])
                    )
                    
                    # Record transaction
                    db.execute(
                        '''INSERT INTO transactions 
                           (from_account_id, to_account_id, amount, description) 
                           VALUES (?, ?, ?, ?)''',
                        (from_account['id'], to_account['id'], amount, description)
                    )
                    
                    db.commit()
                    
                    flash(f'Successfully transferred ${amount:.2f} to {to_account_number}', 'success')
                    return redirect(url_for('dashboard'))
            
            flash(error, 'error')
        
        # Get user's account info
        from app.db import get_db
        account = get_db().execute(
            'SELECT * FROM accounts WHERE user_id = ?',
            (g.user['id'],)
        ).fetchone()
        
        # Get other accounts for testing
        other_accounts = get_db().execute(
            '''SELECT a.account_number, u.username 
               FROM accounts a 
               JOIN users u ON a.user_id = u.id 
               WHERE a.user_id != ?''',
            (g.user['id'],)
        ).fetchall()
        
        return render_template('transfer.html', account=account, other_accounts=other_accounts)
    

    
    # SECURE Download route – Path Traversal PROTECTED
    @app.route('/download')
    @auth.login_required
    def download():
        """
        Download transaction statement or documents

        ✅ SECURE: Path Traversal protection implemented
        - Path validation and normalization
        - Whitelist-based file access
        - User-specific file access control
        """
        import os
        from pathlib import Path
        
        try:
            # ✅ SECURE: Get filename from query parameter
            filename = request.args.get('file', '')
            
            if not filename:
                flash('File parameter is required', 'error')
                return redirect(url_for('dashboard'))
            
            # ✅ SECURE: Normalize path and prevent directory traversal
            # Remove any path separators and normalize
            filename = os.path.basename(filename)  # Get only the filename, no path
            
            # ✅ SECURE: Whitelist - only allow files in statements directory
            statements_dir = os.path.join(app.instance_path, 'statements')
            os.makedirs(statements_dir, exist_ok=True)
            
            # ✅ SECURE: Construct safe filepath
            filepath = os.path.join(statements_dir, filename)
            
            # ✅ SECURE: Verify file is within allowed directory (prevent path traversal)
            # Resolve to absolute path to prevent any remaining traversal attempts
            filepath = os.path.abspath(filepath)
            allowed_dir = os.path.abspath(statements_dir)
            
            # ✅ SECURE: Ensure file is within allowed directory
            if not filepath.startswith(allowed_dir):
                flash('Access denied: Invalid file path', 'error')
                return redirect(url_for('dashboard'))
            
            # ✅ SECURE: Verify file exists and is readable
            if not os.path.exists(filepath) or not os.path.isfile(filepath):
                flash('File not found', 'error')
                return redirect(url_for('dashboard'))
            
            # ✅ SECURE: Optional - Verify user owns this file (check account number in filename)
            from app.db import get_db
            account = get_db().execute(
                'SELECT * FROM accounts WHERE user_id = ?',
                (g.user['id'],)
            ).fetchone()
            
            # Only allow download if filename contains user's account number or user ID
            if account['account_number'] not in filename and str(account['id']) not in filename:
                flash('Access denied: You can only download your own statements', 'error')
                return redirect(url_for('dashboard'))
            
            return send_file(filepath, as_attachment=True)

        except Exception as e:
            flash(f'Error downloading file: {str(e)}', 'error')
            return redirect(url_for('dashboard'))

    
    
    # Statements route - List available statements
    @app.route('/statements')
    @auth.login_required
    def statements():
        """
        List available transaction statements for download
        """
        import os
        from app.db import get_db
        
        # Get user's account
        account = get_db().execute(
            'SELECT * FROM accounts WHERE user_id = ?',
            (g.user['id'],)
        ).fetchone()
        
        # Create statements directory if not exists
        statements_dir = os.path.join(app.instance_path, 'statements')
        os.makedirs(statements_dir, exist_ok=True)
        
        # Create sample statement files for demonstration
        sample_files = [
            f'statement_{account["account_number"]}_2024_01.txt',
            f'statement_{account["account_number"]}_2024_02.txt',
            f'receipt_{account["id"]}_001.txt'
        ]
        
        for sample_file in sample_files:
            filepath = os.path.join(statements_dir, sample_file)
            if not os.path.exists(filepath):
                with open(filepath, 'w') as f:
                    f.write(f"Transaction Statement\n")
                    f.write(f"Account: {account['account_number']}\n")
                    f.write(f"Balance: ${account['balance']:.2f}\n")
                    f.write(f"Generated: 2024-01-01\n")
        
        # List all files in statements directory
        try:
            files = os.listdir(statements_dir)
            # Filter to show only user's files
            user_files = [f for f in files if account['account_number'] in f or str(account['id']) in f]
        except:
            user_files = []
        
        return render_template('statements.html', files=user_files, account=account)

    return app
