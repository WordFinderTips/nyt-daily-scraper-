import requests
import json
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_la_times():
    # LA Times ka direct API source (Sabse stable)
    date_id = datetime.now().strftime("%y%m%d")
    url = f"https://games.arkadium.com/latimes-daily-crossword/data/{date_id}.json"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        return res.json() if res.status_code == 200 else {"error": "LA Times side down"}
    except:
        return {}

def main():
    print("🚀 Fetching from stable backup sources...")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # LA Times Data
    la_data = get_la_times()
    
    # NYT Backup (Word.Tips se answers ka rasta)
    # Kyunki NYT direct GitHub ko block kar raha hai
    master_json = {
        "last_updated": now,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "la_times": la_data,
        "nyt_backup_links": {
            "spelling_bee": "https://word.tips/nyt-spelling-bee-answers/",
            "connections": "https://word.tips/nyt-connections-answers/",
            "strands": "https://word.tips/nyt-strands-answers/"
        },
        "status": "Success - Data from Arkadium"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print(f"✅ data.json populated at {now}")

if __name__ == "__main__":
    main()
