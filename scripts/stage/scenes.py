"""The Cyclorama: a night-to-day stage whose light reveals the year's work.

Every builder returns (width, height, body, title, style) for one theme and
layout ("wide" for desktop, "narrow" for phones); svg.themed/adaptive wrap it.
"""

import math
from datetime import timedelta

from . import data
from .svg import escape, fam, hash01, num, text, width, wrap

THEMES = {
    # Night cue: depthless black, a low cobalt horizon, rose gathering above it.
    "dark": dict(
        sky=[("0", "#03040A"), ("0.55", "#080B22"), ("0.86", "#131C5E"), ("1", "#2A3DE0")],
        ground=[("0", "#0B1030"), ("1", "#04050C")], glow="#3B5BFF", glow2="#FF6F91", haze="#3B5BFF",
        horizon="#5A76FF", ink="#F2F3F8", muted="#A7AECC", faint="#6B7394",
        card="#080A15", card_line="#1C2238", day="#1A1530", night="#0C1030",
        b_front="#10152E", b_side="#0A0E22", b_top="#1D2552",
        win_private="#FFC4D2", win_public="#8FA2FF", win_off="#161C3A",
        accent="#6F87FF", rose="#FF7A9A", rose_soft="#FFB8C8", track="#1C2238",
        ramp=["#4F6BFF", "#7A5CF0", "#B056D8", "#FF6F91", "#FFB0C2", "#5A6284"],
        chip="#3B5BFF", chip_on="#FFFFFF", chip_line="#8FA2FF", stars=True,
        mini=("#5A74FF", "#2E43C4", "#C3CCFF")),
    # Day cue: white wash, rose haze at the horizon, cobalt architecture.
    "light": dict(
        sky=[("0", "#FFFFFF"), ("0.62", "#FCFCFF"), ("0.9", "#FFE8EE"), ("1", "#FFCBD7")],
        ground=[("0", "#FFEFF3"), ("1", "#FFFFFF")], glow="#FF9DB3", glow2="#6D80F6", haze="#FF9DB3",
        horizon="#2340F0", ink="#0B0D1A", muted="#545B73", faint="#8C92A8",
        card="#FFFFFF", card_line="#E1E4F0", day="#FFF1F5", night="#EDF0FD",
        b_front="#2340F0", b_side="#1627B0", b_top="#7486F7",
        win_private="#FF93AE", win_public="#DCE3FF", win_off="#3550F2",
        accent="#2340F0", rose="#C8325A", rose_soft="#FF9DB3", track="#E7EAF4",
        ramp=["#2340F0", "#5A45DC", "#9444C4", "#D2406A", "#F08CA5", "#9AA0B4"],
        chip="#2340F0", chip_on="#FFFFFF", chip_line="#2340F0", stars=False,
        mini=("#2340F0", "#16269E", "#8FA0FA")),
}

VARIANTS = {
    "personal": dict(role="AI, Automation & Full-Stack Engineer",
                     line="Lahore, Pakistan · open to roles and projects"),
    "praivox": dict(role="AI, Automation & Full-Stack Engineer",
                    line="Founder, Praivox · Lahore, Pakistan"),
}

SHOWCASE = [
    # Facts match the Europass CV (see PRODUCT.md): no claim here that the CV does not make.
    ("AlphaVenue.ai", "Multi-tenant SaaS for wedding and event venues, as sole engineer: ELLA, an LLM assistant with 104 tools, RAG and an MCP server.",
     "Express · TypeScript · React · MongoDB · Redis · Qdrant · Pipecat", False),
    ("LogicOne Dialer", "AI sales-calling platform at logicone.ai, as primary engineer: predictive dialling, live call coaching, voice agents, Stripe Connect.",
     "Next.js · Prisma · PostgreSQL · Twilio · Pipecat · Gemini Live", False),
    ("Elio", "Construction marketplace at elio.care for homeowners, contractors and vendors: quotes, milestones, invoices, payouts, a four-role mobile app.",
     "Express · TypeScript · React · MongoDB · Socket.io · Flutter", False),
    ("RestaurantOS", "White-label restaurant ERP, as technical lead of four: 15 Spring Boot microservices, row-level security, OPA authorisation.",
     "Java · Spring Cloud · Next.js · RabbitMQ · ClickHouse · Kubernetes", False),
    ("HRIA-DMS", "Donation management for an educational academy: Electron desktop app on a 169-endpoint API, receipt printing, TOTP 2FA, Urdu reports.",
     "Electron · Express · TypeScript · MongoDB", False),
    ("SocialSync", "Social-media scheduling SaaS, as co-developer: publishing connectors for Facebook, Instagram, LinkedIn, X and YouTube, and Stripe billing.",
     "Next.js · Prisma · PostgreSQL · BullMQ", False),
    ("Terra plugins", "Nine merged pull requests to Juno Innovations' open-source Kubernetes plugin catalogue: cert-issuer, external-dns, domain-manager.",
     "Kubernetes · Helm · Argo CD · Gateway API", True),
    ("cursor-powered-up", "One clone, one install: spec-driven workflows, agent memory, CodeGraph and MCP wiring for Cursor and VS Code.",
     "Shell · MCP", True),
]

MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

MOTION = (
    ".tw{animation:tw 5.2s ease-in-out infinite}@keyframes tw{0%,100%{opacity:1}50%{opacity:.2}}"
    ".st{animation:st 7s ease-in-out infinite}@keyframes st{0%,100%{opacity:1}50%{opacity:.15}}"
    ".gl{animation:gl 9s ease-in-out infinite}@keyframes gl{0%,100%{opacity:1}50%{opacity:.72}}"
    ".pu{transform-box:fill-box;transform-origin:50% 50%;animation:pu 2.4s cubic-bezier(.2,.6,.3,1) infinite}"
    "@keyframes pu{0%{transform:scale(1);opacity:.55}100%{transform:scale(2.6);opacity:0}}"
    "@media (prefers-reduced-motion:reduce){.tw,.st,.gl,.pu{animation:none}.pu{opacity:0}}")


def plural(n, word):
    return f"{num(n)} {word}{'' if n == 1 else 's'}"


def stops(pairs):
    return "".join(f"<stop offset='{o}' stop-color='{c}'/>" for o, c in pairs)


# ---------------------------------------------------------------- hero

HERO = {
    "wide": dict(W=1200, H=640, horizon=500, name=82, name_lines=1, name_y=(118,), name_x=54,
                 role=26, role_y=168, line=18, line_y=202, credit=19, credit_y=(258,), credit_w=1090,
                 x0=48, x1=1152, bw=14, depth=7, hmax=232, label=13, legend_y=606, cols=2),
    "narrow": dict(W=600, H=1010, horizon=820, name=66, name_lines=2, name_y=(96, 166), name_x=30,
                   role=22, role_y=214, line=17, line_y=244, credit=19, credit_y=(300, 328), credit_w=540,
                   x0=26, x1=574, bw=7, depth=4, hmax=340, label=15, legend_y=926, cols=1),
}


def hero(theme, layout, stats, variant):
    t, g, v = THEMES[theme], HERO[layout], VARIANTS[variant]
    p = f"h{theme[0]}{layout[0]}"
    W, H, hz = g["W"], g["H"], g["horizon"]
    weeks = data.weekly(stats["days"])
    peak = max((c for _, c in weeks), default=1) or 1
    share = stats["private"] / stats["total"] if stats["total"] else 0

    out = [f"<defs><clipPath id='{p}c'><rect width='{W}' height='{H}' rx='22'/></clipPath>"
           f"<linearGradient id='{p}s' x1='0' y1='0' x2='0' y2='{hz}' gradientUnits='userSpaceOnUse'>{stops(t['sky'])}</linearGradient>"
           f"<linearGradient id='{p}g' x1='0' y1='{hz}' x2='0' y2='{H}' gradientUnits='userSpaceOnUse'>{stops(t['ground'])}</linearGradient>"
           f"<radialGradient id='{p}r'><stop offset='0' stop-color='{t['glow']}' stop-opacity='.9'/>"
           f"<stop offset='.45' stop-color='{t['glow']}' stop-opacity='.35'/><stop offset='1' stop-color='{t['glow']}' stop-opacity='0'/></radialGradient>"
           f"<radialGradient id='{p}q'><stop offset='0' stop-color='{t['glow2']}' stop-opacity='.55'/><stop offset='1' stop-color='{t['glow2']}' stop-opacity='0'/></radialGradient>"
           f"<linearGradient id='{p}fg' x1='0' y1='{hz}' x2='0' y2='{hz + (H - hz) * .7:.0f}' gradientUnits='userSpaceOnUse'>"
           f"<stop offset='0' stop-color='#fff'/><stop offset='1' stop-color='#000'/></linearGradient>"
           f"<mask id='{p}f' maskUnits='userSpaceOnUse' x='0' y='{hz}' width='{W}' height='{H - hz}'>"
           f"<rect y='{hz}' width='{W}' height='{H - hz}' fill='url(#{p}fg)'/></mask>"
           f"<mask id='{p}m'><circle cx='0' cy='0' r='24' fill='#fff'/><circle cx='10' cy='-7' r='21' fill='#000'/></mask>"
           f"</defs><g clip-path='url(#{p}c)'>",
           f"<rect width='{W}' height='{hz}' fill='url(#{p}s)'/>",
           # The cyc light: a wide horizon glow, a second tint drifting above it.
           f"<ellipse class='gl' cx='{W * .6:.0f}' cy='{hz}' rx='{W * .62:.0f}' ry='{(hz * .42):.0f}' fill='url(#{p}r)'/>",
           f"<ellipse cx='{W * .24:.0f}' cy='{hz - 40}' rx='{W * .34:.0f}' ry='{hz * .26:.0f}' fill='url(#{p}q)'/>"]

    if t["stars"]:
        for i in range(90 if layout == "wide" else 60):
            x, y = hash01("sx", i) * W, 20 + hash01("sy", i) * (hz - 120)
            r, o = .5 + hash01("sr", i) * 1.1, .25 + hash01("so", i) * .7
            cls = f" class='st' style='animation-delay:{hash01('sd', i) * 7:.2f}s'" if hash01("sc", i) < .22 else ""
            out.append(f"<circle{cls} cx='{x:.1f}' cy='{y:.1f}' r='{r:.2f}' fill='#FFFFFF' fill-opacity='{o:.2f}'/>")
        mx, my = (W * .9, 96) if layout == "wide" else (W * .86, 300)
        out.append(f"<circle cx='0' cy='0' r='24' fill='#F6F2FF' mask='url(#{p}m)' transform='translate({mx:.0f} {my})'/>")
    else:
        sx, sy = (W * .9, 100) if layout == "wide" else (W * .86, 300)
        out.append(f"<circle cx='{sx:.0f}' cy='{sy}' r='58' fill='{t['glow']}' fill-opacity='.22'/>")
        out.append(f"<circle cx='{sx:.0f}' cy='{sy}' r='40' fill='{t['glow']}' fill-opacity='.35'/>")
        out.append(f"<circle cx='{sx:.0f}' cy='{sy}' r='27' fill='#FF7C9C'/>")

    out.append(f"<rect y='{hz}' width='{W}' height='{H - hz}' fill='url(#{p}g)'/>")
    out.append(f"<rect y='{hz - 1}' width='{W}' height='2' fill='{t['horizon']}' fill-opacity='.9'/>")

    # The skyline: one building per week, height = contributions, lit windows
    # = contributions, warm windows = private work.
    x0, x1, bw, d = g["x0"], g["x1"], g["bw"], g["depth"]
    pitch = (x1 - x0) / max(len(weeks), 1)
    dy = d * .6
    top_i = max(range(len(weeks)), key=lambda i: weeks[i][1]) if weeks else 0
    tops = []
    out.append(f"<g id='{p}b'>")
    for i, (wk, c) in enumerate(weeks):
        ratio = (c / peak) ** .5 if c else 0
        h = round(12 + (g["hmax"] - 12) * ratio) if c else 6
        x, y = x0 + i * pitch, hz - h
        tops.append((x, y))
        out.append(f"<rect x='{x:.1f}' y='{y}' width='{bw}' height='{h}' fill='{t['b_front']}'/>")
        dens = .22 + .72 * ratio if c else 0
        cols = [3, 8] if g["cols"] == 2 else [2]
        wy, row = y + 6, 0
        while wy + 3 < hz - 4:
            for ci, cx in enumerate(cols):
                lit = hash01("w", i, row, ci) < dens
                fill = (t["win_private"] if hash01("p", i, row, ci) < share else t["win_public"]) if lit else t["win_off"]
                cls = ""
                if lit and hash01("t", i, row, ci) < .07:
                    cls = f" class='tw' style='animation-delay:{hash01('td', i, row, ci) * 5.2:.2f}s'"
                out.append(f"<rect{cls} x='{x + cx:.1f}' y='{wy:.1f}' width='3' height='3.2' fill='{fill}'/>")
            wy += 7 if g["cols"] == 2 else 6
            row += 1
        out.append(f"<polygon points='{x + bw:.1f},{y} {x + bw + d:.1f},{y - dy:.1f} {x + bw + d:.1f},{hz - dy:.1f} {x + bw:.1f},{hz}' fill='{t['b_side']}'/>")
        out.append(f"<polygon points='{x:.1f},{y} {x + d:.1f},{y - dy:.1f} {x + bw + d:.1f},{y - dy:.1f} {x + bw:.1f},{y}' fill='{t['b_top']}'/>")

    out.append("</g>")
    # The city over still water: the skyline mirrored at the horizon, fading out.
    # The mask sits on an untransformed group: a userSpaceOnUse mask on the
    # flipped <use> itself would flip with it and cover the sky instead.
    out.append(f"<g mask='url(#{p}f)'><use href='#{p}b' transform='translate(0 {2 * hz}) scale(1 -1)' opacity='.5'/></g>")
    for k in range(1, 6):
        ry = hz + 6 + k * k * 3.2
        out.append(f"<line x1='0' y1='{ry:.1f}' x2='{W}' y2='{ry:.1f}' stroke='{t['horizon']}' "
                   f"stroke-opacity='{.16 - k * .022:.3f}' stroke-dasharray='{14 + k * 6} {8 + k * 4}'/>")
    out.append(f"<rect y='{hz + 1}' width='{W}' height='1' fill='{t['horizon']}' fill-opacity='.35'/>")

    if weeks:
        px, py = tops[top_i][0] + bw / 2 + d / 2, tops[top_i][1] - dy
        anchor = "end" if px > W - 170 else "start"
        out.append(f"<line x1='{px:.1f}' y1='{py - 22:.1f}' x2='{px:.1f}' y2='{py - 6:.1f}' stroke='{t['ink']}' stroke-opacity='.7'/>")
        out.append(text(px + (-6 if anchor == "end" else 6), py - 12, f"peak week · {num(weeks[top_i][1])}",
                        g["label"], "text", t["ink"], anchor=anchor, extra="fill-opacity='.85'"))

    seen = set()
    for i, (wk, _) in enumerate(weeks):
        ms = wk + timedelta(days=6)
        if ms.day <= 7 and ms.month % 3 == 1 and ms.month not in seen:
            seen.add(ms.month)
            x = x0 + i * pitch
            out.append(f"<line x1='{x:.1f}' y1='{hz + 4}' x2='{x:.1f}' y2='{hz + 12}' stroke='{t['muted']}'/>")
            out.append(text(x + 4, hz + 12 + g["label"] + 4, MONTHS[ms.month - 1], g["label"], "text", t["muted"]))

    # Titles in the sky.
    names = ["Muhammad Umer"] if g["name_lines"] == 1 else ["Muhammad", "Umer"]
    for word, y in zip(names, g["name_y"]):
        out.append(text(g["name_x"], y, word, g["name"], "display", t["ink"], extra="letter-spacing='-2'"))
    out.append(text(g["name_x"] + 3, g["role_y"], v["role"], g["role"], "medium", t["ink"]))
    out.append(text(g["name_x"] + 3, g["line_y"], v["line"], g["line"], "text", t["muted"]))
    pct = round(share * 100)
    credit = [(num(stats["total"]), True), (" contributions in the last 12 months · ", False),
              (f"{pct}%", True), (" in private repositories", False)]
    if len(g["credit_y"]) == 1:
        lines = [credit]
    else:
        lines = [[credit[0], (" contributions in the last 12 months", False)],
                 [credit[2], credit[3]]]
    for parts, y in zip(lines, g["credit_y"]):
        spans = "".join(
            f"<tspan font-family=\"{fam('medium' if strong else 'text')}\" fill='{t['ink'] if strong else t['muted']}' "
            f"xml:space='preserve'>{escape(s)}</tspan>" for s, strong in parts)
        out.append(f"<text x='{g['name_x'] + 3}' y='{y}' font-size='{g['credit']}'>{spans}</text>")
    rule_y = g["credit_y"][-1] + 22
    out.append(f"<rect x='{g['name_x'] + 3}' y='{rule_y}' width='56' height='3' fill='{t['rose']}'/>")

    # Legend and colophon on the ground.
    ly = g["legend_y"]
    lx = g["name_x"] + 3
    items = [(t["win_private"], "private work"), (t["win_public"], "public work")]
    for col, label in items:
        out.append(f"<rect x='{lx + .5}' y='{ly - 9.5}' width='10' height='10' fill='{col}' stroke='{t['muted']}' stroke-opacity='.6'/>")
        out.append(text(lx + 16, ly, label, g["label"], "text", t["muted"]))
        lx += 16 + width(label, "text", g["label"]) + 22
    note = "one building per week · height and lit windows = contributions"
    updated = f"Updated {stats['now'].strftime('%-d %b %Y')}"
    if layout == "wide":
        out.append(text(lx, ly, note, g["label"], "text", t["muted"]))
        out.append(text(W - 54, ly, updated, g["label"], "text", t["muted"], anchor="end"))
    else:
        out.append(text(g["name_x"] + 3, ly + 28, note, g["label"] - 1, "text", t["muted"]))
        out.append(text(g["name_x"] + 3, ly + 54, updated, g["label"] - 1, "text", t["muted"]))

    out.append("</g>")
    out.append(f"<rect x='.5' y='.5' width='{W - 1}' height='{H - 1}' rx='22' fill='none' stroke='{t['card_line']}'/>")
    title = (f"Muhammad Umer, {v['role']}. A skyline of the last 52 weeks: {num(stats['total'])} contributions, "
             f"{pct}% in private repositories.")
    return W, H, "".join(out), title, MOTION


# ---------------------------------------------------------------- tiles

def card(cw, ch, t, p):
    """A small stage: the theme's horizon haze rises from the card floor."""
    haze = (f"<path d='M1 {ch - 110}H{cw - 1}V{ch - 19}A18 18 0 0 1 {cw - 19} {ch - 1}H19A18 18 0 0 1 1 {ch - 19}Z' "
            f"fill='url(#{p}hz)'/>")
    return (f"<rect x='.5' y='.5' width='{cw - 1}' height='{ch - 1}' rx='18' fill='{t['card']}' stroke='{t['card_line']}'/>"
            + haze)


def haze_def(t, p):
    return (f"<defs><linearGradient id='{p}hz' x1='0' y1='0' x2='0' y2='1'>"
            f"<stop offset='0' stop-color='{t['haze']}' stop-opacity='0'/>"
            f"<stop offset='1' stop-color='{t['haze']}' stop-opacity='.16'/></linearGradient></defs>")


def heading(t, title, sub, cw):
    return (text(30, 50, title, 20, "medium", t["ink"]) +
            "".join(text(30, 76 + i * 20, line, 14, "text", t["muted"])
                    for i, line in enumerate(wrap(sub, "text", 14, cw - 60, 2))))


def arc_sector(cx, cy, r0, r1, a0, a1):
    """Annular sector between angles a0 > a1 (degrees, counter-clockwise from +x)."""
    def pt(r, a):
        return cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))
    p1, p2, p3, p4 = pt(r1, a0), pt(r1, a1), pt(r0, a1), pt(r0, a0)
    return (f"M{p1[0]:.2f} {p1[1]:.2f}A{r1} {r1} 0 0 1 {p2[0]:.2f} {p2[1]:.2f}"
            f"L{p3[0]:.2f} {p3[1]:.2f}A{r0} {r0} 0 0 0 {p4[0]:.2f} {p4[1]:.2f}Z")


def tile_sun(t, p, stats, cw, compact):
    """When I build: 24 hours as the sun's path, day above the horizon, night below."""
    hours = stats["hours"]
    total = sum(hours) or 1
    peak_h = max(range(24), key=lambda h: hours[h])
    after_dark = round(sum(hours[h] for h in list(range(18, 24)) + list(range(0, 6))) / total * 100)
    ch = 640 if compact else 440
    cx, cy = (cw / 2, 268) if compact else (196, 262)
    r0, span = 52, 88
    rmax = r0 + span + 8
    out = [card(cw, ch, t, p), heading(t, "When I build", "Commits by hour, Lahore time · last 12 months, private repos included", cw),
           f"<path d='M{cx - rmax} {cy}A{rmax} {rmax} 0 0 1 {cx + rmax} {cy}Z' fill='{t['day']}'/>",
           f"<path d='M{cx - rmax} {cy}A{rmax} {rmax} 0 0 0 {cx + rmax} {cy}Z' fill='{t['night']}'/>"]
    peak = max(hours) or 1
    for h in range(24):
        a0 = 180 - (h - 6) * 15
        a1 = a0 - 15
        length = max(3, span * hours[h] / peak)
        day = 6 <= h < 18
        fill = t["rose"] if day else t["accent"]
        op = "1" if h == peak_h else ".78"
        out.append(f"<path d='{arc_sector(cx, cy, r0, r0 + length, a0 - .9, a1 + .9)}' fill='{fill}' fill-opacity='{op}'/>")
    out.append(f"<line x1='{cx - rmax - 10}' y1='{cy}' x2='{cx + rmax + 10}' y2='{cy}' stroke='{t['muted']}' stroke-opacity='.6'/>")
    for label, (dx, dy, anchor) in {"06": (-rmax - 14, 5, "end"), "18": (rmax + 14, 5, "start"),
                                    "12": (0, -rmax - 8, "middle"), "00": (0, rmax + 20, "middle")}.items():
        out.append(text(cx + dx, cy + dy, label, 13, "text", t["muted"], anchor=anchor))
    out.append(f"<circle cx='{cx}' cy='{cy}' r='{r0 - 8}' fill='{t['card']}' stroke='{t['card_line']}'/>")
    out.append(text(cx, cy - 2, "24h", 15, "medium", t["ink"], anchor="middle"))
    out.append(text(cx, cy + 16, "Lahore", 11, "text", t["muted"], anchor="middle"))

    figures = [(f"{peak_h:02d}:00", "busiest hour"), (f"{after_dark}%", "of commits after dark")]
    if compact:
        for i, (big, small) in enumerate(figures):
            x = 30 + i * (cw - 60) / 2
            out.append(text(x, 516, big, 40, "display", t["ink"], extra="letter-spacing='-1'"))
            out.append(text(x, 542, small, 15, "text", t["muted"]))
        out.append(text(30, 600, f"{num(stats['commits'])} commits in 12 months", 16, "medium", t["ink"]))
    else:
        px0 = cw - 208
        for i, (big, small) in enumerate(figures):
            out.append(text(px0, 196 + i * 96, big, 44, "display", t["ink"], extra="letter-spacing='-1'"))
            out.append(text(px0 + 2, 222 + i * 96, small, 14, "text", t["muted"]))
        out.append(text(px0 + 2, 384, f"{num(stats['commits'])} commits", 16, "medium", t["ink"]))
        out.append(text(px0 + 2, 404, "in 12 months", 14, "text", t["muted"]))
    return ch, "".join(out)


def tile_strata(t, p, stats, cw, compact):
    """Languages as strata of sky, from the cobalt horizon up to rose."""
    langs = data.top_languages(stats["langs"])
    ch = 440
    bx, by, bh = 30, 116, 290
    bwid = 150 if cw < 500 else 220
    out = [card(cw, ch, t, p), heading(t, "Languages", f"By code size across {stats['repos']} repositories, private included", cw)]
    heights = [max(18, bh * pct / 100) for _, pct in langs]
    scale = bh / sum(heights) if heights else 1
    heights = [h * scale for h in heights]
    y = by
    centers = []
    for i, ((name, pct), h) in enumerate(zip(langs, heights)):
        out.append(f"<rect x='{bx}' y='{y:.1f}' width='{bwid}' height='{max(h - 3, 1):.1f}' fill='{t['ramp'][i]}'/>")
        centers.append(y + (h - 3) / 2)
        y += h
    # Keep labels at least 30 apart, pushed down in order, then fitted to the band stack.
    ly = []
    for c in centers:
        ly.append(max(c, ly[-1] + 30) if ly else c)
    overflow = ly[-1] - (by + bh - 10) if ly else 0
    if overflow > 0:
        ly = [y - overflow for y in ly]
    lx = bx + bwid + 26
    for (name, pct), c, yl in zip(langs, centers, ly):
        out.append(f"<path d='M{bx + bwid + 4} {c:.1f}L{lx - 8} {yl:.1f}' stroke='{t['muted']}' stroke-opacity='.55' fill='none'/>")
        out.append(text(lx, yl + 6, name, 17, "medium", t["ink"]))
        out.append(text(cw - 30, yl + 6, f"{pct:.1f}%", 17, "text", t["muted"], anchor="end"))
    return ch, "".join(out)


def tile_callsheet(t, p, stats, cw, compact):
    """On stage now: the projects with the latest pushes."""
    ch = 440
    projects = sorted(((n, v) for n, v in stats["projects"].items() if v["pushed"]),
                      key=lambda kv: kv[1]["pushed"], reverse=True)[:5]
    most = max((v["recent"] for _, v in projects), default=1) or 1
    out = [card(cw, ch, t, p), heading(t, "On stage now", "Latest pushes across my projects · refreshed daily", cw)]
    bar_w = 110 if cw < 500 else 170
    for i, (name, v) in enumerate(projects):
        y = 136 + i * 60
        when = data.ago(v["pushed"], stats["now"])
        live = when in ("today", "yesterday")
        dot = t["rose"] if live else t["faint"]
        if live:
            out.append(f"<circle class='pu' style='animation-delay:{i * .4:.1f}s' cx='38' cy='{y - 6}' r='5' fill='{dot}'/>")
        out.append(f"<circle cx='38' cy='{y - 6}' r='5' fill='{dot}'/>")
        out.append(text(56, y, name, 17, "medium", t["ink"]))
        out.append(text(cw - 30, y, when, 14, "text", t["rose"] if live else t["muted"], anchor="end"))
        if not v["recent"]:
            out.append(text(56, y + 22, "private repository", 13, "text", t["muted"]))
            continue
        out.append(text(56, y + 22, f"{plural(v['recent'], 'commit')} in the last 30 days", 13, "text", t["muted"]))
        bx = cw - 30 - bar_w
        out.append(f"<rect x='{bx}' y='{y + 14}' width='{bar_w}' height='5' fill='{t['track']}'/>")
        out.append(f"<rect x='{bx}' y='{y + 14}' width='{max(2, bar_w * v['recent'] / most):.1f}' height='5' fill='{t['accent']}'/>")
    if not projects:
        out.append(text(30, 140, "No recent pushes yet.", 16, "text", t["muted"]))
    return ch, "".join(out)


def ledger_rows(stats):
    today = stats["now"].date()
    active = sum(1 for _, c in stats["days"] if c > 0)
    cp = round(stats["commits_private"] / stats["commits"] * 100) if stats["commits"] else 0
    pct = round(stats["private"] / stats["total"] * 100) if stats["total"] else 0
    return [
        ("Contributions", f"{num(stats['total'])} · {pct}% private"),
        ("Commits authored", f"{num(stats['commits'])} · {cp}% private"),
        ("Current streak", f"{data.current_streak(stats['days'], today)} days"),
        ("Longest streak", f"{data.longest_streak(stats['days'])} days"),
        ("Active days", f"{active} of {len(stats['days'])}"),
        ("Pull requests and reviews", num(stats["prs"] + stats["reviews"])),
        ("Repositories", f"{stats['repos']} · {stats['private_repos']} private"),
    ]


def tile_ledger(t, p, stats, cw, compact):
    ch = 440
    out = [card(cw, ch, t, p), heading(t, "The year, counted", "Last 12 months. Contributions are GitHub's calendar count; commits are counted from each repository's history.", cw)]
    for i, (label, value) in enumerate(ledger_rows(stats)):
        y = 142 + i * 40
        out.append(text(30, y, label, 16, "text", t["muted"]))
        out.append(text(cw - 30, y, value, 16, "medium", t["ink"], anchor="end"))
        if i < 6:
            out.append(f"<line x1='30' y1='{y + 16.5}' x2='{cw - 30}' y2='{y + 16.5}' stroke='{t['card_line']}'/>")
    return ch, "".join(out)


def pair(theme, layout, stats, left, right, title, split):
    """Two tiles in an asymmetric bento row on desktop; stacked and enlarged on phones."""
    t = THEMES[theme]
    p = f"{theme[0]}{layout[0]}{left.__name__[5:8]}"
    if layout == "wide":
        w1, w2 = split
        h1, b1 = left(t, p, stats, w1, False)
        h2, b2 = right(t, p, stats, w2, False)
        body = haze_def(t, p) + f"<g>{b1}</g><g transform='translate({w1 + 40} 0)'>{b2}</g>"
        return 1200, max(h1, h2) + 20, body, title, MOTION  # +20: air between bento rows
    cw = 460
    s = 600 / cw
    h1, b1 = left(t, p, stats, cw, True)
    h2, b2 = right(t, p, stats, cw, True)
    body = (haze_def(t, p) + f"<g transform='scale({s:.4f})'>{b1}</g>"
            f"<g transform='translate(0 {h1 * s + 24:.1f}) scale({s:.4f})'>{b2}</g>")
    return 600, round((h1 + h2) * s + 24 + 20), body, title, MOTION


def rhythm(theme, layout, stats):
    hours = stats["hours"]
    peak_h = max(range(24), key=lambda h: hours[h])
    langs = ", ".join(f"{n} {p:.0f}%" for n, p in data.top_languages(stats["langs"]))
    return pair(theme, layout, stats, tile_sun, tile_strata,
                f"When I build: most commits land at {peak_h:02d}:00 Lahore time. Languages: {langs}.", (700, 460))


def activity(theme, layout, stats):
    rows = ". ".join(f"{l}: {v}" for l, v in ledger_rows(stats))
    return pair(theme, layout, stats, tile_callsheet, tile_ledger, f"On stage now and the year counted. {rows}.", (460, 700))


# ---------------------------------------------------------------- work

def work_card(t, p, stats, i, cw, name, desc, stack, public):
    ch = 270 if cw < 500 else 246
    proj = stats["projects"].get(name, {"weeks": [], "total": 0})
    out = [card(cw, ch, t, p), text(28, 50, name, 22, "medium", t["ink"])]
    out.append(chip("open" if public else "private", t, cw - 28, 30))
    lines = wrap(desc, "text", 15, cw - 56, 3 if cw < 500 else 2)
    for j, line in enumerate(lines):
        out.append(text(28, 84 + j * 22, line, 15, "text", t["ink"], extra="fill-opacity='.86'"))
    sy = 84 + len(lines) * 22 + 8
    out.append(text(28, sy, stack, 13, "text", t["muted"]))
    # This project's own skyline: its 52 weeks of commits as a miniature city,
    # windows lit warm for private work and cool for open source.
    base, top = ch - 26, ch - 96
    sx0, sx1 = 28, cw - 180
    out.append(f"<line x1='{sx0}' y1='{base + .5}' x2='{cw - 28}' y2='{base + .5}' stroke='{t['haze']}' stroke-opacity='.8'/>")
    if proj["total"] < 20:
        # Under 20 matched commits the count would describe the matching, not
        # the project, so the card makes no claim about activity at all.
        return ch, "".join(out)
    weeks = proj["weeks"] or [0] * 52
    pitch = (sx1 - sx0) / len(weeks)
    peak = max(weeks) or 1
    front, side, roof = t["mini"]
    win = t["win_public"] if public else t["win_private"]
    bw, d = max(pitch - 2.2, 2), 2.6
    for k, c in enumerate(weeks):
        if not c:
            continue
        h = max(4, (base - top) * (c / peak) ** .5)
        x, y = sx0 + k * pitch, base - h
        out.append(f"<rect x='{x:.1f}' y='{y:.1f}' width='{bw:.1f}' height='{h:.1f}' fill='{front}'/>")
        wy = y + 3
        while wy < base - 3:
            out.append(f"<rect x='{x + bw / 2 - .9:.1f}' y='{wy:.1f}' width='1.8' height='1.8' fill='{win}'/>")
            wy += 4
        out.append(f"<polygon points='{x + bw:.1f},{y:.1f} {x + bw + d:.1f},{y - d * .6:.1f} {x + bw + d:.1f},{base - d * .6:.1f} {x + bw:.1f},{base}' fill='{side}'/>")
        out.append(f"<polygon points='{x:.1f},{y:.1f} {x + d:.1f},{y - d * .6:.1f} {x + bw + d:.1f},{y - d * .6:.1f} {x + bw:.1f},{y:.1f}' fill='{roof}'/>")
    out.append(text(cw - 28, base - 18, num(proj["total"]), 22, "display", t["ink"], anchor="end"))
    out.append(text(cw - 28, base - 2, "commits · last 12 months", 12, "text", t["muted"], anchor="end"))
    return ch, "".join(out)


def work(theme, layout, stats):
    t = THEMES[theme]
    p = f"w{theme[0]}{layout[0]}"
    parts = [haze_def(t, p)]
    if layout == "wide":
        y = 0
        for r in range(0, len(SHOWCASE), 2):
            row_h = 0
            for c, item in enumerate(SHOWCASE[r:r + 2]):
                h, b = work_card(t, p, stats, r + c, 580, *item)
                parts.append(f"<g transform='translate({c * 620} {y})'>{b}</g>")
                row_h = max(row_h, h)
            y += row_h + 24
        W, H = 1200, y - 24
    else:
        cw, y = 460, 0
        s = 600 / cw
        for i, item in enumerate(SHOWCASE):
            h, b = work_card(t, p, stats, i, cw, *item)
            parts.append(f"<g transform='translate(0 {y:.1f}) scale({s:.4f})'>{b}</g>")
            y += h * s + 20
        W, H = 600, round(y - 20)
    title = "Selected work: " + "; ".join(
        f"{n} ({'open source' if pub else 'private'}): {d} {stats['projects'].get(n, {}).get('total', 0)} commits in the last 12 months."
        for n, d, _, pub in SHOWCASE)
    return W, H, "".join(parts), title, ""


# ---------------------------------------------------------------- chips & buttons

def chip(kind, t, right_x, y):
    label, solid = ("Private", True) if kind == "private" else ("Open source", False)
    w = round(width(label, "medium", 12) + 22)
    x = right_x - w
    if solid:
        return (f"<rect x='{x}' y='{y}' width='{w}' height='22' rx='11' fill='{t['chip']}'/>" +
                text(x + 11, y + 15.5, label, 12, "medium", t["chip_on"]))
    return (f"<rect x='{x + .75}' y='{y + .75}' width='{w - 1.5}' height='20.5' rx='10.25' fill='none' "
            f"stroke='{t['chip_line']}' stroke-width='1.5'/>" + text(x + 11, y + 15.5, label, 12, "medium", t["chip_line"]))


BUTTONS = {
    "email": dict(label="umer.jahangier@gmail.com", icon="mail", primary=True),
    "email-praivox": dict(label="hello@praivox.com", icon="mail", primary=True),
    "praivox": dict(label="praivox.com", icon="globe", primary=False),
    "linkedin": dict(label="LinkedIn", icon="linkedin", primary=False),
    "instagram": dict(label="Instagram", icon="instagram", primary=False),
}

ICONS = {
    "mail": "<rect x='1' y='3' width='18' height='14' rx='2.5' fill='none' stroke='{c}' stroke-width='1.8'/>"
            "<path d='M1.8 4.6 10 11l8.2-6.4' fill='none' stroke='{c}' stroke-width='1.8' stroke-linejoin='round'/>",
    "linkedin": "<rect x='1' y='1' width='18' height='18' rx='3.5' fill='{c}'/>"
                "<path d='M5.2 8h2.3v7H5.2zM6.35 4.4a1.3 1.3 0 1 1 0 2.6 1.3 1.3 0 0 1 0-2.6zM9.2 8h2.2v1c.4-.7 1.3-1.2 2.4-1.2 2.2 0 2.7 1.4 2.7 3.3V15h-2.3v-3.4c0-.9-.1-1.9-1.2-1.9s-1.5.9-1.5 1.8V15H9.2z' fill='{g}'/>",
    "instagram": "<rect x='1.9' y='1.9' width='16.2' height='16.2' rx='4.6' fill='none' stroke='{c}' stroke-width='1.8'/>"
                 "<circle cx='10' cy='10' r='3.7' fill='none' stroke='{c}' stroke-width='1.8'/>"
                 "<circle cx='14.6' cy='5.4' r='1.1' fill='{c}'/>",
    "globe": "<circle cx='10' cy='10' r='8.2' fill='none' stroke='{c}' stroke-width='1.8'/>"
             "<path d='M1.8 10h16.4M10 1.8c2.4 2.3 3.4 5 3.4 8.2s-1 5.9-3.4 8.2c-2.4-2.3-3.4-5-3.4-8.2s1-5.9 3.4-8.2z' fill='none' stroke='{c}' stroke-width='1.6'/>",
}


def button(theme, name):
    t, b = THEMES[theme], BUTTONS[name]
    w = round(52 + width(b["label"], "medium", 16) + 46)
    H = 50
    if b["primary"]:
        bg = f"<rect width='{w}' height='{H}' rx='14' fill='{t['chip']}'/>"
        fg, glyph_bg = t["chip_on"], t["chip"]
    else:
        bg = (f"<rect x='.75' y='.75' width='{w - 1.5}' height='{H - 1.5}' rx='13.25' fill='{t['card']}' "
              f"stroke='{t['card_line']}' stroke-width='1.5'/>")
        fg, glyph_bg = t["ink"], t["card"]
    icon = ICONS[b["icon"]].format(c=fg, g=glyph_bg)
    arrow = (f"<path d='M{w - 30} {H / 2 + 5}l9-9m-6.5 0H{w - 21}v6.5' fill='none' stroke='{fg}' "
             f"stroke-width='1.7' stroke-linecap='round' stroke-linejoin='round'/>")
    body = bg + f"<g transform='translate(20 15)'>{icon}</g>" + text(52, 31, b["label"], 16, "medium", fg) + arrow
    return w, H, body, b["label"], ""
