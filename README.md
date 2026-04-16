# FAB Inventory Tool

Standalone Windows inventory manager for Flesh and Blood cards with a Supabase-backed data workflow.

## What this repo is for

This repository is a portfolio-ready project that demonstrates a complete data workflow:

- a user-facing `.exe` for non-technical inventory entry
- an internal ETL pipeline for card metadata syncing
- a Supabase database backend for collaborative inventory tracking
- clear public/private separation for production and maintenance

## Project highlights

- Shared inventory system with Supabase backend
- Additive inventory changes (`qty_change`) instead of destructive updates
- Monthly metadata refresh from GitHub card data
- Packaged Windows executable so friends can use the tool without installing Python
- Documentation and portfolio case study for data roles

## What is included here

- `dist/` — packaged Windows executable builds
- `README.md` — public-facing project overview
- `PORTFOLIO.md` — deeper case study and architecture
- `private/` — internal maintenance files and ETL workflows (kept local)

## Quick start

Open `dist/` and run the latest executable:

```powershell
./dist/FAB_Inventory_Tool_0.0.04.exe
```

If you want to run the source tool instead:

```powershell
python src/inventory/input_inventory.py
```

## Notes for reviewers

- The `.exe` is designed to work standalone on Windows.
- `private/.env` is local and not included in the repo.
- `private/` contains internal ETL and maintenance scripts, not the user deliverable.
- See `PORTFOLIO.md` for the full data architecture and workflow.
