import os
import json
import requests
from rich.progress import track

def extract_urls(json_file):
    with open(json_file, 'r') as jf:
        data = json.load(jf)
        return data

def download_pdf(name, url, download_folder):
    file_name = f'{name}.pdf'
    file_path = os.path.join(download_folder, file_name)
    
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an exception for error HTTP statuses
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
            print(f'Downloaded {file_name}')
            
    except requests.exceptions.RequestException as e:
        print(f'Error downloading {url}: {e}')
        
    
def process_json(json_file):
    flag_file = os.path.join(os.path.dirname(json_file), 'processed.txt')
    
    if os.path.exists(flag_file):
        print(f"Json File {json_file} already processed!")
        return
    
    urls_dict = extract_urls(json_file)
    
    for name,url in track(urls_dict.items(), description=f"Processing file"):
        download_pdf(name, url, json_file)
        
    with open(flag_file, 'w') as ff:
        ff.write(f'{json_file} processed')