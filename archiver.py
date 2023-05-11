import os
import re
import requests
import zipfile

import helpers

thingiverse_api = 'https://api.thingiverse.com'
access_token = '23315f10d27e53bce6528e0b4ef1fc46'

def download_collection(url):
    if url.startswith("https://www.thingiverse.com"):
        collection_id = re.search(r"/collections/(\d+)/", url).group(1)
        print("#################################################")
        print("## Starting download of Thingiverse collection ##")
        print("#################################################")
        print()
        print("Parsing", url)
        print()
    else:
        print("Invalid Thingiverse URL:", url)

    collections_endpoint = f"{thingiverse_api}/collections/{collection_id}/things"
    headers = { "Authorization": f"Bearer {access_token}" }
    resp = requests.get(collections_endpoint, headers=headers)

    if resp.status_code == 200:
        things = resp.json()
        print(f'Found {len(things)} things in the collection\n')
        
        downloads_folder = f"collection_{collection_id}"
        if not os.path.exists(downloads_folder):
            os.makedirs(downloads_folder)
        
        for thing in things:
            print(f"{thing['name']}")
            thing_zip_url = f"{thing['public_url']}/zip"
            thing_zip_resp = requests.get(thing_zip_url, headers=headers)
            if(thing_zip_resp.status_code == 200):
                filename = helpers.normalize_filename(f"{thing['name']}.zip")
                file_path = os.path.join(downloads_folder, filename)
                with open(file_path, 'wb') as f:
                    f.write(thing_zip_resp.content)
                print("↳ Saved as:", file_path, "\n")
            else:
                raise Exception("Failed to download thing:", {thing['public_url']})
            
        return downloads_folder
    else:
        raise Exception("Error downloading Thingiverse collection")

def archive_collection(collection_id):
    print("##################################################################")
    print("## Creating a zip file of things downloaded from the collection ##")
    print("##################################################################")
    print()

    zip_filename = f"collection_{collection_id}.zip"
    folder_path = f"collection_{collection_id}"

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, rel_path)

    print(f"Zip archive saved as: {zip_filename} ({helpers.convert_bytes(os.path.getsize(zip_filename))})")
    
    return zip_filename