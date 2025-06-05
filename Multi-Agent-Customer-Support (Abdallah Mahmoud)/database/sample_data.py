from database.sql_manager import db
from database.vector_manager import vector_db

def populate_sample_data():
    """Populate database with sample data for testing"""
    
    # Sample customers
    customers_data = [
        ("CUST001", "John Smith", "john.smith@email.com", "555-0101", "ecommerce"),
        ("CUST002", "Jane Johnson", "jane.johnson@email.com", "555-0102", "banking"),
        ("CUST003", "Bob Wilson", "bob.wilson@email.com", "555-0103", "telecom"),
        ("CUST004", "Alice Brown", "alice.brown@email.com", "555-0104", "ecommerce"),
        ("CUST005", "Charlie Davis", "charlie.davis@email.com", "555-0105", "banking")
    ]
    
    for customer in customers_data:
        query = """INSERT OR REPLACE INTO customers 
                   (customer_id, name, email, phone, domain) 
                   VALUES (?, ?, ?, ?, ?)"""
        db.execute_query(query, customer)
    
    # Sample products
    products_data = [
        ("PROD001", "Wireless Headphones", 99.99, 50, "Electronics"),
        ("PROD002", "Laptop Stand", 49.99, 30, "Accessories"),
        ("PROD003", "USB-C Cable", 19.99, 100, "Cables"),
        ("PROD004", "Bluetooth Speaker", 79.99, 25, "Electronics"),
        ("PROD005", "Phone Case", 24.99, 75, "Accessories")
    ]
    
    for product in products_data:
        query = """INSERT OR REPLACE INTO products 
                   (product_id, name, price, stock_quantity, category) 
                   VALUES (?, ?, ?, ?, ?)"""
        db.execute_query(query, product)
    
    # Sample orders
    orders_data = [
        ("ORD001", "CUST001", "Wireless Headphones", "shipped", 99.99, "123 Main St, City, State", "TRK001"),
        ("ORD002", "CUST001", "USB-C Cable", "delivered", 19.99, "123 Main St, City, State", "TRK002"),
        ("ORD003", "CUST004", "Laptop Stand", "processing", 49.99, "456 Oak Ave, City, State", None),
        ("ORD004", "CUST004", "Bluetooth Speaker", "shipped", 79.99, "456 Oak Ave, City, State", "TRK003")
    ]
    
    for order in orders_data:
        query = """INSERT OR REPLACE INTO orders 
                   (order_id, customer_id, product_name, status, total_amount, shipping_address, tracking_number) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)"""
        db.execute_query(query, order)
    
    # Sample bank accounts
    accounts_data = [
        ("ACC001", "CUST002", "checking", 2500.75, "active"),
        ("ACC002", "CUST005", "savings", 15000.00, "active"),
        ("ACC003", "CUST002", "savings", 5750.25, "active")
    ]
    
    for account in accounts_data:
        query = """INSERT OR REPLACE INTO bank_accounts 
                   (account_number, customer_id, account_type, balance, status) 
                   VALUES (?, ?, ?, ?, ?)"""
        db.execute_query(query, account)
    
    # Sample transactions
    transactions_data = [
        ("TXN001", "ACC001", -45.00, "debit", "Grocery Store Purchase"),
        ("TXN002", "ACC001", 1200.00, "credit", "Salary Deposit"),
        ("TXN003", "ACC001", -89.99, "debit", "Online Purchase"),
        ("TXN004", "ACC002", 500.00, "credit", "Transfer from Checking"),
        ("TXN005", "ACC003", -25.00, "debit", "ATM Withdrawal")
    ]
    
    for transaction in transactions_data:
        query = """INSERT OR REPLACE INTO transactions 
                   (transaction_id, account_number, amount, transaction_type, description) 
                   VALUES (?, ?, ?, ?, ?)"""
        db.execute_query(query, transaction)
    
    # Sample telecom accounts
    telecom_data = [
        ("555-0103", "CUST003", "Unlimited Plan", 89.99, 45.2, "active", "2024-01-15"),
        ("555-0106", "CUST003", "Basic Plan", 39.99, 12.1, "active", "2024-01-10")
    ]
    
    for telecom in telecom_data:
        query = """INSERT OR REPLACE INTO telecom_accounts 
                   (phone_number, customer_id, plan_type, monthly_charge, data_usage_gb, status, last_payment_date) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)"""
        db.execute_query(query, telecom)
    
    # Populate vector database
    vector_db.populate_sample_knowledge()
    
    print("Sample data populated successfully!")

if __name__ == "__main__":
    populate_sample_data()