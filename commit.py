import os
import requests
import shutil
from git import Repo

# GitHub repository details
owner = 'bpechetti'
repo = 'CICD_Pipeline'
branch = 'main'

# Paths
local_repo_path = 'D:\herovired\CICD\CICD_Pipeline'
nginx_path = '/var/www/html/CICD_Pipeline'
file_to_copy = 'index.html'

# # GitHub Personal Access Token
access_token = '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'


# API request headers
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
previous_commit_hash_file = '45de3bc0af9ef4ecb645d2798a8e43df6db0c258'
if os.path.exists(previous_commit_hash_file):
    with open(previous_commit_hash_file, 'r') as file:
        previous_commit_hash = file.read().strip()
else:
    previous_commit_hash = None

if latest_commit_hash and latest_commit_hash != previous_commit_hash:
    print("New commit detected:", latest_commit_hash)
    
    # Clone or pull the repository
    if os.path.exists(local_repo_path):
        repo = Repo(local_repo_path)
        repo.remotes.origin.pull()
    else:
        repo = Repo.clone_from(f'https://github.com/{owner}/{repo}.git', local_repo_path)

    # Check if index.html has changed
    if repo.git.diff(previous_commit_hash, latest_commit_hash, '--', file_to_copy):
        src_path = os.path.join(local_repo_path, file_to_copy)
        dest_path = os.path.join(nginx_path, file_to_copy)
        if os.path.exists(src_path):
            shutil.copy(src_path, dest_path)
            print("Copied index.html to Nginx folder.")
    else:
        print("No changes in index.html.")

    # Update the previous commit hash
    with open(previous_commit_hash_file, 'w') as file:
        file.write(latest_commit_hash)
else:
    print("No new commits.")

