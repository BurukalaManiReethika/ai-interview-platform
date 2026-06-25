import re


def calculate_ats_score(resume_text):

    score = 0

    sections = [
        "education",
        "skills",
        "projects",
        "experience",
        "certifications"
    ]

    for section in sections:

        if section.lower() in resume_text.lower():
            score += 20

    return min(score, 100)


def extract_skills(resume_text):

    predefined_skills = [

        "python",
        "java",
        "c",
        "c++",
        "javascript",
        "html",
        "css",
        "react",
        "flask",
        "django",
        "sql",
        "mysql",
        "mongodb",
        "machine learning",
        "deep learning",
        "nlp",
        "git",
        "github",
        "aws"
    ]

    found = []

    for skill in predefined_skills:

        if skill.lower() in resume_text.lower():
            found.append(skill)

    return list(set(found))


def missing_skills(found_skills):

    market_skills = [

        "python",
        "sql",
        "git",
        "github",
        "aws",
        "docker",
        "rest api",
        "data structures",
        "oop"
    ]

    missing = []

    for skill in market_skills:

        if skill not in found_skills:
            missing.append(skill)

    return missing
