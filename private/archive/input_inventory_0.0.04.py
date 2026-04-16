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

# Foiling and Pitch Mapping
FOIL_MAP = {"r": "Rainbow Foil", "c": "Cold Foil", "reg": "Regular", "f": "Full Art", "g": "Gold Cold Foil"}
PITCH_MAP = {1: "Red", 2: "Yellow", 3: "Blue"}

def is_connected():
    """Checks if Supabase is reachable before starting."""
    print("📡 Testing connection to vault...", end="\r")
    try:
        httpx.head(SUPABASE_URL, timeout=3.0)
        print("📡 Connection: ONLINE          ")
        return True
    except:
        print("\n❌ Connection Error: Ensure you have internet access.")
        return False

def print_menu(username):
    """The persistent command guide, printed only when actions occur."""
    print(f"\n{'─'*70}")
    print(f" 👤 USER: {username}")
    print(f" 🕹️  COMMANDS: [inv] View All | [search <text>] Search | [logout] | [q] Exit")
    print(f" ➕ ADD CARDS: Type '<ID> <FOIL> <QTY>' (e.g. PEN001 reg 5)")
    print(f"{'─'*70}")

def check_user_exists(username):
    """Verifies if the user exists in the Supabase 'users' table."""
    try:
        url = f"{SUPABASE_URL}/rest/v1/users?username=eq.{username}"
        resp = httpx.get(url, headers=headers)
        return len(resp.json()) > 0
    except: return False

def get_inventory(username, filter_code=None):
    """Fetches card data and maps Pitch -> Color."""
    print(f"🔍 Fetching vault for {username}...")
    # Relationship: Inventories -> Card Prints -> Cards (to get Name and Pitch)
    query = "qty_change,print_id,card_prints(cards(name,pitch))"
    url = f"{SUPABASE_URL}/rest/v1/inventories?username=eq.{username}&select={query}"
    
    try:
        resp = httpx.get(url, headers=headers)
        data = resp.json()
        
        if not data or isinstance(data, dict):
            print("🤷 Your vault is currently empty.")
            return

        vault = {}
        for entry in data:
            pid = entry.get('print_id') or ""
            qty = entry.get('qty_change', 0)
            
            p_data = entry.get('card_prints') or {}
            c_data = p_data.get('cards') or {}
            
            name = c_data.get('name', 'Unknown')
            pitch_val = c_data.get('pitch')
            color = PITCH_MAP.get(pitch_val, "N/A")

            # Parse Print ID (e.g., PEN001-Cold Foil) into Set and Foil
            parts = pid.split('-', 1)
            set_id = parts[0] if len(parts) > 0 else "???"
            foil = parts[1] if len(parts) > 1 else "Regular"

            # Filter logic for Search command
            if filter_code:
                fc = filter_code.upper()
                if fc not in name.upper() and fc not in set_id.upper():
                    continue

            if pid not in vault:
                vault[pid] = {"name": name, "set": set_id, "foil": foil, "color": color, "total": 0}
            vault[pid]["total"] += qty

        # Output Table
        title = "ALL ITEMS" if not filter_code else f"SEARCH: {filter_code.upper()}"
        print(f"\n📋 {title}")
        print("═"*105)
        print(f"{'NAME':<25} | {'SET ID':<12} | {'FOILING':<18} | {'COLOR':<10} | {'OWNED'}")
        print("─"*105)
        
        found = False
        for pid in sorted(vault.keys()):
            item = vault[pid]
            if item['total'] <= 0: continue
            found = True
            print(f"{item['name'][:24]:<25} | {item['set']:<12} | {item['foil']:<18} | {item['color']:<10} | {item['total']}")
        
        if not found: print(" (No matches found)")
        print("═"*105)
    except Exception as e:
        print(f"❌ Error fetching inventory: {e}")

def process_line(line, username):
    """Logs a single card entry to the database."""
    parts = line.split()
    if len(parts) < 3: return f" ⚠️  Format Error: '{line}'"
    
    try:
        card_code, f_key, qty = parts[0].upper(), parts[1].lower(), int(parts[2])
        foil = FOIL_MAP.get(f_key, "Regular")
        print_id = f"{card_code}-{foil}"
        
        payload = {
            "print_id": print_id, 
            "qty_change": qty, 
            "username": username, 
            "updated_at": datetime.now().isoformat()
        }
        
        resp = httpx.post(
            f"{SUPABASE_URL}/rest/v1/inventories", 
            headers={**headers, "Prefer": "resolution=merge-duplicates"}, 
            json=payload
        )
        
        if resp.status_code in [200, 201]:
            return f" ✅  {print_id} x{qty} saved."
        else:
            return f" ❌  Sync Error ({resp.status_code})"
    except Exception as e:
        return f" ❌  Failed on '{line}': {e}"

def run_app():
    # RESTORED CLASSIC HEADER
    print("╔" + "═"*41 + "╗")
    print("║        FAB INVENTORY INPUT v0.0.04      ║")
    print("╚" + "═"*41 + "╝")
    
    if not is_connected(): return

    while True:
        name_in = input("\n👤 Username (or 'q' to quit): ").strip().upper()
        if name_in == 'Q': break
        if not name_in: continue

        # Identity Verification
        if not check_user_exists(name_in):
            print(f"❓ User '{name_in}' not found.               ")
            if input("📝 Register new user? (y/n): ").lower() == 'y':
                httpx.post(f"{SUPABASE_URL}/rest/v1/users", headers=headers, json={"username": name_in})
                print(f"✅ Registered {name_in}")
            else: continue

        print_menu(name_in)

        while True:
            line = input(f"{name_in} > ").strip()
            
            # PREVENT MENU SPAM: If empty, just give a new line
            if not line:
                continue 
            
            cmd_parts = line.split()
            cmd_lower = cmd_parts[0].lower()
            
            if cmd_lower == 'q': sys.exit()
            if cmd_lower == 'logout': break
            
            if cmd_lower == 'inv':
                get_inventory(name_in)
                print_menu(name_in)
                continue
                
            if cmd_lower == 'search':
                term = " ".join(cmd_parts[1:]) if len(cmd_parts) > 1 else ""
                get_inventory(name_in, filter_code=term)
                print_menu(name_in)
                continue
            
            # Batch Mode for multi-line pasting
            input_lines = [line]
            print("\n📥 BATCH ENTRY: Hit [ENTER] on an empty line to save.")
            while True:
                next_l = input("   + ").strip()
                if not next_l: break
                input_lines.append(next_l)
            
            print(f"\n⏳ Syncing to cloud...")
            for entry in input_lines:
                print(process_line(entry, name_in))
            
            # Show menu again after finishing batch
            print_menu(name_in)

if __name__ == "__main__":
    try:
        run_app()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(f"\n🛑 Fatal Crash: {e}")
        input("Press Enter to close...")