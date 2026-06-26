import os
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_response(prompt: str) -> str:
    """Send a prompt to Gemini and return the text response."""
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"
