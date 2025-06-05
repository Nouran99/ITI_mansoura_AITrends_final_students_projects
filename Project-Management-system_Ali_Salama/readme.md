# Multi-Agent AI Project Managemensystem

> Transform your project ideas into comprehensive Agile plans using AI agents powered by **Google Gemini 2.5 Flash**

[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Gemini](https://img.shields.io/badge/Gemini-2.5--Flash-4285F4.svg)](https://ai.google.dev)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-purple.svg)](https://crewai.com)

##  Overview

The **Agile Project Planner** is a sophisticated multi-agent AI system that generates professional-grade project documentation, sprint plans, user stories, and team recommendations. Powered by Google's cutting-edge **Gemini 2.5 Flash** model, it provides a complete solution for transforming your project ideas into actionable Agile plans with enterprise-level documentation.

###  Key Highlights

- **🤖 6 Specialized AI Agents** working in perfect coordination
- **⚡ High-Performance AI** - Powered by Google Gemini 2.5 Flash
- **📋 Complete Agile Framework** - From requirements to deployment
- **🎨 Professional Documentation** - HTML/PDF export with modern design
- **📊 Comprehensive Planning** - Sprints, budgets, risks, and timelines

---

##  Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Multi-Agent AI System** | 6 specialized agents orchestrated by CrewAI |
| **Professional Documentation** | Modern HTML templates with embedded CSS |
| **Comprehensive Planning** | Complete Agile project plans with sprints and timelines |
| **Technology Recommendations** | Smart tech stack suggestions based on requirements |
| **Team Structure Planning** | Optimal team composition with cost estimates |
| **Advanced Export Options** | Professional HTML/PDF reports with modern design |
| **Risk Assessment** | Color-coded risk matrices with mitigation strategies |

### Advanced Features

- **Executive-Ready Documentation** with modern gradient designs
- **Budget Estimation** with detailed cost breakdowns and justifications
- **Milestone Tracking** with visual timeline components
- **User Story Generation** with comprehensive acceptance criteria
- **Technology Architecture** recommendations with scalability considerations
- **Team Role Mapping** with skill requirements and cost analysis
- **Risk Management** with impact assessment and mitigation plans

---

## 🏗️ Architecture

### AI Agents Ecosystem

The application leverages **CrewAI** to orchestrate a sophisticated multi-agent system powered by **Google Gemini 2.5 Flash**:

#### 🤖 Agent Roles & Responsibilities

1. **🧏 Customer Listener Agent** 
   - **Role**: Customer Requirements Specialist
   - **Purpose**: Analyzes project requirements, goals, and constraints
   - **Output**: Structured project requirements document

2. **📋 Requirements Extractor Agent**
   - **Role**: Requirements Analyst  
   - **Purpose**: Converts customer input into structured functional/non-functional requirements
   - **Output**: JSON formatted requirements specification

3. **📅 Planning & Milestone Agent**
   - **Role**: Agile Project Planner
   - **Purpose**: Creates sprint breakdowns, timelines, and project milestones
   - **Output**: Detailed sprint plan with timeline and dependencies

4. **✍️ User Story Generator Agent**
   - **Role**: User Story Creator
   - **Purpose**: Writes detailed user stories with acceptance criteria and story points
   - **Output**: Complete user stories with acceptance criteria

5. **💻 Technology Advisor Agent**
   - **Role**: Technical Architecture Advisor
   - **Purpose**: Recommends optimal tech stacks based on requirements and constraints
   - **Output**: JSON formatted technology recommendations

6. **📦 Plan Packager Agent**
   - **Role**: Project Documentation Specialist
   - **Purpose**: Compiles everything into a comprehensive, professional HTML document
   - **Output**: Executive-ready project plan with modern design

### Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Orchestration**: CrewAI + LangChain
- **Language Model**: Google Gemini 2.5 Flash (via CrewAI LLM)
- **Document Generation**: Custom HTML templates with embedded CSS
- **Environment Management**: python-dotenv
- **Export Formats**: HTML, PDF-ready documents

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google AI API access (Gemini 2.5 Flash)
- CrewAI API key
- 4GB RAM minimum (8GB recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/3lis0/Multi-Agent-AI-Project-Management-system.git
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your API keys:
   ```env
   CREWAI_API_KEY=your_crewai_api_key_here
   GOOGLE_API_KEY=your_google_ai_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

---

## 📋 Usage Guide

### 1. Project Input Phase
Define your project with comprehensive details:
- **Project Overview**: Name, description, and problem statement
- **Target Audience**: User demographics and personas  
- **Feature Requirements**: Must-have and nice-to-have features
- **Constraints**: Budget range, timeline, and technical limitations
- **Preferences**: Platform choices and technology preferences

### 2. AI Processing Pipeline
Watch the multi-agent system work through your requirements:

```
Customer Input → Requirements Analysis → Project Planning → User Stories → Tech Stack → Documentation
```

Each agent processes the output from the previous stage, creating a comprehensive understanding of your project needs.

### 3. Generated Deliverables

#### Executive Summary
- High-level project overview with key metrics
- Business goals and success criteria
- Project scope and timeline overview

#### Detailed Documentation
- **Requirements Specification**: Functional and non-functional requirements
- **Sprint Planning**: Detailed sprint breakdowns with feature assignments
- **User Stories**: Complete with acceptance criteria and story points
- **Technology Architecture**: Recommended tech stack with justifications
- **Team Structure**: Role definitions with skill requirements and costs
- **Risk Assessment**: Risk matrix with mitigation strategies
- **Budget Analysis**: Detailed cost breakdown with justifications

### 4. Export & Collaboration
- **Professional HTML**: Modern, responsive design optimized for viewing
- **PDF-Ready**: Print-optimized layouts for executive presentations
- **JSON Export**: Structured data for integration with project tools
- **Shareable Links**: Easy stakeholder collaboration

---

## 📁 Project Structure

```
agile-project-planner/
├── crew_local.py
├── app.py                      # Main Streamlit application
├── agents.py                 # AI agent definitions using CrewAI
├── tasks.py                  # Task definitions for each agent
├── utils/
│   └── base_model.py        # LLM configuration 
│   └── requirements.txt         # Python dependencies
│   └── html_pdf_generator.py
│   └── main_styles.css   
├── Example/  
│   └── project_plan.html        
├── README.md               # This documentation
```

---

## 🔧 Configuration

### Environment Variables (.env)

```env
# CrewAI Configuration
CREWAI_API_KEY=your_crewai_api_key

# Google AI Configuration  
GOOGLE_API_KEY=your_google_ai_api_key

# Application Settings
APP_TITLE=Agile Project Planner
DEBUG_MODE=False

# AI Model Settings
MODEL_TEMPERATURE=0.7
MODEL_NAME=gemini/gemini-2.5-flash-preview-04-17
```

### API Key Setup

1. **CrewAI API Key**:
   - Visit [CrewAI Platform](https://crewai.com)
   - Sign up and obtain your API key
   - Add to `.env` file

2. **Google AI API Key**:
   - Visit [Google AI Studio](https://ai.google.dev)
   - Create a new project and enable Gemini API
   - Generate API key and add to `.env` file

---

## 🎨 Customization

### Agent Behavior Modification

Customize agent roles and behaviors in `agents.py`:

```python
def custom_agent(self):
    return Agent(
        role='Your Custom Role',
        goal='Your specific goal',
        backstory="""Your agent's background and expertise""",
        verbose=True,
        allow_delegation=False,
        llm=self.llm
    )
```

### Task Configuration

Modify agent tasks in `tasks.py` to change output formats or requirements:

```python
def custom_task(self, agent, context):
    return Task(
        description="Your custom task description",
        agent=agent,
        context=context,
        expected_output="Your expected output format"
    )
```

### Document Styling

The HTML templates use modern CSS with:
- **CSS Variables** for consistent theming
- **Responsive Design** for all screen sizes
- **Print Optimization** for PDF conversion
- **Professional Typography** with Inter font family
- **Modern Components** like gradient headers and metric cards


---

## 🔍 Troubleshooting

### Common Issues

**1. API Key Errors**
```bash
# Check your .env file
cat .env

# Verify API keys are valid
# Test CrewAI API connection
# Test Google AI API connection
```

**2. Dependencies Issues**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear pip cache
pip cache purge
```

**3. Streamlit Issues**
```bash
# Clear Streamlit cache
streamlit cache clear

# Reset Streamlit configuration
rm -rf ~/.streamlit/
```

**4. Memory Issues**
```bash
# Monitor memory usage
htop

# Reduce model temperature for faster processing
# Close other applications
```

### Debug Mode

Enable debug mode in `.env`:
```env
DEBUG_MODE=True
```

This provides detailed logging and error information in the Streamlit interface.

---

##  Acknowledgments

- **Google AI** for the Gemini 2.5 Flash model
- **CrewAI** team for the multi-agent framework
- **Streamlit** for the excellent web framework
- **LangChain** for LLM integration capabilities
- **Open Source Community** for continuous inspiration

---

##  Support 

- **Developer**: [@3lis0](https://github.com/3lis0)

