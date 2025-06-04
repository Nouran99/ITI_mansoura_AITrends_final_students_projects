

# CrewAI Multi-Agent Data Pipeline

The **CrewAI Multi-Agent Data Pipeline** is an interactive web application built with Streamlit that automates the machine learning pipeline using a team of intelligent agents. From uploading a dataset to performing exploratory data analysis, generating dashboards, cleaning data, and suggesting machine learning models, this tool provides an end-to-end experience suitable for data scientists, students, and ML engineers.

---

## Overview

This application leverages **CrewAI**, a framework for coordinating autonomous agents, to perform a structured data workflow. The agents collaborate to process datasets and produce outputs necessary for building machine learning models. The platform is designed to minimize manual effort and accelerate decision-making in the data science lifecycle.

You can try it from here: https://saragamilmohamed-crewai-crewaimulti-agentdatapipelineapp-ilocbm.streamlit.app/

**Key Capabilities:**

* Automated EDA generation
* Dashboard creation with visual insights
* Preprocessing pipeline including encoding, imputation, and scaling
* Intelligent model recommendations using context-aware reasoning

---

## Project Structure

```
project_root/
├── agents/
│   ├── eda_agent.py                  # Performs Exploratory Data Analysis
│   ├── dashboard_agent.py            # Generates HTML-based data visualizations
│   ├── preprocessing_agent.py        # Handles data cleaning and transformation
│   └── model_suggestion_agent.py     # Recommends suitable machine learning models
├── processed_output/
│   ├── processed_data.csv            # Output of the preprocessing pipeline
│   └── preprocessing_strategy.txt    # Explanation of preprocessing decisions
├── dashboard_output/
│   └── insights_dashboard.html       # HTML dashboard with charts and graphs
├── eda_report.txt                    # Text file summarizing EDA findings
├── app.py                            # Streamlit app script (main entry point)
└── data/
    └── [uploaded_csv_files]         # User-uploaded datasets
```

---

## Features

### 1. File Upload Interface

* Upload any CSV dataset through the web interface.
* Automatically saves uploaded files to a `data/` directory.

### 2. Exploratory Data Analysis (EDA)

* Conducts comprehensive analysis including:

  * Data types, missing values
  * Summary statistics
  * Correlation matrix
  * Potential data quality issues
* Output is saved to `eda_report.txt` and displayed in the UI.

### 3. Dashboard Generation

* Visualizations are created using data columns and inferred types.
* The dashboard includes:

  * Histograms
  * Boxplots
  * Correlation heatmaps
* Rendered and saved as `insights_dashboard.html`.

### 4. Data Preprocessing

* Applies common preprocessing techniques such as:

  * Dropping duplicates
  * Filling missing values (with mode or median)
  * Encoding categorical columns (Ordinal or OneHot)
  * Scaling numerical features using RobustScaler
* Outputs:

  * Processed dataset (`processed_data.csv`)
  * Summary of transformations (`preprocessing_strategy.txt`)

### 5. Model Suggestion Agent

* Suggests appropriate ML models based on:

  * EDA results
  * Dashboard insights
  * External research using given keywords (e.g., Kaggle or GitHub datasets)
* Output includes rationale for suggested models and use cases.

---

## Technologies Used

* **CrewAI**: For orchestrating collaborative AI agents.
* **Streamlit**: For building the interactive user interface.
* **Pandas**: For data manipulation.
* **Scikit-learn**: For preprocessing techniques.
* **Matplotlib / Seaborn / Plotly** (if used in agents): For visualization.

---

### Sample `requirements.txt`

```text
streamlit
pandas
scikit-learn
crewai
```


### Steps to Use:

1. Upload a dataset (CSV format).
2. Click the buttons to run:

   * EDA Agent
   * Dashboard Agent
   * Preprocessing Agent
   * Model Suggestion Agent
3. View and download outputs such as:

   * EDA reports
   * Visual dashboards
   * Processed datasets
   * Suggested models and rationales

---

## Output Files

| File Name                    | Description                                             |
| ---------------------------- | ------------------------------------------------------- |
| `eda_report.txt`             | Text report detailing exploratory data analysis results |
| `processed_data.csv`         | Cleaned and transformed dataset                         |
| `preprocessing_strategy.txt` | Summary of applied preprocessing techniques             |
| `insights_dashboard.html`    | HTML file containing interactive visualizations         |
| `model_suggestions.txt`      | Recommended ML models with justifications               |

---

## Example Use Cases

This application is ideal for:

* Rapid prototyping of ML workflows
* Data exploration and cleaning without code
* Educational projects and data science training
* Initial ML model recommendations for research or competitions


