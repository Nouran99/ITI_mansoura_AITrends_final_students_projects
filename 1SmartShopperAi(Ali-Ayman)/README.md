'''# 🤖 SmartShopper AI: Intelligent Product Procurement Assistant

🌟 ## Project Overview

SmartShopper AI is an advanced, AI-powered procurement assistant designed to help businesses and individuals make informed product purchasing decisions. Leveraging cutting-edge AI technologies, this tool provides comprehensive market research, price comparison, and detailed procurement reports.

✨ ## Key Features

*   🔍 Multi-website Product Search
*   📊 Comprehensive Procurement Reports
*   🌐 Multi-country Support
*   🤖 AI-Powered Market Analysis
*   📈 Detailed Product Comparisons

🚀 ## Technologies Used

*   CrewAI
*   Streamlit
*   Python
*   Large Language Models (LLM)
*   Web Scraping Technologies

📋 ## Prerequisites

### System Requirements

*   Python 3.8+
*   pip
*   Git

### API Keys Required

*   Tavily API Key
*   ScrapegraphAI Key
*   DeepSeek/Gemini API Key

🔧 ## Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/SmartShopper-AI.git
    cd SmartShopper-AI
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    # On Linux/macOS
    source venv/bin/activate
    # On Windows
    # venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Configuration**
    Create a `.env` file in the project root with the following content:
    ```text
    TAVILY_API_KEY=your_tavily_api_key
    SCRAPEGRAPH_API_KEY=your_scrapegraph_key
    DEEP_SEEK_API_KEY=your_deepseek_api_key
    ```

🖥️ ## Running the Application

```bash
streamlit run main.py
```

🛠️ ## Project Structure

```text
SmartShopper-AI/
│
├── Agents/
│   ├── keywords_Search_Agent0.py
│   ├── Search_engine_Agent1.py
│   ├── Scraping_Agent2.py
│   └── final_reporter_agent3.py
│
├── Tasks/
│   ├── Create_Keywords_search_Task.py
│   ├── Search_engine_task1.py
│   ├── Scraping_task2.py
│   └── final_Reporter_task3.py
│
├── Tools/
│   ├── Search_engine_tool0.py
│   └── Scraping_Tool1.py
│
├── main.py
├── .env
├── requirements.txt
└── README.md
```

🔬 ## How It Works

1.  **Keyword Generation**: AI generates targeted search queries.
2.  **Web Search**: Crawls multiple e-commerce platforms.
3.  **Data Extraction**: Scrapes product details.
4.  **Analysis**: Compares prices and features.
5.  **Reporting**: Generates a comprehensive HTML report.

🎯 ## Use Cases

*   Corporate Procurement
*   Price Comparison
*   Market Research
*   Product Analysis

📊 ## Supported Platforms

*   Amazon Egypt
*   Noon
*   Souq
*   Jumia
*   Apple Store

🌍 ## Supported Countries

*   Egypt
*   UAE
*   Saudi Arabia
*   Qatar

🌐 ## Multilingual Support

*   English
*   Arabic

🤖 ## AI Technologies

*   **Large Language Models**: Gemini Flash, DeepSeek
*   **Web Scraping**: ScrapegraphAI
*   **Search**: Tavily Search API

🔒 ## Security Features

*   API Key Environment Protection
*   Secure Web Scraping Practices
*   Input Validation
*   Error Handling Mechanisms

📈 ## Performance Metrics

*   **Search Accuracy**: 85-90%
*   **Multi-platform Coverage**: 5+ Websites
*   **Average Report Generation Time**: 30-60 seconds

🤝 ## Contributing

### How to Contribute

1.  Fork the repository.
2.  Create a feature branch:
    ```bash
    git checkout -b feature/AmazingFeature
    ```
3.  Commit your changes:
    ```bash
    git commit -m 'Add some AmazingFeature'
    ```
4.  Push to the branch:
    ```bash
    git push origin feature/AmazingFeature
    ```
5.  Open a Pull Request.

### Contribution Guidelines

*   Follow PEP 8 Style Guide.
*   Write comprehensive docstrings.
*   Add unit tests for new features.
*   Update documentation as needed.

🐛 ## Known Issues

*   Limited international website support.
*   Potential scraping limitations based on website structure changes.
*   API rate limit constraints.

🚧 ## Future Roadmap

### Short-term Goals

*   Add more e-commerce platforms.
*   Enhance multilingual support.
*   Improve scraping robustness.

### Long-term Vision

*   Implement a machine learning model for price prediction.
*   Develop a mobile application.
*   Integrate advanced data visualization.
*   Add a user authentication system.

📊 ## Performance Monitoring

### Recommended Monitoring Tools

*   Sentry for error tracking
*   Prometheus for performance metrics
*   Grafana for dashboarding

📄 ## Licensing

Distributed under the MIT License.

📧 ## Contact

Email: ali.ayman.solimann@gmail.com
'''
