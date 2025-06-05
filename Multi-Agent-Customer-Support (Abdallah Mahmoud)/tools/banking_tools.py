from crewai.tools import tool
from database.sql_manager import db
from database.vector_manager import vector_db

@tool
def get_account_balance(account_number: str) -> str:
    """Get account balance for a specific account number"""
    try:
        balance = db.get_account_balance(account_number)
        if balance is not None:
            return f"Your current account balance is: ${balance:,.2f}"
        else:
            return "Account not found. Please verify your account number."
    except Exception as e:
        return f"Error retrieving balance: {str(e)}"

@tool
def get_recent_transactions(account_number: str) -> str:
    """Get recent transactions for an account"""
    try:
        result = db.get_recent_transactions(account_number, limit=5)
        if not result.empty:
            transactions = []
            for _, transaction in result.iterrows():
                transactions.append(f"{transaction['created_at']}: {transaction['transaction_type']} ${transaction['amount']} - {transaction['description']}")
            return f"Recent transactions:\n" + "\n".join(transactions)
        else:
            return "No recent transactions found."
    except Exception as e:
        return f"Error retrieving transactions: {str(e)}"

@tool
def search_banking_knowledge(query: str) -> str:
    """Search banking knowledge base for relevant information"""
    try:
        results = vector_db.search_knowledge("banking", query, n_results=2)
        if results and results['documents']:
            knowledge = "\n".join(results['documents'][0])
            return f"Banking information: {knowledge}"
        else:
            return "No relevant banking information found."
    except Exception as e:
        return f"Error searching banking knowledge: {str(e)}"

@tool
def check_account_status(account_number: str) -> str:
    """Check the status of a bank account"""
    try:
        query = "SELECT account_type, status, created_at FROM bank_accounts WHERE account_number = ?"
        result = db.execute_query(query, (account_number,))
        if not result.empty:
            account = result.iloc[0]
            return f"Account Type: {account['account_type']}, Status: {account['status']}, Opened: {account['created_at']}"
        else:
            return "Account not found."
    except Exception as e:
        return f"Error checking account status: {str(e)}"