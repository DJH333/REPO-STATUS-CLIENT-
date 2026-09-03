# DEVICE STATUS API CLIENT BUILD / STEPS

**ORIGIN STORY (for interviews):** "I built a device-status concept with static local JSON first (forklift project), realized I needed real API and auth experience before building my own API, went and got that experience deliberately with GitHub's REST API (device status client API project), then came back and finished the forklift project properly."

This file includes each building block / step I took and why (used for explaining the project on my resume, in a README, and out loud in an interview).

**Legend:** `[STEP]` = something I did/built. `[CONCEPT]` = something I learned/understood along the way. Some lines are both.

---

## WHY GITHUB API

- `[CONCEPT]` Chose GitHub API because it's closer to a real SaaS integration pattern (Bearer token in a header) than query-param API keys — more representative of what I'd see in actual SE/Implementation Engineer work.

## SMALLEST POSSIBLE VERSION — DONE FIRST

- `[CONCEPT]` Postman-first, matching the workflow: read docs → test in Postman → understand it → implement in Python → add error handling.
- `[CONCEPT]` The smallest version does exactly one thing: authenticate to the GitHub API with a token and retrieve a list of repos for one account, then just print the raw JSON. No business rules, no offline/stale logic yet, no report formatting. Just prove the connection and auth work end to end.
- `[CONCEPT]` Why start that small? Mirrors a real SE workflow: validate raw connectivity and auth in isolation before building logic on top of it. If something breaks later, the connection is already ruled out as the cause.

## AUTH SETUP

- `[STEP]` Created a fine-grained personal access token on GitHub, scoped to **Public Repositories (read-only)** — least-privilege choice since I only need to read public repo data.
  - Token value intentionally not stored in this file — kept only in `.env`, which is gitignored. (Redacted a real token that had been pasted here earlier — good reminder that any file holding a real secret in plain text is a risk, gitignored or not.)
- `[CONCEPT]` For "Public Repositories (read-only)" tokens, GitHub doesn't require selecting specific repos or permissions — that access already exists for anyone, authenticated or not. An empty "Repository access" / "Repository permissions" panel for this token type is expected, not a misconfiguration.
- `[STEP]` Found the endpoint for "list repositories for a user": `https://api.github.com/users/{username}/repos`
  - `[CONCEPT]` Distinguished this from `/repos/{owner}/{repo}`, which takes a specific repo name and returns a single repo object, not a list — wrong shape for what I needed.
- `[STEP]` Created a Postman GET request to `https://api.github.com/users/DJH333/repos` with the Bearer token attached.
- `[STEP]` Identified fields in the Postman JSON response that could be useful for this project:
  - `open_issues`
  - `pushed_at` / `updated_at`
  - `visibility`: `"public"`
- `[CONCEPT]` `updated_at` reacts to more than code changes (description edits, stars, etc.), making it a noisy/unreliable signal for a "staleness" rule. `pushed_at` only updates on an actual `git push`, making it the more trustworthy field for detecting real inactivity.
- `[CONCEPT]` `/users/{username}/repos` is a public endpoint — it works with zero authentication, since public repo data is readable by anyone. Authenticating still matters for a much higher rate limit (~5,000/hr vs. ~60/hr unauthenticated) and for realistic auth practice.

## POSTMAN → PYTHON

- `[STEP]` Created the equivalent GET request in Python: `response = requests.get('https://api.github.com/users/DJH333/repos')`
- `[STEP]` Created a `.env` file to store the PAT, kept out of Git via `.gitignore`.
- `[STEP]` Used `from dotenv import load_dotenv` → `load_dotenv()` to read the `.env` file, then `os.getenv("GITHUB_TOKEN")` stored into a variable.
- `[STEP]` Added the PAT as a header in the GET request:
  `requests.get(url, headers={"Authorization": f"Bearer {token}"})`
- `[CONCEPT]` A header is metadata riding along with a request — not the content itself, but instructions about how to handle it (same idea as an envelope vs. a letter). `Authorization` is the header GitHub reads to identify who's making the request.
- `[CONCEPT]` The `f` in an f-string (`f"Bearer {token}"`) tells Python to substitute the variable's actual value into the string. Without it, `{token}` would be sent as literal text, not the real token value.
- `[STEP]` Wrapped this all in a function (`get_github_response()`) so it can be reused/called cleanly later.

## DEBUGGING NOTES (real errors hit + how I reasoned through them)

- `[CONCEPT]` Got a 401 even with the token wired in — narrowed it down by printing `token` directly and seeing `None`. Root cause: the file was accidentally named `.env.py` instead of `.env`, so `load_dotenv()` was silently finding nothing.
- `[CONCEPT]` `response.status_code` printed nothing when run as a `.py` script — because scripts don't auto-display expression results the way an interactive shell does. Needed an explicit `print()`.
- `[CONCEPT]` Github docs page for authentication mostly showed CLI (`gh`) examples — realized the underlying pattern (`Authorization: Bearer TOKEN`) is identical across CLI, Postman, and Python; only the way you *set* that header changes per tool.

## GIT SETUP

- `[CONCEPT]` A commit is a saved snapshot of the project at a point in time, with a message, timestamp, and link back to the previous commit — not just an overwrite like a normal file save.
- `[CONCEPT]` Staging (`git add`) and committing (`git commit`) are separate steps so you can control exactly what goes into each snapshot, rather than committing everything blindly.
- `[STEP]` Installed Git (had to install it fresh — `git init` initially failed with "not recognized," fixed by installing Git for Windows and restarting the terminal).
- `[STEP]` Made a `.gitignore` file **before** the first commit, so secrets never get a chance to be staged. Ignored: `.env`, `.venv`, `.idea/`.
- `[CONCEPT]` Caught a real near-miss: had a `.txt` file with my actual token pasted into it, untracked but sitting in the project folder. Cleaned the token out of the file, added the filename to `.gitignore` as a safety net, and made a mental note to regenerate tokens that have ever touched plain text outside of `.env`.
- `[STEP]` Ran first `git add` and `git commit -m "Initial project setup"`.
- `[STEP]` Created a fresh, empty GitHub repo (no README/license/gitignore auto-created) — avoids unrelated commit histories colliding on first push.
- `[STEP]` `git remote add origin <URL>` — registers the remote URL under the nickname "origin"; doesn't transfer anything yet, just bookkeeping.
- `[STEP]` `git remote -v` — confirmed fetch and push both point to the right URL.
- `[STEP]` `git branch` — checked local branch name (`master`) before pushing.
- `[STEP]` `git push -u origin master` — pushed commit history for the first time.
- `[CONCEPT]` The `-u` flag (`--set-upstream`) links the local branch to track the remote branch permanently, so every future push/pull from this branch can just be `git push` / `git pull` with no extra arguments.

## ADDED JSON PARSING

- `[STEP]` Added `parse_repos(data)` function.
- `[STEP]` Made a list called `repos`.
- `[STEP]` Looped through each `repo` in `data`.
- `[STEP]` Pulled out named fields per repo (e.g. `repo_name = repo["name"]`).
- `[STEP]` Appended each repo's data as one dictionary into the `repos` list: `repos.append({"name": repo_name, "pushed_at": repo_pushed_at, "open_issues": repo_open_issues})`
- `[STEP]` Returned `repos` as a list of dictionaries.
- `[CONCEPT]` First attempt used three separate parallel lists (`repo_name`, `repo_pushed_at`, `repo_open_issues`) instead of one list of dictionaries — this required manual index-matching (`repo_name[i]`, `repo_pushed_at[i]`, etc.) via `range(total_repos)`, which is fragile: if the lists ever get out of sync, data silently mismatches with no error thrown.
- `[CONCEPT]` Refactored to match the pattern already used successfully in the forklift project: one list, where each item is a single dictionary holding everything about one entity together. Adding a new field later just means adding one more key to the dictionary — no new list, no new index to keep in sync.

## ADDED PRINT REPORT FUNCTION

- `[STEP]` Added `print_report(repos)` function.
- `[STEP]` Used `datetime.now()` for a generated timestamp in the report header.
- `[STEP]` Looped through each `repo` in `repos`, printing its `name`, `pushed_at`, and `open_issues` directly from the dictionary (`repo["name"]`, etc.).
- `[CONCEPT]` Distinguished function **definitions** (the `def` blocks — describe what a function *would* do) from the actual **execution** lines at the bottom of the script that call those functions in order and pass results between them:
  ```
  data = get_github_response()
  repos = parse_repos(data)
  print_report(repos)
  ```

## COMMIT 2 — "Added JSON parsing"

- `[STEP]` Ran `git status` before staging — confirmed only `main.py` showed as modified.
- `[STEP]` `git add main.py` → `git commit -m "parsing raw JSON into structured repo data, printing a report from it"`
- `[STEP]` `git push` (no need for `-u origin master` again — the tracking relationship was already set from the first push).

## DATE MATH FOR STALENESS RULE (tested in a scratch file before adding to the real project)

- `[CONCEPT]` Goal: compare a repo's `pushed_at` timestamp to "how many days ago," to support a rule like "flag as stale if not pushed to in 30+ days."
- `[CONCEPT]` `pushed_at` comes back as a string (e.g. `"2026-08-20T03:01:45Z"`) — not something Python can do date math on directly.
- `[STEP]` Used `datetime.fromisoformat(test_date_string)` to convert the string into a real `datetime` object. Confirmed this Python version handles GitHub's trailing `Z` automatically — no manual `Z` → `+00:00` replace needed.
- `[CONCEPT]` Tried `datetime.now() - pushed_date` → error: `can't subtract offset-naive and offset-aware datetimes`. `pushed_date` is "offset-aware" (knows it's UTC), plain `datetime.now()` is "offset-naive" (no timezone info) — Python won't compare mismatched types.
- `[CONCEPT]` Tried `datetime.utcnow()` as a fix — wrong approach. It returns UTC-correct *values* but is still naive (no `+00:00` attached), so the same error would occur. Also being phased out in newer Python versions for this exact reason.
- `[STEP]` Correct fix: `datetime.now(timezone.utc)` — passing `timezone.utc` into `.now()` makes both sides of the subtraction timezone-aware. Required `from datetime import timezone` as an extra import.
- `[CONCEPT]` Subtracting two `datetime` objects returns a `timedelta` — a type representing a *span* of time, not a specific point in time (different from `datetime`, which represents one point in time).
- `[STEP]` Printed the `timedelta` directly → readable output like `14 days, 0:30:48.794300`.
- `[STEP]` Found `.days` on the `timedelta` object → returns a plain integer (`14`), exactly what's needed to compare against a 30-day threshold.
- `[CONCEPT]` Chose 30 days as the staleness threshold — a defensible middle ground (not so short it flags normal breaks in activity, not so long it misses genuinely abandoned repos). Worth being able to justify this choice, not just state it, if asked in an interview.
- `[CONCEPT]` Tested this whole sequence in an isolated scratch file first, separate from the real project — same "prove the small piece works before combining it with real logic" habit used at the very start of this project (Postman before Python, raw request before parsing).

## BUSINESS RULE 1 — STALENESS

- `[STEP]` Built `check_stale_repos(repos)` in `main.py`, applying the date-math pattern proven out in the scratch file.
- `[STEP]` Chose Option B for storing the result: added a `"stale"` key (`True`/`False`) directly onto each repo's dictionary, rather than building a separate list of alert strings. Keeps each repo's full status self-contained in one object.
- `[CONCEPT]` Hit two bugs here worth remembering: comparing a `timedelta` object directly to an int (`difference > 30`) instead of `difference.days > 30`; and calling the function without capturing its return value (`check_stale_repos(repos)` alone does nothing useful — needed `repos = check_stale_repos(repos)`, same "don't throw away the return value" lesson as `os.getenv()` and `response.status_code` earlier).
- `[STEP]` Chose 30 days as the threshold (see earlier date-math section for reasoning).
- `[STEP]` Spot-checked the flag against GitHub's own UI ("Updated X weeks ago" label) for a few repos to confirm the logic actually matches real-world behavior — not just "it ran without an error."
- `[CONCEPT]` GitHub's "Updated X ago" label on the repo list page is generally driven by `pushed_at`, not `updated_at`, despite the word "Updated" — confirmed this by direct comparison rather than assuming.

## BUSINESS RULE 2 — NEEDS ATTENTION

- `[STEP]` Built `check_needs_attention(repos)` as a **separate** function from `check_stale_repos`, rather than combining both checks into one function.
  - `[CONCEPT]` Reasoning: each function checks one distinct condition, which keeps each one simple and independently testable later with `pytest` — matches the single-responsibility thinking behind the planned `api_client.py`/`device_rules.py`/`report_generator.py` split.
- `[STEP]` Rule: flag `"needs_attention": True` if `open_issues > 0`. Simple threshold, appropriate since these are practice repos with typically zero issues — any issue at all is notable.
- `[STEP]` Same pattern as `check_stale_repos`: loop through `repos`, add a key to each dictionary, return `repos`.

## ALERTS LAYER

- `[STEP]` Built `check_alerts(repos)` — reads the `"stale"` and `"needs_attention"` flags already sitting on each repo's dictionary and turns them into human-readable message strings, collected into an `alerts` list.
- `[CONCEPT]` Deliberately kept this separate from the two flag-calculating functions: `check_stale_repos`/`check_needs_attention` decide *what's true*, `check_alerts` decides *what to say about it*. Two different responsibilities, same reasoning as splitting `print_report` from the rules themselves.
- `[STEP]` Built `print_alerts(alerts)` matching the forklift project's exact pattern: loop through `alerts` one at a time, print each on its own line; include an `else` branch for "no alerts" so the report always shows a clear state either way.
  - `[CONCEPT]` First attempt printed the whole `alerts` list in one f-string (`{alerts}`) instead of looping — would have shown Python's raw list syntax (brackets, quotes, commas) instead of a clean, readable report. Fixed by looping individually, matching the established forklift pattern.

## COMMIT 3 — SPLITTING BY CONCERN

- `[CONCEPT]` Had `main.py` (business rules + alerts) and `build_notes.md` (new documentation file) both staged together for one commit. Paused and reconsidered: these are two different *kinds* of change — a functional code milestone vs. a documentation addition — and bundling them buries the code milestone under an unrelated file in the commit history.
- `[STEP]` Used `git restore --staged build_notes.md` to unstage just that one file without losing any actual changes — unstaging only affects what's included in the *next* commit, not the file's contents on disk.
- `[STEP]` Committed `main.py` alone first, with a message describing the business-rules/alerts work specifically.
- `[STEP]` Committed `build_notes.md` separately afterward, with its own message describing it as documentation.
- `[CONCEPT]` General principle worth keeping: a commit should represent one coherent change. If two changes are genuinely unrelated in *kind* (code vs. docs, one feature vs. another), stage and commit them separately, even if they happened to land in the same working session.

## NEXT UP

- `[STEP]` Split `main.py` into `api_client.py` / `device_rules.py` / `report_generator.py` — the file now holds four genuinely different responsibilities (API communication, two business rules, alert generation, output formatting) rather than one simple pipeline. This is the natural trigger point discussed earlier.
- `[STEP]` Add error handling for expected failure cases: 401, 404, timeout, rate limiting (429), malformed JSON.
- `[STEP]` Add basic `pytest` tests for the business rules (`check_stale_repos`, `check_needs_attention`) now that they're simple, isolated functions — good candidates for testing before the file gets split.
- `[STEP]` Export the Postman collection into a `postman/` folder in the project.
- `[STEP]` Write the README once the project structure stabilizes after the file split.
