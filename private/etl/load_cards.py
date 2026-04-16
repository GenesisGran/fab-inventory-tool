import json
import httpx
import os
from pathlib import Path
from tqdm import tqdm

# --- CONFIGURATION ---
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://eycwwbgymeuggayeifce.supabase.co")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_SERVICE_KEY:
    raise RuntimeError("SUPABASE_SERVICE_KEY environment variable must be set before running this script.")

# The specific GitHub URL you provided
EXTERNAL_SETS_URL = "https://raw.githubusercontent.com/the-fab-cube/flesh-and-blood-cards/refs/heads/develop/json/english/set.json"

# Local file paths
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CARDS_JSON = DATA_DIR / "cards.json"
SETS_JSON = DATA_DIR / "sets.json"
RARITIES_JSON = DATA_DIR / "rarities.json"

BATCH_SIZE = 50
client = httpx.Client(timeout=30.0)

headers = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates" # This handles the 'Upsert'
}

def load_local_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def sync_everything():
    # 1. Fetch External Sets Data (GitHub)
    print("🌐 Fetching latest set release dates from GitHub...")
    external_set_map = {}
    try:
        sets_resp = client.get(EXTERNAL_SETS_URL)
        sets_resp.raise_for_status()
        external_data = sets_resp.json()
        
        # Build a temporary map: { "SET_CODE": "RELEASE_DATE" }
        for s in external_data:
            set_id = s.get("id")
            if set_id and s.get("printings"):
                raw_date = s["printings"][0].get("initial_release_date")
                if raw_date:
                    external_set_map[set_id] = raw_date.split('T')[0]
    except Exception as e:
        print(f"⚠️ Warning: Could not fetch external dates. Proceeding with local data only. ({e})")

    # 2. Load Local Data
    print("📖 Loading local files...")
    try:
        cards_data = load_local_json(CARDS_JSON)
        local_sets_data = load_local_json(SETS_JSON) # This is your local dict/list
        rarities_data = load_local_json(RARITIES_JSON)
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find local file {e.filename}.")
        return

    # 3. Sync Sets (Merge GitHub Dates with Local Names)
    print("📦 Syncing Sets (Merging External + Local)...")
    set_payload = []
    
    # Assuming your local sets.json is a Dictionary { "CODE": "NAME" }
    for code, name in local_sets_data.items():
        set_payload.append({
            "id": code,
            "name": name,
            "release_date": external_set_map.get(code) # Get date from GitHub map if it exists
        })
    
    # Bulk upload the sets (Upsert will update names/dates if code exists)
    client.post(f"{SUPABASE_URL}/rest/v1/sets", headers=headers, json=set_payload)

    # 4. Sync Rarities
    print("✨ Syncing Rarities...")
    rarity_payload = [{"id": r['code'], "name": r['name']} for r in rarities_data]
    client.post(f"{SUPABASE_URL}/rest/v1/rarities", headers=headers, json=rarity_payload)

    # 5. Process Cards and Prints
    print(f"🃏 Preparing {len(cards_data)} cards for upload...")
    master_cards = []
    all_printings = []
    seen_print_ids = set() 
    
    for card in cards_data:
        r_name = card.get("rarities", [None])[0]
        r_code = next((item['code'] for item in rarities_data if item['name'] == r_name), "U")
        
        master_cards.append({
            "id": card["cardIdentifier"],
            "name": card["name"],
            "pitch": card.get("pitch"),
            "classes": card.get("classes", []),
            "type_text": card.get("typeText"),
            "rarity_id": r_code
        })

        for p in card.get("printings", []):
            foiling_val = p.get("foiling", "Regular")
            set_code = "".join(filter(str.isalpha, p["identifier"]))
            print_id = f"{p['identifier']}-{foiling_val}"
            
            if print_id not in seen_print_ids:
                all_printings.append({
                    "id": print_id,
                    "card_id": card["cardIdentifier"],
                    "set_id": set_code,
                    "foiling": foiling_val,
                    "rarity": p.get("rarity"),
                    "image_url": p.get("image")
                })
                seen_print_ids.add(print_id)

    # --- EXECUTE BULK UPLOADS ---
    for i in tqdm(range(0, len(master_cards), BATCH_SIZE), desc="🃏 Uploading Master Cards"):
        batch = master_cards[i:i + BATCH_SIZE]
        resp = client.post(f"{SUPABASE_URL}/rest/v1/cards", headers=headers, json=batch)
        if resp.status_code >= 400: print(f"\n⚠️ Card Error: {resp.text}")

    for i in tqdm(range(0, len(all_printings), BATCH_SIZE), desc="🖨️ Uploading Printings   "):
        batch = all_printings[i:i + BATCH_SIZE]
        resp = client.post(f"{SUPABASE_URL}/rest/v1/card_prints", headers=headers, json=batch)
        if resp.status_code >= 400: print(f"\n⚠️ Printing Error: {resp.text}")

    print("\n✅ High-speed sync complete!")

if __name__ == "__main__":
    sync_everything()