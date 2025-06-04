## 💰 Personal Finance Planner

A smart and interactive application for analyzing personal financial data and generating clear advice using a locally running LLM model (e.g., LLaMA 3 via Ollama).
Built with a user-friendly Streamlit interface and powered by multiple agents for data processing, financial analysis, and advice generation.

---

### 🚀 Features

* Upload financial data from CSV, Excel, or TXT files.
* Automatically analyze budget and spending patterns.
* Generate savings plans and financial advice in plain language.
* Save advice in a downloadable text report.
* Runs fully offline using LLaMA 3 through [Ollama](https://ollama.com/).

---

### 🗂️ Project Structure

```
personal_finance_planner/
│
├── agents/
│   ├── advice_agent.py            # Agent for generating financial advice
│   ├── analysis_agent.py          # Agent for analyzing financial data
│   └── data_processing_agent.py   # Agent for reading and formatting user data
│
├── utils/
│   └── llm_model.py               # Wrapper for communicating with LLaMA 3 via Ollama
│
├── data/
│   └── Sample_test.csv            # Example input file
│
├── output/
│   └── financial_advice_report.txt  # Generated advice report
│
├── app.py                         # Streamlit web interface
└── README.md                      # Project documentation
```

---

### ⚙️ Requirements

* Python 3.9+
* [Ollama](https://ollama.com/) installed and running locally
* LLaMA 3 model downloaded:

```bash
ollama pull llama3
```

* Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

### 📦 `requirements.txt` (suggested)

```txt
streamlit
pandas
ollama
```

---

### 📄 Sample Input Format

```csv
Income,Age,Dependents,Occupation,City_Tier,Rent,Loan_Repayment,Insurance,Groceries,Transport,Eating_Out,Entertainment,Utilities,Healthcare,Education,Miscellaneous,Desired_Savings_Percentage,Desired_Savings,Disposable_Income,Potential_Savings_Groceries,Potential_Savings_Transport,Potential_Savings_Eating_Out,Potential_Savings_Entertainment,Potential_Savings_Utilities,Potential_Savings_Healthcare,Potential_Savings_Education,Potential_Savings_Miscellaneous
44637.24963568593,49,0,Self_Employed,Tier_1,13391.174890705775,0.0,2206.490129258186,6658.768340572072,2636.9706962044347,1651.8017262162875,1536.1842554984205,2911.792230881923,1546.9145393077706,0.0,831.5251201893564,13.890948127514209,6200.537192442157,11265.6277068517,1685.696221820344,328.895281163744,465.7691723793779,195.1513197044244,678.292858894135,67.68247059153573,0.0,85.7355167261814

```

---

### 🖥️ How to Run

To launch the web interface:

```bash
streamlit run app.py
```

---

### 📤 Output

* Personalized financial analysis.
* Practical savings and budgeting tips.
* Report saved under `output/financial_advice_report.txt`.

---

### 🤖 Using LLaMA 3 with Ollama

The LLM model is called locally using Ollama:

```python
ollama.chat(model="llama3", messages=[...])
```

This ensures privacy and removes the need for paid cloud APIs.

---

### 🔧 Future Improvements

* Add charts and visualizations.
* Multilingual support (e.g., Arabic, French).
* Google Sheets integration.
* Docker container for deployment.

---

