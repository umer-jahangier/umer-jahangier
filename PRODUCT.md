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

Source of truth: the Europass CVs (Industry and Academic, 2026-09-28). Every public claim must match them.

- **AlphaVenue.ai** (Kindwell Solutions): sole engineer. Multi-tenant venue SaaS with 132 data models and 179 pages; ELLA LLM assistant with 104 tools, RAG (Qdrant) and an MCP server; Pipecat voice agent; native CRM.
- **LogicOne Dialer**, logicone.ai (Logicbuilder.ai): primary engineer. Predictive dialling, live call coaching, voice agents, Stripe Connect. Next.js, Prisma, Twilio.
- **Elio**, elio.care (ArchiPartnerDesign, 03/2024–12/2025): construction marketplace. Express, React + Vite, MongoDB, Socket.io, Flutter app.
- **RestaurantOS**: technical lead of four. 15 Spring Boot domain microservices, PostgreSQL RLS, OPA. Private repo; never link it.
- **HRIA-DMS**: Electron app with a 169-endpoint API. **SocialSync**: co-developer. **AI take-off pipeline**: freelance.
- **Terra plugins**: 9 merged PRs to juno-fx/Terra-Official-Plugins (public).
- **cursor-powered-up** and **domain-manager**: public.

Never claim: over two years' experience stated as more; Next.js or React Native for Elio; SocialSync lead; take-off accuracy; commit counts on CVs. Praivox is deliberately absent from the CV and LinkedIn; it appears only in the optional `praivox` variant. Absent, and not to be fabricated: testimonials, client logos, revenue or user counts.

## Product Principles

1. Prove, don't claim: real numbers from the API and real named projects outrank adjectives and badges.
2. Private work counts: show its weight honestly (counts and languages), never its contents.
3. One way in: every audience finds contact within one screen.
4. Nothing breaks: no third-party image services that rate-limit or go down; everything renders from this repo.
5. Scannable in ten seconds, rewarding in sixty.

## Accessibility & Inclusion

Every image carries meaningful `alt` text. Both light and dark GitHub themes must hold contrast ≥4.5:1 for body text in every card.
