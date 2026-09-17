from api_client import get_github_response, parse_repos
from device_rules import check_needs_attention, check_alerts, check_stale_repos
from report_generator import print_report, print_alerts



if __name__ == "__main__":
    username = input("Enter GitHub username: ")
    data = get_github_response(username)
    repos = parse_repos(data)
    repos = check_stale_repos(repos)
    repos = check_needs_attention(repos)
    alerts = check_alerts(repos)
    print_report(repos)
    print_alerts(alerts)
