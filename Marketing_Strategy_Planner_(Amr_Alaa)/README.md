# Marketing System

Simple CrewAI-based marketing analysis system with 3 agents using Gemini 2.0 Flash:
- SWOT Analysis Agent
- Marketing Plan Agent  
- Content Planning Agent

## Setup
1. Get Gemini API key from Google AI Studio: https://makersuite.google.com/app/apikey
2. Add your API key to `config/config.yaml`
3. Install dependencies: `pip install -r requirements.txt`
4. Create directories: `mkdir -p data/processed`
5. Run: `python app.py`

## Model
Uses Google's Gemini 2.0 Flash (fast, powerful, and affordable)

## Structure
```
marketing-system/
├── main.py
├── requirements.txt  
├── config/config.yaml
├── data/processed/   # Output reports
└── src/
    ├── agents/
    │   ├── swot_analysis_agent.py
    │   ├── marketing_plan_agent.py
    │   └── content_planning_agent.py
    └── models/
        └── model.py
```
