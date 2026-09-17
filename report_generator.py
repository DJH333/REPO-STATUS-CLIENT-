from datetime import datetime

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
