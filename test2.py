import os
import paramiko

# Load sensitive information from environment variables
hostname = '192.168.253.199'
port = 22
username = 'kali'
private_key_path = os.path.expanduser("~/.ssh/id_rsa")  # Update this path

def main():
    # Establish SSH connection using key-based authentication
    try:
        private_key = paramiko.RSAKey(filename=private_key_path)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port, username, pkey=private_key)
        
        # Now you can execute remote commands using the 'client' object
        
        client.close()
        print("SSH connection closed.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()


