import os
from flask import Flask, render_template, g

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

    return app