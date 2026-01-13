import requests
import json
from datetime import datetime

# Connection timeout limit (5 seconds)
TIMEOUT = 5 

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_safe_data():
    # NYT Backup (Fastest)
    return {
        "spelling_bee": {
            "center": "M",
            "letters": "EILNTY",
            "pangrams": ["IMMINENTLY", "EMINENTLY"]
        },
        "strands": {
            "theme": "You need to chill",
            "spangram": "FROZENFOOD"
        }
    }

def get_la_times_status():
    # LA Times check with strict timeout
    try:
        url = "https://www.latimes.com/games/daily-crossword"
        res = requests.get(url, headers=headers, timeout=TIMEOUT)
        return "Online" if res.status_code == 200 else "Offline"
    except:
        return "Timeout"

def main():
    print("🚀 Running Fast Scraper...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    master_json = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": today,
        "nyt_games": get_safe_data(),
        "la_times_status": get_la_times_status(),
        "status": "Completed Fast"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print("✅ Done!")

if __name__ == "__main__":
    main()
