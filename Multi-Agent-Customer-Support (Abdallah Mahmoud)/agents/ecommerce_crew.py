from crewai import Agent, Task, Crew
from config.llm_config import llm
from tools.ecommerce_tools import get_order_status, get_customer_orders, search_ecommerce_knowledge, check_product_availability

class EcommerceCrew:
    def __init__(self):
        self.tools = [get_order_status, get_customer_orders, search_ecommerce_knowledge, check_product_availability]
        self.setup_agents()
    
    def setup_agents(self):

        llm_config = llm.get_llm_config()
        
        self.order_specialist = Agent(
            role="Order Management Specialist",
            goal="Help customers with order tracking, status updates, and order-related inquiries",
            backstory="You are an experienced e-commerce order specialist with deep knowledge of order processing, shipping, and tracking systems.",
            tools=self.tools,
            llm=llm_config["model"],  
            verbose=True
        )
        
        self.customer_service = Agent(
            role="E-commerce Customer Service Representative",
            goal="Provide comprehensive customer support for e-commerce inquiries including returns, policies, and general questions",
            backstory="You are a friendly and knowledgeable customer service representative specializing in e-commerce support.",
            tools=self.tools,
            llm=llm_config["model"],  
            verbose=True
        )
    
    def handle_query(self, user_query, customer_info):
        task = Task(
            description=f"""
            Customer Information: {customer_info}
            Customer Query: {user_query}
            
            Please help this customer with their e-commerce inquiry. Use the available tools to:
            1. Look up relevant information (orders, products, policies)
            2. Provide accurate and helpful responses
            3. Offer additional assistance if needed
            
            Be friendly, professional, and thorough in your response.
            """,
            agent=self.determine_best_agent(user_query),
            expected_output="A helpful and comprehensive response to the customer's e-commerce inquiry"
        )
        
        crew = Crew(
            agents=[self.order_specialist, self.customer_service],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    def determine_best_agent(self, query):
        """Determine which agent should handle the query"""
        order_keywords = ['order', 'tracking', 'shipment', 'delivery', 'status']
        
        if any(keyword in query.lower() for keyword in order_keywords):
            return self.order_specialist
        else:
            return self.customer_service