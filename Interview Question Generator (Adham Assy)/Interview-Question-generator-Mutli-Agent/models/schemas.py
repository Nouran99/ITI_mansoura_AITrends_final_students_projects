# models/schemas.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class CVContext(BaseModel):
    """Schema for CV data context."""
    cv_text: str = Field(..., description="The text content of the CV")

class JobContext(BaseModel):
    """Schema for job data context."""
    job_title: str = Field(..., description="The job title")
    job_description: str = Field("", description="The job description")

class QuestionContext(BaseModel):
    """Schema combining CV and job data for question generation."""
    cv_text: str = Field(..., description="The text content of the CV")
    job_title: str = Field(..., description="The job title")
    job_description: str = Field("", description="The job description")

class InterviewQuestion(BaseModel):
    """Schema for a single interview question."""
    question: str = Field(..., description="The text of the interview question")
    category: str = Field(..., description="The category of the interview question (e.g., 'Skills', 'Experience')")

class InterviewQuestionList(BaseModel):
    """Schema for a list of interview questions."""
    questions: List[InterviewQuestion] = Field(..., description="List of interview questions")

class Skill(BaseModel):
    """Schema for a technical skill."""
    name: str = Field(..., description="Name of the skill")
    proficiency: Optional[str] = Field(None, description="Proficiency level if available")

class Education(BaseModel):
    """Schema for educational background."""
    degree: str = Field(..., description="Degree obtained")
    field: str = Field(..., description="Field of study")
    institution: str = Field(..., description="Educational institution")
    year: Optional[str] = Field(None, description="Year of completion")

class Project(BaseModel):
    """Schema for a technical project."""
    title: str = Field(..., description="Project title")
    description: str = Field(..., description="Brief description of the project")
    technologies: List[str] = Field(default_factory=list, description="Technologies used")

class Experience(BaseModel):
    """Schema for work experience."""
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    period: str = Field(..., description="Employment period")
    responsibilities: List[str] = Field(default_factory=list, description="Key responsibilities")
    
class CVData(BaseModel):
    """Schema for structured CV data."""
    skills: List[Skill] = Field(default_factory=list, description="Technical skills")
    education: List[Education] = Field(default_factory=list, description="Educational background")
    projects: List[Project] = Field(default_factory=list, description="Technical projects")
    courses: List[str] = Field(default_factory=list, description="Relevant courses and certifications")
    experience: List[Experience] = Field(default_factory=list, description="Work experience")

class JobProfile(BaseModel):
    """Schema for job profile data."""
    required_skills: List[str] = Field(default_factory=list, description="Required technical skills")
    preferred_tools: List[str] = Field(default_factory=list, description="Preferred tools and technologies")
    knowledge_areas: List[str] = Field(default_factory=list, description="Key knowledge areas")
    responsibilities: List[str] = Field(default_factory=list, description="Key responsibilities")
    prerequisites: List[str] = Field(default_factory=list, description="Prerequisites for the role")