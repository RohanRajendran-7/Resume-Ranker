import os,fitz,re,io

file_types = ["pdf", "docx"]


def extract_document(file, file_extension):
    data = {
        'texts':[]
    }

    if not file_extension in file_types:
        print(f"FILE FORMAT NOT SUPPORTED ({file_extension})")
        return data

    jobDescription = fitz.open(stream = file.read(), filetype = file_extension)

    for page_no in range(len(jobDescription)):
        page = jobDescription[page_no]
        data['texts'].append({'text':page.get_text(),'page_no':page_no})

    return data 

def clean_text_jd(text):
    cleaned_text = text.replace('\n', ' ').replace('\r', '')
    
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    cleaned_text = cleaned_text.strip()
    
    return cleaned_text

def clean_text_resume(text):
    # Remove new line characters
    cleaned_text = text.replace('\n', ' ').replace('\r', '')
    # Remove multiple underscores and new line characters
    cleaned_text = re.sub(r"(__+|\n•\s*)", "", text)
    section_headers = re.findall(r"\b[A-Z][A-Z\s]+(?:\b)", cleaned_text)

    # Add new line before each section header
    for header in section_headers:
        cleaned_text = re.sub(rf"({header})", r"\n\1\n", cleaned_text)

    # formatting for bullet points
    cleaned_text = re.sub(r"([A-Za-z]),\n([A-Za-z])", r"\1, \2", cleaned_text)
    cleaned_text = re.sub(r"\n\s*\n", "\n", cleaned_text)
    
    return cleaned_text