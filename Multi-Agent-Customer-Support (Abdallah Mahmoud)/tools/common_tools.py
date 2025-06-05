from crewai.tools import tool
from database.sql_manager import db
from database.vector_manager import vector_db
import json
from datetime import datetime

@tool
def get_customer_info(customer_id: str) -> str:
    """Get customer information by customer ID"""
    try:
        query = "SELECT * FROM customers WHERE customer_id = ?"
        result = db.execute_query(query, (customer_id,))
        if not result.empty:
            customer = result.iloc[0]
            return f"Customer: {customer['name']}, Email: {customer['email']}, Phone: {customer['phone']}, Domain: {customer['domain']}"
        else:
            return f"Customer {customer_id} not found."
    except Exception as e:
        return f"Error retrieving customer info: {str(e)}"

@tool
def search_general_knowledge(query: str) -> str:
    """Search across all knowledge bases for general information"""
    try:
        all_results = []
        domains = ["ecommerce", "banking", "telecom"]
        
        for domain in domains:
            results = vector_db.search_knowledge(domain, query, n_results=1)
            if results and results['documents']:
                all_results.extend(results['documents'][0])
        
        if all_results:
            return f"General information found: {' | '.join(all_results[:2])}"
        else:
            return "No relevant information found in knowledge base."
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"

@tool
def log_chat_session(session_id: str, customer_id: str, domain: str, messages: str) -> str:
    """Log chat session for analytics and history"""
    try:
        query = """INSERT INTO chat_sessions 
                   (session_id, customer_id, domain, messages) 
                   VALUES (?, ?, ?, ?)"""
        
        db.execute_query(query, (session_id, customer_id, domain, messages))
        return f"Chat session {session_id} logged successfully."
    except Exception as e:
        return f"Error logging chat session: {str(e)}"

@tool
def get_system_status() -> str:
    """Get overall system status and statistics"""
    try:
        # Count customers by domain
        query = "SELECT domain, COUNT(*) as count FROM customers GROUP BY domain"
        result = db.execute_query(query)
        
        status_info = ["System Status: Online"]
        
        if not result.empty:
            for _, row in result.iterrows():
                status_info.append(f"{row['domain'].title()}: {row['count']} customers")
        
        return " | ".join(status_info)
    except Exception as e:
        return f"System status check failed: {str(e)}"

@tool
def validate_user_input(input_data: str, expected_format: str) -> str:
    """Validate user input against expected format"""
    try:
        if expected_format == "email":
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_pattern, input_data):
                return "Valid email format"
            else:
                return "Invalid email format"
        
        elif expected_format == "phone":
            # Simple phone validation
            cleaned = re.sub(r'[^\d]', '', input_data)
            if len(cleaned) >= 10:
                return "Valid phone format"
            else:
                return "Invalid phone format"
        
        elif expected_format == "order_id":
            if input_data.startswith("ORD") and len(input_data) >= 6:
                return "Valid order ID format"
            else:
                return "Invalid order ID format (should start with 'ORD')"
        
        else:
            return "Unknown validation format"
            
    except Exception as e:
        return f"Validation error: {str(e)}"

@tool
def get_business_hours() -> str:
    """Get current business hours and availability"""
    try:
        current_time = datetime.now()
        hour = current_time.hour
        day = current_time.weekday()  # 0 = Monday, 6 = Sunday
        
        # Business hours: Monday-Friday 9 AM - 6 PM
        if day < 5:  # Weekday
            if 9 <= hour < 18:
                return "We are currently open! Business hours: Monday-Friday 9 AM - 6 PM EST"
            else:
                return "We are currently closed. Business hours: Monday-Friday 9 AM - 6 PM EST. AI support is available 24/7."
        else:  # Weekend
            return "We are closed on weekends. Business hours: Monday-Friday 9 AM - 6 PM EST. AI support is available 24/7."
    
    except Exception as e:
        return f"Error checking business hours: {str(e)}"

@tool
def escalate_to_human(issue_description: str, customer_id: str, priority: str = "normal") -> str:
    """Escalate issue to human agent"""
    try:
        # In a real system, this would create a ticket in your support system
        escalation_id = f"ESC_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Log escalation (you could add an escalations table)
        escalation_info = {
            "escalation_id": escalation_id,
            "customer_id": customer_id,
            "issue": issue_description,
            "priority": priority,
            "created_at": datetime.now().isoformat()
        }
        
        return f"Your issue has been escalated to a human agent. Escalation ID: {escalation_id}. Priority: {priority}. You will be contacted within 2-4 hours during business hours."
    
    except Exception as e:
        return f"Error escalating to human agent: {str(e)}"