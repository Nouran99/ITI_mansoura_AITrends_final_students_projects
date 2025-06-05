# 🎯 AI Interview Question Generator (Multi-Agent System)

A multi-agent AI system that generates customized **technical interview questions** based on a candidate's uploaded **CV (PDF)** and the **target job title** — powered by **LLMs from Hugging Face**, a **Streamlit frontend**, and **CrewAI-based agents**.

🚀 Try it online: [Streamlit Cloud App]( https://lnkd.in/eV9k_HWd)

---

##  Key Features

-  Upload a resume in PDF format
-  Extract and analyze skills, projects, and education using AI agents
-  Match against job title and optional job description
-  Generate 10 role-specific, technical interview questions
-  Export as PDF or JSON
-  Add your own Hugging Face API key to bypass token limits

---

##  How It Works

The system uses **three cooperative agents** via [CrewAI](https://github.com/joaomdmoura/crewAI):

1. **CV Agent** – Parses structured data from the candidate’s CV
2. **Role Agent** – Extracts technical requirements from the job title/description
3. **Question Agent** – Synthesizes role-specific interview questions using the data from the above agents

Agents share information via tasks, and collaborate to generate concise and targeted interview questions.

---

## 🧪 Tech Stack

| Layer              | Technology                                      |
|--------------------|-------------------------------------------------|
|  LLMs              | Mistral-7B, Hugging Face API                    |
|  Agents            | [CrewAI](https://github.com/joaomdmoura/crewAI) |
|  Frontend          | [Streamlit](https://streamlit.io)               |
|  PDF Handling      | `pdfparser`, `PyMuPDF`,`jobtitle`               |
|  Exporting         | `reportlab`, `json`                             |
|  Utilities         | `dotenv`, `tqdm`, `pydantic`                    |

---

##  Directory Structure

```text
.
├── streamlit_app.py           # Streamlit UI (main entry point)
├── models/
    ├──huggingface_llm.py      # The llm model class
    ├──schemas.py              # pydantic schemas
├── crew/
│   ├── mycrew.py              # Orchestrates agent tasks
│   ├── agents.py              # Defines individual agents (CV, Role, Question)
├── tools/
    └── pdf_parser_tool.py     # PDF parsing logic
    └── job_profile_tool.py    # Map job title with its coreesponding skills
├── utils/
│   └── pdf_exporter.py        # Converts question list to PDF
├── requirements.txt           # All project dependencies
├── .env                       # Hugging Face token (optional)
└── README.md                  # This file

