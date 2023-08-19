import os
import paramiko
import requests
import json

# Load sensitive information from environment variables
#hostname = '192.168.253.199'
#port = 22
#username = os.environ.get('SSH_USERNAME')
#password = os.environ.get('SSH_PASSWORD')
#github_access_token = os.environ.get('GITHUB_ACCESS_TOKEN')

#SSH connection function
#def ssh_connect(hostname, port, username, password):
#    try:
#        client = paramiko.SSHClient()
 #       client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 #       client.connect(hostname, port, username, password)
  #      return client
   # except Exception as e:
    #    print("Error:", e)
     #   return None

# ... rest of the code remains unchanged ...
import os
import paramiko
import requests
import json

# Load sensitive information from environment variables
hostname = '192.168.253.199'
port = 22
username = 'kali'
private_key_path = os.path.expanduser("~/.ssh/id_rsa")  # Update this path

# ...

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, port, username, key_filename=private_key_path)

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
