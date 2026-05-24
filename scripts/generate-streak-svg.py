#!/usr/bin/env python3
"""Generate contribution streak SVG from GitHub GraphQL (includes private contributions)."""

import json
import os
import sys
import urllib.request


QUERY = """
query {
  viewer {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
  }
}
"""


def streaks(days):
    current = 0
    for _, count in reversed(days):
        if count > 0:
            current += 1
        else:
            break

    longest = run = 0
    for _, count in days:
        if count > 0:
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    return current, longest


def fetch_calendar(token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "umer-jahangier-profile-stats",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        payload = json.loads(resp.read())

    cal = payload["data"]["viewer"]["contributionsCollection"]["contributionCalendar"]
    days = sorted(
        (d["date"], d["contributionCount"])
        for week in cal["weeks"]
        for d in week["contributionDays"]
    )
    return cal["totalContributions"], days


def svg(theme):
    is_dark = theme == "dark"
    bg = "#0d1117" if is_dark else "#ffffff"
    text = "#c9d1d9" if is_dark else "#151515"
    muted = "#8b949e" if is_dark else "#464646"
    accent = "#00fff5" if is_dark else "#ff0080"
    fire = "#bf00ff" if is_dark else "#FB8C00"
    line = "#30363d" if is_dark else "#E4E2E2"

    return f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 495 195' width='495' height='195'>
  <rect width='495' height='195' rx='4.5' fill='{bg}' stroke='{line}' stroke-width='1'/>
  <line x1='165' y1='28' x2='165' y2='170' stroke='{line}' stroke-width='1'/>
  <line x1='330' y1='28' x2='330' y2='170' stroke='{line}' stroke-width='1'/>
  <text x='82.5' y='78' text-anchor='middle' fill='{text}' font-family='Segoe UI, Ubuntu, sans-serif' font-size='28' font-weight='700'>{{total}}</text>
  <text x='82.5' y='108' text-anchor='middle' fill='{text}' font-family='Segoe UI, Ubuntu, sans-serif' font-size='14'>Total Contributions</text>
  <text x='82.5' y='132' text-anchor='middle' fill='{muted}' font-family='Segoe UI, Ubuntu, sans-serif' font-size='12'>{{range_start}} - Present</text>
  <circle cx='247.5' cy='71' r='40' fill='none' stroke='{fire}' stroke-width='5'/>
  <text x='247.5' y='78' text-anchor='middle' fill='{text}' font-family='Segoe UI, Ubuntu, sans-serif' font-size='28' font-weight='700'>{{current}}</text>
  <text x='247.5' y='108' text-anchor='middle' fill='{text}' font-family='Segoe UI, Ubuntu, sans-serif' font-size='14'>Current Streak</text>
  <text x='247.5' y='132' text-anchor='middle' fill='{muted}' font-family='Segoe UI, Ubuntu, sans-serif' font-size='12'>{{current_end}}</text>
  <text x='412.5' y='78' text-anchor='middle' fill='{text}' font-family='Segoe UI, Ubuntu, sans-serif' font-size='28' font-weight='700'>{{longest}}</text>
  <text x='412.5' y='108' text-anchor='middle' fill='{text}' font-family='Segoe UI, Ubuntu, sans-serif' font-size='14'>Longest Streak</text>
  <text x='412.5' y='132' text-anchor='middle' fill='{muted}' font-family='Segoe UI, Ubuntu, sans-serif' font-size='12'>{{longest_range}}</text>
  <text x='247.5' y='24' text-anchor='middle' fill='{accent}' font-family='Segoe UI, Ubuntu, sans-serif' font-size='13' font-weight='600'>Contribution Streak</text>
</svg>"""


def longest_range(days):
    best = (0, 0, "")
    run_start = None
    run_len = 0
    for i, (date, count) in enumerate(days):
        if count > 0:
            if run_len == 0:
                run_start = date
            run_len += 1
            if run_len > best[1]:
                best = (run_start, run_len, date)
        else:
            run_len = 0
            run_start = None
    if best[1] == 0:
        return "—"
    start = best[0]
    end = best[2]
    return f"{start[5:].replace('-', ' ')} - {end[5:].replace('-', ' ')}"


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN required", file=sys.stderr)
        sys.exit(1)

    out_dir = sys.argv[1] if len(sys.argv) > 1 else "dist/stats"
    os.makedirs(out_dir, exist_ok=True)

    total, days = fetch_calendar(token)
    current, longest = streaks(days)
    active = [(d, c) for d, c in days if c > 0]
    range_start = active[0][0] if active else days[0][0]
    current_end = active[-1][0] if active else "—"
    lrange = longest_range(days)

    fmt = dict(
        total=total,
        current=current,
        longest=longest,
        range_start=range_start,
        current_end=current_end[5:].replace("-", " ") if current_end != "—" else "—",
        longest_range=lrange,
    )

    for theme in ("light", "dark"):
        path = os.path.join(out_dir, f"streak-{theme}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg(theme).format(**fmt))
        print(f"Wrote {path} total={total} current={current} longest={longest}")


if __name__ == "__main__":
    main()
