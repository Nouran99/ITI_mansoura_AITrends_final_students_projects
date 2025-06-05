import streamlit as st
from config.settings import DOMAINS, USER_INFO_FIELDS

def render_header():
    """Render the main header"""
    st.markdown("""
    <div class="header-container">
        <h1>🤖 AI Customer Support System</h1>
        <p>Multi-Agent Customer Support powered by DeepSeek & CrewAI</p>
    </div>
    """, unsafe_allow_html=True)

def render_domain_selection():
    """Render domain selection cards"""
    st.markdown("### Choose Your Support Domain")
    
    cols = st.columns(3)
    
    for idx, (domain_key, domain_info) in enumerate(DOMAINS.items()):
        with cols[idx]:
            st.markdown(f"""
            <div class="domain-card" style="--card-color: {domain_info['color']}">
                <span class="domain-icon">{domain_info['icon']}</span>
                <div class="domain-title">{domain_info['name']}</div>
                <div class="domain-description">{domain_info['description']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Select {domain_info['name']}", key=f"btn_{domain_key}", use_container_width=True):
                st.session_state.selected_domain = domain_key
                st.session_state.user_info_collected = False
                st.rerun()

def render_user_info_form(domain):
    """Render user information collection form"""
    domain_info = DOMAINS[domain]
    required_fields = USER_INFO_FIELDS[domain]
    
    st.markdown(f"""
    <div class="user-info-form" style="--primary-color: {domain_info['color']}">
        <h3>{domain_info['icon']} {domain_info['name']} Support</h3>
        <p>Please provide the following information to get personalized assistance:</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form(f"{domain}_user_info"):
        user_info = {}
        
        for field in required_fields:
            if field == "name":
                user_info[field] = st.text_input("Full Name *", placeholder="Enter your full name")
            elif field == "email":
                user_info[field] = st.text_input("Email Address *", placeholder="Enter your email")
            elif field == "phone":
                user_info[field] = st.text_input("Phone Number *", placeholder="Enter your phone number")
            elif field == "order_id":
                user_info[field] = st.text_input("Order ID *", placeholder="Enter your order ID (e.g., ORD001)")
            elif field == "account_number":
                user_info[field] = st.text_input("Account Number *", placeholder="Enter your account number")
            elif field == "phone_number":
                user_info[field] = st.text_input("Phone Number *", placeholder="Enter your phone number")
            elif field == "account_id":
                user_info[field] = st.text_input("Account ID *", placeholder="Enter your account ID")
        
        submitted = st.form_submit_button("Start Chat", use_container_width=True)
        
        if submitted:
            # Validate required fields
            missing_fields = [field for field, value in user_info.items() if not value.strip()]
            
            if missing_fields:
                st.error(f"Please fill in all required fields: {', '.join(missing_fields)}")
            else:
                st.session_state.user_info = user_info
                st.session_state.user_info_collected = True
                st.session_state.chat_messages = []
                st.success("Information collected! You can now start chatting.")
                st.rerun()

def render_chat_interface(domain):
    """Render the chat interface"""
    domain_info = DOMAINS[domain]
    
    st.markdown(f"""
    <div class="chat-container">
        <h3>{domain_info['icon']} {domain_info['name']} Support Chat</h3>
        <p>Hello {st.session_state.user_info.get('name', 'Customer')}! How can I help you today?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input - FIXED VERSION
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat FIRST
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Get response from agent
                response = get_agent_response(domain, prompt, st.session_state.user_info)
                
                # Display response
                st.markdown(response)
                
                # Add assistant response to chat history ONLY ONCE
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
        
        # Force rerun to update chat display
        st.rerun()

def render_sidebar():
    """Enhanced sidebar with accurate test data matching the database"""
    with st.sidebar:
        st.markdown("### 📊 System Statistics")
        
        try:
            from config.llm_config import llm
            usage_stats = llm.get_usage_stats()
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="stats-card">
                    <span class="stats-number">{usage_stats['tokens_used']:,}</span>
                    <div class="stats-label">Tokens Used</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stats-card">
                    <span class="stats-number">{usage_stats['usage_percentage']:.1f}%</span>
                    <div class="stats-label">Daily Usage</div>
                </div>
                """, unsafe_allow_html=True)
            
            usage_percentage = usage_stats.get('usage_percentage', 0)
            if usage_percentage > 0:
                st.progress(usage_percentage / 100)
                st.caption(f"Usage: {usage_percentage:.1f}%")
        except Exception as e:
            st.warning("LLM stats unavailable")
        
        # ACCURATE TEST DATA SECTION
        st.markdown("---")
        st.markdown("### 🧪 Test Data Available")
        st.info("💡 Use this exact sample data from the database!")
        
        domain_data = {
            "🛒 E-commerce": {
                "customers": [
                    {
                        "name": "John Smith",
                        "email": "john.smith@email.com",
                        "phone": "555-0101",
                        "customer_id": "CUST001",
                        "orders": [
                            {"id": "ORD001", "product": "Wireless Headphones", "status": "🚚 shipped", "amount": "$99.99", "tracking": "TRK001"},
                            {"id": "ORD002", "product": "USB-C Cable", "status": "✅ delivered", "amount": "$19.99", "tracking": "TRK002"}
                        ]
                    },
                    {
                        "name": "Alice Brown",
                        "email": "alice.brown@email.com", 
                        "phone": "555-0104",
                        "customer_id": "CUST004",
                        "orders": [
                            {"id": "ORD003", "product": "Laptop Stand", "status": "⏳ processing", "amount": "$49.99", "tracking": "None"},
                            {"id": "ORD004", "product": "Bluetooth Speaker", "status": "🚚 shipped", "amount": "$79.99", "tracking": "TRK003"}
                        ]
                    }
                ],
                "available_products": [
                    "Wireless Headphones ($99.99)",
                    "Laptop Stand ($49.99)", 
                    "USB-C Cable ($19.99)",
                    "Bluetooth Speaker ($79.99)",
                    "Phone Case ($24.99)"
                ],
                "sample_questions": [
                    "Where is my order ORD001?",
                    "Track shipment TRK001",
                    "What's the status of order ORD003?",
                    "I want to return my headphones",
                    "When will my laptop stand arrive?"
                ]
            },
            "🏦 Banking": {
                "customers": [
                    {
                        "name": "Jane Johnson",
                        "email": "jane.johnson@email.com",
                        "phone": "555-0102", 
                        "customer_id": "CUST002",
                        "accounts": [
                            {"number": "ACC001", "type": "Checking", "balance": "$2,500.75", "status": "✅ active"},
                            {"number": "ACC003", "type": "Savings", "balance": "$5,750.25", "status": "✅ active"}
                        ],
                        "recent_transactions": [
                            "TXN001: -$45.00 (Grocery Store)",
                            "TXN002: +$1,200.00 (Salary)",
                            "TXN003: -$89.99 (Online Purchase)"
                        ]
                    },
                    {
                        "name": "Charlie Davis",
                        "email": "charlie.davis@email.com",
                        "phone": "555-0105",
                        "customer_id": "CUST005", 
                        "accounts": [
                            {"number": "ACC002", "type": "Savings", "balance": "$15,000.00", "status": "✅ active"}
                        ],
                        "recent_transactions": [
                            "TXN004: +$500.00 (Transfer from Checking)",
                            "TXN005: -$25.00 (ATM Withdrawal)"
                        ]
                    }
                ],
                "sample_questions": [
                    "What's my balance for account ACC001?",
                    "Show recent transactions for ACC001",
                    "I see a charge for $89.99, what was it?",
                    "Transfer money between accounts",
                    "Why was I charged $25 ATM fee?"
                ]
            },
            "📱 Telecom": {
                "customers": [
                    {
                        "name": "Bob Wilson",
                        "email": "bob.wilson@email.com",
                        "phone": "555-0103",
                        "customer_id": "CUST003",
                        "lines": [
                            {
                                "number": "555-0103", 
                                "plan": "Unlimited Plan", 
                                "charge": "$89.99/month", 
                                "usage": "45.2 GB used", 
                                "status": "✅ active",
                                "last_payment": "2024-01-15"
                            },
                            {
                                "number": "555-0106",
                                "plan": "Basic Plan",
                                "charge": "$39.99/month", 
                                "usage": "12.1 GB used",
                                "status": "✅ active", 
                                "last_payment": "2024-01-10"
                            }
                        ]
                    }
                ],
                "available_plans": [
                    "Unlimited Plan ($89.99/month)",
                    "Basic Plan ($39.99/month)",
                    "Family Plan (starting at $129.99)",
                    "Business Plan (starting at $79.99)"
                ],
                "sample_questions": [
                    "How much data have I used on 555-0103?",
                    "My internet is very slow today",
                    "I want to upgrade from Basic to Unlimited",
                    "When is my next payment due?",
                    "Why is my bill $89.99 this month?"
                ]
            }
        }
        
        for domain_name, domain_info in domain_data.items():
            with st.expander(domain_name, expanded=False):
                # Show customers with their specific data
                for i, customer in enumerate(domain_info['customers']):
                    if i > 0:
                        st.markdown("---")
                    
                    st.markdown(f"**👤 {customer['name']}**")
                    st.markdown(f"📧 `{customer['email']}`")
                    st.markdown(f"📞 `{customer['phone']}`")
                    st.markdown(f"🆔 `{customer['customer_id']}`")
                    
                    # Domain-specific data
                    if domain_name == "🛒 E-commerce":
                        st.markdown("**📦 Orders:**")
                        for order in customer['orders']:
                            st.markdown(f"• `{order['id']}` - {order['product']}")
                            st.markdown(f"  {order['status']} | {order['amount']} | Track: {order['tracking']}")
                    
                    elif domain_name == "🏦 Banking":
                        st.markdown("**💳 Accounts:**")
                        for account in customer['accounts']:
                            st.markdown(f"• `{account['number']}` ({account['type']})")
                            st.markdown(f"  {account['balance']} | {account['status']}")
                        
                        st.markdown("**💸 Recent Transactions:**")
                        for transaction in customer['recent_transactions']:
                            st.markdown(f"• {transaction}")
                    
                    elif domain_name == "📱 Telecom":
                        st.markdown("**📱 Lines:**")
                        for line in customer['lines']:
                            st.markdown(f"• `{line['number']}` ({line['plan']})")
                            st.markdown(f"  {line['charge']} | {line['usage']} | {line['status']}")
                            st.markdown(f"  Last payment: {line['last_payment']}")
                
                # Show additional reference data
                if 'available_products' in domain_info:
                    st.markdown("**🛍️ Available Products:**")
                    for product in domain_info['available_products'][:3]:
                        st.markdown(f"• {product}")
                
                if 'available_plans' in domain_info:
                    st.markdown("**📋 Available Plans:**")
                    for plan in domain_info['available_plans'][:3]:
                        st.markdown(f"• {plan}")
                
                # Show sample questions
                st.markdown("**💬 Try asking:**")
                for question in domain_info['sample_questions'][:3]:
                    st.markdown(f"• *{question}*")
                    
        st.markdown("---")
        
        # Quick reference section
        # with st.expander("🔧 Quick Reference", expanded=False):
        #     st.markdown("""
        #     **Test Scenarios:**
            
        #     **✅ Working Orders:**
        #     • ORD001 (shipped) - John Smith
        #     • ORD002 (delivered) - John Smith
        #     • ORD004 (shipped) - Alice Brown
            
        #     **⏳ Processing:**
        #     • ORD003 (processing) - Alice Brown
            
        #     **💰 Active Accounts:**
        #     • ACC001 ($2,500.75) - Jane Johnson
        #     • ACC002 ($15,000.00) - Charlie Davis
        #     • ACC003 ($5,750.25) - Jane Johnson
            
        #     **📱 Active Lines:**
        #     • 555-0103 (Unlimited, 45.2GB) - Bob Wilson
        #     • 555-0106 (Basic, 12.1GB) - Bob Wilson
            
        #     **🎯 Test Tips:**
        #     • Use exact IDs from above
        #     • Try cross-domain questions
        #     • Test error scenarios with fake IDs
        #     """)
        
        # st.markdown("---")
        
        if st.button("🔄 Reset Chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()
        
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.selected_domain = None
            st.session_state.user_info_collected = False
            st.session_state.chat_messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🎯 Current Session")
        if "selected_domain" in st.session_state and st.session_state.selected_domain:
            domain_info = DOMAINS[st.session_state.selected_domain]
            st.markdown(f"**Domain:** {domain_info['icon']} {domain_info['name']}")
            
            if "user_info" in st.session_state:
                st.markdown("**Customer:** " + st.session_state.user_info.get('name', 'Unknown'))

def get_agent_response(domain, user_query, user_info):
    """Get response from appropriate domain crew with intelligent routing"""
    try:
        # Use router for initial classification if needed
        from agents.router_crew import RouterCrew
        router = RouterCrew()
        
        # Get routing analysis
        routing_info = router.route_customer(user_query, user_info)
        recommended_domain = routing_info['domain']
        
        # Use recommended domain or stick with user-selected domain
        final_domain = domain  # Use user's choice, but you could use recommended_domain
        
        # Get response from appropriate domain crew
        if final_domain == "ecommerce":
            from agents.ecommerce_crew import EcommerceCrew
            crew = EcommerceCrew()
        elif final_domain == "banking":
            from agents.banking_crew import BankingCrew
            crew = BankingCrew()
        elif final_domain == "telecom":
            from agents.telecom_crew import TelecomCrew
            crew = TelecomCrew()
        else:
            return "Invalid domain selected."
        
        # Add routing context to the query
        enhanced_context = f"Customer Query: {user_query}\nRouting Analysis: {routing_info['intent_analysis']}"
        
        result = crew.handle_query(enhanced_context, user_info)
        return str(result)
    
    except Exception as e:
        return f"I apologize, but I encountered an error while processing your request: {str(e)}. Please try again or contact support."