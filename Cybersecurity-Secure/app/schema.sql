-- Banking System Database Schema
-- SQLite Database for SECURE Version

-- Drop existing tables if they exist
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS users;

-- Users table: Store user credentials and profile info
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,  -- ✅ SECURE: Stores hashed passwords (werkzeug.security)
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    bio TEXT,  -- ✅ SECURE: HTML escaped before storage
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Accounts table: Store bank account information
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    account_number TEXT UNIQUE NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Transactions table: Store money transfer history
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_account_id INTEGER NOT NULL,
    to_account_id INTEGER NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    description TEXT,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (from_account_id) REFERENCES accounts (id),
    FOREIGN KEY (to_account_id) REFERENCES accounts (id)
);

-- Insert test data for demonstration
-- Note: Passwords will be hashed when users register/login
-- For testing, you can manually hash passwords using werkzeug.security.generate_password_hash()

-- Test users (passwords need to be hashed - use werkzeug.security.generate_password_hash())
-- Example: generate_password_hash('admin123') = 'pbkdf2:sha256:...'
INSERT INTO users (username, password, email, full_name, bio) VALUES
('admin', 'pbkdf2:sha256:600000$XxXxXxXxXxXxXxXx$...', 'admin@bank.com', 'Administrator', 'System Administrator'),
('alice', 'pbkdf2:sha256:600000$XxXxXxXxXxXxXxXx$...', 'alice@email.com', 'Alice Johnson', 'Regular user account'),
('bob', 'pbkdf2:sha256:600000$XxXxXxXxXxXxXxXx$...', 'bob@email.com', 'Bob Smith', 'Another user account');

-- Test accounts with initial balances
INSERT INTO accounts (user_id, account_number, balance) VALUES
(1, 'ACC-1001', 10000.00),  -- admin account
(2, 'ACC-1002', 5000.00),   -- alice account
(3, 'ACC-1003', 3000.00);   -- bob account

-- Sample transactions
INSERT INTO transactions (from_account_id, to_account_id, amount, description) VALUES
(2, 3, 500.00, 'Payment for services'),
(1, 2, 1000.00, 'Salary payment'),
(3, 2, 200.00, 'Refund');

-- Create indexes for better performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_accounts_user ON accounts(user_id);
CREATE INDEX idx_accounts_number ON accounts(account_number);
CREATE INDEX idx_transactions_from ON transactions(from_account_id);
CREATE INDEX idx_transactions_to ON transactions(to_account_id);

UPDATE users
SET password = 'scrypt:32768:8:1$eEyfzd3N3FGhjoJ3$2a88d65651dbac70eb17d2a3a12e30abbe6ff537b8736464a5c4ddec86aac648d09da67e1828a3c7751e6482d5d8a00858c90a89ea663903c2a43481465f26d4'
WHERE username = 'admin';

