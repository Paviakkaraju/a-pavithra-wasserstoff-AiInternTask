from parsing import * 
from docUpdation import *
import asyncio
import pymongo

path = r'C:\Users\pavit\OneDrive\Desktop\ai intern task'

# Checking for any JSON files
json_list = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.json')]

# Downloading PDF from the JSON files
for json_file in json_list:
    process_json(json_file)


async def main():
    client = MongoClient("mongodb://localhost:27017/")  # Replace with your connection string
     # Replace with your database and collection names

    # List of PDF files to process
    file_paths = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.pdf')]  # Replace with your file paths

    tasks = []
    for file_path in file_paths:
        task = asyncio.create_task(process_pdf(file_path, client, "intern_task", "documents"))
        tasks.append(task)

    await asyncio.gather(*tasks)

    client.close()


if __name__ == "__main__":
    asyncio.run(main())