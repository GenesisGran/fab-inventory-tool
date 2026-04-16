# FAB Inventory Tool — Portfolio Project

## Project summary

A data-focused inventory manager for Flesh and Blood card collections with a shared Supabase backend.
This project combines metadata ETL, inventory tracking, and a packaged desktop experience for non-technical users.

## Project highlights

- Centralized Supabase inventory backend for collaborative updates
- Additive `qty_change` model for inventory adjustments
- Monthly metadata refresh pipeline from GitHub card data
- Packaged Windows executable for easy distribution
- Clear separation of public deliverable and private maintenance

## Problem solved

- Track cards by set, foil, class, and quantity
- Record ownership changes as increments rather than overwrites
- Let friends upsert inventory without learning Python
- Maintain a clean, centralized card database
- Keep the deliverable simple with an `.exe`

## What I built

- `src/inventory/input_inventory.py`
  - user-facing CLI for inventory entry and search
  - batch-safe additive inventory updates
- `private/etl/load_cards.py`
  - internal loader that syncs card metadata into Supabase
- `private/js/export.mjs`
  - metadata export step for local JSON generation
- `private/data/`
  - local metadata files for cards, sets, rarities, and printings
- `dist/`
  - packaged executable builds for end users

## Data workflow

1. Export card metadata from the external card dataset
2. Load local JSON files and normalize metadata
3. Sync sets, rarities, cards, and printings to Supabase
4. Use the inventory tool to submit `qty_change` records
5. Aggregate inventory totals by print and user

## Tools and technologies

- Python
- HTTPX for REST API access
- Supabase for the backend database
- PyInstaller for Windows packaging
- GitHub for project versioning

## How to run the flows

### Monthly metadata refresh

```powershell
node private/js/export.mjs
python private/etl/load_cards.py
```

### Weekly inventory updates

```powershell
python src/inventory/input_inventory.py
```

or run the packaged executable from `dist/`.

## Why this is a strong portfolio project

- demonstrates ETL and data pipeline design
- shows practical backend integration with Supabase
- highlights productization with a user-friendly executable
- models inventory as additive event data, not destructive state
- documents both public delivery and private maintenance

## Notes for presentation

- Use `README.md` as the main recruiter-facing summary.
- Link to `PORTFOLIO.md` for deeper architecture and workflow details.
- Emphasize the data engineering value: ETL, data sync, schema design, and delivery.
