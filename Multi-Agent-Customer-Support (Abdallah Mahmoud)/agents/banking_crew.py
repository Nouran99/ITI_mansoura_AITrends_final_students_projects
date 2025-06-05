from crewai import Agent, Task, Crew
from config.llm_config import llm
from tools.banking_tools import get_account_balance, get_recent_transactions, search_banking_knowledge, check_account_status

class BankingCrew:
    def __init__(self):
        self.tools = [get_account_balance, get_recent_transactions, search_banking_knowledge, check_account_status]
        self.setup_agents()
    
    def setup_agents(self):
        llm_config = llm.get_llm_config()
        
        self.account_specialist = Agent(
            role="Banking Account Specialist",
            goal="Assist customers with account inquiries, balance checks, and account management",
            backstory="You are a professional banking specialist with expertise in account services, transactions, and banking policies.",
            tools=self.tools,
            llm=llm_config["model"],  
            verbose=True
        )
        
        self.transaction_analyst = Agent(
            role="Transaction Analyst",
            goal="Help customers understand their transactions, investigate discrepancies, and provide transaction history",
            backstory="You are a detail-oriented transaction analyst with extensive knowledge of banking operations and transaction processing.",
            tools=self.tools,
            llm=llm_config["model"],  
            verbose=True
        )

    
    def handle_query(self, user_query, customer_info):
        task = Task(
            description=f"""
            Customer Information: {customer_info}
            Customer Query: {user_query}
            
            Please assist this banking customer with their inquiry. Use the available tools to:
            1. Access account information securely
            2. Provide accurate financial data
            3. Explain banking policies and procedures
            4. Ensure customer satisfaction and security
            
            Maintain the highest standards of security and professionalism.
            """,
            agent=self.determine_best_agent(user_query),
            expected_output="A secure and informative response to the customer's banking inquiry"
        )
        
        crew = Crew(
        agents=[self.account_specialist, self.transaction_analyst],
        tasks=[task],
        verbose=True
        )
    
        
        result = crew.kickoff()
        return result
    
    def determine_best_agent(self, query):
        """Determine which agent should handle the query"""
        transaction_keywords = ['transaction', 'transfer', 'payment', 'history', 'charge']
        
        if any(keyword in query.lower() for keyword in transaction_keywords):
            return self.transaction_analyst
        else:
            return self.account_specialist