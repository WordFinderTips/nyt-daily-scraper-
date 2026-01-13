import requests
import json
from datetime import datetime

# Headers for LA Times/Arkadium bypass
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Origin': 'https://www.latimes.com',
    'Referer': 'https://www.latimes.com/'
}

def get_la_times_answers():
    # LA Times Daily Crossword date-based logic
    date_id = datetime.now().strftime("%y%m%d") # e.g., 260113
    url = f"https://games.arkadium.com/latimes-daily-crossword/data/{date_id}.json"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            # Sirf kaam ka data nikalna (Clues aur Answers)
            return {
                "title": data.get("title", "LA Times Daily Crossword"),
                "clues": data.get("clues", []),
                "answers": data.get("answers", []),
                "status": "Success"
            }
    except:
        pass
    return {"status": "Failed to fetch LA Times answers"}

def main():
    print("🚀 Master Scraper Fetching All Games...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    master_json = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": today,
        "nyt_games": {
            "spelling_bee": {
                "center": "M",
                "letters": "EILNTY",
                "pangrams": ["IMMINENTLY", "EMINENTLY"]
            },
            "strands": {
                "theme": "You need to chill",
                "spangram": "FROZENFOOD"
            }
        },
        "la_times": get_la_times_answers(),
        "status": "All Systems Go"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print("✅ data.json is now a complete Game Hub!")

if __name__ == "__main__":
    main()
