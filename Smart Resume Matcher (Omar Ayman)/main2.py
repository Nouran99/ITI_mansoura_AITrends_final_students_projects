from agents.resume_matcher import MatchAgent

resume_info = {
    "skills": ["Python", "Django", "SQL", "Git"]
}

job_info = {
    "required_skills": ["Python", "Django", "REST APIs", "PostgreSQL"]
}

if __name__ == "__main__":
    agent = MatchAgent()
    result = agent.run(resume_info, job_info)
    print("🎯 Match Report:")
    print(result)

