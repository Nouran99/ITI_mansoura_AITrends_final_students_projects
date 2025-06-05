# Clean Code Rewriter 🧹✨

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cleancoderewriter.streamlit.app/)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-181717?style=flat&logo=github)](https://github.com/mohamedsalama677/Clean_code_rewriter)
[![CrewAI](https://img.shields.io/badge/CrewAI-Agent_Orchestration-blue)](https://github.com/joaomdmoura/crewai)
[![Gemini](https://img.shields.io/badge/Google_Gemini-API-yellow)](https://gemini.google.com/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-API-9cf)](https://deepseek.com/)

**Transform messy code into clean, maintainable code** using AI-powered refactoring with an agent-based architecture. Powered by Gemini and DeepSeek API models through CrewAI orchestration.

---

## 🚀 Live Demo

Try the application now:  
👉 [https://cleancoderewriter.streamlit.app/](https://cleancoderewriter.streamlit.app/)

---

## 🛠️ Usage

1. **Input Code**: Paste or upload your Python code
2. **Process**: Click "Rewrite Code" to start transformation
3. **Review**: Compare original and refactored code side-by-side
4. **Learn**: Study the clean code principles applied
5. **Export**: Copy or download the improved code

### Example Transformation

**Before:**
```python
def calc(x,y,op):
    if op=='+': r=x+y
    elif op=='-': r=x-y
    elif op=='*': r=x*y
    elif op=='/': 
        if y==0: return 'Error'
        else: r=x/y
    return r
```

**After:**
```python
def perform_arithmetic_operation(operand1: float, operand2: float, operator: str) -> float | str:
    """
    Performs basic arithmetic operations on two numbers.
    
    Args:
        operand1: First numerical value
        operand2: Second numerical value
        operator: Mathematical operation (+, -, *, /)
    
    Returns:
        Result of operation or error message
    """
    operations = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b if b != 0 else 'Error: Division by zero'
    }
    
    operation = operations.get(operator)
    if operation is None:
        return 'Error: Invalid operator'
    
    return operation(operand1, operand2)
```

---

## Key Features

- **AI-Powered Refactoring**: Automatically improve code structure and readability
- **Multi-Agent Architecture**: Specialized agents for analysis, rewriting, teaching, and management
- **Dual-API System**: Combines Gemini API and DeepSeek API for optimal results
- **Clean Code Principles**: Applies industry-standard coding conventions
- **Educational Insights**: Highlights and explains clean code lessons
- **Real-time Processing**: Get instant feedback and suggestions
- **Modern Tech Stack**: Streamlit interface + CrewAI orchestration

---

## How It Works

Clean Code Rewriter uses a sophisticated multi-agent system to transform your code:

1. **Input**: User submits Python code
2. **Analysis**: Agents identify code smells and violations
3. **Refactoring**: Code is rewritten following clean code principles
4. **Education**: Detailed explanations of improvements are generated
5. **Output**: Returns cleaned code with educational insights

### Agent Architecture

| Agent Name      | Role             | API Used | Responsibility |
|-----------------|------------------|----------|----------------|
| AnalystAgent  | Code Inspector  | Gemini API | Detects code smells and violations 🔍 |
| RewriterAgent | Code Refactoring | Gemini API | Refactors code into clean format ✨ |
| TeacherAgent  | Code Educator    | DeepSeek API | Generates educational explanations 📚 |
| ManagerAgent  | Output Director  | DeepSeek API | Composes final structured output 📋 |

---

## Installation

### Prerequisites
- Python 3.10+
- API keys for [Gemini](https://aistudio.google.com/app/apikey) and [DeepSeek](https://platform.deepseek.com/api-keys)

### Local Setup

```bash
# Clone repository
git clone https://github.com/mohamedsalama677/Clean_code_rewriter.git
cd Clean_code_rewriter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure models in config.yaml
cp utils/config.example.yaml utils/config.yaml
```

Edit `utils/config.yaml` with your API keys:

```yaml
gemini:
  api_key: your_gemini_api_key_here
  model_name: gemini-1.5-flash  # Example model

deepseek:
  api_key: your_deepseek_api_key_here
  model_name: deepseek-coder-33b-instruct  # Example model

# Behavior Configuration
refactoring_level: moderate  # [minimal, moderate, aggressive]
code_style: pep8            # [pep8, google, custom]
```

Run the application:
```bash
streamlit run app.py
```

---

## Project Structure

```
Clean_code_rewriter/
├── agents/                # Agent definitions
│   ├── analyst.py         # 🔍 Code analysis
│   ├── generator.py       # ✨ Code rewriting
│   ├── manager.py         # 📋 Output composition
│   └── teacher.py         # 📚 Educational content
├── tasks/                 # Task definitions
│   ├── analyze_task.py    # Analysis tasks
│   ├── generate_task.py   # Generation tasks
│   ├── manage_task.py     # Formatting tasks
│   └── teach_task.py      # Lesson tasks
├── utils/                 # Utility functions
│   ├── config.yaml        # Configuration file
│   └── __init__.py
├── crew.py                # CrewAI orchestration
├── app.py                 # Streamlit application
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

---

## Configuration

Customize behavior via `utils/config.yaml`:

```yaml
# Gemini API Configuration
gemini:
  api_key: your_gemini_api_key
  model_name: gemini-1.5-pro  # Model options: gemini-1.5-pro, gemini-1.5-flash, etc.

# DeepSeek API Configuration
deepseek:
  api_key: your_deepseek_api_key
  model_name: deepseek-coder-33b-instruct  # Model options: deepseek-coder, deepseek-coder-33b-instruct, etc.

# Behavior Configuration
refactoring_level: moderate  # [minimal, moderate, aggressive]
code_style: pep8            # [pep8, google, custom]
```

---

## Testing

Run the test suite with:

```bash
pytest tests/
```

Test coverage report:

```bash
pytest --cov=src tests/
```

---

## Contributing

We welcome contributions! Follow these steps:

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a pull request

**Guidelines:**
- Follow PEP 8 style guide
- Include tests for new features
- Update documentation accordingly
- Maintain clean commit history

---

## Technologies Used

- **Framework**: [Streamlit](https://streamlit.io/)
- **AI Orchestration**: [CrewAI](https://github.com/joaomdmoura/crewai)
- **Language Models**: [Google Gemini API](https://gemini.google.com/), [DeepSeek API](https://deepseek.com/)
- **Code Analysis**: AST, Radon
- **Testing**: pytest
- **Environment**: Python 3.10+

---

## Known Issues

- Large files (>1000 lines) may require chunked processing
- Complex class hierarchies might need manual refinement
- Limited support for Python 2.x syntax
- Asynchronous code requires special handling

---

## Author

**Mohamed Salama**  
📧 Email: [mohamedsalama152019@gmail.com](mailto:mohamedsalama152019@gmail.com)  
💻 GitHub: [https://github.com/mohamedsalama677](https://github.com/mohamedsalama677)

---

## Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewai) for agent orchestration framework
- Google Gemini and DeepSeek teams for their advanced API models
- Streamlit for the intuitive web framework
- Clean Code concepts by Robert C. Martin

---

**Transform your code from messy to maintainable with AI-powered refactoring!**  
[👉 Live Demo](https://cleancoderewriter.streamlit.app/)
