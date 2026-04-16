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
- The internal ETL code may use environment variables for credentials.

### Supabase credentials

- `SUPABASE_URL` — optional override for the Supabase endpoint.
- `SUPABASE_KEY` — anonymous/limited key used by `src/inventory/input_inventory.py`.
- `SUPABASE_SERVICE_KEY` — admin/service role key used by `private/etl/load_cards.py`.

Create a local `.env` file for these values, but do not commit it.

## GitHub policy

- Keep `private/` out of the public repository.
- Push only the public files needed for distribution: `dist/`, `src/inventory/`, and the root `README.md`.
- Use this file for local reference only.
