import os
from flask import Flask, render_template, g, request, redirect, url_for, flash, send_file


def create_app(test_config=None):
    """
    Application factory function.
    Creates and configures the Flask application.
    """
    # Create Flask app
    app = Flask(__name__, instance_relative_config=True)
    
    # Default configuration
    app.config.from_mapping(
        SECRET_KEY='dev-vulnerable-key-do-not-use-in-production',
        DATABASE=os.path.join(app.instance_path, 'banking-vulnerable.sqlite'),
    )

    if test_config is None:
        # Load instance config if it exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load test config
        app.config.from_mapping(test_config)

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
    
    # Profile route - XSS VULNERABILITY
    @app.route('/profile', methods=['GET', 'POST'])
    @auth.login_required
    def profile():
        """
        User profile page
        
        ⚠️ SECURITY WARNING: This page is VULNERABLE to XSS (Cross-Site Scripting)!
        User input (bio) is displayed without HTML escaping.
        """
        from app.db import get_db
        
        if request.method == 'POST':
            bio = request.form.get('bio', '')
            
            # ⚠️ VULNERABLE: No input validation or sanitization
            # Allows XSS payloads like: <script>alert('XSS')</script>
            
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
    
    
    
    # Transfer route - CSRF VULNERABILITY
    @app.route('/transfer', methods=['GET', 'POST'])
    @auth.login_required
    def transfer():
        """
        Money transfer page
        
        ⚠️ SECURITY WARNING: This page is VULNERABLE to CSRF (Cross-Site Request Forgery)!
        No CSRF token validation - attacker can trick users into transferring money.
        """
        from app.db import get_db
        
        if request.method == 'POST':
            to_account_number = request.form.get('to_account')
            amount = request.form.get('amount')
            description = request.form.get('description', '')
            
            db = get_db()
            error = None
            
            # Get user's account
            from_account = db.execute(
                'SELECT * FROM accounts WHERE user_id = ?',
                (g.user['id'],)
            ).fetchone()
            
            # Get recipient's account
            to_account = db.execute(
                'SELECT * FROM accounts WHERE account_number = ?',
                (to_account_number,)
            ).fetchone()
            
            # Basic validation
            try:
                amount = float(amount)
            except (ValueError, TypeError):
                error = 'Invalid amount'
            
            if not to_account_number:
                error = 'Recipient account is required'
            elif not to_account:
                error = f'Account {to_account_number} not found'
            elif amount <= 0:
                error = 'Amount must be greater than 0'
            elif amount > from_account['balance']:
                error = 'Insufficient balance'
            elif from_account['account_number'] == to_account_number:
                error = 'Cannot transfer to your own account'
            
            if error is None:
                # ⚠️ VULNERABLE: No CSRF token validation!
                # Any website can submit this form and transfer money
                
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
    


    
    # VULNERABLE Download route – Path Traversal via query parameter
    @app.route('/download')
    @auth.login_required
    def download():
        """
        Download transaction statement or documents

        ⚠️ SECURITY WARNING: This function is VULNERABLE to Path Traversal!
        The 'file' query parameter is not validated, so attackers can use
        ../ to access files outside the intended directory.
        Example: /download?file=../../app/schema.sql
        """
        try:
            # Base directory = instance folder
            # Legit files nằm ở: instance/statements/...
            base_dir = app.instance_path

            # ⚠️ VULNERABLE: Lấy trực tiếp input từ query, không kiểm tra
            filename = request.args.get('file', '')

            # Nối path thẳng với user input
            filepath = os.path.join(base_dir, filename)

            return send_file(filepath, as_attachment=True)

        except FileNotFoundError:
            flash(f'File not found: {filepath}', 'error')
            return redirect(url_for('dashboard'))
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
    

    

    # Account details route - IDOR VULNERABILITY
    @app.route('/account/<int:account_id>')
    @auth.login_required
    def account_details(account_id):
        """
        View account details
        
        ⚠️ SECURITY WARNING: IDOR (Insecure Direct Object Reference)!
        User can view ANY account by changing the account_id in URL.
        No authorization check to verify account belongs to logged-in user.
        """
        from app.db import get_db
        
        # ⚠️ VULNERABLE: No authorization check!
        # Directly fetching account based on user-supplied ID
        account = get_db().execute(
            'SELECT * FROM accounts WHERE id = ?',
            (account_id,)
        ).fetchone()
        
        if account is None:
            flash('Account not found', 'error')
            return redirect(url_for('dashboard'))
        
        # Get account owner info
        owner = get_db().execute(
            'SELECT * FROM users WHERE id = ?',
            (account['user_id'],)
        ).fetchone()
        
        # Get account transactions
        transactions = get_db().execute(
            '''SELECT t.*, 
                    a1.account_number as from_account, 
                    a2.account_number as to_account
            FROM transactions t
            JOIN accounts a1 ON t.from_account_id = a1.id
            JOIN accounts a2 ON t.to_account_id = a2.id
            WHERE t.from_account_id = ? OR t.to_account_id = ?
            ORDER BY t.transaction_date DESC
            LIMIT 20''',
            (account_id, account_id)
        ).fetchall()
        
        # ⚠️ VULNERABLE: Displaying other user's sensitive data!
        return render_template('account_details.html', 
                            account=account, 
                            owner=owner, 
                            transactions=transactions)

    return app