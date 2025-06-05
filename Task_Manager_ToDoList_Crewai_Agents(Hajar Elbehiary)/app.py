import streamlit as st
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from crew import ProductivityCrew  # تم تغيير الاستيراد هنا
# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3']=sys.modules.pop('pysqlite3')

load_dotenv()

def run_scheduling_process(tasks_content):
    """دالة وسيطة لتشغيل ProductivityCrew"""
    crew = ProductivityCrew()
    return crew.run(tasks_content)

def main():
    st.set_page_config(
        page_title="Smart Task Manager",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Smart Task Manager with AI Agents")
    st.subheader("Intelligent task scheduling system with deadline priority using CrewAI")
    
    # Check for API Key
    if not os.getenv("GEMINI_API_KEY"):
        st.error("⚠️ Please add GEMINI_API_KEY to your .env file")
        st.stop()
    
    # Manual task input FIRST (switched order)
    st.sidebar.header("✍️ Manual Input")
    manual_tasks = st.sidebar.text_area(
        "Write your tasks here:",
        placeholder="Example:\n- Finish project report (deadline: today 5pm, 3 hours)\n- Team meeting (deadline: tomorrow 2pm, 1 hour)\n- Buy groceries (deadline: this weekend, 30 min)"
    )
    
    # Sidebar for task input SECOND
    st.sidebar.header("📁 Task Input")
    uploaded_file = st.sidebar.file_uploader("Choose a task file", type=['txt'])
    
    # Sample tasks with deadlines
    if st.sidebar.button("🎯 Use Sample Tasks"):
        manual_tasks = """- Complete quarterly presentation (deadline: today 4pm, 2 hours)
- Client meeting preparation (deadline: tomorrow 9am, 1 hour)
- Review and respond to emails (deadline: today end of day, 30 minutes)
- Gym workout session (deadline: today evening, 45 minutes)
- Read development book chapter (deadline: this week, 1 hour)
- Prepare dinner (deadline: today 7pm, 45 minutes)
- Call family (deadline: today night, 30 minutes)
- Submit expense report (deadline: tomorrow noon, 20 minutes)
- Code review for team project (deadline: today 3pm, 1.5 hours)
- Plan weekend trip (deadline: next week, 45 minutes)"""
    
    # Get task content
    tasks_content = ""
    if uploaded_file:
        tasks_content = uploaded_file.read().decode('utf-8')
    elif manual_tasks:
        tasks_content = manual_tasks
    
    # Display input tasks
    if tasks_content:
        st.header("📋 Input Tasks")
        st.text_area("", tasks_content, height=150, disabled=True)
        
        # Run system button
        if st.button("🚀 Generate Smart Schedule", type="primary"):
            with st.spinner("Analyzing tasks and creating deadline-prioritized schedule... ⏳"):
                try:
                    # Run scheduling process
                    result = run_scheduling_process(tasks_content)
                    
                    # Display results
                    st.success("✅ Schedule created successfully with deadline priority!")
                    
                    # Display schedule
                    st.header("📅 Your Optimized Schedule")
                    st.markdown(result)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Schedule",
                        data=str(result),
                        file_name=f"schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                    
                    # Additional insights
                    with st.expander("📊 Schedule Insights"):
                        st.markdown("""
                        **Key Features of Your Schedule:**
                        - ⏰ Tasks sorted by deadline urgency
                        - 🎯 Deadline-critical tasks scheduled in prime hours
                        - ⚡ Productivity techniques applied
                        - 🛑 Break times included for sustainability
                        - 📢 Deadline reminders and alerts
                        """)
                    
                except Exception as e:
                    st.error(f"❌ Error occurred: {str(e)}")
                    st.info("💡 Make sure your GROQ_API_KEY is valid and you have internet connection")
    
    else:
        st.info("📝 Please upload a task file or enter tasks manually to get started")
        
        # Instructions
        with st.expander("📖 How to format your tasks"):
            st.markdown("""
            **Task Format Examples:**
            ```
            - Task name (deadline: today 3pm, 2 hours)
            - Meeting with client (deadline: tomorrow morning, 1 hour)
            - Submit report (deadline: Friday, 30 minutes)
            - Call John (deadline: today evening, 15 minutes)
            - Project review (deadline: next week, 3 hours)
            ```
            
            **Deadline Keywords:**
            - `today`, `tomorrow`
            - `this morning/afternoon/evening`
            - Specific times: `2pm`, `3:30pm`
            - Days: `Monday`, `Friday`
            - Relative: `next week`, `this weekend`
            """)
    
    # System information
    with st.expander("ℹ️ About the System"):
        st.markdown("""
        **The system consists of 3 specialized AI agents:**
        
        1. **🔍 Task Analyzer Agent**: 
           - Parses tasks and extracts deadlines
           - Sorts tasks by deadline urgency
           - Classifies task types and priorities
        
        2. **📊 Schedule Builder Agent**: 
           - Creates deadline-optimized schedules
           - Ensures urgent tasks get prime time slots
           - Balances workload throughout the day
        
        3. **⚡ Productivity Enhancer Agent**: 
           - Adds strategic breaks and focus techniques
           - Implements Pomodoro methodology
           - Provides productivity tips and reminders
        
        **Technologies Used:**
        - 🤖 CrewAI for agent orchestration
        - 🧠 Groq API for fast LLM inference
        - 🖥️ Streamlit for user interface
        - ⏰ Advanced deadline parsing and prioritization
        """)

if __name__ == "__main__":
    main()