# 🛤️ Pathway – Your Local AI Learning Coach

A lightweight, fully local AI-powered assistant that helps you go from a vague learning goal to a structured, interactive 4-week plan — using nothing but open-source tools and your machine.

![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-orange?style=flat-square&logo=streamlit)

---

## 🧭 Overview

**Pathway** is a local-first AI learning assistant built with Streamlit and LLaMA 3.1 via Ollama. It helps you define your learning goal, assess your current level, and receive a personalized, structured 4-week curriculum — rendered as an interactive plan with checkboxes, resource links, and real-time progress tracking.

Built entirely from scratch **without agentic AI libraries**, Pathway uses a modular multi-agent design to hand off data step-by-step:

1. 🔍 **Diagnostic agent** → generates yes/no questions  
2. 🧠 **Assessment agent** → reasons about your current level  
3. 📅 **Curriculum agent** → builds a week-by-week learning roadmap  
4. 🧱 **JSON converter agent** → transforms the roadmap into an editable, session-aware format  
5. 🌐 **Resource agent** → suggests curated YouTube and Medium content for each week  

Everything runs locally, with **no cloud dependencies**, in a clean Streamlit interface that’s simple enough for non-technical users.

Whether you're trying to learn Python, Algebra, or Photoshop — Pathway gives you clarity, structure, and relevant resources to get started.

---

## ✨ Features

- ✅ **Interactive Progress Tracker**  
  Your learning plan is displayed as a checkbox-based tracker, with persistent state and automatic progress updates.

- 🧠 **Personalized Diagnostic Assessment**  
  A local LLM (LLaMA 3.1 via Ollama) asks yes/no questions tailored to your goal to gauge your familiarity with core concepts.

- 📊 **Reasoning-Based Skill Assessment**  
  The system builds a high-level narrative of your strengths and weaknesses based on your answers — not just a score.

- 📅 **4-Week Custom Curriculum Generator**  
  Automatically generates a detailed, structured weekly plan with clear objectives, study topics, and tasks.

- 🧱 **Structured JSON Plan Architecture**  
  Each topic/task is wrapped as a dictionary with metadata (e.g. `{"name": ..., "completed": False}`), allowing real-time state updates and reusability.

- 🔍 **Smart Resource Suggestions**  
  For every week in your learning plan, the app fetches relevant YouTube videos and Medium articles based on your goal and weekly objectives — then displays them under collapsible sections for easy exploration.

- 🔁 **Modular Multi-Agent Pipeline**  
  Clean separation of responsibilities between Diagnostic, Assessment, Curriculum, and JSON agents — each building on the previous output.

- 💾 **Export & Reload Plans**  
  Download your progress as a `.json` or `.pdf` file.

- 🧩 **Built Entirely from Scratch**  
  No LangChain, no CrewAI, no LangGraph. Just Python, Streamlit, and clean logic.

- 🔐 **Local-first & Private by Default**  
  No internet calls. The model runs via Ollama on your own machine — you control your data.

- 🌱 **Simple Interface**  
  Designed with clarity and ease of use in mind.

---

  ## 🧠 Agent Pipeline

The system is powered by four custom agents, each with a single responsibility. Together, they form a clear reasoning chain from input to output:

- **1. Diagnostic Agent**  
  Analyzes the user's learning goal and generates a concise set of yes/no questions to quickly evaluate familiarity with fundamental concepts.

- **2. Assessment Agent**  
  Takes the user’s answers and synthesizes a skill-level profile — highlighting strengths, gaps, and readiness for advanced topics. This acts as the core rationale behind the generated plan.

- **3. Curriculum Agent**  
  Builds a structured 4-week learning roadmap based on the assessment. Each week includes:
  - A clear learning objective  
  - Topics categorized by activity type (e.g. "Read", "Watch", "Review")  
  - Actionable tasks (e.g. "Try exercises", "Build mini-project")

- **4. JSON Converter Agent**  
  Converts the plain-text plan into a **structured JSON object**, wrapping every topic and task in dictionaries with `completed: False` fields. This enables real-time interaction and progress tracking within the app.

- **5. Search Agent**  
  For each week’s learning objective, this agent generates a focused search keyword and queries for high-quality resources from platforms like YouTube and Medium — returning only relevant, educational links.

Each agent receives only what it needs and passes its output directly to the next — keeping the pipeline simple, debuggable, and explainable.

---

## 🛠️ Installation

Follow these steps to get **Pathway** running locally.

### 1. Clone the repositor

### 2. Install Python dependencies

Make sure you’re using Python 3.9+ and a virtual environment:

```
pip install -r requirements.txt
```

### 3. Install and run Ollama

This project uses **LLaMA 3.1 via Ollama** as the local language model.

* Download and install Ollama: [https://ollama.com](https://ollama.com)
* Then pull the model used by Pathway:

```
ollama pull llama3.1
```

Optional: Test the model locally before running the app:

```
ollama run llama3.1
```

💡 You can change the model used by editing your `.env` file.


### 4. Set up environment variables

Create a `.env` file in the root directory.

Inside `.env`, add:

```env
MODEL_NAME=llama3.1
GOOGLE_API_KEY=your_google_api_key
SEARCH_ENGINE_ID=your_custom_search_engine_id
```

You can change `MODEL_NAME` to any model available in your Ollama setup.

These keys are required for the resource suggestion feature, which uses **Google Programmable Search Engine (CSE)** to fetch relevant YouTube and Medium links.

> 🔐 **Note:** You can create your own Programmable Search Engine at [programmablesearchengine.google.com](https://programmablesearchengine.google.com), and generate an API key via [Google Cloud Console](https://console.cloud.google.com/apis/credentials).

---


### ✅ You’re ready to go!

Now run the Streamlit app:

```
streamlit run main.py
```

---

## 🔮 Future Work

Here are the next planned steps for improving **Pathway**:

* **🔼 Upload Support**
  Enable users to re-upload a previously exported JSON file, resuming their interactive plan with full progress tracking.

* **📚 Smarter Resource Ranking**
  Prioritize resources based on quality, popularity, and content type (e.g., tutorials vs. lectures), and allow user feedback to refine suggestions.

* **🔁 Adaptive Plan Refinement**
  Add a fifth agent that re-evaluates and refines the learning plan based on user progress and feedback — enabling a more dynamic, personalized loop.

* **📊 Progress Analytics**
  Provide visual summaries and analytics to show how far the learner has come and which areas need more focus.

* **🧠 Smarter Plans with Diverse Models**
  Experiment with new models and prompting strategies to enhance the quality and structure of generated plans — especially for complex or cross-domain topics.

* **🌐 Multi-Language & Domain Expansion**
  Extend the app to support non-English learners and apply the framework to domains beyond education (e.g., skill onboarding, employee training).


Here’s a clean and fitting **Conclusion** section in Markdown format for the end of your `README.md`:

---

## ✅ Conclusion

**Pathway** is a small but intentional step toward making learning more personal, adaptive, and structured — powered by local LLMs and designed from scratch with flexibility in mind.

By combining agentic reasoning with clean data structures and an interactive UI, it shows how even a solo project can orchestrate AI meaningfully — without relying on heavyweight frameworks.

The goal wasn’t to be flashy — it was to be useful, extendable, and local-first.

Thanks for checking it out. Feedback, ideas, and collaboration are always welcome.

