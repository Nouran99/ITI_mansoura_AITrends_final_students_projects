from crewai.tools import BaseTool
from pydantic import BaseModel
from typing import Type, Dict, List

class JobProfileToolArgs(BaseModel):
    """Input schema for JobProfileTool."""
    job_title: str
    job_description: str = ""

class JobProfileTool(BaseTool):
    name: str = "job_profile_tool"
    description: str = "Maps job titles and descriptions to expected technical skills and responsibilities."
    args_schema: Type[JobProfileToolArgs] = JobProfileToolArgs

    def _run(self, job_title: str, job_description: str = "") -> str:
        """Extract technical expectations based on job title and description."""
        # Base mapping by job title
        mapping: Dict[str, List[str]] = {
            "Machine Learning Engineer": [
                "Python", "TensorFlow", "PyTorch", "Model Evaluation", "Feature Engineering", "Data Preprocessing"
            ],
            "Data Scientist": [
                "Python", "R", "SQL", "Statistical Analysis", "Data Visualization", "Machine Learning"
            ],
            "Software Engineer": [
                "Programming Languages (Java/Python/C++)", "Data Structures", "Algorithms",
                "Software Design", "Testing", "Version Control"
            ],
            "Frontend Developer": [
                "HTML/CSS", "JavaScript", "React/Angular/Vue", "Responsive Design", "UI/UX Principles"
            ],
            "Backend Developer": [
                "Server Languages (Python/Java/Node.js)", "Databases", "API Design",
                "Authentication", "Server Management"
            ],
            "DevOps Engineer": [
                "CI/CD", "Docker", "Kubernetes", "Cloud Services", "Infrastructure as Code", "Monitoring"
            ]
        }

        # Look up skills for the given job title
        if job_title in mapping:
            skills = mapping[job_title]
        else:
            skills = [
                "Problem-solving",
                "Technical aptitude", 
                "Communication skills",
                "Teamwork",
                "Adaptability"
            ]
        
        # Format the response as structured data
        response = {
            "job_title": job_title,
            "required_skills": skills,
            "responsibilities": ["Responsibility analysis would be based on job description"],
            "knowledge_areas": ["Knowledge areas extracted from skills and job description"],
            "preferred_tools": ["Tools commonly used with the identified skills"]
        }
        
        # Add job description analysis if provided
        if job_description:
            response["job_description_analysis"] = f"Analysis of provided job description: {job_description[:100]}..."
            
        return str(response)

    def _arun(self, job_title: str, job_description: str = "") -> str:
        """Run the tool asynchronously."""
        raise NotImplementedError("This tool does not support async")