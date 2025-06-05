import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your-openrouter-api-key")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-api-key")

# Database Configuration
DATABASE_PATH = "data/customer_support.db"
VECTOR_DB_PATH = "data/knowledge_base"

# UI Configuration
PAGE_TITLE = "AI Customer Support System"
PAGE_ICON = "🤖"

# Domain Configuration
DOMAINS = {
    "ecommerce": {
        "name": "E-commerce",
        "icon": "🛒",
        "color": "#FF6B6B",
        "description": "Order tracking, returns, product inquiries"
    },
    "banking": {
        "name": "Banking",
        "icon": "🏦",
        "color": "#4ECDC4", 
        "description": "Account balance, transactions, card services"
    },
    "telecom": {
        "name": "Telecom",
        "icon": "📱",
        "color": "#45B7D1",
        "description": "Billing, network issues, plan changes"
    }
}

# Required User Information
USER_INFO_FIELDS = {
    "ecommerce": ["name", "email", "order_id"],
    "banking": ["name", "account_number", "phone"],
    "telecom": ["name", "phone_number", "account_id"]
}