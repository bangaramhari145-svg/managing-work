Angel One trading-bot (web/GitHub Actions)

Quick start

1) Add GitHub Secrets (Repository settings → Secrets):
   - ANGEL_BASE_URL (e.g. https://apiconnect.example)
   - ANGEL_CLIENT_ID
   - ANGEL_CLIENT_SECRET
   - ANGEL_ACCESS_TOKEN
   - ANGEL_REFRESH_TOKEN
   - ANGEL_ACCOUNT_ID
   - PAPER_MODE (true/false) — use true to avoid live orders (recommended for first runs)

2) Run locally
   - Create a .env with the same keys or export envvars
   - python -m venv .venv && .\.venv\Scripts\activate
   - pip install -r trading-bot\requirements.txt
   - python -m trading_bot.main --once

3) GitHub Actions
   - The workflow .github/workflows/trading-bot.yml runs on manual dispatch and schedule
   - Keep PAPER_MODE=true in Secrets for testing, set to false only when ready to go live

Safety
 - Always start with PAPER_MODE=true.
 - Limit capital in config and use MAX_DAILY_LOSS.
 - Review logs and small-size trades before scaling.

Files
 - trading-bot/trading_bot: code
 - .github/workflows/trading-bot.yml: CI/runner

