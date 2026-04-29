# FAB Inventory Tool: Backend & ETL Pipeline

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Supabase](https://img.shields.io/badge/Database-Supabase-green.svg)](https://supabase.com/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://github.com/GenesisGran/fab-inventory-tool/releases)

A standalone Windows administrative suite designed to manage a high-fidelity inventory for Flesh and Blood TCG. This repository houses the **Admin/Write** side of the FAB Vault ecosystem, focusing on data integrity, automated master data synchronization, and ETL workflows.

## 🏗️ Architecture & Data Workflow
This project acts as the **ETL (Extract, Transform, Load)** engine for the inventory system:
* **Extraction:** Pulls the latest card metadata (JSON/CSV) from community-maintained data sources.
* **Transformation:** Normalizes card identifiers, handles specific print variants (e.g., Cold Foil vs. Rainbow Foil), and prepares records for Upserting.
* **Loading:** Syncs local changes to a remote **Supabase (PostgreSQL)** instance via a secure Python-based pipeline.

## 🚀 Key Features
* **Safe-Write Logic:** Implements additive inventory changes (`qty_change`) instead of destructive updates to prevent accidental data loss.
* **Automated Master Data Sync:** The `load_cards.py` script serves as a maintenance pipeline to refresh card metadata without downtime.
* **Windows Distribution:** Packaged using **PyInstaller**, allowing for a portable `.exe` that friends or collaborators can use without needing a Python environment.
* **Security by Design:** Separates administrative write-access scripts from the public-facing web repository.

## 📂 Project Structure
* `/src`: Core Python logic for inventory input and data validation.
* `/dist`: Production-ready Windows executable builds.
* `load_cards.py`: The ETL script responsible for updating Supabase master tables.
* `PORTFOLIO.md`: A deep-dive case study on the data architecture and schema design.

## 🛠️ Quick Start

**To run the latest stable tool on Windows:**
1. Navigate to `/dist/`.
2. Launch the latest `.exe` file.

**To run from source:**
```powershell
pip install -r requirements.txt
python src/inventory/input_inventory.py
