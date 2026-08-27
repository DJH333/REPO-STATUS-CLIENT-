import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

def get_github_response():

    response = requests.get('https://api.github.com/users/DJH333/repos' ,headers={"Authorization": f"Bearer {token}"})
    # print(response.status_code)

    data = response.json()
    return data
    #print(json.dumps(data, indent=4))

def parse_repos(data):

    #total_repos = len(data)
    #repo_name = []
    #repo_pushed_at = []
    #repo_open_issues = []

    repos = []

    for repo in data:

        repo_name = repo["name"]
        repo_pushed_at = repo["pushed_at"]
        repo_open_issues = repo["open_issues"]

        repos.append({"name": repo_name,"pushed_at": repo_pushed_at, "open_issues": repo_open_issues})

    return repos

def print_report(repos):

    print(f"""
-------------------------------
REPOSITORY STATUS REPORT

GENERATED: {datetime.now()}
-------------------------------""")

    for repo in repos:
        print(f"""
NAME: {repo["name"]}
PUSHED_AT: {repo["pushed_at"]}
OPEN_ISSUE: {repo["open_issues"]}""")

data = get_github_response()
repos = parse_repos(data)
print_report(repos)
