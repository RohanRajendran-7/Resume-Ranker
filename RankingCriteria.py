from google import genai
from google.genai.types import HttpOptions
from google.genai import types
from dotenv import load_dotenv
import os


def create_criteria(clean_text):
    load_dotenv()

    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

    if GEMINI_API_KEY is None:
        raise ValueError("API_KEY not found")

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=f"Extract the key ranking criteria based on the job responsibilites and requirements given.\n\nJob Description\n{clean_text}",
        config=types.GenerateContentConfig(
            system_instruction='Make sure to include the mandatory/minimum requirements and the preferred qualifications.Do not provide any comments, headers or information which is not present in the input. Mention the points as bullet points - *', 
            temperature=0.1,
        ),
    )
    criteria_text = response.text.replace('*', '')
    criteria_list = [point.strip() for point in criteria_text.strip().split("\n")]
    return(criteria_list)
