from device_rules import check_needs_attention, check_stale_repos


def test_check_stale_repos():
    fake_repos = [
        {"name": "old-repo", "pushed_at": "2026-06-01T00:00:00Z", "open_issues": 0}
    ]

    result = check_stale_repos(fake_repos)

    assert result[0]["stale"] == True

def test_check_stale_repos_not_stale():
    fake_repos = [
        {"name": "old-repo", "pushed_at": "2026-09-01T00:00:00Z", "open_issues": 0}
    ]

    result = check_stale_repos(fake_repos)

    assert result[0]["stale"] == False

def test_check_needs_attention():
    fake_repos = [
        {"name": "old-repo", "pushed_at": "2026-06-01T00:00:00Z", "open_issues": 1}
    ]

    result = check_needs_attention(fake_repos)

    assert result[0]["needs_attention"] == True

def test_check_needs_attention_no_issues():
    fake_repos = [
        {"name": "old-repo", "pushed_at": "2026-06-01T00:00:00Z", "open_issues": 0}
    ]

    result = check_needs_attention(fake_repos)

    assert result[0]["needs_attention"] == False