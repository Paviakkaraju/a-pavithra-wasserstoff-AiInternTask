import os
from PyPDF2 import PdfReader
import hashlib
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import asyncio

# Metadata to be updated
def get_metadata(file_path):
    with open(file_path, 'rb') as pdf:
        reader = PdfReader(pdf)
        meta_data = {
            'doc_name': os.path.basename(file_path),
            'location': file_path,
            'size_in_bytes': os.path.getsize(file_path),
            'number_of_pages': len(reader.pages),
            'file_processed_on': datetime.now().isoformat()
        }
    return meta_data

# Establishing a MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["pdf_reader"]
collection = db["pdf_collections"]

# Updating the Metadata
async def update_metadata_async(pdf_path, metadata):
    result = collection.find_one({"location": pdf_path})
    if result and "metadata" in result and result["metadata"]:
        return
    collection.update_one({"location": pdf_path}, {"$set": {"metadata": metadata}}, upsert=True)

# Updating the Keywords
async def update_keywords_async(pdf_path, keywords):
    result = collection.find_one({"location": pdf_path})
    if result and "keywords" in result and result["keywords"]:
        return
    collection.update_one({"location": pdf_path}, {"$set": {"keywords": keywords}}, upsert=True)

# Updating the Summary
async def update_summary_async(pdf_path, summary):
    result = collection.find_one({"location": pdf_path})
    if result and "summary" in result and result["summary"]:
        return
    collection.update_one({"location": pdf_path}, {"$set": {"summary": summary}}, upsert=True)
