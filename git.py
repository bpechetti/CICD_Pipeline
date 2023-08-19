#from git import repo

#git clone https://github.com/bpechetti/CICD_Pipeline.git
#cd  https://github.com/bpechetti/CICD_Pipeline.git

#from git.repo.base import Repo
#Repo.clone_from("https://github.com/bpechetti/CICD_Pipeline.git, "C:\git_repo_test")
                
import os
import subprocess
import git
# Define the path to the directory where you want to clone the Git repository
repo_path = '/D/herovired/git_repo_test/'
branch_name = 'dev'

# Define the URL of the Git repository you want to clone
repo_url = 'https://github.com/bpechetti/CICD_Pipeline.git'

# Clone the Git repository
if not os.path.exists(repo_path):
    subprocess.run(['git', 'clone', repo_url, repo_path])
    

# Change the current working directory to the repository path
os.chdir(repo_path)

# Switch to the specified branch
subprocess.run(['git', 'checkout', branch_name])

# Pull any changes from the remote repository
subprocess.run(['git', 'pull'])

# Make changes to the repository files as needed

# Add all changes to the staging area
subprocess.run(['git', 'add', '.'])

# Commit changes with a message
commit_message = 'Commit message goes here'
subprocess.run(['git', 'commit', '-m', commit_message])

# Push changes to the remote repository
subprocess.run(['git', 'push'])