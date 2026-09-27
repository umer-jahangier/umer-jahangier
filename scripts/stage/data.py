"""Everything the scenes draw, fetched from GitHub and reduced to aggregates.

Private repository names never leave this module: commits are bucketed into
public project names by keyword (PROJECTS), and anything unmatched is counted
only in totals.
"""

import http.client
import json
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import date, datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
    LOCAL_TZ = ZoneInfo("Asia/Karachi")
except Exception:  # pragma: no cover - zoneinfo missing
    LOCAL_TZ = timezone(timedelta(hours=5))

USER = "umer-jahangier"

# Display name -> keywords matched against lowercase repository names.
# Only names the owner approved for the profile appear here.
PROJECTS = [
    ("LogicOne Dialer", ("salespulse", "dailer", "dialer", "logicone")),
    ("AlphaVenue.ai", ("alphavenue",)),
    ("Elio", ("elio",)),
    ("SocialSync", ("socialsync",)),
    ("HRIA-DMS", ("hria",)),
    ("RestaurantOS", ("resturantos", "restaurantos")),
    ("Terra plugins", ("terra",)),
    ("Qalb-e-Saleem", ("qalb",)),
    ("madaddGar", ("madadd",)),
    ("cursor-powered-up", ("cursor-powered",)),
    ("domain-manager", ("domain-manager",)),
]

# Languages that describe markup or config rather than engineering work.
HIDE_LANGS = {"HTML", "CSS", "SCSS", "EJS", "Handlebars", "Makefile", "Dockerfile",
              "Procfile", "Batchfile", "PowerShell", "CMake", "Swift", "Objective-C",
              "Kotlin", "C", "Ruby", "Jupyter Notebook", "Nix", "Mustache"}


def project_for(repo_name):
    name = repo_name.lower()
    for display, keys in PROJECTS:
        if any(k in name for k in keys):
            return display
    return None


# ---------------------------------------------------------------- transport

def _request(token, url, body=None, accept="application/vnd.github+json"):
    """GET/POST with three attempts: large commit pages sometimes arrive truncated."""
    data = json.dumps(body).encode() if body is not None else None
    last = None
    for attempt in range(3):
        req = urllib.request.Request(url, data=data, method="POST" if data else "GET", headers={
            "Authorization": f"Bearer {token}", "Accept": accept,
            "Content-Type": "application/json", "User-Agent": f"{USER}-profile"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read()), resp.headers.get("Link", "")
        except urllib.error.HTTPError as err:
            if err.code in (401, 403, 404, 409, 422):
                raise RuntimeError(f"HTTP {err.code} for {url.split('?')[0]}") from err
            last = err
        except (urllib.error.URLError, http.client.IncompleteRead, TimeoutError, ConnectionError) as err:
            last = err
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Gave up on {url.split('?')[0]}: {last}")


def gql(token, query, variables=None):
    payload, _ = _request(token, "https://api.github.com/graphql",
                          {"query": query, "variables": variables or {}})
    if payload.get("errors") or "data" not in payload:
        raise RuntimeError(f"GraphQL error: {json.dumps(payload.get('errors'))[:400]}")
    return payload["data"]


# ---------------------------------------------------------------- queries

YEAR_Q = """
query($login: String!) {
  user(login: $login) {
    createdAt
    contributionsCollection {
      totalCommitContributions totalPullRequestContributions
      totalPullRequestReviewContributions totalIssueContributions
      restrictedContributionsCount
      commitContributionsByRepository(maxRepositories: 100) { repository { isPrivate } contributions { totalCount } }
      issueContributionsByRepository(maxRepositories: 100) { repository { isPrivate } contributions { totalCount } }
      pullRequestContributionsByRepository(maxRepositories: 100) { repository { isPrivate } contributions { totalCount } }
      pullRequestReviewContributionsByRepository(maxRepositories: 100) { repository { isPrivate } contributions { totalCount } }
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""

TOTAL_Q = """
query($login: String!, $from: DateTime, $to: DateTime) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) { contributionCalendar { totalContributions } }
  }
}"""

REPO_FIELDS = """
  pageInfo { hasNextPage endCursor }
  nodes {
    nameWithOwner name isPrivate isFork pushedAt
    languages(first: 12, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
  }"""

VIEWER_REPOS_Q = """
query($cursor: String) {
  viewer {
    repositories(first: 100, after: $cursor, isFork: false,
                 ownerAffiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER]) {%s}
  }
}""" % REPO_FIELDS

PUBLIC_REPOS_Q = """
query($login: String!, $cursor: String) {
  user(login: $login) {
    repositories(first: 100, after: $cursor, isFork: false, privacy: PUBLIC,
                 ownerAffiliations: OWNER) {%s}
  }
}""" % REPO_FIELDS


def fetch_repos(token, personal):
    repos, cursor = [], None
    while True:
        if personal:
            conn = gql(token, VIEWER_REPOS_Q, {"cursor": cursor})["viewer"]["repositories"]
        else:
            conn = gql(token, PUBLIC_REPOS_Q, {"login": USER, "cursor": cursor})["user"]["repositories"]
        repos += conn["nodes"]
        if not conn["pageInfo"]["hasNextPage"]:
            return repos
        cursor = conn["pageInfo"]["endCursor"]


def fetch_commit_times(token, repos, since):
    """(local datetime, repo) for every commit the user authored since `since`."""
    out = []
    stamp = since.strftime("%Y-%m-%dT%H:%M:%SZ")
    for repo in repos:
        if repo["pushedAt"] < stamp:
            continue
        url = (f"https://api.github.com/repos/{repo['nameWithOwner']}/commits"
               f"?author={USER}&since={stamp}&per_page=100")
        while url:
            try:
                page, link = _request(token, url)
            except RuntimeError as err:
                # An empty repo answers 409; skip it rather than fail the run.
                print(f"::notice::skipped a repository ({err})")
                break
            for c in page:
                when = datetime.fromisoformat(c["commit"]["author"]["date"].replace("Z", "+00:00"))
                out.append((when.astimezone(LOCAL_TZ), repo))
            url = next((part.split(";")[0].strip(" <>") for part in link.split(",")
                        if 'rel="next"' in part), None)
    return out


# ---------------------------------------------------------------- reduce

def week_start(d):
    return d - timedelta(days=(d.weekday() + 1) % 7)  # weeks start Sunday, like GitHub


def fetch(token, personal):
    now = datetime.now(timezone.utc)
    data = gql(token, YEAR_Q, {"login": USER})["user"]
    cc = data["contributionsCollection"]
    days = sorted((d["date"], d["contributionCount"])
                  for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"])
    total = cc["contributionCalendar"]["totalContributions"]

    # Private share. Contributions the token cannot see arrive only as the
    # restricted count; ones it can see (a PAT acting as the user) arrive per
    # repository. Summing both is right with either token.
    visible_private = sum(
        e["contributions"]["totalCount"]
        for kind in ("commit", "issue", "pullRequest", "pullRequestReview")
        for e in cc[f"{kind}ContributionsByRepository"] if e["repository"]["isPrivate"])
    private = min(cc["restrictedContributionsCount"] + visible_private, total)

    created = datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00"))
    all_time, start = 0, created
    while start < now:
        end = min(start + timedelta(days=365), now)
        coll = gql(token, TOTAL_Q, {"login": USER, "from": start.isoformat(), "to": end.isoformat()})
        all_time += coll["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
        start = end

    repos = fetch_repos(token, personal)
    langs = Counter()
    for repo in repos:
        for edge in repo["languages"]["edges"]:
            if edge["node"]["name"] not in HIDE_LANGS:
                langs[edge["node"]["name"]] += edge["size"]

    since = now - timedelta(days=365)
    commits = fetch_commit_times(token, repos, since)
    hours = [0] * 24
    for when, _ in commits:
        hours[when.hour] += 1

    # Per-project activity: 52 weekly counts, last push, last-30-day commits.
    weeks = [week_start(d) for d in sorted({week_start(date.fromisoformat(x)) for x, _ in days})][-52:]
    index = {w: i for i, w in enumerate(weeks)}
    projects = {}
    for when, repo in commits:
        name = project_for(repo["name"])
        if not name:
            continue
        p = projects.setdefault(name, {"weeks": [0] * len(weeks), "total": 0, "recent": 0, "pushed": ""})
        p["total"] += 1
        i = index.get(week_start(when.date()))
        if i is not None:
            p["weeks"][i] += 1
        if when >= now - timedelta(days=30):
            p["recent"] += 1
    for repo in repos:
        name = project_for(repo["name"])
        if name in projects and repo["pushedAt"] > projects[name]["pushed"]:
            projects[name]["pushed"] = repo["pushedAt"]

    return dict(
        now=now, days=days, total=total, private=private,
        commits_contrib=cc["totalCommitContributions"],
        prs=cc["totalPullRequestContributions"], reviews=cc["totalPullRequestReviewContributions"],
        all_time=all_time, since=created.year,
        langs=langs, repos=len(repos), private_repos=sum(r["isPrivate"] for r in repos),
        commits=len(commits), commits_private=sum(r["isPrivate"] for _, r in commits),
        hours=hours, projects=projects, personal=personal,
    )


# ---------------------------------------------------------------- metrics

def weekly(days):
    weeks = Counter()
    for d, c in days:
        weeks[week_start(date.fromisoformat(d))] += c
    keys = sorted(weeks)[-52:]
    return [(k, weeks[k]) for k in keys]


def current_streak(days, today):
    """Consecutive active days ending today; a quiet *today* does not break it yet."""
    counts = dict(days)
    cursor = today if counts.get(today.isoformat(), 0) > 0 else today - timedelta(days=1)
    streak = 0
    while counts.get(cursor.isoformat(), 0) > 0:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def longest_streak(days):
    best = run = 0
    for _, count in days:
        run = run + 1 if count > 0 else 0
        best = max(best, run)
    return best


def top_languages(langs, limit=6):
    total = sum(langs.values()) or 1
    ranked = langs.most_common()
    head = [(name, size / total * 100) for name, size in ranked[:limit - 1]]
    rest = sum(size for _, size in ranked[limit - 1:]) / total * 100
    if rest > 0.05:
        head.append(("Other", rest))
    return head


def ago(iso, now):
    if not iso:
        return ""
    delta = now - datetime.fromisoformat(iso.replace("Z", "+00:00"))
    hours = delta.total_seconds() / 3600
    if hours < 24:
        return "today"
    d = int(hours // 24)
    if d == 1:
        return "yesterday"
    if d < 14:
        return f"{d} days ago"
    if d < 60:
        return f"{d // 7} weeks ago"
    return f"{d // 30} months ago"
