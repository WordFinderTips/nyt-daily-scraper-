import requests
import json
import re
from datetime import datetime, timedelta

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

def get_la_times():
    # Pehle aaj ki date check karega, agar fail hua toh kal ki (Latest available)
    dates_to_try = [
        datetime.now().strftime("%y%m%d"),
        (datetime.now() - timedelta(days=1)).strftime("%y%m%d")
    ]
    
    for d in dates_to_try:
        url = f"https://games.arkadium.com/latimes-daily-crossword/data/{d}.json"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                return res.json()
        except:
            continue
    return {"error": "Puzzles not released yet"}

def get_connections():
    url = "https://word.tips/nyt-connections-answers/"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        # Category names nikalne ka pattern
        categories = re.findall(r'<h3>(.*?)</h3>', res.text)
        return categories if categories else ["Fetching next update..."]
    except:
        return ["Source temporarily unavailable"]

def main():
    print("🚀 Fetching Latest Available Data...")
    now_pk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    master_json = {
        "last_updated": now_pk,
        "note": "Timezone: Pakistan (PKT). Data updates when US puzzles go live.",
        "connections_preview": get_connections(),
        "la_times_data": get_la_times(),
        "status": "Running"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print(f"✅ data.json updated successfully at {now_pk}")

if __name__ == "__main__":
    main()
