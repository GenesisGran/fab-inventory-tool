# FAB Inventory Tool

This repository contains the public distribution for the FAB Inventory Tool.

## Public distribution

- `dist/` contains the user-facing `.exe` files.
- Users should run the `.exe` directly.
- No Python environment or dependencies should be required for the packaged build.

## Run the tool

Open `dist/` and run the latest executable, for example:

```powershell
./dist/FAB_Inventory_Tool_0.0.04.exe
```

## Notes for users

- The `.exe` is built to run standalone on Windows.
- It may require internet access if it connects to Supabase.
- The app does not expose the internal ETL workflows or private maintenance files.
