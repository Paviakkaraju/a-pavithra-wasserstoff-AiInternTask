import os
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter 
import re
import asyncio
from pymongo import MongoClient

def extract_text(path):
    with open(path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''

        for pagenum in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[pagenum]
            text += page.extract_text()

        return text

def clean(text, top_n=10):
    cleaned1 = re.sub(r'[\s+]', ' ', text)
    cleaned2 = re.sub(r"\([^)]*\)", "", cleaned1.lower())
    cleaned3 = re.sub(r"\n", " ", cleaned2)
    clean_words = re.sub(r'[0-9.-_;:"",/-]',"", cleaned3)

    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [w for w in words if w not in stop_words]

    word_freq = Counter(filtered_words)
    keywords = [word for word, freq in word_freq.most_common(top_n)]
    return keywords


client = MongoClient("mongodb://localhost:27017/")
database_name = "intern_task"
collection_name = "documents"
pdf_collection = client["intern_task"]["documents"]

#async def insert_document(client, database_name, collection_name, document):
    #db = client[database_name]
    #collection = db[collection_name]
    #result = await collection.insert_one(document)
    #print(f"Inserted document with ID: {result.inserted_id}")
    
async def process_pdf(file_path, client, database_name, collection_name):
    db = client[database_name]
    collection = db[collection_name]

    # Check if the document exists and has keywords
    existing_doc = collection.find_one({'file_path': file_path})
    if existing_doc and 'keywords' in existing_doc:
        print(f"Document details and keywords already available for {file_path}")
        return
    
    
async def update_keywords_in_db(file_path, keywords, client, database_name, collection_name):
    result = await client[database_name][collection_name].update_one(
        {'file_path': file_path},
        {'$set': {'keywords': keywords}}
    )

    if result.modified_count > 0:
        print(f"Keywords extracted and updated for {file_path}")
    else:
        print(f"Document already updated or error occurred for {file_path}")

