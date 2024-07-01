import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from azure.storage.blob import BlobServiceClient
import json
from dotenv import load_dotenv
import os
from GoogleCustomDocAI import process_document
# enabling flask
app = Flask(__name__)
CORS(app)
load_dotenv()

PROJECT_ID = os.getenv('project_id')
LOCATION = os.getenv('location')
PROCESSOR_ID = os.getenv('processor_id')

def extract_pdf_document(file):
    if file.filename == '':
        print("No file selected for uploading")
        print(f"File uploaded: {file.filename}")
        return {"error": "No selected file"}, 400
    # Save the file to a temporary location
    temp_dir = tempfile.gettempdir()
    pdf_file_path = os.path.join(temp_dir, file.filename)
    file.save(pdf_file_path)
    # Extract text from PDF
    try:
        entities = process_document(PROJECT_ID, LOCATION, PROCESSOR_ID, pdf_file_path)
        return entities, 200
    except Exception as extraction_error:
        print(f"Error extracting text from PDF: {str(extraction_error)}")
        return {"error": f"Error extracting text from PDF: {str(extraction_error)}"}, 500
    finally:
        # Clean up the temporary file
        if os.path.exists(pdf_file_path):
            os.remove(pdf_file_path)
@app.route('/home', methods=['GET'])
def home():
    return ({"response" : "Hello from the backend"})


@app.route('/upload', methods=['POST'])
def upload_file():
    select_option = request.form.get('selectOption')
    pdf_file1 = request.files.get('pdfFile1')
    pdf_file2 = request.files.get('pdfFile2')

    # Process the received data as needed
    print(f"Selected option: {select_option}")
    print(f"PDF File 1: {pdf_file1.filename if pdf_file1 else 'No file'}")
    print(f"PDF File 2: {pdf_file2.filename if pdf_file2 else 'No file'}")

    combined_results = []

    try:
        if select_option == 'LeasingDoc':
            if not pdf_file1:
                print("No file part in the request")
                return jsonify({"error": "No file part"}), 400
            response, status_code = extract_pdf_document(pdf_file1)
            if status_code == 200:
                combined_results.extend(response)
            else:
                return jsonify(response), status_code
        elif select_option == 'compare-gst':
            if not pdf_file1:
                print("No file part in the request")
                return jsonify({"error": "No file part"}), 400
            response1, status_code1 = extract_pdf_document(pdf_file1)
            if status_code1 == 200:
                combined_results.extend(response1)
            else:
                return jsonify(response1), status_code1
            if not pdf_file2:
                print("No second file part in the request")
                return jsonify({"error": "No second file part"}), 400
            response2, status_code2 = extract_pdf_document(pdf_file2)
            if status_code2 == 200:
                combined_results.extend(response2)
            else:
                return jsonify(response2), status_code2
        return jsonify(combined_results)
    except Exception as upload_error:
        print(f"Error processing upload: {str(upload_error)}")
        return jsonify({"error": f"Error processing upload: {str(upload_error)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
