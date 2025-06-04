import random

class CoverLetterAgent:
    def __init__(self, user_name="Omar Ayman"):
        self.user_name = user_name
    def run(self, job_info: dict, resume_info: dict, position_title="the open role", tone="Professional", extra_context="") -> str:
        strengths = resume_info.get("skills", [])
        job_skills = job_info.get("required_skills", [])
        preferred_tech = job_info.get("preferred_tools_or_technologies", [])
        overlap = set(strengths).intersection(set(job_skills))
        overlap_list = ", ".join(overlap) if overlap else "my background in AI and related technologies"
        top_strengths = ", ".join(strengths[:3]) if strengths else "machine learning, data science, and software development"
        tech_focus = ", ".join(preferred_tech) if preferred_tech else "cutting-edge tools and emerging platforms"
        user_name = self.user_name
        templates = [
            f"""Dear Hiring Manager,

I am writing to express my strong interest in the {position_title} role at your esteemed organization.
My background in {overlap_list}, combined with experience in {top_strengths}, positions me well to contribute to your team’s goals.
Throughout my career, I have pursued meaningful challenges and continuously expanded my capabilities.
I’m especially excited by your use of {tech_focus}, and I look forward to applying my skills in a collaborative, forward-thinking environment.
Thank you for your time and consideration. I would be honored to bring my passion and expertise to your organization.


Best regards,
{user_name}
""",
            f"""Dear Hiring Manager,

I am excited to submit my application for the {position_title} role. With a foundation in {overlap_list} and proven strengths in {top_strengths},
I bring a blend of technical knowledge and collaborative spirit that aligns well with your team’s mission.
Your organization’s focus on innovation and excellence—especially in areas like {tech_focus}—resonates deeply with my professional values. I am confident that my background will allow me to contribute meaningfully from day one.
Thank you for your consideration.I look forward to the opportunity to grow and contribute with your team.


Best regards,
{user_name}
""",
            f"""Dear Hiring Manager,

It is with great enthusiasm that I apply for the {position_title} position.
My background in {overlap_list} and practical experience in {top_strengths} equip me with the tools to thrive in a fast-paced, evolving environment.
I’m especially inspired by your use of {tech_focus} and believe that your company’s vision perfectly complements my skills and career ambitions.
I am ready to bring value and grow within your innovative team.
Thank you for considering my application.


Best regards,
{user_name}
""",
            f"""Dear Hiring Manager,

As a passionate professional with a strong foundation in {overlap_list},I’m excited to apply for the {position_title} position.
Whether working independently or within a dynamic team, I thrive on solving real-world challenges using tools like {tech_focus}.
With hands-on experience in {top_strengths}, I bring both creativity and technical rigor to everything I do. I’m eager to grow with a team that values innovation and purpose.
Thank you for considering my application. I look forward to the opportunity to make a meaningful contribution.


Best regards,
{user_name}
""",
            f"""Dear Hiring Team,

I’m excited to apply for the {position_title} opportunity.
I bring a proven track record in {overlap_list} and have consistently delivered results through skills such as {top_strengths}.
Your focus on {tech_focus} aligns perfectly with my enthusiasm for cutting-edge technologies.
I’m eager to bring my energy, expertise, and adaptability to help achieve your goals.

I would welcome the chance to further discuss how I can support your mission.

Best regards,
{user_name}
""",
            f"""Dear Hiring Manager,

I’m thrilled to express my interest in the {position_title} role.
My background in {overlap_list} and hands-on experience with {top_strengths} make me confident in my ability to learn fast and contribute meaningfully.
While I bring a strong foundation,I’m equally driven by the opportunity to grow.
I’m especially excited by the chance to work with technologies like {tech_focus}, and I’m confident I can bring value to your team from day one.
Thank you for considering my application.


Best regards,
{user_name}
"""
        ]

        return random.choice(templates)
