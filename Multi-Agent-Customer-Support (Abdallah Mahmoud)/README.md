# Multi-Agent-Customer-Support 🤖📞💳

A multi-agent AI-powered customer support system built with [CrewAI](https://docs.crewai.com/) and [DeepSeek](https://huggingface.co/deepseek-ai), tailored to handle user queries across **Banking**, **E-commerce**, and **Telecom** domains. This project simulates a smart support team capable of accessing domain-specific knowledge and customer information to respond interactively through a friendly [Streamlit](https://streamlit.io) interface.

🚀 **[Try the Live Demo](https://multi-agent-customer-support.streamlit.app/)**

---

## 🧠 Project Highlights

- **Multi-Agent Architecture**: Separate agents for Banking, E-commerce, and Telecom, managed via CrewAI.
- **DeepSeek LLM**: Integrated as the primary model for generating context-aware and human-like responses.
- **Streamlit Interface**: A user-friendly GUI where users can simulate customer queries with test data.
- **Customer Info DB (SQLite3)**: Agents access structured customer information from a SQLite3 database.
- **Knowledge Base (ChromaDB)**: Uses ChromaDB to semantically retrieve relevant information from vectorized documents.
- **Tools & Crew Tools**: Modular toolset for handling domain-specific functions like account info, transactions, orders, billing, etc.

---

## 📁 Project Structure

```
Multi-Agent-Customer-Support/
├── agents/               # Crew agents for different domains
│   ├── __init__.py  
│   ├── base_agent.py  
│   ├── banking_crew.py  
│   ├── ecommerce_crew.py  
│   ├── telecom_crew.py  
│   └── router_crew.py  
├── config/               # LLM and environment configurations
│   ├── llm_config.py
│   └── settings.py
├── data/                 # Data resources 
│   ├── knowledge_base/            # Domain-specific documents
│   └── customer_support.db        # SQLite3 customer data
├── database/             # Database and vector store management  
│   ├── __init__.py  
│   ├── init_db.py                 # DB initializer  
│   ├── sample_data.py             # Insert test data  
│   ├── sql_manager.py             # SQLite operations  
│   └── vector_manager.py          # ChromaDB operations 
├── tools/                # Toolkits for domain-specific logic
│   ├── __init__.py  
│   ├── banking_tools.py  
│   ├── ecommerce_tools.py  
│   ├── telecom_tools.py  
│   └── common_tools.py 
├── ui/                   # Streamlit UI components
│   ├── components.py
│   └── styles.py
├── .env.example                   # Example environment config
├── .gitignore                     # Files and folders to be excluded from Git tracking
├── main.py                        # Entry point for Streamlit app  
├── requirements.txt               # Project dependencies 
└── README.md                      # Project info
```

---

## 🖥️ How to Run Locally

1. **Clone the repository**

```bash
git clone https://github.com/abdallahm7moud/Multi-Agent-Customer-Support.git
cd Multi-Agent-Customer-Support
```

2. **Create and activate a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Add your API keys**

Copy `.env.example` to `.env` and fill in required keys (e.g., for DeepSeek, CrewAI, etc.)

```bash
cp .env.example .env
```

5. **Run the Streamlit app**

```bash
streamlit run main.py
```

---

## 🛠️ Tech Stack

- 🧠 **LLM**: [DeepSeek](https://huggingface.co/deepseek-ai)
- 👥 **Agent Framework**: [CrewAI](https://docs.crewai.com/)
- 💡 **Interface**: [Streamlit](https://streamlit.io)
- 🗃️ **Customer Info DB**: SQLite3
- 📚 **Knowledge Base**: ChromaDB (vector database)
- 🧰 **Semantic Search**: Custom `vector_manager.py` for retrieval

---

## 📚 Use Case Domains

| Domain      | Example Scenarios                                      |
|-------------|--------------------------------------------------------|
| Banking     | Balance inquiries, transaction issues, card problems   |
| E-commerce  | Order tracking, return policies, payment issues        |
| Telecom     | Internet speed, billing queries, plan upgrades         |

---

## 🌐 Online Demo

Experience the full application here:  
👉 **[https://multi-agent-customer-support.streamlit.app/](https://multi-agent-customer-support.streamlit.app/)**
