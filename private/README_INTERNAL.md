# FAB Inventory Tool — Internal Documentation

This folder contains the private internal workspace used to maintain, build, and package the FAB Inventory Tool.

## Purpose

- `dist/` contains the user-facing `.exe` builds.
- `private/` contains ETL scripts, metadata, packaging specs, and internal build artifacts.
- Only the public `dist/` and the user-facing source should be shared on GitHub.

## Folder layout

- `src/inventory/`
  - public inventory CLI source code
- `private/etl/`
  - internal loader scripts for syncing card metadata and rarities
- `private/data/`
  - local metadata JSON files used by ETL
- `private/js/`
  - private Node tooling and helper scripts
- `private/packaging/`
  - PyInstaller spec files and packaging assets
- `private/build/`
  - internal build outputs, not for public distribution
- `dist/`
  - user-facing Windows executable builds
- `private/archive/`
  - legacy and backup files

## Running and maintenance notes

- The public `.exe` builds in `dist/` are intended to run standalone.
- Internal scripts in `private/etl/` should only be run locally by the maintainer.
- The internal ETL code uses environment variables for credentials.

### Supabase credentials

- `SUPABASE_URL` — optional override for the Supabase endpoint.
- `SUPABASE_KEY` — anonymous/limited key for `src/inventory/input_inventory.py`.
- `SUPABASE_SERVICE_KEY` — service/admin key for `private/etl/load_cards.py`.

Create a local `.env` file from `private/.env.example` and do not commit it.

### Monthly card metadata update

Run the export script first, then run the ETL loader to sync card metadata into Supabase:

```powershell
node private/js/export.mjs
python private/etl/load_cards.py
```

This workflow:

- exports card metadata from the external package to local JSON files
- downloads GitHub release dates and merges them with local set data
- builds and uploads `cards.json`, `sets.json`, `rarities.json`, and `prints.json`
- uploads sets, rarities, cards, and printings to Supabase

### Weekly inventory input

Use the user-facing inventory tool to append quantity changes:

```powershell
python src/inventory/input_inventory.py
```

or run the packaged executable from `dist/`.

This tool is designed to:

- add inventory changes via `qty_change`
- preserve existing records instead of overwriting
- support batch entry for multiple lines
- allow friends to upsert inventory without learning Python

## GitHub policy

- Keep `private/` out of the public repository when sharing the distributable.
- Public files should include `dist/`, `README.md`, and `PORTFOLIO.md`.
- Use this file for local reference and maintenance only.
