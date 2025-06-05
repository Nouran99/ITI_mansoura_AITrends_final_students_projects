import sqlite3
import pandas as pd
from datetime import datetime
from config.settings import DATABASE_PATH

class SQLManager:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize database with all required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                phone VARCHAR(20),
                domain VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # E-commerce tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id VARCHAR(50) UNIQUE NOT NULL,
                customer_id VARCHAR(50) NOT NULL,
                product_name VARCHAR(200),
                status VARCHAR(20) DEFAULT 'processing',
                total_amount DECIMAL(10,2),
                shipping_address TEXT,
                tracking_number VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(200) NOT NULL,
                price DECIMAL(10,2),
                stock_quantity INTEGER DEFAULT 0,
                category VARCHAR(50),
                description TEXT
            )
        ''')
        
        # Banking tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bank_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number VARCHAR(20) UNIQUE NOT NULL,
                customer_id VARCHAR(50) NOT NULL,
                account_type VARCHAR(20) DEFAULT 'checking',
                balance DECIMAL(15,2) DEFAULT 0.00,
                status VARCHAR(20) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id VARCHAR(50) UNIQUE NOT NULL,
                account_number VARCHAR(20) NOT NULL,
                amount DECIMAL(15,2) NOT NULL,
                transaction_type VARCHAR(20) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_number) REFERENCES bank_accounts(account_number)
            )
        ''')
        
        # Telecom tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS telecom_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number VARCHAR(15) UNIQUE NOT NULL,
                customer_id VARCHAR(50) NOT NULL,
                plan_type VARCHAR(50),
                monthly_charge DECIMAL(8,2),
                data_usage_gb DECIMAL(5,2) DEFAULT 0,
                status VARCHAR(20) DEFAULT 'active',
                last_payment_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        ''')
        
        # Chat sessions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id VARCHAR(50) NOT NULL,
                customer_id VARCHAR(50) NOT NULL,
                domain VARCHAR(20) NOT NULL,
                messages TEXT, -- JSON format
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            conn.close()
            return pd.DataFrame(results, columns=columns) if results else pd.DataFrame()
        else:
            conn.commit()
            conn.close()
            return True
    
    # E-commerce methods
    def get_order_status(self, order_id):
        query = "SELECT * FROM orders WHERE order_id = ?"
        return self.execute_query(query, (order_id,))
    
    def get_customer_orders(self, customer_id):
        query = "SELECT * FROM orders WHERE customer_id = ? ORDER BY created_at DESC"
        return self.execute_query(query, (customer_id,))
    
    # Banking methods
    def get_account_balance(self, account_number):
        query = "SELECT balance FROM bank_accounts WHERE account_number = ?"
        result = self.execute_query(query, (account_number,))
        return result.iloc[0]['balance'] if not result.empty else None
    
    def get_recent_transactions(self, account_number, limit=5):
        query = """SELECT * FROM transactions 
                   WHERE account_number = ? 
                   ORDER BY created_at DESC LIMIT ?"""
        return self.execute_query(query, (account_number, limit))
    
    # Telecom methods
    def get_telecom_account(self, phone_number):
        query = "SELECT * FROM telecom_accounts WHERE phone_number = ?"
        return self.execute_query(query, (phone_number,))
    
    def get_usage_data(self, phone_number):
        query = "SELECT data_usage_gb, monthly_charge FROM telecom_accounts WHERE phone_number = ?"
        return self.execute_query(query, (phone_number,))

# Global database instance
db = SQLManager()