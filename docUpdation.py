import os
from PyPDF2 import PdfReader
import hashlib
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import asyncio

# Updating the metadata in MongoDB
client = MongoClient("mongodb://localhost:27017/")
database_name = "intern_task"
collection_name = "documents"
pdf_collection = client["intern_task"]["documents"]


async def insert_document(client, database_name, collection_name, document):
    db = client[database_name]
    collection = db[collection_name]
    result = collection.insert_one(document)
    print(f"Inserted document with ID: {result.inserted_id}")


async def process_pdf(file_path, client, database_name, collection_name):
    # Check if PDF is already processed based on hash
    if check_pdf(file_path):
        print(f"Document details already available for {file_path}!")
        return

    # Extract metadata and calculate hash
    meta_data, _ = metadata(file_path)
    with open(file_path, 'rb') as f:
        meta_data['file_hash'] = hashlib.md5(f.read()).hexdigest()

    # Insert document asynchronously
    await insert_document(client, database_name, collection_name, meta_data)
    print(f'Added {os.path.basename(file_path)} to the database')


def metadata(file_path):
    with open(file_path, 'rb') as pdf:
        reader = PdfReader(pdf)
        meta_data = {
            'doc_name': os.path.basename(file_path),
            'location': file_path,
            'size_in_bytes': os.path.getsize(file_path),
            'number_of_pages': len(reader.pages),
            'file_processed_on': datetime.now().isoformat()
        }
    return meta_data, pdf


def check_pdf(file_path):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    return pdf_collection.find_one({'file_hash': file_hash}) is not None
