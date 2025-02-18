from flask import Flask, request, jsonify
from jobDescription import text_process, allowed_file
from extractText import extract_document
from scoreResumes import resume_text, rank_resume
import json,csv
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/extract-criteria', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file found', 400

    file = request.files['file']
    
    if file.filename == '':
        return 'Empty File', 400

    
    if file and allowed_file(file.filename):
        filename = file.filename
        file_extension = filename.rsplit('.', 1)[1].lower()
        extracted_text = extract_document(file, file_extension)
        criteria = text_process(extracted_text) 
        return criteria
    else:
        return 'File type not allowed', 400

@app.route('/score-resumes', methods=['POST'])
def score_resumes():
    total_rank = ''
    criteria_str = request.form.get('criteria')
    if not criteria_str:
        return jsonify({"error": "No criteria in request"}), 400

    try:
        criteria = json.loads(criteria_str)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in criteria"}), 400

    if not isinstance(criteria, dict) or 'criteria' not in criteria:
        return jsonify({"error": "Criteria is not valid"}), 400

    if 'file' not in request.files:
        return 'No file found', 400

    files = request.files.getlist('file')
    
    if len(files) == 0:
        return 'No files uploaded', 400

    uploaded_files = {}

    for file in files:
        if file.filename == '':
            return 'Empty file found', 400
        
        filename = file.filename     
        file_extension = filename.rsplit('.', 1)[1].lower()
        uploaded_files[filename] = {
            'file': file,
            'filename': filename,
            'extension': file_extension
        }

    all_rows = [] 
    for file in uploaded_files:
        final_data = resume_text(uploaded_files[file]['extension'], uploaded_files[file]['file'], uploaded_files[file]['filename'])
        all_rows = rank_resume(final_data, criteria, all_rows)  

    with open('resume_scores.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_rows)

    return jsonify({"message": "Resumes ranked and saved to CSV."})


if __name__ == '__main__':
    app.run(debug=True)