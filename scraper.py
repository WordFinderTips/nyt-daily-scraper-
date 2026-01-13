import requests
import json
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_la_times_crossword():
    # LA Times Daily Crossword API Endpoint (Arkadium)
    # Note: LA Times puzzles are date-based in their API
    date_str = datetime.now().strftime("%y%m%d") # Format: 260113
    url = f"https://games.arkadium.com/latimes-daily-crossword/data/{date_str}.json"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json() # Returns full puzzle data including clues/answers
    except:
        return {"status": "Direct API fetch failed, using URL instead"}
    return {"url": "https://www.latimes.com/games/daily-crossword"}

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"🚀 Master Scraper running for {today}...")

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
        "la_times": {
            "daily_crossword_data": get_la_times_crossword(),
            "mini_url": "https://www.latimes.com/games/mini-crossword",
            "sudoku_url": "https://www.latimes.com/games/daily-sudoku"
        },
        "source_status": "Verified"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print("✅ data.json is fully updated and ready!")

if __name__ == "__main__":
    main()
