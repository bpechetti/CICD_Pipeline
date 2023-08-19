import subprocess

remote_repo_url = "https://github.com/bpechetti/CICD_Pipeline.git"
local_path = "/opt/gittest"
branch_name = "dev"

git_clone_command = ["git", "clone", remote_repo_url, local_path]
git_checkout_command = ["git", "checkout", branch_name]

try:
    subprocess.run(git_clone_command, check=True)
    subprocess.run(git_checkout_command, cwd=local_path, check=True)
    print("Code cloned and switched to the specified branch.")
except subprocess.CalledProcessError as e:
    print("An error occurred:", e)
