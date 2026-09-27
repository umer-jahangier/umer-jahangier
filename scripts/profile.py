#!/usr/bin/env python3
"""Generate every profile SVG from the GitHub API into dist/.

  cover-<variant>-<light|dark|mobile>.svg   the skyline hero
  rhythm-<light|dark|mobile>.svg            when I build + languages
  activity-<light|dark|mobile>.svg          on stage now + the year counted
  work-<light|dark|mobile>.svg              selected work with activity silhouettes
  btn-<name>-<light|dark>.svg               contact buttons

Token: PROFILE_TOKEN (classic PAT, `repo` + `read:user`) adds private repos,
their languages and their commit times. Without it the script falls back to
GITHUB_TOKEN and public data. Stdlib only, so the workflow needs no installs.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stage import data, scenes  # noqa: E402
from stage.svg import ROOT, adaptive, doc, themed  # noqa: E402

OUT = os.path.join(ROOT, "dist")


def build(stats):
    files = {}
    for variant in scenes.VARIANTS:
        files[f"cover-{variant}-mobile.svg"] = adaptive(scenes.hero, "narrow", stats, variant)
        for theme in scenes.THEMES:
            files[f"cover-{variant}-{theme}.svg"] = themed(scenes.hero, theme, "wide", stats, variant)
    for name, builder in (("rhythm", scenes.rhythm), ("activity", scenes.activity), ("work", scenes.work)):
        files[f"{name}-mobile.svg"] = adaptive(builder, "narrow", stats)
        for theme in scenes.THEMES:
            files[f"{name}-{theme}.svg"] = themed(builder, theme, "wide", stats)
    for theme in scenes.THEMES:
        for name in scenes.BUTTONS:
            w, h, body, title, style = scenes.button(theme, name)
            files[f"btn-{name}-{theme}.svg"] = doc(w, h, title, body, style)
    return files


def main():
    token = os.environ.get("PROFILE_TOKEN") or ""
    personal = bool(token)
    if not token:
        token = os.environ.get("GITHUB_TOKEN") or ""
        print("::warning::PROFILE_TOKEN is not set; private repos, languages and commit times are left out.")
    if not token:
        sys.exit("Set PROFILE_TOKEN or GITHUB_TOKEN.")

    stats = data.fetch(token, personal)
    os.makedirs(OUT, exist_ok=True)
    files = build(stats)
    for name, content in files.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(content)
    share = round(stats["private"] / stats["total"] * 100) if stats["total"] else 0
    print(f"Wrote {len(files)} files · contributions={stats['total']} ({share}% private) "
          f"commits={stats['commits']} repos={stats['repos']} projects={len(stats['projects'])}")


if __name__ == "__main__":
    main()
