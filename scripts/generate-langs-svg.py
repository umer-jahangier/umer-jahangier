#!/usr/bin/env python3
"""Generate top-languages SVG from GitHub GraphQL (includes private repos)."""

import json
import os
import sys
import urllib.request
from collections import Counter

HIDE = {"html", "css", "scss", "ejs", "nsis", "json", "markdown", "yaml", "xml", "svg"}

COLORS = {
    "Python": "#3572A5",
    "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a",
    "Dart": "#00B4AB",
    "Java": "#b07219",
    "C++": "#f34b7d",
    "C#": "#178600",
    "Kotlin": "#A97BFF",
    "Swift": "#F05138",
    "Go": "#00ADD8",
    "Rust": "#dea584",
    "PHP": "#4F5D95",
    "Ruby": "#701516",
    "Shell": "#89e051",
    "Cython": "#3776ab",
}

QUERY = """
query($cursor: String) {
  viewer {
    repositories(first: 100, after: $cursor, ownerAffiliations: OWNER) {
      pageInfo { hasNextPage endCursor }
      nodes {
        languages(first: 15, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
  }
}
"""


def fetch_languages(token):
    totals = Counter()
    cursor = None
    while True:
        variables = {"cursor": cursor} if cursor else {}
        body = json.dumps({"query": QUERY, "variables": variables}).encode()
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "umer-jahangier-profile-stats",
            },
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            payload = json.loads(resp.read())

        repos = payload["data"]["viewer"]["repositories"]
        for repo in repos["nodes"]:
            for edge in repo["languages"]["edges"]:
                name = edge["node"]["name"]
                if name.lower() in HIDE:
                    continue
                totals[name] += edge["size"]

        if not repos["pageInfo"]["hasNextPage"]:
            break
        cursor = repos["pageInfo"]["endCursor"]

    return totals


def svg(theme, items):
    is_dark = theme == "dark"
    bg = "#0d1117" if is_dark else "#ffffff"
    title = "#00fff5" if is_dark else "#ff0080"
    text = "#c9d1d9" if is_dark else "#24292f"
    muted = "#8b949e" if is_dark else "#57606a"
    track = "#30363d" if is_dark else "#eaeef2"

    rows = []
    y = 0
    for lang, pct in items:
        color = COLORS.get(lang, "#8b949e")
        bar_w = max(4, int(205 * pct / 100))
        rows.append(f"""
  <g transform="translate(0, {y})">
    <text x="2" y="15" fill="{text}" font-family="Segoe UI, Ubuntu, sans-serif" font-size="11">{lang}</text>
    <text x="215" y="34" fill="{muted}" font-family="Segoe UI, Ubuntu, sans-serif" font-size="11">{pct:.2f}%</text>
    <rect x="0" y="25" width="205" height="8" rx="5" fill="{track}"/>
    <rect x="0" y="25" width="{bar_w}" height="8" rx="5" fill="{color}"/>
  </g>""")
        y += 40

    body = "".join(rows)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="495" height="195" viewBox="0 0 495 195">
  <rect width="495" height="195" rx="4.5" fill="{bg}" stroke="{track}" stroke-width="1"/>
  <text x="25" y="35" fill="{title}" font-family="Segoe UI, Ubuntu, sans-serif" font-size="18" font-weight="600">Most Used Languages</text>
  <g transform="translate(25, 55)">{body}
  </g>
</svg>"""


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN required", file=sys.stderr)
        sys.exit(1)

    out_dir = sys.argv[1] if len(sys.argv) > 1 else "dist/stats"
    os.makedirs(out_dir, exist_ok=True)

    totals = fetch_languages(token)
    if not totals:
        print("No language data found", file=sys.stderr)
        sys.exit(1)

    grand = sum(totals.values())
    ranked = [(lang, (size / grand) * 100) for lang, size in totals.most_common(6)]

    for theme in ("light", "dark"):
        path = os.path.join(out_dir, f"langs-{theme}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg(theme, ranked))
        summary = ", ".join(f"{l} {p:.1f}%" for l, p in ranked)
        print(f"Wrote {path}: {summary}")


if __name__ == "__main__":
    main()
