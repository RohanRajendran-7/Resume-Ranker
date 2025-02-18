from RankingCriteria import create_criteria
import os,fitz,re,io
from extractText import extract_document, clean_text_jd

criteria_dict = {}
file_types = ["pdf", "docx"]

def text_process(data):
    global criteria_dict
    combined_text = ''

    for page in data['texts']:
        page_text = page['text']
        cleaned_page_text = clean_text_jd(page_text)
        combined_text += cleaned_page_text

    criteria_list = create_criteria(combined_text)
    criteria_dict = {
        "criteria": criteria_list
    }
    return (criteria_dict)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in file_types

def createcsv(response):
    csv_file_path = 'resume_scores.csv'

    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=response[0].keys())
        writer.writeheader()
        
        for row in response:
            writer.writerow(row)