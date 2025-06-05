from crewai import Agent, Task, Crew
from config.llm_config import llm
from tools.common_tools import get_customer_info, search_general_knowledge, get_system_status, validate_user_input

class RouterCrew:
    def __init__(self):
        self.tools = [get_customer_info, search_general_knowledge, get_system_status, validate_user_input]
        self.setup_agents()
    
    def setup_agents(self):
        llm_config = llm.get_llm_config()
        
        self.domain_classifier = Agent(
            role="Domain Classification Specialist",
            goal="Analyze customer queries and determine the most appropriate domain",
            backstory="You are an expert at understanding customer inquiries and routing them to the right department.",
            tools=self.tools,
            llm=llm_config["model"], 
            verbose=True,
            allow_delegation=False
        )
        
        self.intent_analyzer = Agent(
            role="Customer Intent Analyzer", 
            goal="Understand the customer's specific intent and gather additional context",
            backstory="You are skilled at reading between the lines of customer messages.",
            tools=self.tools,
            llm=llm_config["model"], 
            verbose=True,
            allow_delegation=False
        )
    

    
    def classify_domain(self, user_query, user_info=None):
        """Classify the domain for a user query"""
        
        task = Task(
            description=f"""
            Analyze the following customer query and determine which domain it belongs to:
            
            Customer Query: "{user_query}"
            Customer Info: {user_info if user_info else "Not provided"}
            
            Available domains:
            1. ECOMMERCE - Orders, shipping, returns, products, refunds, tracking, shopping
            2. BANKING - Account balance, transactions, payments, cards, loans, transfers
            3. TELECOM - Phone bills, data usage, network issues, plan changes, roaming
            
            Your task:
            1. Analyze the query content and keywords
            2. Look for domain-specific indicators
            3. Consider the customer information if available
            4. Return ONLY the domain name: "ecommerce", "banking", or "telecom"
            5. If unclear, make the best educated guess based on keywords
            
            Examples:
            - "Where is my order?" → ecommerce
            - "Check my account balance" → banking  
            - "My internet is slow" → telecom
            - "Return a product" → ecommerce
            - "Transfer money" → banking
            - "Data usage" → telecom
            
            Response format: Just return the domain name in lowercase.
            """,
            agent=self.domain_classifier,
            expected_output="The domain name (ecommerce, banking, or telecom) that best matches the customer query"
        )
        
        crew = Crew(
            agents=[self.domain_classifier, self.intent_analyzer],
            tasks=[task],
            verbose=True
        )
        
    
        result = crew.kickoff()
        
        # Extract domain from result (clean up the response)
        domain_result = str(result).lower().strip()
        
        # Ensure we return a valid domain
        valid_domains = ["ecommerce", "banking", "telecom"]
        for domain in valid_domains:
            if domain in domain_result:
                return domain
        
        # Default fallback
        return "ecommerce"
    
    def analyze_intent(self, user_query, user_info=None):
        """Analyze customer intent and urgency"""
        
        task = Task(
            description=f"""
            Analyze the customer's intent and provide context for better service:
            
            Customer Query: "{user_query}"
            Customer Info: {user_info if user_info else "Not provided"}
            
            Analyze and provide:
            1. Primary intent (what does the customer want?)
            2. Urgency level (low, medium, high)
            3. Emotional tone (frustrated, neutral, happy, confused)
            4. Key information needed (what info might the agent need?)
            5. Suggested approach (how should the agent handle this?)
            
            Consider:
            - Keywords indicating urgency (urgent, emergency, asap, immediately)
            - Emotional indicators (angry, frustrated, pleased, confused)
            - Complexity of the request
            - Time sensitivity
            
            Provide a brief, structured analysis that will help the domain agent provide better service.
            """,
            agent=self.intent_analyzer,
            expected_output="A structured analysis of customer intent, urgency, tone, and recommended approach"
        )
        
        crew = Crew(
        agents=[self.domain_classifier, self.intent_analyzer],
        tasks=[task],
        verbose=True
      )
        
        result = crew.kickoff()
        return str(result)
    
    def route_customer(self, user_query, user_info=None):
        """Complete routing analysis - domain + intent"""
        
        # Get domain classification
        domain = self.classify_domain(user_query, user_info)
        
        # Get intent analysis
        intent_analysis = self.analyze_intent(user_query, user_info)
        
        return {
            "domain": domain,
            "intent_analysis": intent_analysis,
            "confidence": "high",  # You could implement confidence scoring
            "routing_reason": f"Query classified as {domain} based on content analysis"
        }
    
    def get_domain_from_query(self, user_query, user_info=None):
        """Simple method to get just the domain (used by main app)"""
        return self.classify_domain(user_query, user_info)

# Example usage and testing
if __name__ == "__main__":
    router = RouterCrew()
    
    # Test queries
    test_queries = [
        "Where is my order ORD123?",
        "What's my account balance?", 
        "My phone bill is too high",
        "I want to return this product",
        "Transfer $100 to my savings",
        "My internet connection is slow"
    ]
    
    for query in test_queries:
        domain = router.get_domain_from_query(query)
        print(f"Query: '{query}' → Domain: {domain}")