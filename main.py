from parsing import * 
from docUpdation import *
from keywords import *
import asyncio
import pymongo

path = r'C:\Users\pavit\OneDrive\Desktop\ai intern task'

# Checking for any JSON files
json_list = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.json')]

# Downloading PDF from the JSON files
for json_file in json_list:
    process_json(json_file)

# Getting the pdf documents
file_paths = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.pdf')] 

# Updating the metadata in MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your connection string
db = client["intern_task"]
collection = db["documents"]

async def process_pdf(pdf_path):
    # Extract metadata, keywords, and summary for the PDF
    metadata = get_metadata(pdf_path)
    keywords = get_keywords(extract_text(pdf_path))
    # summary = 


    await asyncio.gather(
        update_metadata_async(pdf_path, metadata),
        update_keywords_async(pdf_path, keywords),
        # update_summary_async(pdf_path, summary)
    )

async def main():
    pdf_paths = file_paths  # List of PDF paths

    tasks = []
    for pdf_path in pdf_paths:
        tasks.append(process_pdf(pdf_path))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())