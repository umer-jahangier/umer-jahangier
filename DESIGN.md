---
name: umer-jahangier profile
description: A GitHub profile set as a Swiss annual report, one cobalt field and live numbers that count private work.
colors:
  cobalt: "#2340F0"
  cobalt-2: "#4A62F2"
  cobalt-3: "#6479F4"
  cobalt-rest: "#7487F4"
  on-field-muted: "#DDE2FF"
  paper: "#FFFFFF"
  ink: "#0B0D12"
  muted: "#5A6170"
  rule: "#D9DCE3"
  slate-5: "#6E7482"
  slate-6: "#838997"
  night-ground: "#0D1117"
  night-ink: "#E8ECF2"
  night-muted: "#9AA3B2"
  night-rule: "#2A313C"
  night-cobalt: "#2F4BFF"
  night-accent: "#93A3FF"
  night-peak: "#B9C3FF"
  night-rest: "#4F63E6"
  night-step-1: "#A9B5FF"
  night-step-2: "#8595FF"
  night-step-3: "#6A7DFA"
  night-step-4: "#5468F0"
  night-slate-5: "#8A93A3"
  night-slate-6: "#6B7383"
typography:
  display:
    fontFamily: "Archivo Expanded (embedded 'A-display'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "86px"
    fontWeight: 800
    lineHeight: "90px"
    letterSpacing: "-2px"
    fontVariation: "'wdth' 125, 'wght' 800"
  display-figure:
    fontFamily: "Archivo Expanded (embedded 'A-display'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "64px"
    fontWeight: 800
    letterSpacing: "-1.5px"
    fontVariation: "'wdth' 125, 'wght' 800"
  headline:
    fontFamily: "Archivo (embedded 'A-medium'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "27px"
    fontWeight: 600
    fontVariation: "'wdth' 100, 'wght' 600"
  title:
    fontFamily: "Archivo (embedded 'A-medium'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "16px"
    fontWeight: 600
    fontVariation: "'wdth' 100, 'wght' 600"
  body:
    fontFamily: "Archivo (embedded 'A-text'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: "36px"
    fontVariation: "'wdth' 100, 'wght' 400"
  body-figure:
    fontFamily: "Archivo (embedded 'A-medium'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "17px"
    fontWeight: 600
    fontVariation: "'wdth' 100, 'wght' 600"
  label:
    fontFamily: "Archivo (embedded 'A-text'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    fontVariation: "'wdth' 100, 'wght' 400"
  chip:
    fontFamily: "Archivo (embedded 'A-medium'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "12px"
    fontWeight: 600
    fontVariation: "'wdth' 100, 'wght' 600"
rounded:
  none: "0px"
spacing:
  bar-gap: "2px"
  grid: "8px"
  button-inset: "20px"
  field-pad: "32px"
  field-pad-narrow: "40px"
  row: "36px"
  block-gutter: "72px"
  tick: "80px"
components:
  button-primary:
    backgroundColor: "{colors.cobalt}"
    textColor: "{colors.paper}"
    typography: "{typography.title}"
    rounded: "{rounded.none}"
    padding: "0 30px 0 20px"
    height: "48px"
  button-primary-dark:
    backgroundColor: "{colors.night-cobalt}"
    textColor: "{colors.paper}"
    typography: "{typography.title}"
    rounded: "{rounded.none}"
    height: "48px"
  button-secondary:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.title}"
    rounded: "{rounded.none}"
    padding: "0 30px 0 20px"
    height: "48px"
  button-secondary-dark:
    backgroundColor: "{colors.night-ground}"
    textColor: "{colors.night-ink}"
    typography: "{typography.title}"
    rounded: "{rounded.none}"
    height: "48px"
  tag-private:
    backgroundColor: "{colors.cobalt}"
    textColor: "{colors.paper}"
    typography: "{typography.chip}"
    rounded: "{rounded.none}"
    padding: "0 10px"
    height: "22px"
  tag-private-dark:
    backgroundColor: "{colors.night-cobalt}"
    textColor: "{colors.paper}"
    typography: "{typography.chip}"
    rounded: "{rounded.none}"
    height: "22px"
  tag-open:
    textColor: "{colors.cobalt}"
    typography: "{typography.chip}"
    rounded: "{rounded.none}"
    padding: "0 10px"
    height: "22px"
  tag-open-dark:
    textColor: "{colors.night-accent}"
    typography: "{typography.chip}"
    rounded: "{rounded.none}"
    height: "22px"
  cover-field:
    backgroundColor: "{colors.cobalt}"
    textColor: "{colors.paper}"
    padding: "{spacing.field-pad}"
    width: "480px"
    height: "440px"
  cover-field-dark:
    backgroundColor: "{colors.night-cobalt}"
    textColor: "{colors.paper}"
    padding: "{spacing.field-pad}"
  ledger-row:
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    height: "38px"
    width: "352px"
---

# Design System: umer-jahangier profile

## Overview

**Creative North Star: "The Annual Report"**

The profile is typeset as a Swiss International Style annual report of one engineer's year. A white page (GitHub's ink ground in dark mode) carries one expanded name and one committed cobalt field that owns a whole region of the cover. Numbers are the evidence: the year's contributions, the private share, the languages, the weekly rhythm and a ledger are set as report figures, measured on hairline rules and tick marks, and rebuilt every day from the API.

Everything visual is a generated SVG, because GitHub's sanitizer strips CSS from the page. The system lives in `scripts/profile.py`: two theme token sets, fixed geometry per layout, and a small set of builders (cover, three number blocks, buttons, chips). Density is report-like: generous ground on the left, a packed data field on the right, figures right-aligned against labels. The world rejects the neon-terminal dev profile and the badge wall.

**Key Characteristics:**
- One cobalt field per cover, holding the live 52-week chart in white.
- A single visual code everywhere: solid means private (or primary), outline means public (or secondary).
- Archivo embedded in three cut instances: expanded black for the name and the headline figure, normal-width semibold and regular for everything else.
- Hairline rules and 80px tick marks; square corners; whole-pixel bar pitches.
- Ink, cobalt tints and neutral slates only. No language brand colours.
- One motion: a single oscilloscope sweep across the chart, invisible at its first and last frame.

## Colors

A two-theme palette of paper, ink and one cobalt, with cobalt tints and slates doing all data work.

### Primary
- **Report Cobalt** (cobalt): the field. Fills the cover's right 40% (below the name on phones), the primary contact button, the Private chip, the top-ranked language and the busiest weekday bar. White on it measures 6.86:1.
- **Night Cobalt** (night-cobalt): the same field in dark mode, lifted slightly so it holds against GitHub's ink ground; white on it measures 5.88:1.
- **Night Accent** (night-accent): cobalt as a line on dark ground, used for the Open source chip outline and its label (8.04:1).

### Secondary
- **Cobalt Rank Tints** (cobalt-2, cobalt-3, cobalt-rest; dark: night-step-1 to night-step-4): language shares by rank, and the non-peak weekday bars (cobalt-rest light, night-rest dark). Salience follows share. Every mark is at least 3:1 on its ground.
- **Field Mist** (on-field-muted): secondary text on the cobalt field (the contributions label, month ticks, peak label, public share). 5.35:1 on cobalt, 4.59:1 on night cobalt.

### Neutral
- **Paper** (paper) / **Ink Ground** (night-ground): the page. The dark ground matches GitHub's own dark canvas so the cover bleeds into it.
- **Ink** (ink) / **Night Ink** (night-ink): names, figures, row values, block heads and the block-head rule.
- **Report Grey** (muted) / **Night Grey** (night-muted): role line, ledger labels, colophon, unselected weekday labels (6.22:1 and 7.44:1).
- **Hairline** (rule) / **Night Hairline** (night-rule): row dividers, the colophon rule and its ticks. Decorative dividers only, never a text colour.
- **Slates** (slate-5, slate-6; dark: night-slate-5, night-slate-6): the fifth language and "Other", so the tail reads as neutral rather than as another brand hue.

### Named Rules
**The One Field Rule.** Cobalt appears as a filled region or as a ranked datum. It never tints running text, never decorates, and there is one field per surface.

**The Ranked Tint Rule.** Categorical series are coloured by rank in cobalt tints, then slates. Language brand colours (the GitHub rainbow) are never used.

**The Legible Mark Rule.** Text on any ground is at least 4.5:1; every chart mark is at least 3:1. A new tint earns its place by passing both in both themes.

## Typography

**Display Font:** Archivo, expanded black instance (wdth 125, wght 800), embedded as base64 woff2 subset (with 'Helvetica Neue', Helvetica, Arial)
**Body Font:** Archivo, normal width, regular (wdth 100, wght 400) and semibold (wdth 100, wght 600) instances, embedded the same way

**Character:** One grotesque family in two widths. The expanded black is the report's masthead voice; the normal width is the report's reading and figure voice. Each SVG embeds only the instances it uses.

### Hierarchy
- **Display** (800 expanded, 86px wide / 70px phone, -2px tracking, 90px / 78px baseline step): the name, set once on two lines. The one word big enough to win.
- **Display figure** (800 expanded, 64px wide / 58px phone, -1.5px tracking): the year's contribution total on the field. The only other use of the display cut.
- **Headline** (600, 27px wide / 24px phone): the role line under the name.
- **Title** (600, 16px): number-block heads above an ink rule, and button labels.
- **Body** (400, 17px on a 36px row; ledger 38px): language names and ledger labels; the paired value on the same row is Body figure (600, 17px), right-aligned.
- **Label** (400, 13–15px): peak label, month ticks, weekday labels, colophon, secondary lines. City line is 19px regular in Report Grey.
- **Chip** (600, 12px): the Private / Open source chips.

The markdown between the SVGs (section heads, table, toolbox, paragraph) renders in GitHub's own type; the medium does not allow it to be restyled.

### Named Rules
**The One Big Word Rule.** The expanded display cut is reserved for the name and the single headline figure. Nothing else is set expanded.

**The Figure Weight Rule.** Labels are regular, their values semibold and right-aligned; weight, not colour, separates a number from its caption.

## Layout

Two fixed canvases per visual, never fluid. Wide covers are 1200 x 440: name block on the left 60% (x 0 to 640), cobalt field from x 720 to the right edge, 32px field padding. Phone covers are 600 x 860: name on top, field full-width from y 320, 40px padding. The number band is 1200 x 360 wide (three 352px blocks on a 72px gutter, at x 0 / 424 / 848) and 600 x 1390 on phones (the same blocks stacked and scaled 1.25x).

Rhythm is on an 8px grid with integer edges: 36px list rows, 38px ledger rows, 80px colophon ticks, 48px buttons, 22px chips. Bar charts divide their span into 52 whole-pixel pitches (8px = 6 + 2 wide, 10px = 8 + 2 phone) so every bar edge is crisp; 1px hairlines sit on half-pixel offsets.

Responsive behaviour follows the sanitizer. Each full-width visual is a `<picture>` whose first source is `(max-width: 600px)` pointing at a single adaptive SVG that carries both themes and switches internally on `prefers-color-scheme`; the next source is the dark wide SVG; the `<img>` is the light wide SVG. Buttons and chips use a plain two-source `<picture>`. Page order: cover, contact row, one paragraph, selected work table, numbers, toolbox, contribution snake, closing contact line.

### Named Rules
**The Fixed Budget Rule.** Every figure has a fixed geometry per layout; values change daily, the frame does not. New data must fit the existing box.

**The Whole Pixel Rule.** Bar pitches are whole pixels and hairlines sit on .5 offsets. No fractional bar widths on the cover.

## Elevation & Depth

Flat. There are no shadows anywhere; depth is carried by the cobalt field against the ground and by hairline rules. The only translucency is in-field: zero-contribution weeks at 35% white, the chart baseline at 50%, month ticks at 70%, and the sweep's trailing band at 14%.

### Named Rules
**The Flat Report Rule.** Surfaces are printed, not lifted. No drop shadows, glows or offset shadows on any element.

## Shapes

Square everything: fields, bars, buttons, chips, swatches and the split bar have 0 radius. Outlines are 1.5px strokes inset by 0.75px so they land on whole pixels; hairlines are 1px. The private/public split bar is a 12px solid segment followed, after a 3px gap, by a 1px outlined segment. Rounding appears only inside the drawn LinkedIn, Instagram and mail marks, which are reproductions of those marks, not a corner style.

## Components

### Buttons
Contact is one row of 48px-tall SVG buttons directly under the cover.
- **Shape:** square corners (0px), height 48px, width fits the label.
- **Primary:** Report Cobalt fill, white label (Title, 16px semibold); email only. Dark: Night Cobalt.
- **Secondary:** page-ground fill with a 1.5px ink outline, ink label; LinkedIn, Instagram, praivox.com. Dark: ink ground, night-ink outline.
- **Anatomy:** a 20px drawn mark at x 20, the label at x 52, a drawn north-east arrow 30px from the right edge in the label colour.
- **States:** none; these are images inside links, and GitHub owns hover and focus.

### Chips
- **Private:** solid cobalt rectangle, white 12px semibold label, 22px tall.
- **Open source:** 1.5px cobalt outline (Night Accent in dark), label in the outline colour.
- **Use:** under each project name in the selected-work table. The chip code matches the cover's split bar.

### Cover
The signature component. Left: name in Display, role in Headline, city line in Report Grey, then (wide only) an 80px-ticked hairline colophon with the profile URL and update date. Right: the cobalt field with the display figure, its label in Field Mist, 52 white weekly bars on a square-root scale with a peak tick and label, quarter month ticks, and the private/public split bar with its two labels. On phones the colophon moves inside the field's foot.

### Number blocks
Three blocks, each opened by a Title head over a full-width 1px ink rule.
- **Languages:** an 18px stacked share bar (2px gaps), then 12px square swatches with names left and semibold percentages right, one hairline per row.
- **Weekly rhythm:** seven bars on a 12px gap, the busiest day in the peak colour with an ink label, the rest in the rest colour with grey labels; a semibold sentence and grey caption below.
- **Ledger ("The year, counted"):** grey label left, semibold ink value right, hairline under each 38px row.

### Sweep (motion)
One oscilloscope pass across the chart: a 2px white scan line with a 24px band at 14%, 2.4s `cubic-bezier(.45,0,.2,1)` after a .3s delay, opacity 0 at the first and last keyframe so a renderer that never advances time shows the finished chart. Removed under `prefers-reduced-motion`.

## Do's and Don'ts

### Do:
- **Do** generate every visual as an SVG from `THEMES` and `COVER_GEOMETRY` in `scripts/profile.py`, in a light, a dark and (for full-width visuals) an adaptive phone file.
- **Do** keep solid for private or primary and outline for public or secondary, everywhere.
- **Do** colour categorical data by rank in cobalt tints, then slates, and check every mark at 3:1 and every text pair at 4.5:1 in both themes.
- **Do** embed only the Archivo instances a file uses, with the Helvetica stack as fallback.
- **Do** keep bars on whole-pixel pitches and hairlines on half-pixel offsets.
- **Do** make any animation invisible at its first and last frame and remove it under reduced motion.

### Don't:
- **Don't** use language brand colours or any hue outside ink, cobalt tints and slates.
- **Don't** set anything but the name and the headline figure in the expanded display cut.
- **Don't** add shadows, glows or rounded corners to fields, bars, buttons or chips.
- **Don't** put a second cobalt field on a surface or tint running text cobalt.
- **Don't** load third-party image services or external fonts; everything renders from this repo.
- **Don't** let a figure grow its box; values change inside a fixed geometry.
