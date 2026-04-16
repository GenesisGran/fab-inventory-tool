import httpx
import os
from datetime import datetime
import sys

# --- CONFIGURATION ---
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://eycwwbgymeuggayeifce.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_KEY environment variable must be set before running this script.")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

FOIL_MAP = {
    "r": "Rainbow Foil", "c": "Cold Foil", "reg": "Regular", 
    "f": "Full Art", "g": "Gold Cold Foil"
}

def get_card_info(print_id):
    params = {"select": "cards(name)", "id": f"eq.{print_id}"}
    try:
        resp = httpx.get(f"{SUPABASE_URL}/rest/v1/card_prints", headers=headers, params=params)
        data = resp.json()
        if data: return data[0]['cards']['name']
    except: pass
    return "Unknown Card"

def is_connected():
    """Quick silent check to see if the database is reachable."""
    try:
        httpx.head(SUPABASE_URL, timeout=3.0)
        return True
    except:
        return False

def check_user_exists(username):
    try:
        resp = httpx.get(f"{SUPABASE_URL}/rest/v1/users", headers=headers, params={"username": f"eq.{username}"})
        return len(resp.json()) > 0
    except: return False

def process_line(line, username):
    """Processes entry ONLY if internet is alive."""
    if not is_connected():
        return "📡 ERROR: Connection lost. Reconnect and try again."

    parts = line.split()
    if len(parts) < 3:
        return f" ⚠️  Format Error: {line}"
        
    card_code = parts[0].upper()
    foil_code = parts[1].lower()
    
    if foil_code not in FOIL_MAP:
        return f" ❌  Foil '{foil_code}' invalid in: {line}"
    
    try:
        qty = int(parts[2])
        full_print_id = f"{card_code}-{FOIL_MAP[foil_code]}"
        card_name = get_card_info(full_print_id)
        
        payload = {
            "print_id": full_print_id, 
            "qty_change": qty, 
            "username": username,
            "updated_at": datetime.now().isoformat()
        }
        
        upsert_headers = {**headers, "Prefer": "resolution=merge-duplicates"}
        resp = httpx.post(f"{SUPABASE_URL}/rest/v1/inventories", headers=upsert_headers, json=payload)
        
        if resp.status_code in [200, 201]:
            return f" ✅  {card_name} ({card_code}) x{qty}"
        return f" ❌  Server Error: {resp.status_code}"
    except Exception as e:
        return f" ⚠️  Error processing line: {e}"

def run_app():
    # Initial startup check
    print("🌐 Connecting to Database...")
    if not is_connected():
        print("\n❌ Startup Failed: No Internet Connection.")
        input("Press Enter to exit...")
        sys.exit()

    print("╔" + "═"*41 + "╗")
    print("║        FAB INVENTORY INPUT v0.0.03      ║")
    print("╚" + "═"*41 + "╝")

    while True:
        # Username handling with internet check
        name_in = input("\n👤 Username (or 'q' to quit): ").strip().upper()
        if name_in == 'Q': break
        if not name_in: continue
        
        if not is_connected():
            print("📡 Connection lost. Check internet.")
            continue

        # Check/Register User
        if not check_user_exists(name_in):
            print(f"❓ User '{name_in}' not found.")
            reg = input("📝 Register this name? (y/n): ").lower()
            if reg == 'y':
                httpx.post(f"{SUPABASE_URL}/rest/v1/users", headers=headers, json={"username": name_in})
                print(f"✅ Registered {name_in}")
            else: continue
        
        print("\n" + "─"*50)
        print(f" 👉 ACTIVE USER: {name_in}")
        print(f" 👉 Paste list or type, then press ENTER twice to submit")
        print(f" 👉 COMMANDS: 'logout' to switch user | 'q' to quit")
        print("─"*50)

        while True:
            # 1. Wait for the very first line of input
            line = input(f"\n{name_in} (Input Card or 'q' to quit) > ").strip()
            
            # If empty, just loop back without re-printing everything
            if not line:
                continue 

            # 2. Check for logout/quit before starting batch collection
            if line.lower() == 'q': sys.exit()
            if line.lower() == 'logout': break
            
            # 3. If it's a card entry, collect additional lines (Batch mode)
            input_lines = [line]
            print("   (Enter more lines or hit Enter to submit)")
            
            while True:
                next_line = input("   > ").strip()
                if not next_line: 
                    break
                input_lines.append(next_line)
            
            # 4. Sync the collected batch
            print(f" ⏳ Syncing {len(input_lines)} item(s)...")
            for entry in input_lines:
                result = process_line(entry, name_in)
                print(result)
                if "📡" in result:
                    print("\n🛑 BATCH HALTED: Check your connection.")
                    break
            print("Done.")

if __name__ == "__main__":
    try:
        run_app()
    except KeyboardInterrupt:
        sys.exit()