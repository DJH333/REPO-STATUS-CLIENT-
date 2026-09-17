from datetime import datetime
from datetime import timezone


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