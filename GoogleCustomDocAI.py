from google.cloud import documentai_v1beta3 as documentai
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from azure.storage.blob import BlobServiceClient
import json

load_dotenv()

AZURE_CONNECTION_STRING = os.getenv('connection_string')
AZURE_CONTAINER_NAME = os.getenv('container_name')
AZURE_BLOB_NAME = os.getenv('blob_name')
#print("Azure storage credentials",AZURE_CONNECTION_STRING,AZURE_CONTAINER_NAME,AZURE_BLOB_NAME)

pdf_file_path = "Cust_pdf.pdf"


# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=AZURE_BLOB_NAME)

# Download the blob content as bytes
blob_data = blob_client.download_blob().readall()

# Decode the bytes into a string (assuming it's JSON content)
blob_content = blob_data.decode('utf-8')

# Parse the JSON content
json_content = json.loads(blob_content)

# Specify the target directory where you want to save the JSON file
target_directory = os.path.join(os.getcwd(), "Final Backend")

# Ensure the target directory exists; create if it doesn't
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

# Construct the file path in the target directory
custom_document_ai_json_file_path = os.path.join(target_directory, "custom_document_ai.json")

# Check if the file already exists
if os.path.exists(custom_document_ai_json_file_path):
    # If it exists, delete the file
    os.remove(custom_document_ai_json_file_path)
    #print(f"Existing file '{custom_document_ai_json_file_path}' deleted.")

# Write content to the JSON file
with open(custom_document_ai_json_file_path, 'w') as file:
    json.dump(json_content, file, indent=2)

#print(f"New file '{custom_document_ai_json_file_path}' created successfully.")
AZURE_CONNECTION_STRING = os.getenv('connection_string')
AZURE_CONTAINER_NAME = os.getenv('container_name')
AZURE_BLOB_NAME = os.getenv('blob_name')
#print("Azure storage credentials",AZURE_CONNECTION_STRING,AZURE_CONTAINER_NAME,AZURE_BLOB_NAME)

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=AZURE_BLOB_NAME)

# Download the blob content as bytes
blob_data = blob_client.download_blob().readall()

# Decode the bytes into a string (assuming it's JSON content)
blob_content = blob_data.decode('utf-8')

# Parse the JSON content
json_content = json.loads(blob_content)

# Specify the target directory where you want to save the JSON file
target_directory = os.path.join(os.getcwd(), "Final Backend")

# Ensure the target directory exists; create if it doesn't
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

# Construct the file path in the target directory
custom_document_ai_json_file_path = os.path.join(target_directory, "custom_document_ai.json")

# Check if the file already exists
if os.path.exists(custom_document_ai_json_file_path):
    # If it exists, delete the file
    os.remove(custom_document_ai_json_file_path)
    #print(f"Existing file '{custom_document_ai_json_file_path}' deleted.")

# Write content to the JSON file
with open(custom_document_ai_json_file_path, 'w') as file:
    json.dump(json_content, file, indent=2)

#print(f"New file '{custom_document_ai_json_file_path}' created successfully.")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "custom_document_ai.json"

def process_document(project_id, location, processor_id, file_path):
    
    # Create a Document AI client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    name = f'projects/{project_id}/locations/{location}/processors/{processor_id}'
    # Read the file into memory
    with open(file_path, 'rb') as image:
        image_content = image.read()

    # Load the document content into a raw document object
    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")

    # Use the document AI client to process the document
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)

    # Get the document text and entities
    document = result.document
    document_text = document.text

    # Extract the entities
    entities = []
    for entity in document.entities:
        entities.append({
            "type": entity.type_,
            "mention_text": entity.mention_text,
            "confidence": entity.confidence,
        })

    return entities


#document_text, entities = process_document(PROJECT_ID, LOCATION, PROCESSOR_ID, file_path)

# print("Document Text:", document_text)
#print("Extracted Entities:", entities)