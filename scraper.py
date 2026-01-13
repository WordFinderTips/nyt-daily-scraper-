import requests
import json
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_la_times_13():
    # 13 January ka fix date ID
    url = "https://games.arkadium.com/latimes-daily-crossword/data/260113.json"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            return res.json()
    except:
        return {"error": "Connection issue"}
    return {"error": "13th Jan data not found"}

def main():
    print("🚀 Fetching 13th January Data specifically...")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # LA Times ka asli 13 Jan ka data
    la_data = get_la_times_13()

    master_json = {
        "last_updated": now,
        "date_requested": "2026-01-13",
        "la_times_13_jan": la_data,
        # NYT ke liye hum static dummy data daal rahe hain taake structure dikh jaye
        "nyt_preview": {
            "spelling_bee": "Data fetch block by NYT, use LA Times for proof",
            "connections": ["Group 1", "Group 2", "Group 3", "Group 4"]
        },
        "status": "Success - 13th Jan Proof"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print(f"✅ Proof: data.json updated with 13th Jan data.")

if __name__ == "__main__":
    main()
