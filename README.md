# FAB Inventory Tool

A polished distribution for a Flesh and Blood inventory manager built for data workflows.

## What is included here

This public repo includes the user-facing deliverable and a portfolio-ready project summary.

- `dist/` — user-accessible Windows executable builds
- `README.md` — public-facing project overview
- `PORTFOLIO.md` — portfolio project summary and architecture

## What is not public

- `private/` contains internal ETL, packaging, metadata, and maintenance files
- `private/` is not needed by end users and should remain local

## Run the tool

Open `dist/` and run the latest executable, for example:

```powershell
./dist/FAB_Inventory_Tool_0.0.04.exe
```

## User notes

- The `.exe` is packaged to run standalone on Windows.
- Internet access is required if it connects to the Supabase backend.
- The user-facing tool is designed for batch inventory entry and search, without requiring Python.

## Portfolio value

This repo demonstrates a data-focused project with:

- ETL workflow for card metadata and pricing data
- data modeling for inventory and prints
- API integration with Supabase
- user-friendly executable distribution
- documentation for both public and private maintenance
