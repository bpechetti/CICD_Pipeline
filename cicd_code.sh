#!/bin/bash

# Define the variables
GIT_REPO_URL="https://github.com/yourusername/yourrepository.git"  # Replace with your Git repository URL
WEB_ROOT="/var/www/html"  # Replace with the path to your web application's root directory
NGINX_RESTART_CMD="sudo systemctl restart nginx"  # Replace with the appropriate command to restart Nginx

# Change to the web root directory
cd "$WEB_ROOT" || exit 1

# Ensure Git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Please install Git."
    exit 1
fi

# Clone the latest code from the Git repository
git pull origin master  # You can replace 'master' with the branch you want to clone

# Check if the Git operation was successful
if [ $? -eq 0 ]; then
    echo "Code successfully updated from Git repository."

    # Restart Nginx
    echo "Restarting Nginx..."
    $NGINX_RESTART_CMD

    # Check if Nginx restart was successful
    if [ $? -eq 0 ]; then
        echo "Nginx restarted successfully."
    else
        echo "Failed to restart Nginx. Please check the Nginx configuration and try again."
        exit 1
    fi
else
    echo "Failed to update code from Git repository. Please check the Git repository and try again."
    exit 1
fi
