from services.gemini_service import generate_response


def generate_interview_questions(resume_text: str) -> str:
    """Use Gemini to generate interview questions tailored to the resume."""
    prompt = f"""
You are an expert technical interviewer. Based on the resume below, generate 10 relevant interview questions.

Include a mix of:
- Technical questions based on skills mentioned
- Behavioural questions (STAR format)
- Project/experience based questions

Format each question on a new line with a number prefix (e.g. "1. ...").

Resume:
{resume_text[:3000]}
"""
    return generate_response(prompt)
