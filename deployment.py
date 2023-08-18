import subprocess
import time
import requests
import logging
import json
import paramiko

GITHUB_API_URL = "https://api.github.com/repos/bpechetti/CICD_Pipeline"
REMOTE_SERVER = "192.168.253.199"
REMOTE_USERNAME = "kali"
REMOTE_PRIVATE_KEY_PATH = "~/.ssh/id_rsa"

# Configure logging
logging.basicConfig(filename='deployment_log.json', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_latest_commit(branch_name):
    response = requests.get(GITHUB_API_URL + f"/commits/{branch_name}")
    commit_info = response.json()
    return commit_info

def deploy(branch_name):
    try:
        # SSH into the remote server
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(REMOTE_SERVER, username=REMOTE_USERNAME, key_filename=REMOTE_PRIVATE_KEY_PATH)

        # Execute deployment commands
        commands = [
            f"cd /path/to/your/code/on/remote/server",
            "git pull origin " + branch_name,
            "cp -r /path/to/code /var/www/html/",
            "systemctl reload nginx"
        ]
        command = "; ".join(commands)
        stdin, stdout, stderr = client.exec_command(command)
        deployment_output = stdout.read().decode()
        client.close()

        commit_info = get_latest_commit(branch_name)
        deployment_info = {
            "branch": branch_name,
            "status": "success",
            "commit": commit_info["sha"],
            "author": commit_info["commit"]["author"]["name"],
            "message": commit_info["commit"]["message"],
            "output": deployment_output.strip()
        }
        logging.info(json.dumps(deployment_info, indent=2))

    except Exception as e:
        error_info = {
            "branch": branch_name,
            "status": "error",
            "error_message": str(e)
        }
        logging.error(json.dumps(error_info, indent=2))

def check_and_deploy():
    try:
        # Fetch branch information from GitHub API
        response = requests.get(GITHUB_API_URL + "/branches")
        branches = response.json()

        for branch in branches:
            branch_name = branch["name"]
            if branch_name == "dev" or branch_name == "prod":
                response = requests.get(GITHUB_API_URL + f"/compare/{branch['commit']['sha']}...{branch_name}")
                comparison = response.json()

                if "files" in comparison and len(comparison["files"]) > 0:
                    deploy(branch_name)
                    print(f"Deployed changes from {branch_name} branch")

    except Exception as e:
        error_info = {
            "branch": "unknown",
            "status": "error",
            "error_message": str(e)
        }
        logging.error(json.dumps(error_info, indent=2))

if __name__ == "__main__":
    while True:
        check_and_deploy()
        time.sleep(5)  # Check every 10 minutes
