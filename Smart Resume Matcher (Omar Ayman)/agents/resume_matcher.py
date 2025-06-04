from rapidfuzz import fuzz
from typing import List, Dict, Set

class MatchAgent:
    def __init__(self, threshold: float = 51.0):
        self.threshold = threshold

    def _is_similar(self, skill1: str, skill2: str) -> bool:
        return fuzz.token_sort_ratio(skill1.lower().strip(), skill2.lower().strip()) >= self.threshold

    def _normalize_skills(self, skills: List[str]) -> Set[str]:
        return set(skill.strip().lower() for skill in skills if skill)

    def run(self, resume_data: Dict, job_data: Dict) -> Dict:
        resume_skills = self._normalize_skills(resume_data.get("skills", []))
        job_skills = self._normalize_skills(job_data.get("required_skills", []))

        matched = set()
        unmatched = set(job_skills)

        for job_skill in job_skills:
            if any(self._is_similar(job_skill, resume_skill) for resume_skill in resume_skills):
                matched.add(job_skill)
                unmatched.discard(job_skill)

        score = int((len(matched) / len(job_skills)) * 100) if job_skills else 0

        return {
            "match_score": score,
            "missing_skills": sorted(unmatched),
            "strengths": sorted(matched),
            "recommendations": (
                f"🧠 Consider learning: {', '.join(sorted(unmatched))}"
                if unmatched else "✅ You are a great fit for this role!"
            )
        }
