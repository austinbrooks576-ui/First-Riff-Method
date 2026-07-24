# ai-creator-ops

Operations scaffolding for a **disclosed, AI-generated** adult-creator brand.

This project handles the **non-explicit** business layer: compliance, subscriber
CRM, tier logic, reinvestment budgeting, and posting/DM ops planning. It does
**not** generate, host, or send explicit content — that stays with the operator
and their chosen tools.

## Hard boundaries baked into this project

1. **Open disclosure, always.** Every account states plainly that the character
   is AI-generated fiction. No buried or ambiguous labeling. See
   `disclosure.md`. This is both a compliance requirement and, in the AI-creator
   niche, a selling point.
2. **No real human is impersonated.** The character is fiction. Payments,
   verification, and payouts are tied to the real operator's KYC identity.
3. **Explicit content is out of scope for this codebase.** The DM helper drafts
   non-sexual messages only (greetings, tier info, upsell, retention). A human
   handles anything sexual.

## Platform posture

| Platform      | Use                          | Note                                                        |
|---------------|------------------------------|-------------------------------------------------------------|
| Fansly        | Primary monetization         | Tag content as AI. Adult OK.                                |
| OnlyFans      | **Do not use**               | Requires a real, verified human in content. Ban/hold risk. |
| Reddit        | Funnel (AI-permitting NSFW subs only) | Read each sub's rules; disclose in title/flair.    |
| Instagram     | SFW top-of-funnel            | No nudity. `AI model` in bio.                               |
| X / Twitter   | Funnel + adult (sensitive)   | Mark account sensitive; AI label in bio.                    |
| Telegram      | Free channel → paid funnel   | Most permissive.                                            |

## Payouts

Payouts are configured by the operator **inside each platform's dashboard**
against their own verified identity. This repo intentionally stores **no** bank
details. See `payout_config.example.json` for the placeholder shape — fill it in
your own private, untracked copy if you want local bookkeeping, and keep it out
of git.

## Contents

- `disclosure.md`   — approved disclosure copy for bios and pinned posts.
- `budget.py`       — net-revenue split incl. the 30% production reinvest.
- `crm.py`          — subscriber records, tiering, VIP prioritization.
- `payout_config.example.json` — placeholder config (no real data).

## Quick start

```bash
python3 budget.py --gross 5000 --platform-fee-pct 20
python3 crm.py demo
```
