import paramiko
import json
import logging
import requests
import time
import subprocess


REMOTE_USERNAME = "kali"
REMOTE_SERVER = "192.168.253.199"
REMOTE_PRIVATE_KEY_PATH = "~/.ssh/id_rsa"
GITHUB_API_URL = "https://api.github.com/repos/bpechetti/CICD_Pipeline"

