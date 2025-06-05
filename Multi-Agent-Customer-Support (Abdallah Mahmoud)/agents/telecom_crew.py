from crewai import Agent, Task, Crew
from config.llm_config import llm
from tools.telecom_tools import get_telecom_account_info, get_data_usage, search_telecom_knowledge, check_network_status

class TelecomCrew:
    def __init__(self):
        self.tools = [get_telecom_account_info, get_data_usage, search_telecom_knowledge, check_network_status]
        self.setup_agents()
    
    def setup_agents(self):
        llm_config = llm.get_llm_config()
        
        self.technical_support = Agent(
            role="Telecom Technical Support Specialist",
            goal="Provide technical assistance for network issues, connectivity problems, and device troubleshooting",
            backstory="You are a skilled technical support specialist with deep knowledge of telecommunications networks and mobile technologies.",
            tools=self.tools,
            llm=llm_config["model"],  
            verbose=True
        )
        
        self.billing_specialist = Agent(
            role="Telecom Billing Specialist",
            goal="Handle billing inquiries, plan changes, usage questions, and account management",
            backstory="You are an experienced billing specialist who helps customers understand their telecom services, usage, and billing.",
            tools=self.tools,
            llm=llm_config["model"],  
            verbose=True
        )
    


    def handle_query(self, user_query, customer_info):
        task = Task(
            description=f"""
            Customer Information: {customer_info}
            Customer Query: {user_query}
            
            Please help this telecom customer with their inquiry. Use the available tools to:
            1. Check account and service status
            2. Diagnose technical issues
            3. Provide billing and usage information
            4. Offer solutions and next steps
            
            Be technical when needed but explain things clearly for the customer.
            """,
            agent=self.determine_best_agent(user_query),
            expected_output="A helpful technical or billing response to the customer's telecom inquiry"
        )
        
        crew = Crew(
        agents=[self.technical_support, self.billing_specialist],
        tasks=[task],
        verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    def determine_best_agent(self, query):
        """Determine which agent should handle the query"""
        technical_keywords = ['network', 'signal', 'connection', 'outage', 'technical', 'slow']
        
        if any(keyword in query.lower() for keyword in technical_keywords):
            return self.technical_support
        else:
            return self.billing_specialist