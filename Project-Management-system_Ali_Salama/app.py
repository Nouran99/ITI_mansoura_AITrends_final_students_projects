import sys
try:
    import pysqlite3.dbapi2 as sqlite3
    sys.modules['sqlite3'] = sqlite3
except ImportError:
    pass

import streamlit as st
import os
from dotenv import load_dotenv
from crew_local import AgileProjectCrew
from utils.html_pdf_generator import html_file_generator
import time
import base64

# Fix encoding issue
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    # Alternative approach for encoding
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        pass

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Project Planner",
    page_icon="📋",
    layout="wide"
)

# Enhanced Custom CSS for Streamlit Light Mode
from pathlib import Path
def load_css(file_name):
    """Load CSS from external file"""
    css_file = Path(__file__).parent / "utils" / file_name
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
load_css("main_styles.css")

# Initialize session state
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'crew_result' not in st.session_state:
    st.session_state.crew_result = None

# Header
st.markdown('<div class="main-header"> <h1>Project Management system</h1></div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">📝 Tell us about your project</h2>', unsafe_allow_html=True)

with st.form("project_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        project_name = st.text_input("Project Name *", placeholder="e.g., Social Reading App")
        problem_statement = st.text_area(
            "What problem does your product solve? *",
            placeholder="e.g., Readers want to connect with others who share similar interests...",
            height=100
        )
        target_users = st.text_area(
            "Who are your target users? *",
            placeholder="e.g., Book enthusiasts, students, book clubs...",
            height=100
        )
        
    with col2:
        budget = st.select_slider(
            "Budget Range",
            options=["< $10k", "$10k-$50k", "$50k-$100k", "$100k-$500k", "> $500k"]
        )
        timeline = st.select_slider(
            "Timeline",
            options=["1 month", "3 months", "6 months", "9 months", "12+ months"]
        )
        platform = st.multiselect(
            "Platform Preferences",
            ["Web", "iOS", "Android", "Desktop", "API Only"]
        )
    
    st.markdown("### 🎯 Features & Requirements")
    
    col3, col4 = st.columns(2)
    
    with col3:
        must_have_features = st.text_area(
            "Must-have Features (one per line) *",
            placeholder="User registration\nContent creation\nSearch functionality\nUser profiles",
            height=150
        )
        
    with col4:
        nice_to_have_features = st.text_area(
            "Nice-to-have Features (one per line)",
            placeholder="Advanced analytics\nAI recommendations\nSocial sharing",
            height=150
        )
    
    constraints = st.text_area(
        "Technical or Business Constraints",
        placeholder="e.g., Must integrate with existing CRM, GDPR compliance required, Must support 10k concurrent users",
        height=100
    )
    
    additional_info = st.text_area(
        "Additional Information",
        placeholder="Any other details that might be helpful...",
        height=100
    )
    
    submit_button = st.form_submit_button("🚀Generate Plan", use_container_width=True)

if submit_button and not st.session_state.processing:
    if project_name and problem_statement and target_users and must_have_features:
        st.session_state.processing = True
        
        # Prepare project description
        project_description = f"""
        Project Name: {project_name}
        
        Problem Statement: {problem_statement}
        
        Target Users: {target_users}
        
        Budget: {budget}
        Timeline: {timeline}
        Platforms: {', '.join(platform) if platform else 'Not specified'}
        
        Must-Have Features:
        {must_have_features}
        
        Nice-to-Have Features:
        {nice_to_have_features or 'None specified'}
        
        Constraints: {constraints or 'None specified'}
        
        Additional Information: {additional_info or 'None provided'}
        """
        
        # Progress tracking
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        with st.spinner("AI Agents are working on your project plan..."):
            # Simulate agent progress
            agent_stages = [
                ("🧏 Customer Listener Agent", "Analyzing your requirements...", 10),
                ("🧾 Requirement Extractor Agent", "Structuring requirements...", 20),
                ("🧠 Planning Agent", "Creating sprint plan...", 35),
                ("✍️ Story Generator Agent", "Writing user stories...", 50),
                ("🧑‍💻 Technology Advisor Agent", "Recommending tech stack...", 65),
                ("📋 Team Mapper Agent", "Defining team structure...", 80),
                ("📦 Plan Packager Agent", "Finalizing project plan...", 95)
            ]
            
            for agent, status, progress in agent_stages:
                progress_placeholder.progress(progress / 100)
                status_placeholder.info(f"{agent}: {status}")
                time.sleep(1)  # Simulate processing time
            
            try:
                # Run the crew
                crew = AgileProjectCrew()
                result = crew.run(project_description)
                
                # Store the raw result for HTML/PDF generation
                st.session_state.crew_result = result
                
                
                progress_placeholder.progress(1.0)
                status_placeholder.success("✅ Project plan generated successfully!")
                time.sleep(1)
                
            except Exception as e:
                st.error(f"Error generating project plan: {str(e)}")
                status_placeholder.error("❌ Failed to generate project plan")
                st.session_state.processing = False
            
        st.session_state.processing = False
        st.rerun()
    else:
        st.error("⚠️ Please fill in all required fields marked with *")

# # Display project data if available
if st.session_state.crew_result:
    # Export Options
    st.markdown('<h2 class="section-header">📥 Export & Download Options</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 HTML Report")
        col1_1, col1_2 = st.columns(2)
        
        with col1_1:
            if st.button("🌐 Generate HTML", use_container_width=True):
                try:
                    with st.spinner("Generating HTML..."):
                        html_file_path = html_file_generator(st.session_state.crew_result)
                        
                        # Read the generated HTML file
                        with open(html_file_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        # Store in session state for download
                        st.session_state.html_content = html_content
                        st.success("✅ HTML generated!")
                        
                except Exception as e:
                    st.error(f"Error generating HTML: {str(e)}")
        
        with col1_2:
            if 'html_content' in st.session_state:
                st.download_button(
                    label="⬇️ Download",
                    data=st.session_state.html_content,
                    file_name=f"{project_name.replace(' ', '_')}_project_plan.html",
                    mime="text/html",
                    use_container_width=True
                )
        
        # Option to open HTML in new tab
        if 'html_content' in st.session_state:
            html_bytes = st.session_state.html_content.encode()
            b64 = base64.b64encode(html_bytes).decode()
            data_url = f'data:text/html;base64,{b64}'
            
            # Using Streamlit's link_button 
            if hasattr(st, 'link_button'):
                st.link_button("🔗 Open HTML in Browser", data_url)
            else:
                # Fallback for older Streamlit versions
                st.markdown(f'[🔗 Open HTML in Browser]({data_url})', unsafe_allow_html=True)
    
    # Uncomment the following section if you want to enable PDF generation
    # with col2:
    #     st.markdown("###  PDF Report")
    #     col2_1, col2_2 = st.columns(2)
        
    #     with col2_1:
    #         if st.button(" Generate PDF", use_container_width=True):
    #             try:
    #                 with st.spinner("Generating PDF..."):
    #                     pdf_file_path = pdf_file_generator(st.session_state.crew_result)
                        
    #                     # Read the generated PDF file
    #                     with open(pdf_file_path, 'rb') as f:
    #                         pdf_content = f.read()
                        
    #                     # Store in session state for download
    #                     st.session_state.pdf_content = pdf_content
    #                     st.success("✅ PDF generated!")
                        
    #             except Exception as e:
    #                 st.error(f"Error generating PDF: {str(e)}")
    #                 st.info("💡 Make sure wkhtmltopdf is installed")
        
    #     with col2_2:
    #         if 'pdf_content' in st.session_state:
    #             st.download_button(
    #                 label="⬇️ Download",
    #                 data=st.session_state.pdf_content,
    #                 file_name=f"{project_name.replace(' ', '_')}_project_plan.pdf",
    #                 mime="application/pdf",
    #                 use_container_width=True
    #             )
    
    
# Footer
st.markdown("---")