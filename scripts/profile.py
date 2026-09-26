#!/usr/bin/env python3
"""Generate every profile SVG from the GitHub GraphQL API.

Stdlib only, so the workflow needs no installs. Writes to dist/:
  cover-<variant>-<theme>.svg   hero with the live 52-week contribution graph
  numbers-<theme>.svg           languages, weekly rhythm, streaks and totals
  btn-<name>-<theme>.svg        contact buttons

Token: PROFILE_TOKEN (classic PAT, scopes `repo` + `read:user`) unlocks private
repo languages. Without it the script falls back to GITHUB_TOKEN and public
data; private contribution *counts* still appear because the profile has
"Include private contributions" switched on. Private repo names never leave
this process: only aggregates are written.
"""

import base64
import json
import os
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from xml.sax.saxutils import escape

USER = "umer-jahangier"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "dist")
FONTS = os.path.join(ROOT, "assets", "fonts")

# Languages that describe markup or config rather than engineering work.
HIDE_LANGS = {"HTML", "CSS", "SCSS", "EJS", "Handlebars", "Makefile", "Dockerfile",
              "Procfile", "Batchfile", "PowerShell", "CMake", "Swift", "Objective-C",
              "Kotlin", "C", "Ruby", "Jupyter Notebook", "Nix", "Mustache"}

THEMES = {
    "light": dict(ground="#FFFFFF", ink="#0B0D12", muted="#5A6170", rule="#D9DCE3",
                  field="#2340F0", on_field="#FFFFFF", on_field_muted="#DDE2FF",
                  accent="#2340F0", rhythm_peak="#2340F0", rhythm_rest="#7487F4",
                  # Language swatches by rank: salience follows share; every mark >= 3:1 on the ground.
                  steps=["#2340F0", "#4A62F2", "#6479F4", "#7487F4", "#6E7482", "#838997"]),
    "dark": dict(ground="#0D1117", ink="#E8ECF2", muted="#9AA3B2", rule="#2A313C",
                 field="#2F4BFF", on_field="#FFFFFF", on_field_muted="#DDE2FF",
                 accent="#93A3FF", rhythm_peak="#B9C3FF", rhythm_rest="#4F63E6",
                 steps=["#A9B5FF", "#8595FF", "#6A7DFA", "#5468F0", "#8A93A3", "#6B7383"]),
}

VARIANTS = {
    "personal": dict(role="AI, Automation & Full-Stack Engineer",
                     line="Lahore, Pakistan · open to roles and projects"),
    "praivox": dict(role="AI, Automation & Full-Stack Engineer",
                    line="Founder, Praivox · Lahore, Pakistan"),
}

BUTTONS = {
    "email": dict(label="umer.jahangier@gmail.com", icon="mail", primary=True),
    "email-praivox": dict(label="hello@praivox.com", icon="mail", primary=True),
    "praivox": dict(label="praivox.com", icon="globe", primary=False),
    "linkedin": dict(label="LinkedIn", icon="linkedin", primary=False),
    "instagram": dict(label="Instagram", icon="instagram", primary=False),
}


# ---------------------------------------------------------------- data

def gql(token, query, variables=None):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables or {}}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json",
                 "User-Agent": f"{USER}-profile"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as err:
        raise RuntimeError(f"GraphQL HTTP {err.code}: {err.read()[:300]!r}") from err
    if payload.get("errors") or "data" not in payload:
        raise RuntimeError(f"GraphQL error: {json.dumps(payload.get('errors'))[:400]}")
    return payload["data"]


YEAR_Q = """
query($login: String!, $from: DateTime, $to: DateTime) {
  user(login: $login) {
    createdAt
    contributionsCollection(from: $from, to: $to) {
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
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar { totalContributions }
    }
  }
}"""

REPOS_FIELDS = """
  pageInfo { hasNextPage endCursor }
  nodes {
    isPrivate isFork
    languages(first: 12, orderBy: {field: SIZE, direction: DESC}) {
      edges { size node { name } }
    }
  }"""

VIEWER_REPOS_Q = """
query($cursor: String) {
  viewer {
    login
    repositories(first: 100, after: $cursor, isFork: false,
                 ownerAffiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER]) {%s}
  }
}""" % REPOS_FIELDS

PUBLIC_REPOS_Q = """
query($login: String!, $cursor: String) {
  user(login: $login) {
    repositories(first: 100, after: $cursor, isFork: false, privacy: PUBLIC,
                 ownerAffiliations: OWNER) {%s}
  }
}""" % REPOS_FIELDS


def fetch_repos(token, personal):
    """Language bytes across every repo the token can see (owned + collaborator)."""
    langs, repos, private = Counter(), 0, 0
    cursor = None
    while True:
        if personal:
            conn = gql(token, VIEWER_REPOS_Q, {"cursor": cursor})["viewer"]["repositories"]
        else:
            conn = gql(token, PUBLIC_REPOS_Q, {"login": USER, "cursor": cursor})["user"]["repositories"]
        for repo in conn["nodes"]:
            repos += 1
            private += repo["isPrivate"]
            for edge in repo["languages"]["edges"]:
                if edge["node"]["name"] not in HIDE_LANGS:
                    langs[edge["node"]["name"]] += edge["size"]
        if not conn["pageInfo"]["hasNextPage"]:
            return langs, repos, private
        cursor = conn["pageInfo"]["endCursor"]


def fetch(token, personal):
    data = gql(token, YEAR_Q, {"login": USER})["user"]
    cc = data["contributionsCollection"]
    days = sorted((d["date"], d["contributionCount"])
                  for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"])

    # All-time total: the API caps each collection at one year.
    created = datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    all_time, start = 0, created
    while start < now:
        end = min(start + timedelta(days=365), now)
        coll = gql(token, TOTAL_Q, {"login": USER, "from": start.isoformat(), "to": end.isoformat()})
        all_time += coll["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
        start = end

    # Private share. Contributions the token cannot see arrive only as the
    # restricted count; ones it can see (a PAT acting as the user) arrive per
    # repository. Summing both is right with either token.
    visible_private = sum(
        entry["contributions"]["totalCount"]
        for kind in ("commit", "issue", "pullRequest", "pullRequestReview")
        for entry in cc[f"{kind}ContributionsByRepository"]
        if entry["repository"]["isPrivate"]
    )
    langs, repos, private_repos = fetch_repos(token, personal)
    return dict(
        days=days,
        total=cc["contributionCalendar"]["totalContributions"],
        private=min(cc["restrictedContributionsCount"] + visible_private,
                    cc["contributionCalendar"]["totalContributions"]),
        commits=cc["totalCommitContributions"],
        prs=cc["totalPullRequestContributions"],
        reviews=cc["totalPullRequestReviewContributions"],
        issues=cc["totalIssueContributions"],
        all_time=all_time,
        langs=langs, repos=repos, private_repos=private_repos,
        since=created.year,
    )


# ---------------------------------------------------------------- metrics

def current_streak(days, today):
    """Consecutive active days ending today.

    Today is still in progress, so a zero on today does not break the streak:
    counting starts from yesterday instead. A zero on any earlier day ends it.
    """
    counts = {d: c for d, c in days}
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


def weekly(days):
    """Contribution totals per calendar week, oldest first (last 52 weeks)."""
    weeks = Counter()
    for d, c in days:
        dt = date.fromisoformat(d)
        weeks[dt - timedelta(days=(dt.weekday() + 1) % 7)] += c  # weeks start Sunday
    keys = sorted(weeks)[-52:]
    return [(k, weeks[k]) for k in keys]


def by_weekday(days):
    sums, n = [0] * 7, [0] * 7
    for d, c in days:
        wd = date.fromisoformat(d).weekday()  # Monday = 0
        sums[wd] += c
        n[wd] += 1
    return [s / k if k else 0 for s, k in zip(sums, n)]


def top_languages(langs, limit=6):
    total = sum(langs.values()) or 1
    ranked = langs.most_common()
    head = [(name, size / total * 100) for name, size in ranked[:limit - 1]]
    rest = sum(size for _, size in ranked[limit - 1:]) / total * 100
    if rest > 0.05:
        head.append(("Other", rest))
    return head


# ---------------------------------------------------------------- svg helpers

def font_face(*names):
    rules = []
    for name in names:
        with open(os.path.join(FONTS, f"archivo-{name}.woff2"), "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode()
        rules.append(f"@font-face{{font-family:'A-{name}';"
                     f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
    return "".join(rules)


STACK = "'Helvetica Neue',Helvetica,Arial,sans-serif"


def fam(name):
    return f"'A-{name}',{STACK}"


def num(n):
    return f"{n:,}"


def svg_doc(w, h, title, body, style=""):
    fonts = [n for n in ("display", "medium", "text") if f"'A-{n}'" in body]
    style = font_face(*fonts) + style
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' "
            f"viewBox='0 0 {w} {h}' role='img' aria-labelledby='t'>"
            f"<title id='t'>{escape(title)}</title><style>{style}</style>{body}</svg>\n")


def text(x, y, s, size, family, fill, anchor="start", extra=""):
    return (f"<text x='{x}' y='{y}' font-family=\"{fam(family)}\" font-size='{size}' "
            f"fill='{fill}' text-anchor='{anchor}' {extra}>{escape(str(s))}</text>")


MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


# ---------------------------------------------------------------- cover

def sweep_style(span):
    """One oscilloscope pass across the chart. Invisible at its first and last
    frame, so a renderer that never advances time shows the finished chart."""
    return (".sweep{animation:sweep 2.4s cubic-bezier(.45,0,.2,1) .3s both}"
            f"@keyframes sweep{{0%{{transform:translateX(0);opacity:0}}10%{{opacity:1}}"
            f"88%{{opacity:1}}100%{{transform:translateX({span}px);opacity:0}}}}"
            "@media (prefers-reduced-motion:reduce){.sweep{animation:none;opacity:0}}")

# Wide: name left, cobalt field right. Narrow (phones): name on top, field below.
COVER_GEOMETRY = {
    # Bar spans are 52 x whole pixels (wide 8 = 6+2, narrow 10 = 8+2): crisp edges.
    "wide": dict(W=1200, H=440, name=86, name_y=(142, 232), name_x=0, role=27, role_y=300,
                 line=19, line_y=336, field=(720, 0), pad=32, total=64, total_dy=96, label=17,
                 top=176, base=318, small=13, split_y=372, split_label=15, colo=14),
    "narrow": dict(W=600, H=860, name=70, name_y=(112, 190), name_x=0, role=24, role_y=246,
                   line=18, line_y=280, field=(0, 320), pad=40, total=58, total_dy=86, label=19,
                   top=508, base=680, small=16, split_y=730, split_label=18, colo=15),
}


def cover_body(stats, variant, theme, layout):
    t, v, g = THEMES[theme], VARIANTS[variant], COVER_GEOMETRY[layout]
    W, H = g["W"], g["H"]
    fx, fy = g["field"]
    weeks = weekly(stats["days"])
    peak = max((c for _, c in weeks), default=1) or 1
    share = round(stats["private"] / stats["total"] * 100) if stats["total"] else 0
    updated = datetime.now(timezone.utc).strftime("%-d %b %Y")

    out = [f"<rect width='{W}' height='{H}' fill='{t['ground']}'/>"]
    # Name: one word big enough to win, set on two lines.
    for word, y in zip(("Muhammad", "Umer"), g["name_y"]):
        out.append(text(g["name_x"], y, word, g["name"], "display", t["ink"], extra="letter-spacing='-2'"))
    out.append(text(g["name_x"] + 2, g["role_y"], v["role"], g["role"], "medium", t["ink"]))
    out.append(text(g["name_x"] + 2, g["line_y"], v["line"], g["line"], "text", t["muted"]))

    if layout == "wide":
        # Colophon on the measured grid, under the name.
        out.append(f"<line x1='0' y1='388.5' x2='640' y2='388.5' stroke='{t['rule']}'/>")
        for x in range(0, 641, 80):
            out.append(f"<line x1='{x + .5}' y1='384' x2='{x + .5}' y2='393' stroke='{t['rule']}'/>")
        out.append(text(0, 418, f"github.com/{USER}", g["colo"], "text", t["muted"]))
        out.append(text(640, 418, f"Updated {updated}", g["colo"], "text", t["muted"], anchor="end"))

    # Cobalt field with the live year.
    out.append(f"<rect x='{fx}' y='{fy}' width='{W - fx}' height='{H - fy}' fill='{t['field']}'/>")
    left, right = fx + g["pad"], W - g["pad"]
    out.append(text(left, fy + g["total_dy"], num(stats["total"]), g["total"], "display", t["on_field"],
                    extra="letter-spacing='-1.5'"))
    out.append(text(left + 2, fy + g["total_dy"] + g["label"] + 14, "contributions in the last 12 months",
                    g["label"], "medium", t["on_field_muted"]))

    base, top = g["base"], g["top"]
    span, gap = right - left, 2
    pitch = span // 52
    bw = pitch - gap
    # Square-root scale: contribution weeks are spiky, and a linear axis turns
    # every ordinary week into a sliver. The peak label anchors the true value.
    peak_i = max(range(len(weeks)), key=lambda i: weeks[i][1]) if weeks else 0
    for i, (wk, c) in enumerate(weeks):
        h = max(2, round((base - top) * (c / peak) ** 0.5)) if c else 2
        x = left + i * pitch
        out.append(f"<rect x='{x}' y='{base - h}' width='{bw}' height='{h}' "
                   f"fill='{t['on_field']}' fill-opacity='{1 if c else .35}'/>")
    out.append(f"<line x1='{left}' y1='{base + .5}' x2='{right}' y2='{base + .5}' "
               f"stroke='{t['on_field']}' stroke-opacity='.5'/>")
    if weeks:
        px = left + peak_i * pitch + bw / 2
        anchor = "end" if px > right - 110 else "start"
        dx = 6 if anchor == "start" else -6
        out.append(f"<line x1='{px:.1f}' y1='{top - 16}' x2='{px:.1f}' y2='{top - 4}' stroke='{t['on_field']}'/>")
        out.append(text(round(px + dx), top - 6, f"peak week {num(weeks[peak_i][1])}", g["small"], "text",
                        t["on_field_muted"], anchor=anchor))
    seen = set()
    for i, (wk, _) in enumerate(weeks):
        month_start = wk + timedelta(days=6)
        if month_start.day <= 7 and month_start.month % 3 == 1 and month_start.month not in seen:
            seen.add(month_start.month)
            x = left + i * pitch
            out.append(f"<line x1='{x}.5' y1='{base}' x2='{x}.5' y2='{base + 8}' stroke='{t['on_field']}' stroke-opacity='.7'/>")
            out.append(text(x + 4, base + g["small"] + 10, MONTHS[month_start.month - 1], g["small"], "text",
                            t["on_field_muted"]))

    # The sweep: a scan line with a faint trailing band, crossing once.
    out.append(f"<style>{sweep_style(span)}</style>")
    out.append(f"<g class='sweep'><rect x='{left - 26}' y='{top - 8}' width='24' height='{base - top + 8}' "
               f"fill='{t['on_field']}' fill-opacity='.14'/><rect x='{left - 2}' y='{top - 8}' width='2' "
               f"height='{base - top + 8}' fill='{t['on_field']}'/></g>")

    # Private / public split: private solid, public outlined.
    sy, sh = g["split_y"], 12
    pw = span * share / 100
    out.append(f"<rect x='{left}' y='{sy}' width='{pw:.1f}' height='{sh}' fill='{t['on_field']}'/>")
    out.append(f"<rect x='{left + pw + 3:.1f}' y='{sy + .5}' width='{max(0, span - pw - 3.5):.1f}' "
               f"height='{sh - 1}' fill='none' stroke='{t['on_field']}'/>")
    ly = sy + g["split_label"] + 24
    out.append(text(left, ly, f"{share}% in private repositories", g["split_label"], "medium", t["on_field"]))
    out.append(text(right, ly, f"{100 - share}% public", g["split_label"], "text", t["on_field_muted"], anchor="end"))

    if layout == "narrow":
        out.append(text(left, H - 30, f"github.com/{USER}", g["colo"], "text", t["on_field_muted"]))
        out.append(text(right, H - 30, f"Updated {updated}", g["colo"], "text", t["on_field_muted"], anchor="end"))

    title = (f"Muhammad Umer, {v['role']}. {num(stats['total'])} contributions in the last "
             f"12 months, {share}% in private repositories.")
    return W, H, "".join(out), title


# ---------------------------------------------------------------- numbers

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def ledger_rows(stats):
    today = datetime.now(timezone.utc).date()
    active = sum(1 for _, c in stats["days"] if c > 0)
    return [
        ("Current streak", f"{current_streak(stats['days'], today)} days"),
        ("Longest streak", f"{longest_streak(stats['days'])} days"),
        ("Active days", f"{active} of {len(stats['days'])}"),
        ("Private contributions", num(stats["private"])),
        ("Pull requests and reviews", num(stats["prs"] + stats["reviews"])),
        ("Repositories", f"{stats['repos']} · {stats['private_repos']} private"),
        (f"All time, since {stats['since']}", num(stats["all_time"])),
    ]


def block_head(t, w, label):
    return (text(0, 26, label, 16, "medium", t["ink"]) +
            f"<line x1='0' y1='42.5' x2='{w}' y2='42.5' stroke='{t['ink']}'/>")


def block_languages(stats, t, w):
    out = [block_head(t, w, "Languages")]
    langs = top_languages(stats["langs"])
    cursor = 0
    for i, (_, pct) in enumerate(langs):
        seg = w * pct / 100
        out.append(f"<rect x='{cursor:.2f}' y='66' width='{max(seg - 2, 1):.2f}' height='18' fill='{t['steps'][i]}'/>")
        cursor += seg
    for i, (name, pct) in enumerate(langs):
        y = 124 + i * 36
        out.append(f"<rect x='0' y='{y - 11}' width='12' height='12' fill='{t['steps'][i]}'/>")
        out.append(text(24, y, name, 17, "text", t["ink"]))
        out.append(text(w, y, f"{pct:.1f}%", 17, "medium", t["ink"], anchor="end"))
        out.append(f"<line x1='0' y1='{y + 12.5}' x2='{w}' y2='{y + 12.5}' stroke='{t['rule']}'/>")
    return "".join(out)


def block_rhythm(stats, t, w):
    out = [block_head(t, w, "Weekly rhythm")]
    avg = by_weekday(stats["days"])
    peak = max(avg) or 1
    busiest = max(range(7), key=lambda i: avg[i])
    base, top = 250, 78
    gap = 12
    bw = (w - 6 * gap) / 7
    for i, a in enumerate(avg):
        h = max(2, round((base - top) * a / peak))
        x = i * (bw + gap)
        out.append(f"<rect x='{x:.1f}' y='{base - h}' width='{bw:.1f}' height='{h}' "
                   f"fill='{t['rhythm_peak'] if i == busiest else t['rhythm_rest']}'/>")
        out.append(text(round(x + bw / 2), base + 24, WEEKDAYS[i][:3], 14, "text",
                        t["ink"] if i == busiest else t["muted"], anchor="middle"))
    out.append(f"<line x1='0' y1='{base + .5}' x2='{w}' y2='{base + .5}' stroke='{t['rule']}'/>")
    day = WEEKDAYS[busiest]
    out.append(text(0, 318, f"{day}s are busiest", 17, "medium", t["ink"]))
    out.append(text(0, 342, f"{avg[busiest]:.1f} contributions on an average {day}", 15, "text", t["muted"]))
    return "".join(out)


def block_ledger(stats, t, w):
    out = [block_head(t, w, "The year, counted")]
    for i, (label, value) in enumerate(ledger_rows(stats)):
        y = 78 + i * 38
        out.append(text(0, y, label, 17, "text", t["muted"]))
        out.append(text(w, y, value, 17, "medium", t["ink"], anchor="end"))
        out.append(f"<line x1='0' y1='{y + 14.5}' x2='{w}' y2='{y + 14.5}' stroke='{t['rule']}'/>")
    return "".join(out)


BLOCKS = (block_languages, block_rhythm, block_ledger)


def numbers_body(stats, theme, layout):
    """Three blocks side by side (wide) or stacked and enlarged (narrow)."""
    t = THEMES[theme]
    if layout == "wide":
        W, H, w, scale = 1200, 360, 352, 1
        places = [(0, 0), (424, 0), (848, 0)]
    else:
        W, H, scale = 600, 1390, 1.25
        w = 528 / scale
        places = [(36, 0), (36, 477), (36, 954)]
    out = [f"<rect width='{W}' height='{H}' fill='{t['ground']}'/>"]
    for block, (x, y) in zip(BLOCKS, places):
        out.append(f"<g transform='translate({x} {y}) scale({scale})'>{block(stats, t, w)}</g>")
    langs = ", ".join(f"{n} {p:.0f}%" for n, p in top_languages(stats["langs"]))
    avg = by_weekday(stats["days"])
    title = (f"The year in numbers. Languages: {langs}. Busiest day: "
             f"{WEEKDAYS[max(range(7), key=lambda i: avg[i])]}. "
             + ". ".join(f"{l}: {v}" for l, v in ledger_rows(stats)) + ".")
    return W, H, "".join(out), title


def themed(builder, theme, *args):
    W, H, body, title = builder(*args[:-1], theme, args[-1])
    return svg_doc(W, H, title, body)


def adaptive(builder, *args):
    """One file carrying both themes, switched by the viewer's colour scheme.

    Used for the phone layout: the <source> that selects it can then use a
    plain width query, which GitHub's <themed-picture> leaves untouched."""
    W, H, light, title = builder(*args[:-1], "light", args[-1])
    _, _, dark, _ = builder(*args[:-1], "dark", args[-1])
    body = f"<g class='L'>{light}</g><g class='D'>{dark}</g>"
    css = ".D{display:none}@media (prefers-color-scheme:dark){.L{display:none}.D{display:inline}}"
    return svg_doc(W, H, title, body, css)


# ---------------------------------------------------------------- buttons

ICONS = {
    "mail": "<rect x='1' y='3' width='18' height='14' rx='1.5' fill='none' stroke='{c}' stroke-width='1.8'/>"
            "<path d='M1.8 4.2 10 11l8.2-6.8' fill='none' stroke='{c}' stroke-width='1.8' stroke-linejoin='round'/>",
    "linkedin": "<rect x='1' y='1' width='18' height='18' rx='3' fill='{c}'/>"
                "<path d='M5.2 8h2.3v7H5.2zM6.35 4.4a1.3 1.3 0 1 1 0 2.6 1.3 1.3 0 0 1 0-2.6zM9.2 8h2.2v1c.4-.7 1.3-1.2 2.4-1.2 2.2 0 2.7 1.4 2.7 3.3V15h-2.3v-3.4c0-.9-.1-1.9-1.2-1.9s-1.5.9-1.5 1.8V15H9.2z' fill='{g}'/>",
    "instagram": "<rect x='1.9' y='1.9' width='16.2' height='16.2' rx='4.6' fill='none' stroke='{c}' stroke-width='1.8'/>"
                 "<circle cx='10' cy='10' r='3.7' fill='none' stroke='{c}' stroke-width='1.8'/>"
                 "<circle cx='14.6' cy='5.4' r='1.1' fill='{c}'/>",
    "globe": "<circle cx='10' cy='10' r='8.2' fill='none' stroke='{c}' stroke-width='1.8'/>"
             "<path d='M1.8 10h16.4M10 1.8c2.4 2.3 3.4 5 3.4 8.2s-1 5.9-3.4 8.2c-2.4-2.3-3.4-5-3.4-8.2s1-5.9 3.4-8.2z' fill='none' stroke='{c}' stroke-width='1.6'/>",
}


def tag(kind, theme):
    """Selected-work chip carrying the cover's code: private solid, public outlined."""
    t = THEMES[theme]
    label, solid = ("Private", True) if kind == "private" else ("Open source", False)
    width, H = round(20 + len(label) * 7.4), 22
    color = t["field"] if theme == "light" else t["accent"]
    if solid:
        bg = f"<rect width='{width}' height='{H}' fill='{t['field']}'/>"
        fg = t["on_field"]
    else:
        bg = f"<rect x='.75' y='.75' width='{width - 1.5}' height='{H - 1.5}' fill='none' stroke='{color}' stroke-width='1.5'/>"
        fg = color
    return svg_doc(width, H, label, bg + text(10, 15.5, label, 12, "medium", fg))


def button(name, theme):
    t, b = THEMES[theme], BUTTONS[name]
    width = round(64 + len(b["label"]) * 9.6 + 22)
    H = 48
    if b["primary"]:
        bg = f"<rect width='{width}' height='{H}' fill='{t['field']}'/>"
        fg, glyph_bg = t["on_field"], t["field"]
    else:
        bg = (f"<rect x='.75' y='.75' width='{width - 1.5}' height='{H - 1.5}' fill='{t['ground']}' "
              f"stroke='{t['ink']}' stroke-width='1.5'/>")
        fg, glyph_bg = t["ink"], t["ground"]
    icon = ICONS[b["icon"]].format(c=fg, g=glyph_bg)
    arrow = (f"<path d='M{width - 30} {H / 2 + 5}l9-9m-6.5 0H{width - 21}v6.5' fill='none' "
             f"stroke='{fg}' stroke-width='1.7' stroke-linecap='square'/>")
    body = (bg + f"<g transform='translate(20 14)'>{icon}</g>" +
            text(52, 30, b["label"], 16, "medium", fg) + arrow)
    return svg_doc(width, H, b["label"], body)


# ---------------------------------------------------------------- main

def main():
    token = os.environ.get("PROFILE_TOKEN") or ""
    personal = bool(token)
    if not token:
        token = os.environ.get("GITHUB_TOKEN") or ""
        print("::warning::PROFILE_TOKEN is not set; languages cover public repos only.")
    if not token:
        sys.exit("Set PROFILE_TOKEN or GITHUB_TOKEN.")

    stats = fetch(token, personal)
    os.makedirs(OUT, exist_ok=True)
    files = {}
    for variant in VARIANTS:
        files[f"cover-{variant}-mobile.svg"] = adaptive(cover_body, stats, variant, "narrow")
    files["numbers-mobile.svg"] = adaptive(numbers_body, stats, "narrow")
    for theme in THEMES:
        for variant in VARIANTS:
            files[f"cover-{variant}-{theme}.svg"] = themed(cover_body, theme, stats, variant, "wide")
        files[f"numbers-{theme}.svg"] = themed(numbers_body, theme, stats, "wide")
        for name in BUTTONS:
            files[f"btn-{name}-{theme}.svg"] = button(name, theme)
        for kind in ("private", "open"):
            files[f"tag-{kind}-{theme}.svg"] = tag(kind, theme)
    for name, content in files.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(content)
    print(f"Wrote {len(files)} files · total={stats['total']} private={stats['private']} "
          f"all_time={stats['all_time']} repos={stats['repos']} "
          f"langs={', '.join(f'{n} {p:.0f}%' for n, p in top_languages(stats['langs']))}")


if __name__ == "__main__":
    main()
