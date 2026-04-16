# FAB Inventory Tool — Portfolio Project

## Project summary

This project is a data-driven inventory manager for Flesh and Blood card collections.
It combines a user-friendly inventory input tool with an ETL workflow that syncs card metadata and inventory data to Supabase.

## Problem solved

- Track owned cards, set codes, classes, and foiling
- Record card quantities as incremental changes (`+` and `-`)
- Allow friends to upsert inventory without learning code
- Maintain a centralized Supabase database for all users
- Keep the public distribution simple with a standalone Windows `.exe`

## Key components

- `dist/`
  - user-facing packaged executables for Windows
- `src/inventory/input_inventory.py`
  - inventory input tool that appends quantity changes and supports batch entry
- `private/etl/load_cards.py`
  - internal ETL script to pull card metadata from GitHub and sync it to Supabase
- `private/data/`
  - local card metadata files used by internal workflows
- `private/README_INTERNAL.md`
  - maintenance notes, credential guidance, and run commands

## Data workflow

1. Fetch card metadata from GitHub
2. Normalize sets, rares, cards, and printings
3. Load metadata into Supabase with the service role key
4. Allow users to submit inventory changes via the `.exe` or CLI
5. Store inventory `qty_change` records instead of overwriting totals
6. View inventory totals by aggregating per card print

## Tools and technologies

- Python
- HTTPX for REST API calls
- Supabase as the backend database
- PyInstaller for building Windows executables
- GitHub for project versioning

## What this demonstrates

- data ingestion from external APIs
- ETL design and metadata normalization
- database-backed inventory tracking
- user-friendly deployment with a packaged executable
- secure handling of credentials via environment variables
- documentation for both public and private use

## How to run the main flows

### Monthly metadata update

```powershell
python private/etl/load_cards.py
```

### Weekly inventory updates

```powershell
python src/inventory/input_inventory.py
```

or run the packaged executable found in `dist/`.

## Portfolio story

This project is a good showcase for data roles because it combines:

- real-world data modeling
- API-driven ETL
- backend database management
- packaging and distribution for non-technical users
- collaborative data input via Supabase

## Notes for portfolio presentation

- Emphasize that the inventory input tool is additive (`qty_change`) and not destructive.
- Highlight the separation of public distribution and private maintenance.
- Note that the `.exe` is designed for friends to run without setup.
