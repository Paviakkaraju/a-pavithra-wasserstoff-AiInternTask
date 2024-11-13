import os
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter 
import re
import asyncio
from pymongo import MongoClient

def extract_text(path):
    with open(path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        
        global pages
        pages = len(pdf_reader.pages)

        for pagenum in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[pagenum]
            text += page.extract_text()

    return text

def get_keywords(text, top_n=10):
    cleaned1 = re.sub(r'[\s+]', ' ', text)
    cleaned2 = re.sub(r"\([^)]*\)", "", cleaned1.lower())
    cleaned3 = re.sub(r"\n", " ", cleaned2)
    clean_words = re.sub(r'[0-9.-_;:""'',/-]',"", cleaned3)

    stop_words = set(stopwords.words('english'))
    words = word_tokenize(clean_words.lower())
    filtered_words = [w for w in words if w not in stop_words]

    word_freq = Counter(filtered_words)
    keywords = [word for word, freq in word_freq.most_common(top_n)]
    return keywords
