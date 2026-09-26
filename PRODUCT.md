# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

GitHub profile README (GitHub-flavored Markdown + sanitized HTML). Every visual is an SVG or image referenced by URL; no CSS, no JavaScript. Cards are generated in-repo by GitHub Actions from the GraphQL API and committed to `dist/`. Light and dark variants are served with `<picture>` + `prefers-color-scheme`.

## Users

One page, four audiences, all arriving from a link (LinkedIn, a proposal, a PR, a search):

- **Recruiters and employers** checking whether Umer can own real systems end to end.
- **Clients** deciding whether to hire him to build an AI automation or a SaaS product.
- **Engineering peers** judging the depth of the work and the open-source tools.
- **Collaborators** looking for how to reach him.

Each decides within seconds whether to scroll, and within a minute whether to make contact.

## Product Purpose

Present Muhammad Umer (`umer-jahangier`, Lahore, Pakistan) as an **AI, Automation & Full-Stack Engineer** who ships production systems, and turn the visit into contact. Success is a visitor who leaves knowing what he builds, believing he has shipped it, and holding one way to reach him.

## Positioning

Most of his output is private: 2,776 contributions in the last year, 1,697 of them to private repositories, across his own repos and client repos where he is a collaborator. The profile's claim is that the private work is real and measurable, shown through self-generated stats that include private activity (numbers only, never code).

## Capabilities and Constraints

- Two variants: `variants/README.personal.md` (default, no Praivox) and `variants/README.praivox.md` (founder framing). `README.md` is a copy of the active variant.
- Contact (personal): umer.jahangier@gmail.com · LinkedIn `muhammad-umer-jahangier` · Instagram `umer_jahangier`. Contact (Praivox): hello@praivox.com · praivox.com.
- Private repos may be named with a one-line description; no links, code or screenshots.
- GitHub strips `<style>`, scripts and most attributes from README HTML. SVGs loaded via `<img>` may animate (SMIL/CSS inside the SVG) but cannot load external fonts or be interactive.

## Evidence on Hand

Real projects (verified from repo READMEs, 2026-09-27):

- **SalesPulse AI**: AI sales-communication platform: power dialer, AI voice agents (Retell), SMS, CRM sync (Merge.dev), Stripe. Next.js 15, Prisma, Twilio. Private.
- **AlphaVenue**: celebration and venue platform: API, web and a React Native/Expo app for couples and venue owners; pnpm monorepo on PM2. Private.
- **Elio** (elio.care): marketplace for contractors, homeowners and vendors: Flutter mobile + React web. Private.
- **HRIA-DMS**: donation management system for an Islamic humanitarian academy: Electron desktop + Express/Mongo API, Zod-typed SDK, English/Urdu i18n. Private.
- **SocialSync**: self-hosted, queue-based social media manager for teams: Instagram, Facebook, LinkedIn, X, YouTube; tokens encrypted at rest. Private.
- **Reveal Your Intentions**: AI social-intelligence mobile app: Expo + Express AI orchestration API. Private.
- **madaddGar**: on-demand home-services marketplace (providers bid, OTP-verified completion). Node, MongoDB, Socket.io. Private.
- **Qalb-e-Saleem**: Flutter app for the majalis, writings and shajra of Hazrat Pir Syed Muhammad Abdullah Shah Mashhadi Qadri: audio player, reader. Private.
- **RestaurantOS**: multi-tenant restaurant OS: POS, inventory, finance, HR, reporting. Public (repo name `ResturantOS`).
- **cursor-powered-up**: one-clone installer that powers up Cursor / VS Code / Antigravity with GSD workflows, agent memory, CodeGraph, MCP wiring. Public.
- **domain-manager**: read-only Kubernetes hostname/DNS/certificate page, stdlib-only Python, multi-arch image on GHCR, Terra plugin. Public.
- **Face-Recognition-Project**: CNN attendance system (TensorFlow, OpenCV). Public.

Absent, and not to be fabricated: testimonials, client logos, revenue or user counts, employer names.

## Product Principles

1. Prove, don't claim: real numbers from the API and real named projects outrank adjectives and badges.
2. Private work counts: show its weight honestly (counts and languages), never its contents.
3. One way in: every audience finds contact within one screen.
4. Nothing breaks: no third-party image services that rate-limit or go down; everything renders from this repo.
5. Scannable in ten seconds, rewarding in sixty.

## Accessibility & Inclusion

Every image carries meaningful `alt` text. Both light and dark GitHub themes must hold contrast ≥4.5:1 for body text in every card.
