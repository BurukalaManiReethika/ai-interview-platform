import re

# Common tech skills to look for in resumes
KNOWN_SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go",
    "rust", "php", "swift", "kotlin", "r", "scala", "sql", "html", "css",
    "flask", "django", "fastapi", "react", "angular", "vue", "node", "express",
    "spring", "laravel", "rails",
    "postgresql", "mysql", "sqlite", "mongodb", "redis", "elasticsearch",
    "docker", "kubernetes", "aws", "gcp", "azure", "terraform", "ansible",
    "git", "linux", "rest", "graphql", "grpc",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
    "communication", "teamwork", "leadership", "problem solving",
    "agile", "scrum", "jira", "ci/cd"
]

# Skills considered important for most roles
IMPORTANT_SKILLS = [
    "python", "sql", "git", "rest", "docker", "communication",
    "problem solving", "agile"
]


def extract_skills(resume_text: str) -> list[str]:
    """Return a list of skills found in the resume text."""
    text_lower = resume_text.lower()
    found = []
    for skill in KNOWN_SKILLS:
        # Use word-boundary matching to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)
    return found


def missing_skills(found_skills: list[str]) -> list[str]:
    """Return important skills that are absent from the resume."""
    found_lower = [s.lower() for s in found_skills]
    return [s for s in IMPORTANT_SKILLS if s not in found_lower]


def calculate_ats_score(resume_text: str) -> int:
    """
    Calculate a simple ATS score (0–100) based on:
    - Number of recognised skills found
    - Presence of key resume sections
    - Length / content density
    """
    score = 0
    text_lower = resume_text.lower()

    # Skills (up to 50 points)
    found_skills = extract_skills(resume_text)
    skill_points = min(len(found_skills) * 3, 50)
    score += skill_points

    # Key sections (up to 30 points)
    sections = ["experience", "education", "skills", "projects", "summary", "objective"]
    for section in sections:
        if section in text_lower:
            score += 5

    # Content length (up to 20 points)
    word_count = len(resume_text.split())
    if word_count >= 300:
        score += 20
    elif word_count >= 150:
        score += 10
    elif word_count >= 50:
        score += 5

    return min(score, 100)
