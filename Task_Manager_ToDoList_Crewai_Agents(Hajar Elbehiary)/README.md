

# 🚀 Tasks Scheduling Manager with AI Agents

![Task Management](https://img.shields.io/badge/Task%20Management-AI%20Powered-brightgreen)
![Built with CrewAI](https://img.shields.io/badge/Built%20with-CrewAI-blue)
![LLM](https://img.shields.io/badge/LLM-Gemini%20API-orange)
![UI](https://img.shields.io/badge/UI-Streamlit-red)

An intelligent task scheduling system that uses multiple AI agents to organize your day based on priorities and deadlines. This project leverages the power of CrewAI and Google's Gemini to create optimized schedules from simple task lists.

## 🎯 Project Overview

This application helps you transform a simple list of tasks with deadlines into a smart, prioritized schedule. The system analyzes deadlines, estimates time requirements, and creates a structured plan that maximizes your productivity.

## ✨ Key Features

- **🔍 Deadline-Based Prioritization**: Automatically identifies urgent tasks and organizes them by priority
- **⏰ Intelligent Time Allocation**: Creates optimized time blocks for your tasks
- **📊 Priority Categories**: Organizes tasks into High, Medium and Low priority groups
- **☕ Strategic Breaks**: Inserts appropriate breaks to maintain productivity
- **📥 Multiple Export Options**: Download your schedule as a standard schedule or checkbox to-do list

## 🧠 How It Works: The AI Agent Team

The system uses a team of three specialized AI agents powered by Google's Gemini 2.0 Flash:

1. **Task Analyzer Agent**
   - Processes raw task input with deadlines
   - Extracts and sorts tasks by urgency
   - Assigns priority levels and estimates time requirements

2. **Schedule Builder Agent**
   - Creates time slots based on task priorities
   - Ensures urgent tasks get priority placement
   - Designs a balanced daily schedule

3. **Productivity Enhancer Agent**
   - Formats the schedule as an easy-to-follow to-do list
   - Adds strategic breaks between tasks
   - Includes productivity tips

## 📋 Task Input Format

Tasks should be entered in this format:
```
- Task name (deadline: when, duration)
```

Examples:
```
- Complete quarterly presentation (deadline: today 4pm, 2 hours)
- Client meeting preparation (deadline: tomorrow 9am, 1 hour)
- Review and respond to emails (deadline: today end of day, 30 minutes)
- Gym workout session (deadline: today evening, 45 minutes)
- Read development book chapter (deadline: this week, 1 hour)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/HajarElbehairy/Tasks_Scheduling_Manager_Agents_Crew_ai.git
   cd Tasks_Scheduling_Manager_Agents_Crew_ai
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Create a `.env` file in the project directory:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure

```
Tasks_Scheduling_Manager_Agents_Crew_ai/
├── app.py                 # Streamlit UI application
├── agents.py              # AI agent definitions with roles & goals
├── tasks.py               # Task definitions for each agent
├── crew.py                # Agent orchestration system
├── requirements.txt       # Project dependencies
├── .env                   # API key configuration (create this file)
└── README.md              # Project documentation
```

## 🔧 Technology Stack

- **Agent Framework**: [CrewAI](https://github.com/joaomdmoura/crewAI) - For agent orchestration
- **LLM Provider**: Google Gemini API (Gemini 2.0 Flash model)
- **UI Framework**: [Streamlit](https://streamlit.io) - For the web interface
- **Python Libraries**: langchain, dotenv, datetime

## 💡 Usage Examples

The system works with both English and Arabic task inputs:

### English Example
```
- Prepare presentation for meeting (deadline: today 3pm, 2 hours)
- Call main client (deadline: tomorrow morning, 30 minutes)
- Complete monthly sales report (deadline: Friday, 3 hours)
- Review new project plan (deadline: next week, 1 hour)
- Respond to emails (deadline: end of day, 45 minutes)
```

### Arabic Example
```
- تحضير عرض تقديمي للاجتماع (deadline: اليوم 3م، 2 ساعة)
- الاتصال بالعميل الرئيسي (deadline: غداً صباحاً، 30 دقيقة)
- إكمال تقرير المبيعات الشهري (deadline: الجمعة، 3 ساعات)
- مراجعة خطة المشروع الجديد (deadline: الأسبوع القادم، 1 ساعة)
- الرد على رسائل البريد الإلكتروني (deadline: نهاية اليوم، 45 دقيقة)
```

## 🔮 Future Enhancements

- Google Calendar integration
- Recurring task support
- Task completion tracking
- Multiple day planning
- Mobile application version

## 📚 Resources & References

- [CrewAI Documentation](https://docs.crewai.com/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Streamlit Documentation](https://docs.streamlit.io)

## 👤 Author

- **Hajar Elbehairy** - [GitHub Profile](https://github.com/HajarElbehairy)



Built with ❤️ using CrewAI and Google Gemini API to make task management smarter and more efficient!
