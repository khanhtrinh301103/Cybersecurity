-- Banking System Database Schema
-- SQLite Database for Vulnerable Version

-- Drop existing tables if they exist
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS users;

-- Users table: Store user credentials and profile info
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,  -- ⚠️ VULNERABLE: Plain text passwords (no hashing)
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    bio TEXT,  -- ⚠️ VULNERABLE: Can contain XSS payloads
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

-- Test users (passwords are plain text - VULNERABLE!)
INSERT INTO users (username, password, email, full_name, bio) VALUES
('admin', 'admin123', 'admin@bank.com', 'Administrator', 'System Administrator'),
('alice', 'alice123', 'alice@email.com', 'Alice Johnson', 'Regular user account'),
('bob', 'bob123', 'bob@email.com', 'Bob Smith', 'Another user account'),
('attacker', 'hacker', 'attacker@evil.com', 'Malicious User', '<script>alert("XSS")</script>');

-- Test accounts with initial balances
INSERT INTO accounts (user_id, account_number, balance) VALUES
(1, 'ACC-1001', 10000.00),  -- admin account
(2, 'ACC-1002', 5000.00),   -- alice account
(3, 'ACC-1003', 3000.00),   -- bob account
(4, 'ACC-1004', 100.00);    -- attacker account

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