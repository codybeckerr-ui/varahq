# VaraHQ Streamlit Pilot

VaraHQ is the platform that governs white-labeled asset portals for real estate brokerages. The base product is intentionally tenant-neutral; Excelsior Realty exists only as pilot data until the core platform is complete.

## Included

- Public Vara product homepage
- Neutral Vara platform-administration shell
- Organization, user, template, render, and system views
- Reusable personalized rendering engine with PNG and PDF output
- Notion repository adapter with safe local demo fallback

Notion is used for operational configuration. It must not store passwords, session tokens, API keys, or serve as the application's authorization boundary.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Without `NOTION_TOKEN`, the app starts in demo mode using the seeded Excelsior Realty organization and Cody Becker profile as platform records—not as the Vara interface brand.

## Enable live Notion data

1. Create a Notion internal integration with read-content access and update-content access for user-profile editing.
2. Share the six VaraHQ source databases with that integration.
3. Copy `.env.example` values into Streamlit secrets or environment variables.
4. Set `NOTION_TOKEN` without committing it to source control.

The adapter uses Notion API version `2026-03-11` and the `/v1/data_sources/{id}/query` endpoint.

## Current MVP boundary

- No production authentication yet
- No physical print ordering
- Demo renderer uses code-generated layouts until approved Excelsior source artwork and fonts are provided
- Generated-asset audit writes and R2 upload are the next backend increment
