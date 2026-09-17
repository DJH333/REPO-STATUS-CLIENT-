import requests
from dotenv import load_dotenv
import os
import sys

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

def get_github_response(username):
    try:
        response = requests.get(f'https://api.github.com/users/{username}/repos', headers={"Authorization": f"Bearer {token}"}, timeout=10)
    except requests.exceptions.Timeout as err:
        print(f"Request timed out while trying to reach GitHub for username '{username}'")
        print(err)
        sys.exit(1)
    if response.status_code == 429:
        print(f"Error: received status code {response.status_code}. You've hit GitHub's rate limit, try again later")
        sys.exit(1)
    elif response.status_code != 200:
        print(f"Error: received status code {response.status_code} for username '{username}'")
        sys.exit(1)
    else:
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError as err:
            print(f"Error: received JSON format error for username '{username}'")
            print(err)
            sys.exit(1)
    return data

def parse_repos(data):
    repos = []
    for repo in data:
        repo_name = repo["name"]
        repo_pushed_at = repo["pushed_at"]
        repo_open_issues = repo["open_issues"]
        repos.append({"name": repo_name,"pushed_at": repo_pushed_at, "open_issues": repo_open_issues})
    return repos