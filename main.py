from parsing import * 
from docUpdation import *
from keywords import *
from summarize import *
import asyncio
import pymongo
from tqdm import tqdm

# FILE_PATH is the path of the desktop file containing the pdf documents and/or Json files
path = os.environ.get('FILE_PATH') 

# Checking for any JSON files
json_list = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.json')]

# Downloading PDF from the JSON files
for json_file in json_list:
    process_json(json_file)

# Getting the pdf documents
file_paths = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.pdf')] 

# Processing each pdf
async def process_pdf(pdf_path):
    # Extract metadata, keywords, and summary for the PDF
    metadata = get_metadata(pdf_path)
    keywords = get_keywords(extract_text(pdf_path))
    summary = summarize(extract_text(pdf_path))


    await asyncio.gather(
        update_metadata_async(pdf_path, metadata),
        update_keywords_async(pdf_path, keywords),
        update_summary_async(pdf_path, summary)
    )

# Processing all pdfs at once
async def main():
    pdf_paths = file_paths  # List of PDF paths

    with tqdm(total=len(pdf_paths), desc="Processing PDFs") as progress_bar:
        tasks = []
        for pdf_path in pdf_paths:
            task = asyncio.create_task(process_pdf(pdf_path))
            tasks.append(task)
            progress_bar.update(1)  # Update progress bar immediately

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())