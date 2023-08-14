"""import subprocess

from flask import Flask
from flask import request

def deploy():
    # Pull the latest code from GitHub
    subprocess.run(['git', 'pull'])

    # Move HTML files to Nginx's web root directory
    subprocess.run(['sudo', 'cp', '-r', './herovired/CICD/CICD_Pipeline/*', '/var/www/html'])

    # Restart Nginx
    subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'])

if __name__ == "__main__":
    deploy()

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Run the deployment script when a webhook is received
    subprocess.run(['python3', 'path_to_deploy.py/deploy.py'])
    return 'Deployment triggered'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)"""
    

import paramiko
import os
import sys  # Import the 'sys' module

# SSH connection parameters
host = '192.168.253.199'
port = 22
username = 'kalki'
#password = 'tilak'  # You should use key-based authentication for security
private_key_path = os.path.expanduser('~/.ssh/id_rsa')  # Path to your private key file

# Connect to the server using key-based authentication
private_key = paramiko.RSAKey(filename=private_key_path)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, pkey=private_key)


# Connect to the server
#ssh = paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh.connect(host, port, username, password)

# Install Nginx
stdin, stdout, stderr = ssh.exec_command('sudo apt update && sudo apt install -y nginx')

# Print command output
print("Nginx Installation Output:")
print(stdout.read().decode())

# Close the SSH connection
ssh.close()

# Determine which branch was pushed
branch = sys.argv[1] if len(sys.argv) > 1 else 'main'  # Default to 'main'

# Mapping of branches to directories
branch_to_directory = {
    'main': '/var/www/html/prod',
    'dev': '/var/www/html/dev',
    'prod': '/var/www/html/prod'
}

if branch not in branch_to_directory:
    print("Branch not supported.")
    sys.exit(1)

remote_directory = branch_to_directory[branch]

# Connect to the server using key-based authentication
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, pkey=private_key)

# Update the files based on branch
commands = [
    f'echo "tilak" | sudo cp -R -S /path/to/your/repo/{branch}/* {remote_directory}/',
    'echo "tilak" | sudo -S service nginx restart'
    'echo "tilak" | sudo -S apt update',
    'echo "tilak" | sudo -S apt install -y nginx',
    'echo "tilak" | sudo -S service nginx restart'
]

for command in commands:
    stdin, stdout, stderr = ssh.exec_command(command)
    print(stdout.read().decode())
    print(stderr.read().decode())

# Close the SSH connection
ssh.close()