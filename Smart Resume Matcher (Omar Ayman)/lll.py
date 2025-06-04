from agents.cover_letter_writer import CoverLetterAgent

job_info = {
    "required_skills": ["Python", "TensorFlow", "Machine Learning"],
    "preferred_tools_or_technologies": ["Docker", "GCP"]
}

resume_info = {
    "skills": ["Python", "SQL", "Machine Learning", "Pandas"]
}

if __name__ == "__main__":
    agent = CoverLetterAgent(user_name="Omar Ayman")
    letter = agent.run(job_info, resume_info, position_title="ML Engineer")
    print("📄 Generated Cover Letter:\n")
    print(letter)