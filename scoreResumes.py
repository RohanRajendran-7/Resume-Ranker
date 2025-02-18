from google import genai
from google.genai.types import HttpOptions
from google.genai import types
from dotenv import load_dotenv
import os,fitz,csv
from extractText import extract_document, clean_text_resume

file_types = ["pdf", "docx"]
all_rows = [] 


def resume_text(file_extension,resume,file_name):
    combined_text = ''
    extracted_text = extract_document(resume, file_extension)
    print(f"*"*40,extracted_text)
    for page in extracted_text['texts']:
        page_text = page['text']
        cleaned_page_text = clean_text_resume(page_text)
        combined_text += cleaned_page_text
    print(combined_text)
    return combined_text 

def rank_resume(clean_text, criteria, all_rows):
    load_dotenv()

    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    csv_file_path = 'resume_scores.csv'

    if GEMINI_API_KEY is None:
        raise ValueError("API_KEY not found")

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=f"Please evaluate the resume based on the following criteria:\n{criteria}\n\nResume Text:\n{clean_text}",
        config=types.GenerateContentConfig(
            system_instruction=""" 
            Score the resume based on the given criteria. Give the score out of 10 with a short column name based on each criteria. 
            Do not provide any comments or information which is not present in the input. 
            Include a column for total score and the value should be the sum of all the scores.
            Give the result as comma separated and group by the full name
            """, 
            temperature=0.1,
        ),
    )
    criteria_text = response.text.strip()
    rows = [row.split(',') for row in criteria_text.split('\n')]

    # Add new rows to all_rows
    if not all_rows: 
        print("No rows")
        all_rows.extend(rows)
    else: 
        print(all_rows)
        all_rows.extend(rows[1:])

    return all_rows

