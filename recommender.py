"""Transparent rule-based career matching prototype (not a trained AI model)."""

CAREERS = {
    "Software Developer": {
        "interests": ["software", "coding", "development", "technology", "apps"],
        "skills": ["python", "java", "c", "problem solving", "javascript"]
    },
    "Data Analyst": {
        "interests": ["data", "analysis", "statistics", "business"],
        "skills": ["python", "sql", "excel", "statistics", "visualization"]
    },
    "Cybersecurity Analyst": {
        "interests": ["security", "network", "cyber", "ethical hacking"],
        "skills": ["networking", "linux", "python", "security", " problem solving"]
    },
    "UI/UX Designer": {
        "interests": ["design", "creative", "interface", "visual"],
        "skills": ["figma", "design", "creativity", "prototyping"]
    },
    "Cloud / DevOps Engineer": {
        "interests": ["cloud", "automation", "infrastructure", "deployment"],
        "skills": ["linux", "git", "python", "networking", "docker"]
    },
    "AI / Machine Learning Engineer": {
        "interests": ["artificial intelligence", "machine learning", "data", "automation"],
        "skills": ["python", "mathematics", "statistics", "machine learning"]
    }
}

def recommend_careers(interests, skills, education="Undergraduate"):
    interest_text = interests.lower()
    skill_set = {s.strip().lower() for s in skills}
    scored = []
    for career, profile in CAREERS.items():
        interest_hits = sum(1 for word in profile["interests"] if word in interest_text)
        skill_hits = sum(1 for skill in profile["skills"] if skill in skill_set)
        total_possible = len(profile["interests"]) + len(profile["skills"])
        score = round(((interest_hits + skill_hits) / total_possible) * 100)
        scored.append({
            "career": career,
            "score": score,
            "matched_interests": interest_hits,
            "matched_skills": skill_hits,
            "reason": f"{skill_hits} relevant skill match(es) and {interest_hits} interest match(es)."
        })
    return sorted(scored, key=lambda item: item["score"], reverse=True)[:3]
