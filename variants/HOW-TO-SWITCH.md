# Profile variants

| File | What it shows |
| :-- | :-- |
| `README.personal.md` | Personal profile, no Praivox. Contact: umer.jahangier@gmail.com |
| `README.praivox.md` | Founder of Praivox framing. Contact: hello@praivox.com, praivox.com |

`ACTIVE` holds the name of the variant that is live. The `Profile` workflow copies that variant to the root `README.md`, so never edit the root `README.md` directly: your change would be overwritten on the next run.

## One-time setup: private stats

The contribution totals already include private work. Private repo **languages** and the private repo count also need a token that acts as you:

1. Create a classic token at <https://github.com/settings/tokens/new> with the scopes `repo` and `read:user`. Name it `profile-stats` and pick an expiry (a year is sensible).
2. In this repo: Settings → Secrets and variables → Actions → New repository secret. Name `PROFILE_TOKEN`, paste the token, save.
3. Actions → Profile → Run workflow.

Without the secret the workflow still runs; languages then cover public repos only, and the run shows a warning.

## Switch variant

Pick whichever is easiest:

1. **From the Actions tab:** Actions → Profile → Run workflow → choose `personal` or `praivox` → Run. Live in about a minute.
2. **From the GitHub website:** open `variants/ACTIVE`, click the pencil, replace the word with `personal` or `praivox`, commit. The push starts the workflow.
3. **From a terminal:**

   ```bash
   echo praivox > variants/ACTIVE && git commit -am "Use Praivox profile" && git push
   ```

## Edit content

Edit the variant file itself (for example `README.personal.md`) and push. Content shared by both variants (selected work, toolbox) lives in both files, so change it in both.

The cards in `dist/` are rebuilt every day by `scripts/profile.py`; the role line and location on the cover come from `VARIANTS` in that script.
