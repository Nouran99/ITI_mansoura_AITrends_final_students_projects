from crewai.tools import tool
from database.sql_manager import db
from database.vector_manager import vector_db

@tool
def get_telecom_account_info(phone_number: str) -> str:
    """Get telecom account information for a phone number"""
    try:
        result = db.get_telecom_account(phone_number)
        if not result.empty:
            account = result.iloc[0]
            return f"Phone: {phone_number}, Plan: {account['plan_type']}, Monthly Charge: ${account['monthly_charge']}, Status: {account['status']}"
        else:
            return "Phone number not found in our system."
    except Exception as e:
        return f"Error retrieving account info: {str(e)}"

@tool
def get_data_usage(phone_number: str) -> str:
    """Get current data usage for a phone number"""
    try:
        result = db.get_usage_data(phone_number)
        if not result.empty:
            usage = result.iloc[0]
            return f"Current data usage: {usage['data_usage_gb']} GB this month. Monthly charge: ${usage['monthly_charge']}"
        else:
            return "Phone number not found."
    except Exception as e:
        return f"Error retrieving usage data: {str(e)}"

@tool
def search_telecom_knowledge(query: str) -> str:
    """Search telecom knowledge base for relevant information"""
    try:
        results = vector_db.search_knowledge("telecom", query, n_results=2)
        if results and results['documents']:
            knowledge = "\n".join(results['documents'][0])
            return f"Telecom information: {knowledge}"
        else:
            return "No relevant telecom information found."
    except Exception as e:
        return f"Error searching telecom knowledge: {str(e)}"

@tool
def check_network_status(phone_number: str) -> str:
    """Check network status for a specific phone number"""
    try:
        # Simulate network check
        result = db.get_telecom_account(phone_number)
        if not result.empty:
            return f"Network status for {phone_number}: Active and operational. Signal strength: Strong."
        else:
            return "Phone number not found in our network."
    except Exception as e:
        return f"Error checking network status: {str(e)}"