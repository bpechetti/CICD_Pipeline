import os
import requests
from config import *
"""import json"""

"""with open('config.json', 'r') as config_json:
    config = json.load(config_json)
    print(config)"""

"""access_token = config['access_token']
owner = config['owner']
repo = config['repo']
branch = config['branch']
local_repo = config['local_repo']
nginx_path = config['nginx_path']
files_to_copy = config['files_to_copy']
"""
# providing the access token
headers = {
    'Authorization': f'Bearer {access_token}'
}

# API URL to get latest commit
url = f'https://api.github.com/repos/{owner}/{repo}/branches/{branch}' 
response = requests.get(url, headers=headers) 

if response.status_code == 200: 
   
    latest_commit_hash = response.json()['commit']['sha'] 
    
else:

    print("Error fetching commit hash:", response.text)
    latest_commit_hash = None

# Check if there's a new commit
previous_commit_hash_file = 'previous_commit_hash.txt' 


if os.path.exists(previous_commit_hash_file):
    with open(previous_commit_hash_file, 'r') as file: 
        previous_commit_hash = file.read().strip()
else:
    previous_commit_hash = None
    
if latest_commit_hash and latest_commit_hash != previous_commit_hash:
    print("New commit detected:", latest_commit_hash)
    
    with open(previous_commit_hash_file, 'w') as file:
        file.write(latest_commit_hash + '\n')

else:
    print("No new commits or no update in index.html file.")