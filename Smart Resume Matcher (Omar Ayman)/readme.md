# 🤖 **Smart Resume Matcher**  

An AI-powered assistant that helps you apply for jobs faster.  
Let this be your AI buddy who handles the boring stuff:  
- Reads job descriptions  
- Checks your resume's compatibility  
- Writes cover letters for you — and might even apply on your behalf  

## All you have to do is sit back and land that dream job.  

- You can try the deployed AI Career Assistant app here:  
👉 [AI Career Assistant on Streamlit](https://ai-career-assistant-f46zxnj2odffryrscbfaur.streamlit.app/)

- Read more about the project on LinkedIn:  
👉 [View LinkedIn Announcement](https://www.linkedin.com/posts/your-post-id)
---

## **Real-World Problem**  

Job seekers often waste hours:  
- Reading lengthy job descriptions  
- Manually tweaking resumes  
- Writing cover letters from scratch  
- Filling out repetitive application forms  

---

## **Project Goal**  

Create a multi-agent AI system that, given a **job title** or **job posting URL**, can:  
1. **Extract** job requirements (skills, experience, tools)  
2. **Match** them with your resume and highlight gaps  
3. **Generate** a personalized, compelling cover letter  

---

# **Agents Overview**  

##  **Agent 1 – Job Description Parser**  
**Purpose:** Extract key data from job descriptions.  
- **Input:** Raw job text or job posting URL  
- **Output:** Structured JSON with:  
  - Required skills  
  - Required years of experience  
  - Keywords  
  - Preferred tools/technologies  

**Powered by:** LLMs  

---

##  **Agent 2 – Resume ↔ Job Skill Matcher**  
**Purpose:** Match your resume to job requirements.  
- **Input:** User resume and job data  
- **Output:**  
  - ✅ Match score (e.g., 76%)  
  - ✅ Strengths (skills you have)  
  - ✅ Gaps (skills you're missing)  
  - ✅ Recommendations  

*Instantly shows how well you fit the role.*  

---

##  **Agent 3 – Cover Letter Generator**  
**Purpose:** Create a personalized cover letter.  
- **Input:** Job data + resume data  
- **Output:** Professional, job-specific cover letter  
