---
name: umer-jahangier profile
description: A GitHub profile set as a cyclorama, a stage lit from night to day where light shows a year of mostly private work.
colors:
  night-sky: "#03040A"
  night-sky-mid: "#080B22"
  night-horizon-deep: "#131C5E"
  night-cobalt: "#2A3DE0"
  night-glow: "#3B5BFF"
  night-horizon: "#5A76FF"
  night-accent: "#6F87FF"
  night-rose-glow: "#FF6F91"
  night-rose: "#FF7A9A"
  night-rose-soft: "#FFB8C8"
  night-ground: "#0B1030"
  night-ground-floor: "#04050C"
  night-card: "#080A15"
  night-card-line: "#1C2238"
  night-ink: "#F2F3F8"
  night-muted: "#A7AECC"
  night-faint: "#6B7394"
  night-building-front: "#10152E"
  night-building-side: "#0A0E22"
  night-building-roof: "#1D2552"
  night-window-private: "#FFC4D2"
  night-window-public: "#8FA2FF"
  night-window-off: "#161C3A"
  night-dial-day: "#1A1530"
  night-dial-night: "#0C1030"
  moon: "#F6F2FF"
  day-sky: "#FFFFFF"
  day-sky-mid: "#FCFCFF"
  day-haze-pale: "#FFE8EE"
  day-haze: "#FFCBD7"
  day-glow: "#FF9DB3"
  day-periwinkle: "#6D80F6"
  cobalt: "#2340F0"
  cobalt-deep: "#1627B0"
  cobalt-roof: "#7486F7"
  day-window-off: "#3550F2"
  day-window-private: "#FF93AE"
  day-window-public: "#DCE3FF"
  day-rose: "#C8325A"
  sun: "#FF7C9C"
  day-ground: "#FFEFF3"
  day-card: "#FFFFFF"
  day-card-line: "#E1E4F0"
  day-track: "#E7EAF4"
  day-ink: "#0B0D1A"
  day-muted: "#545B73"
  day-faint: "#8C92A8"
  day-dial-day: "#FFF1F5"
  day-dial-night: "#EDF0FD"
typography:
  display:
    fontFamily: "Archivo Expanded (embedded 'A-display'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "82px"
    lineHeight: 1
    letterSpacing: "-2px"
  figure:
    fontFamily: "Archivo Expanded (embedded 'A-display'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "44px"
    lineHeight: 1
    letterSpacing: "-1px"
  headline:
    fontFamily: "Archivo Medium (embedded 'A-medium'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "26px"
    fontWeight: 500
    lineHeight: 1.2
  title:
    fontFamily: "Archivo Medium (embedded 'A-medium'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "20px"
    fontWeight: 500
    lineHeight: 1.2
  body:
    fontFamily: "Archivo (embedded 'A-text'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.45
  caption:
    fontFamily: "Archivo (embedded 'A-text'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.4
  label:
    fontFamily: "Archivo (embedded 'A-text'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.3
  chip:
    fontFamily: "Archivo Medium (embedded 'A-medium'), 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "12px"
    fontWeight: 500
    lineHeight: 1
rounded:
  hero: "22px"
  card: "18px"
  button: "14px"
  chip: "11px"
spacing:
  card-inset: "30px"
  work-inset: "28px"
  gutter: "40px"
  work-row: "24px"
  bento-row: "20px"
  row-pitch: "40px"
components:
  button-primary:
    backgroundColor: "{colors.cobalt}"
    textColor: "{colors.day-card}"
    typography: "{typography.title}"
    rounded: "{rounded.button}"
    height: "50px"
    padding: "0 46px 0 20px"
  button-primary-night:
    backgroundColor: "{colors.night-glow}"
    textColor: "{colors.day-card}"
    rounded: "{rounded.button}"
    height: "50px"
    padding: "0 46px 0 20px"
  button-secondary:
    backgroundColor: "{colors.day-card}"
    textColor: "{colors.day-ink}"
    rounded: "{rounded.button}"
    height: "50px"
    padding: "0 46px 0 20px"
  button-secondary-night:
    backgroundColor: "{colors.night-card}"
    textColor: "{colors.night-ink}"
    rounded: "{rounded.button}"
    height: "50px"
    padding: "0 46px 0 20px"
  chip-private:
    backgroundColor: "{colors.cobalt}"
    textColor: "{colors.day-card}"
    typography: "{typography.chip}"
    rounded: "{rounded.chip}"
    height: "22px"
    padding: "0 11px"
  chip-open:
    textColor: "{colors.cobalt}"
    typography: "{typography.chip}"
    rounded: "{rounded.chip}"
    height: "22px"
    padding: "0 11px"
  chip-open-night:
    textColor: "{colors.night-window-public}"
    rounded: "{rounded.chip}"
    height: "22px"
    padding: "0 11px"
  stage-card:
    backgroundColor: "{colors.day-card}"
    rounded: "{rounded.card}"
    padding: "{spacing.card-inset}"
  stage-card-night:
    backgroundColor: "{colors.night-card}"
    rounded: "{rounded.card}"
    padding: "{spacing.card-inset}"
  hero-stage:
    rounded: "{rounded.hero}"
    width: "1200px"
    height: "640px"
---

# Design System: umer-jahangier profile

## Overview

**Creative North Star: "The Cyclorama"**

The profile is a stage backdrop lit from night to day. Light shows a year of mostly private work. Dark mode is the night cue: a depthless black sky that deepens to a low cobalt horizon, rose light gathering above it, and a field of stars. Light mode is the day cue: a white wash, rose haze at the horizon, and cobalt architecture. Every chart is a piece of set. The year is a skyline of 52 weekly buildings, with lit windows for contributions and warm windows for private work. The day is the sun's path. Languages are strata of sky. Each named project stands on its own miniature skyline.

The world rejects two things by construction: the neon-terminal developer profile and the flat grid of stat cards. Depth comes from isometric buildings, a reflection in still water, and the horizon haze that rises from every card floor, never from drop shadows. Type is quiet except in two places: the name and the headline figures, set in an expanded heavy Archivo that spans the sky like a title card.

The medium is fixed and it shapes everything. GitHub sanitizes README markdown, so every visual is a generated SVG loaded through `<img>` inside a `<picture>`. Each SVG embeds its own Archivo subset as base64 WOFF2 and positions text from measured glyph widths, because an `<img>` SVG cannot load external fonts. Desktop gets separate `-light` and `-dark` files switched by `prefers-color-scheme`. Phones get one `-mobile` file through a `(max-width: 600px)` source. GitHub's themed picture leaves that plain media query alone, so the mobile file carries both cues and switches internally.

**Key Characteristics:**
- Two lighting cues of one stage, night (dark) and day (light), always shipped as a pair.
- Isometric skylines as data: height and lit windows encode contributions; warm windows encode private work.
- Horizon haze rising from the floor of every card; hairline edges; no shadows.
- Expanded heavy Archivo for the name and figures only; Archivo Medium and Text for everything else.
- Ambient motion only (twinkling windows and stars, a breathing horizon, a live-push pulse), and every loop starts from the finished frame.

## Colors

The palette is cobalt and rose on black or white. Cobalt is architecture and structure; rose is light and warmth. The two themes are two cues on the same stage, not an inverted copy of each other.

### Primary
- **Cyc Cobalt** (cobalt / night-cobalt / night-glow): the day cue's architecture (building fronts, primary buttons, solid chips, accent bars, the horizon line), and at night the horizon floor and the glow that lights the skyline from below. Deep and roof shades (cobalt-deep, cobalt-roof; night-building-side, night-building-roof) give the isometric side and top faces.
- **Horizon Periwinkle** (night-horizon, night-accent): the lit horizon line and ground ripples at night, and the night-tone accent for sun-dial night hours and push bars.

### Secondary
- **Stage Rose** (day-rose, night-rose, night-rose-glow, day-glow): the warm light. It is the day haze and the sun's glow, the second tint that drifts above the horizon at night, day hours on the sun dial, the "today" call-sheet dot and its pulse, and the short credit rule under the hero stats. Day rose (the deep shade) is the only rose used for text on white.
- **Sun and Moon** (sun, moon): the single celestial body placed where the name ends, a rose disc with two halo rings by day and a crescent by night.

### Tertiary
- **Window Light** (day-window-private / night-window-private warm, day-window-public / night-window-public cool, *-window-off unlit): the private/public encoding. Warm pink windows are private work and cool periwinkle windows are public work. Unlit windows sink into the building face.

### Neutral
- **Night Sky and Ground** (night-sky → night-sky-mid → night-horizon-deep → night-cobalt; night-ground → night-ground-floor): the vertical gradients of the night stage.
- **Day Wash** (day-sky → day-sky-mid → day-haze-pale → day-haze; day-ground → day-sky): the vertical gradients of the day stage.
- **Stage Card** (night-card, day-card) with **Hairline** (night-card-line, day-card-line): tile backgrounds and their 1px edges, which also serve as ledger dividers and dial centers.
- **Ink, Muted, Faint** (night-/day-ink, -muted, -faint): primary text, secondary text and axis labels, and idle status dots.
- **Dial Halves and Track** (*-dial-day, *-dial-night, day-track): the tinted day and night half-discs of the sun dial and empty progress tracks.

### Named Rules
**The Warm Window Rule.** Private is warm and public is cool, everywhere the distinction is drawn: warm windows for private work and cool windows for public work, in the hero skyline and every work card. Chips carry the same split as fill: solid for private, outlined for open source. Never swap the two, and never draw the distinction with a third color.

**The Two Cues Rule.** Every surface ships both cues from the same builder with the same geometry; only the THEMES tokens change. A color that exists in only one cue is a bug unless it is the sky itself (stars and moon at night, sun by day).

## Typography

**Display Font:** Archivo, expanded heavy cut (embedded as `A-display`), falling back to Helvetica Neue, Helvetica, Arial
**Body Font:** Archivo Text (`A-text`) with the same fallback
**Label Font:** Archivo Medium (`A-medium`)

**Character:** A wide title card over a calm grotesque. The expanded display cut is roughly a third wider than the text cut and carries the name and the numbers. Medium and Text do all the reading.

### Hierarchy
- **Display** (expanded heavy, 82px desktop / 66px phone on two lines, -2px tracking): the name only, set in one line across the sky.
- **Figure** (expanded heavy, 44px desktop / 40px phone, -1px tracking; 22px for work-card commit counts): headline numbers such as busiest hour, share after dark, and project commits.
- **Headline** (Medium 500, 26px desktop / 22px phone): the role line under the name.
- **Title** (Medium 500, 20px tile headings, 22px work-card names, 17px list rows, 16px button labels and ledger values).
- **Body** (Text 400, 15–16px): work-card descriptions (at 0.86 ink opacity) and ledger labels in muted.
- **Caption** (Text 400, 14px, muted): tile sub-lines, wrapped to at most two lines.
- **Label** (Text 400, 13px; 11–12px for dial and count captions): axis ticks, legends, stacks, and timestamps.
- **Chip** (Medium 500, 12px).

### Named Rules
**The Expanded Name Rule.** The expanded display cut is reserved for the name and for numbers. Headings, labels, and prose never use it.

**The Measured Text Rule.** Every string is embedded, not linked, and laid out from `metrics.json` glyph widths. It wraps to a fixed line budget and ends in an ellipsis rather than overflowing. Never position text by guessing, and never rely on a system font rendering the same way.

## Layout

The canvas is 1200px wide on desktop and 600px on phones. The README stacks full-width `<picture>` panels. There is a hero stage (1200×640), a contact button row, one line of prose, two asymmetric bento rows, a selected-work grid, a markdown toolbox, the snake, and a closing contact line.

- **Hero geometry:** the horizon sits at y=500 of 640 desktop (820 of 1010 phone). The name baseline is at 118 from a 54px left edge, followed by role, location line, credit line, and a 56×3 rose rule. 52 buildings span x 48–1152 (14px wide, 7px isometric depth, up to 232px tall; 7px, 4px, 340px on phones). The legend and "Updated" colophon sit on the ground at y=606.
- **Bento rows:** tiles are 440px tall. The first row is 700 | 460 and the second is 460 | 700, with a 40px gutter and 20px of air below each row. On phones the pair stacks and scales 460→600 (factor 1.304), with 24px between tiles.
- **Work grid:** two 580px columns on a 620px pitch (40px gutter), 246px cards, and 24px row gaps. On phones there is one column scaled to 600, 270px cards, and 20px gaps.
- **Insets:** tile content starts 30px in from the card edge and work-card content 28px in. Ledger rows run on a 40px pitch and call-sheet rows on a 60px pitch.

**The Asymmetric Bento Rule.** Paired tiles are never equal. The wide tile alternates sides row to row (700/460, then 460/700), so the eye zig-zags down the stage.

## Elevation & Depth

The system has no shadows. Depth is built from the stage itself. Vertical sky and ground gradients meet at a bright 2px horizon. Isometric side and roof faces on every building run one shade darker and one shade lighter than the front. The skyline is mirrored at the horizon at 0.5 opacity and faded by a luminance mask. Five dashed ripple lines widen as they approach the viewer. Radial glows (horizon glow at 0.9→0 opacity, second tint at 0.55→0) light the backdrop. On cards, a linear haze in the theme's haze color rises from 0 to 0.16 opacity over the bottom 110px.

**The One Horizon Rule.** Every card is a small stage and carries the theme's horizon haze on its floor: cobalt at night, rose by day. The horizon is the only light source, so a surface lifts by standing on it, never by casting a shadow.

**The Hairline Rule.** Containers are defined by a 1px card-line edge (1.5px on outlined buttons and chips). Nothing gets a drop shadow, an offset shadow, or a glow on its edge.

## Shapes

Soft rounded rectangles hold hard-edged architecture. The hero stage has a 22px radius, tiles and work cards 18px, buttons 14px, and chips are full pills (11px on a 22px height). Everything drawn inside the stages is square: buildings, windows (3×3.2px hero, 1.8px work cards), strata bands separated by 3px gaps, and progress tracks 5px tall. The sun-dial wedges are annular sectors with 0.9° gaps. Status dots are circles with a 5px radius.

## Components

### Buttons
Contact is the one action, so buttons are calm, wide, and explicit.
- **Shape:** gently rounded (14px), 50px tall. The width is measured from the label (label width + 98px).
- **Primary (email):** solid cobalt fill (night-glow at night) with white label and glyph. A 20px inline SVG mail icon sits at x=20, the label at x=52, and an up-right arrow stroke 30px from the right edge.
- **Secondary (LinkedIn, Instagram, praivox.com):** card fill with a 1.5px hairline edge and ink label, icon, and arrow.
- **States:** none. The buttons are images inside `<a>` links, and GitHub gives them no hover or focus styling beyond its own.

### Chips
- **Private:** a solid cobalt pill (night-glow at night) with a white 12px Medium label.
- **Open source:** an outlined pill, 1.5px cobalt edge (night-window-public at night), with the label in the edge color.
- Chips sit top-right on work cards, right-aligned 28px from the edge.

### Stage Cards (tiles)
- **Corner Style:** 18px.
- **Background:** stage card color, a 1px hairline, and floor haze (see Elevation).
- **Heading block:** a 20px Medium title at (30, 50) and a 14px muted sub-line at 76, wrapped to two lines.
- **Tiles in use:** *When I build* (the sun path: 24 annular wedges over a day/night split disc, rose for 06–18 and cobalt for night, the peak hour at full opacity and the rest at 0.78; a 24h hub; two display figures). *Languages* (strata: stacked ramp bands with leader lines to labels). *On stage now* (call sheet: five latest pushes, a rose pulsing dot for today or yesterday, a faint dot otherwise, a 30-day commit bar in accent on a track). *The year, counted* (ledger: seven muted-label, ink-value rows with hairline dividers).

### Work Card (signature)
A 580×246 stage holding the project name (22px Medium), a chip, a description (15px, 2–3 lines), a 13px muted stack line, and the project's own 52-week miniature skyline standing on a haze-colored baseline. The skyline uses the theme's mini triad for front, side, and roof, with one window column per building, lit warm for private and cool for public. A display-cut commit count sits bottom-right.

**The Honest Silence Rule.** Under 20 matched commits the card draws only the empty baseline and makes no activity claim. An empty stage is correct; never fill it with invented or placeholder bars.

### Hero Stage (signature)
The first viewport: sky gradient, horizon glow, stars and moon (night) or haloed sun (day) at the end of the name, the 52-building skyline with its reflection and ripples, and a peak-week callout on the tallest tower. Quarter-month ticks run on the ground, followed by the private/public legend, a one-line key, and the updated date.

### Motion
All motion is CSS inside the SVG and is ambient. Lit windows twinkle (about 7% of them, 5.2s), stars twinkle (22% of them, 7s), the horizon glow breathes (9s, opacity 1→0.72), and today's call-sheet dot pulses (2.4s scale to 2.6 and fade). Delays are deterministic hashes, so the scene never reshuffles between daily builds.

**The Finished Frame Rule.** Every loop starts and ends at full opacity on the finished frame, so a static render, a first paint, or a screenshot is always the complete picture. `prefers-reduced-motion: reduce` turns every animation off and hides the pulse ring.

### Snake
The contribution snake is recolored to the world: a day-rose snake over cobalt dots on pale grounds by day, and a rose-soft snake over cobalt dots on night navy (steps listed in the sidecar).

## Do's and Don'ts

### Do:
- **Do** ship every new visual as a pair of cues from one builder: `-light` and `-dark` at 1200 wide, plus a `-mobile` file at 600 wide that carries both cues and switches on `prefers-color-scheme`.
- **Do** encode private as warm windows and solid chips, and public as cool windows and outlined chips.
- **Do** give every new tile the 18px stage card, the hairline, the floor haze, and the 30px heading block.
- **Do** keep paired tiles asymmetric (700/460 or 460/700) with a 40px gutter.
- **Do** start every animation loop from the finished frame and disable it under reduced motion.
- **Do** embed Archivo and measure every string; wrap to a line budget and ellipsize.
- **Do** draw data as set pieces on the stage: buildings, horizon, sky, sun path.

### Don't:
- **Don't** use drop shadows or offset shadows. Depth comes from the horizon, reflections, and isometric faces.
- **Don't** set headings, labels, or prose in the expanded display cut. It is for the name and numbers only.
- **Don't** make the night cue a neon terminal: no monospace, no green on black, no glow on type. Glow belongs to the horizon.
- **Don't** fall back to a flat grid of equal stat cards.
- **Don't** rely on markdown styling, external fonts, or interactivity. GitHub strips `<style>` from the README, and `<img>` SVGs cannot load resources.
- **Don't** draw activity for a project under 20 matched commits.
