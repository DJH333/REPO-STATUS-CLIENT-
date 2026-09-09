import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime
from datetime import timezone
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

def check_stale_repos(repos):
    for repo in repos:
        pushed_date = datetime.fromisoformat(repo["pushed_at"])
        difference = datetime.now(timezone.utc) - pushed_date

        if difference.days > 30:
            repo["stale"] = True
        else:
            repo["stale"] = False
    return repos

def check_needs_attention(repos):
    for repo in repos:
        repo_open_issues = repo["open_issues"]
        if repo_open_issues > 0:
            repo["needs_attention"] = True
        else:
            repo["needs_attention"] = False
    return repos

def check_alerts(repos):
    alerts = []
    for repo in repos:
        if repo["needs_attention"]:
            alerts.append(f"{repo['name']} needs attention")
        if repo["stale"]:
            alerts.append(f"{repo['name']} is stale")
    return alerts

def print_report(repos):

    print(f"""
---------------------------------------
REPOSITORY STATUS REPORT

GENERATED: {datetime.now()}
---------------------------------------""")

    for repo in repos:
        print(f"""
NAME: {repo["name"]}
PUSHED_AT: {repo["pushed_at"]}
OPEN_ISSUE: {repo["open_issues"]}""")

def print_alerts(alerts):
    if alerts:
        print(f"""
----------
ALERTS: 
----------""")
        for alert in alerts:
            print(f"""{alert}""")
    else:
        print(f"""
-------------
NO ALERTS: 
-------------""")

username = input("Enter GitHub username: ")
data = get_github_response(username)
repos = parse_repos(data)
repos = check_stale_repos(repos)
repos = check_needs_attention(repos)
alerts = check_alerts(repos)
#print(json.dumps(repos, indent=4))
print_report(repos)
print_alerts(alerts)
