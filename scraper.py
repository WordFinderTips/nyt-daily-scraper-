import requests
import json
import re
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_la_times():
    # Aaj ki naya date ID (260114)
    date_id = datetime.now().strftime("%y%m%d")
    url = f"https://games.arkadium.com/latimes-daily-crossword/data/{date_id}.json"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            return res.json()
    except:
        return {"error": "Connection issue"}
    return {"error": "Data not ready yet for this date"}

def get_connections_answers():
    # Word.tips se Connections ke answers nikalne ka tareeka
    url = "https://word.tips/nyt-connections-answers/"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        # Category names nikalne ka logic
        categories = re.findall(r'<h3>(.*?)</h3>', res.text)
        return categories if categories else ["Update coming soon"]
    except:
        return []

def main():
    print("🚀 Fetching Fresh Data for Jan 14...")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    master_json = {
        "last_updated": now,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "connections_today": get_connections_answers(),
        "la_times_crossword": get_la_times(),
        "status": "System Online"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print(f"✅ data.json Updated for {now}")

if __name__ == "__main__":
    main()
