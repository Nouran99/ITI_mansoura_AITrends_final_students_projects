from crewai import Crew, Task
from .agents import cv_agent, role_agent, question_agent
import json
from typing import Dict, Any, List
import re
from models.huggingface_llm import HuggingFaceLLM


FALLBACK_QUESTIONS = [
    {"question": "Can you describe your technical background?", "category": "Technical Skills"},
    {"question": "What is your most significant project experience?", "category": "Projects"},
    {"question": "How do you stay updated with new technologies?", "category": "General"},
    {"question": "Describe a challenging problem you solved recently.", "category": "Problem Solving"},
    {"question": "What interests you about this position?", "category": "General"},
    {"question": "What experience do you have with this role's responsibilities?", "category": "Experience"},
    {"question": "Can you walk me through your most challenging technical project?", "category": "Projects"},
    {"question": "What programming languages are you most comfortable with?", "category": "Technical Skills"},
    {"question": "How do you approach problem-solving in technical scenarios?", "category": "Problem Solving"},
    {"question": "What interests you most about this role?", "category": "General"}
]

def run_interview_process(cv_text: str, job_title: str, job_description: str = "", hf_token=None) -> List[Dict[str, str]]:
    """
    Run the interview question generation process.
    """
    # 🧠 Instantiate Hugging Face LLM and assign to agents
    try:
        llm = HuggingFaceLLM(api_token=hf_token)
        cv_agent.llm = llm
        role_agent.llm = llm
        question_agent.llm = llm
        print("✅ Custom HF LLM assigned to agents")
    except Exception as e:
        print("❌ LLM initialization failed:", e)
        return FALLBACK_QUESTIONS
    
    cv_task = Task(
    agent=cv_agent,
    description=f"""Parse the following CV text and extract structured technical details:
        - Technical skills (group by category if possible)
        - Degrees and majors (highlight relevant technical fields)
        - Notable technical projects (focus on tools, methods, outcomes)
        - Relevant courses and certifications (especially core subjects in the major)
        - Work experience (with focus on technical responsibilities and outcomes)

        CV Text: {str(cv_text)}
        """,
            expected_output="JSON with: skills, education, projects, courses, experience"
        )

    role_task = Task(
    agent=role_agent,
    description=f"""Analyze the job title '{job_title}' and job description '{job_description}' to extract only the technical aspects:
        - Required technical skills and frameworks
        - Key responsibilities with technical context
        - Tools, platforms, or methodologies mentioned

        Avoid HR fluff or soft skills.
        """,
            expected_output="JSON with: required_skills, tools, responsibilities"
        )


    question_task = Task(
    agent=question_agent,
    description="""Act as a senior technical interviewer preparing questions for a candidate based on their CV and the target job role.

        Use the structured CV and role profile to generate **10 concise, specific technical interview questions** that probe the candidate's:
        - **Core technical skills** relevant to the job
        - **Hands-on project experience**, especially real-world applications
        - **Knowledge of tools, frameworks, and algorithms**
        - **Understanding of courses taken** that relate to the job
        - **Problem-solving abilities in technical scenarios**

        Avoid generic or HR-style questions. Focus strictly on domain-relevant, technical questions. Prefer short, direct, and insightful prompts like:
        - “How did you implement XYZ in your final-year project?”
        - “What are the trade-offs of using ABC vs DEF in [relevant course/project]?”
        - “Can you optimize a function in [language] that does XYZ?”

        Output format:
        [
        {"question": "How did you use TensorFlow in your image classification project?", "category": "Projects"},
        {"question": "Can you explain how a GRU differs from an LSTM?", "category": "Technical Skills"}
        ]
        """,
            expected_output="JSON array of 10 structured technical questions with 'question' and 'category'"
        )


    
    interview_crew = Crew(
        agents=[cv_agent, role_agent, question_agent],
        tasks=[cv_task, role_task, question_task],
        verbose=True
    )

    try:
        result = interview_crew.kickoff()
        output_text = getattr(result, 'raw', None) or getattr(result, 'result', None) or str(result)
        print(f"Raw crew output: {output_text}")

        real_questions = parse_questions_from_output(output_text)

        # Pad with fallback if fewer than 10
        if len(real_questions) < 10:
            remaining = 10 - len(real_questions)
            real_questions.extend(FALLBACK_QUESTIONS[:remaining])

        return real_questions[:10]

    except Exception as e:
        print(f"Error in crew execution: {str(e)}")
        return FALLBACK_QUESTIONS[:10]


def parse_questions_from_output(output_text: str) -> List[Dict[str, str]]:
    """
    Parse interview questions from Crew output text.
    """
    try:
        json_pattern = r'\[\s*\{[^}]*"question"[^}]*\}[^]]*\]'
        json_match = re.search(json_pattern, output_text, re.DOTALL)
        if json_match:
            questions = json.loads(json_match.group(0))
            if isinstance(questions, list):
                return questions
        questions = json.loads(output_text)
        if isinstance(questions, list):
            return questions
        elif isinstance(questions, dict) and "questions" in questions:
            return questions["questions"]
    except (json.JSONDecodeError, AttributeError):
        pass
    return parse_questions_manually(output_text)


def parse_questions_manually(text: str) -> List[Dict[str, str]]:
    """
    Extract question lines manually if no JSON is found.
    """
    questions = []
    lines = text.split('\n')
    current_category = "General"

    for line in lines:
        line = line.strip()
        if any(cat in line.lower() for cat in ["technical", "skills"]):
            current_category = "Technical Skills"
        elif "experience" in line.lower():
            current_category = "Experience"
        elif "project" in line.lower():
            current_category = "Projects"
        elif "problem" in line.lower():
            current_category = "Problem Solving"

        if line.endswith('?') or any(keyword in line.lower() for keyword in ['explain', 'describe', 'tell me']):
            clean_question = line.lstrip('-*0123456789. ').strip()
            if len(clean_question) > 10:
                questions.append({
                    "question": clean_question,
                    "category": current_category
                })

    return questions[:10]
