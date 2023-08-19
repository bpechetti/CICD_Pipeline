import os
import paramiko

# Load sensitive information from environment variables
hostname = '192.168.253.199'
port = 22
username = 'kali'
private_key_path = os.path.expanduser("~/.ssh/id_rsa")  # Update this path

sudo_cmd = "echo 'tilak' | sudo -S apt-get update && echo 'tilak' | sudo -S apt-get install -y nginx"
stdin, stdout, stderr = client.exec_command(sudo_cmd)


def check_nginx_installed(client):
    stdin, stdout, stderr = client.exec_command("nginx -v")
    output = stdout.read().decode('utf-8')
    
    if "nginx version" in output:
        print("Nginx is already installed:", output.strip())
    else:
        print("Nginx is not installed. Installing...")
        stdin, stdout, stderr = client.exec_command("sudo apt-get update && sudo apt-get install -y nginx")
        install_output = stdout.read().decode('utf-8')
        install_error = stderr.read().decode('utf-8')
        if install_error:
            print("Installation Error:", install_error.strip())
        else:
            print("Installation Output:", install_output.strip())

def main():
    # Establish SSH connection using key-based authentication
    try:
        private_key = paramiko.RSAKey(filename=private_key_path)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port, username, pkey=private_key)

        # Check if Nginx is installed and install if needed
        check_nginx_installed(client)
        
        client.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
