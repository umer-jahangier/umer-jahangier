"""SVG building blocks: embedded Archivo, measured text, themed documents."""

import base64
import hashlib
import json
import os
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTS = os.path.join(ROOT, "assets", "fonts")
with open(os.path.join(FONTS, "metrics.json"), encoding="utf-8") as fh:
    METRICS = json.load(fh)

STACK = "'Helvetica Neue',Helvetica,Arial,sans-serif"


def fam(face):
    return f"'A-{face}',{STACK}"


def width(s, face, size, spacing=0):
    m = METRICS[face]
    return sum(m.get(ch, 0.6) for ch in str(s)) * size + spacing * max(len(str(s)) - 1, 0)


def wrap(s, face, size, max_w, max_lines=3):
    lines, line = [], ""
    for word in str(s).split():
        trial = f"{line} {word}".strip()
        if width(trial, face, size) <= max_w or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    lines.append(line)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(",.;:") + "…"
    return lines


def text(x, y, s, size, face, fill, anchor="start", extra=""):
    return (f"<text x='{x:g}' y='{y:g}' font-family=\"{fam(face)}\" font-size='{size}' "
            f"fill='{fill}' text-anchor='{anchor}' {extra}>{escape(str(s))}</text>")


def num(n):
    return f"{n:,}"


def _font_face(faces):
    rules = []
    for face in faces:
        with open(os.path.join(FONTS, f"archivo-{face}.woff2"), "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode()
        rules.append(f"@font-face{{font-family:'A-{face}';src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
    return "".join(rules)


def doc(w, h, title, body, style=""):
    faces = [f for f in ("display", "medium", "text") if f"'A-{f}'" in body]
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}' "
            f"role='img' aria-labelledby='t'><title id='t'>{escape(title)}</title>"
            f"<style>{_font_face(faces)}{style}</style>{body}</svg>\n")


def themed(builder, theme, layout, *args):
    w, h, body, title, style = builder(theme, layout, *args)
    return doc(w, h, title, body, style)


def adaptive(builder, layout, *args):
    """Both themes in one file, switched by the viewer's colour scheme.

    Phones get this file through a plain (max-width) <source>, which GitHub's
    <themed-picture> leaves alone. Ids are theme-prefixed by the builders, so
    the two copies never collide."""
    w, h, light, title, s1 = builder("light", layout, *args)
    _, _, dark, _, s2 = builder("dark", layout, *args)
    body = f"<g class='L'>{light}</g><g class='D'>{dark}</g>"
    css = ".D{display:none}@media (prefers-color-scheme:dark){.L{display:none}.D{display:inline}}"
    return doc(w, h, title, body, css + s1 + s2)


def hash01(*parts):
    """Deterministic 0..1 from its arguments, so windows and stars do not reshuffle daily.

    BLAKE2 rather than FNV: FNV outputs for ("sx", 1), ("sx", 2)... correlate,
    which lined the stars up along diagonals."""
    digest = hashlib.blake2b("|".join(map(str, parts)).encode(), digest_size=8).digest()
    return int.from_bytes(digest, "big") / 0xFFFFFFFFFFFFFFFF
