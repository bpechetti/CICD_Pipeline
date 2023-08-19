import paramiko
import requests
import json

# SSH connection details
hostname = '192.168.253.199'
port = 22
username = 'kali'
password = 'tilak'
private_key_path = os.path.expanduser("~/.ssh/id_rsa")  # Update this path
sudo_password = 'tilak'  # Replace with your sudo password

# GitHub repository details
repo_owner = 'bpechetti'
repo_name = 'CICD_Pipeline'
access_token = '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'

# SSH connection function
def ssh_connect(hostname, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port, username, password)
        return client
    except Exception as e:
        print("Error:", e)
        return None

# Check if Nginx is installed
def check_nginx_installed(client):
    stdin, stdout, stderr = client.exec_command("nginx -v")
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    if "nginx version" in output:
        print("Nginx is already installed:", output.strip())
    else:
        print("Nginx is not installed. Installing...")
        stdin, stdout, stderr = client.exec_command("sudo apt-get update && sudo apt-get install -y nginx")
        install_output = stdout.read().decode('utf-8')
        install_error = stderr.read().decode('utf-8')
        print("Installation Output:", install_output.strip())
        print("Installation Error:", install_error.strip())

# Get latest commit for a branch from GitHub
def get_latest_commit(branch):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{branch}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    commit_data = json.loads(response.text)
    return commit_data['sha']

# Clone repository and copy files to /var/www/html/
def copy_files_to_webroot(client, branch):
    repo_url = f"https://github.com/{repo_owner}/{repo_name}.git"
    clone_cmd = f"git clone {repo_url} /tmp/{repo_name}"
    copy_cmd = f"sudo cp -r /tmp/{repo_name}/{branch}/* /var/www/html/{branch}/"
    
    stdin, stdout, stderr = client.exec_command(clone_cmd)
    clone_output = stdout.read().decode('utf-8')
    clone_error = stderr.read().decode('utf-8')
    
    if clone_error:
        print("Clone Error:", clone_error.strip())
        return
    
    stdin, stdout, stderr = client.exec_command(copy_cmd)
    copy_output = stdout.read().decode('utf-8')
    copy_error = stderr.read().decode('utf-8')
    
    print("Copy Output:", copy_output.strip())
    print("Copy Error:", copy_error.strip())

def main():
    client = ssh_connect(hostname, port, username, password)
    if client:
        print("SSH connection successful")
        
        check_nginx_installed(client)
        
        branches_to_monitor = ['dev', 'prod', 'main']
        
        for branch in branches_to_monitor:
            latest_commit = get_latest_commit(branch)
            # Logic to compare with previous commit and trigger copy if changed
            copy_files_to_webroot(client, branch)
        
        client.close()
    else:
        print("SSH connection failed")

if __name__ == "__main__":
    main()
