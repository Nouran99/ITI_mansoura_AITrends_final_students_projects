import streamlit as st
import os
from config.settings import PAGE_TITLE, PAGE_ICON, DOMAINS
from ui.styles import get_custom_css
from ui.components import (
    render_header, 
    render_domain_selection, 
    render_user_info_form,
    render_chat_interface,
    render_sidebar
)

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state
if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = None

if "user_info_collected" not in st.session_state:
    st.session_state.user_info_collected = False

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "user_info" not in st.session_state:
    st.session_state.user_info = {}

def main():
    """Main application logic"""
    
    # Initialize database on first run
    if not os.path.exists("data/customer_support.db"):
        with st.spinner("🚀 Setting up system for first time..."):
            from database.init_db import initialize_system
            initialize_system()
        st.success("✅ System initialized successfully!")
        st.rerun()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    render_header()
    
    # Navigation logic
    if not st.session_state.selected_domain:
        # Show domain selection
        render_domain_selection()
        
        # Show system info
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 🤖 Powered by AI
            - **DeepSeek LLM** for intelligent responses
            - **CrewAI** for multi-agent coordination
            - **Real-time** data integration
            """)
        
        with col2:
            st.markdown("""
            ### 🛠️ Features
            - **Multi-domain** support
            - **Intelligent routing** to specialists
            - **Context-aware** conversations
            """)
        
        with col3:
            st.markdown("""
            ### 🔒 Secure & Reliable
            - **Data privacy** protection
            - **Accurate** information retrieval
            - **Professional** customer service
            """)
    
    elif not st.session_state.user_info_collected:
        # Show user info collection form
        render_user_info_form(st.session_state.selected_domain)
    
    else:
        # Show chat interface
        render_chat_interface(st.session_state.selected_domain)
        
        # Show user info summary in expander
        with st.expander("👤 Customer Information", expanded=False):
            user_info = st.session_state.user_info
            for key, value in user_info.items():
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")

if __name__ == "__main__":
    main()