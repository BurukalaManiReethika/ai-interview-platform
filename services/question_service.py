from services.gemini_service import generate_response


def generate_interview_questions(resume_text):

    prompt = f"""
    Analyze this resume.

    Generate:

    15 Technical Questions

    10 HR Questions

    10 Project Based Questions

    5 Coding Questions

    Resume:

    {resume_text}
    """

    return generate_response(prompt)
