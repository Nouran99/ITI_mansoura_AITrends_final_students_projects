import chromadb
from chromadb.config import Settings
import json
from config.settings import VECTOR_DB_PATH

class VectorManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
        self.collections = {}
        self.init_collections()
    
    def init_collections(self):
        """Initialize collections for each domain"""
        domains = ["ecommerce", "banking", "telecom"]
        
        for domain in domains:
            try:
                collection = self.client.get_collection(f"{domain}_knowledge")
            except:
                collection = self.client.create_collection(
                    name=f"{domain}_knowledge",
                    metadata={"description": f"Knowledge base for {domain} domain"}
                )
            
            self.collections[domain] = collection
    
    def add_knowledge(self, domain, documents, metadatas, ids):
        """Add knowledge to specific domain collection"""
        if domain in self.collections:
            self.collections[domain].add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
    
    def search_knowledge(self, domain, query, n_results=3):
        """Search knowledge in specific domain"""
        if domain in self.collections:
            results = self.collections[domain].query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        return None
    
    def populate_sample_knowledge(self):
        """Populate with sample knowledge base"""
        
        # E-commerce knowledge
        ecommerce_docs = [
            "To track your order, you need your order ID. Orders typically ship within 1-2 business days.",
            "Our return policy allows returns within 30 days of purchase with original receipt.",
            "Free shipping is available on orders over $50. Standard shipping takes 3-5 business days.",
            "You can cancel your order within 2 hours of placing it if it hasn't been processed yet."
        ]
        
        ecommerce_metadata = [
            {"topic": "order_tracking", "category": "shipping"},
            {"topic": "returns", "category": "policy"},
            {"topic": "shipping", "category": "policy"},
            {"topic": "cancellation", "category": "policy"}
        ]
        
        ecommerce_ids = [f"ecom_{i}" for i in range(len(ecommerce_docs))]
        
        self.add_knowledge("ecommerce", ecommerce_docs, ecommerce_metadata, ecommerce_ids)
        
        # Banking knowledge
        banking_docs = [
            "To check your account balance, provide your account number and we'll verify your identity.",
            "ATM withdrawals are limited to $500 per day for security purposes.",
            "If you suspect fraudulent activity, contact us immediately to freeze your account.",
            "Wire transfers typically take 1-3 business days to complete."
        ]
        
        banking_metadata = [
            {"topic": "balance_inquiry", "category": "account_services"},
            {"topic": "atm_limits", "category": "security"},
            {"topic": "fraud_protection", "category": "security"},
            {"topic": "wire_transfers", "category": "transactions"}
        ]
        
        banking_ids = [f"bank_{i}" for i in range(len(banking_docs))]
        
        self.add_knowledge("banking", banking_docs, banking_metadata, banking_ids)
        
        # Telecom knowledge
        telecom_docs = [
            "Data usage is calculated in real-time. You can check your usage in your account portal.",
            "Network outages are rare but can be checked on our service status page.",
            "Plan changes take effect at the beginning of your next billing cycle.",
            "International roaming charges apply when using your phone outside the country."
        ]
        
        telecom_metadata = [
            {"topic": "data_usage", "category": "billing"},
            {"topic": "network_status", "category": "technical"},
            {"topic": "plan_changes", "category": "account"},
            {"topic": "roaming", "category": "international"}
        ]
        
        telecom_ids = [f"telecom_{i}" for i in range(len(telecom_docs))]
        
        self.add_knowledge("telecom", telecom_docs, telecom_metadata, telecom_ids)

# Global vector database instance
vector_db = VectorManager()