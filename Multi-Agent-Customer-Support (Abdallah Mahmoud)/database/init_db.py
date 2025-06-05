from database.sql_manager import db
from database.vector_manager import vector_db
from database.sample_data import populate_sample_data
import os

def initialize_system():
    """Initialize the entire database system"""
    print("🚀 Initializing Customer Support System...")
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/knowledge_base", exist_ok=True)
    
    # Initialize SQL database
    print("📊 Setting up SQL database...")
    db.init_database()
    
    # Initialize vector database
    print("🧠 Setting up vector database...")
    vector_db.init_collections()
    
    # Populate with sample data
    print("🌱 Populating sample data...")
    populate_sample_data()
    
    print("✅ System initialization complete!")

if __name__ == "__main__":
    initialize_system()