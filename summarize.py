import os
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter 
import re
import asyncio
from pymongo import MongoClient
import numpy as np

# Extracts the text from the PDF
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

# Pre-processing and Extractive Summarization of the text
def summarize(text):
    
    cleaned1 = re.sub(r'[\s+]', ' ', text)
    cleaned2 = re.sub(r"\([^)]*\)", "", cleaned1.lower())
    cleaned3 = re.sub(r"\n", " ", cleaned2)
    clean_sent = re.sub(r'[0-9-_;:""'',/-]',"", cleaned3)
    
    if pages <= 5:
        num_sentences=3
    elif pages >5 and pages<=15:
        num_sentences = 5
    else:
        num_sentences = 7

    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(clean_sent)

    # Create a simple frequency-based scoring system
    word_frequencies = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence):
            word_frequencies[word] = word_frequencies.get(word, 0) + 1

    # Score sentences based on word frequencies
    sentence_scores = []
    for sentence in sentences:
        score = 0
        for word in nltk.word_tokenize(sentence):
            score += word_frequencies[word]
        sentence_scores.append(score)

    # Rank sentences by score and select top N
    ranked_sentences = sorted(enumerate(sentence_scores), key=lambda x: x[1], reverse=True)
    top_n_sentences = [sentences[i] for i, _ in ranked_sentences[:num_sentences]]

    # Join the top-ranked sentences into a summary
    summary = '\n'.join(top_n_sentences)
    return summary