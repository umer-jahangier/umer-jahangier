# Profile variants

| File | What it shows |
| :-- | :-- |
| `README.personal.md` | Personal profile. Contact: umer.jahangier@gmail.com |

`ACTIVE` holds the name of the variant that is live. The `Profile` workflow copies that variant to the root `README.md`, so never edit the root `README.md` directly: your change would be overwritten on the next run.

## One-time setup: private stats

The contribution totals already include private work. Private repo **languages** and the private repo count also need a token that acts as you:

1. Create a classic token at <https://github.com/settings/tokens/new> with the scopes `repo` and `read:user`. Name it `profile-stats` and pick an expiry (a year is sensible).
2. In this repo: Settings → Secrets and variables → Actions → New repository secret. Name `PROFILE_TOKEN`, paste the token, save.
3. Actions → Profile → Run workflow.

Without the secret the workflow still runs; languages then cover public repos only, and the run shows a warning.

## Edit content

Edit the variant file itself (for example `README.personal.md`) and push.

The images in `dist/` are rebuilt every day by `scripts/profile.py`. The role line and location on the cover come from `VARIANTS`, and the Selected work cards from `SHOWCASE`, both in `scripts/stage/scenes.py`. Project names are matched to repositories by keyword in `PROJECTS` in `scripts/stage/data.py`.
