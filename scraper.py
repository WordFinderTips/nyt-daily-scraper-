import requests
import json
import re
from datetime import datetime

# Yahan apni Scrapeless API Key dalain
API_KEY = 'sk_nVuhvhluWV4sjpXfO7s8OjUJm8Zip8tjB1ZiX39LuHPcHJ1uEhhGLf9tD0OshMWQ'

def fetch_nyt_game(url):
    api_url = "https://api.scrapeless.com/v1/scraper/request"
    payload = {
        "url": url,
        "method": "GET",
        "proxy_country": "US"
    }
    headers = {"x-api-token": API_KEY, "Content-Type": "application/json"}
    try:
        res = requests.post(api_url, headers=headers, json=payload, timeout=30)
        if res.status_code == 200:
            html = res.json().get('body', '')
            match = re.search(r'window\.gameData\s*=\s*(\{.*?\})', html)
            if match:
                return json.loads(match.group(1))
    except:
        return None
    return None

def get_la_times(game_path):
    # LA Times (Arkadium) API logic
    date_id = datetime.now().strftime("%y%m%d")
    url = f"https://games.arkadium.com/{game_path}/data/{date_id}.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        return res.json() if res.status_code == 200 else "Unavailable"
    except:
        return "Error"

def main():
    print("🚀 Extracting All Games Data...")
    
    # 1. Fetch NYT Games
    bee_raw = fetch_nyt_game("https://www.nytimes.com/puzzles/spelling-bee")
    conn_raw = fetch_nyt_game("https://www.nytimes.com/puzzles/connections")
    strands_raw = fetch_nyt_game("https://www.nytimes.com/puzzles/strands")
    wordle_raw = fetch_nyt_game("https://www.nytimes.com/games/wordle")
    
    # 2. Structure Final JSON
    master_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nyt": {
            "spelling_bee": bee_raw.get('today', {}) if bee_raw else {},
            "connections": conn_raw.get('categories', []) if conn_raw else [],
            "strands": strands_raw.get('clues', {}) if strands_raw else {},
            "wordle": wordle_raw.get('today', {}) if wordle_raw else {},
            "letter_boxed": fetch_nyt_game("https://www.nytimes.com/puzzles/letter-boxed") or {}
        },
        "la_times": {
            "daily_crossword": get_la_times("latimes-daily-crossword"),
            "mini_crossword": get_la_times("latimes-mini-crossword"),
            "sudoku": get_la_times("daily-sudoku")
        },
        "other_games": {
            "tiles": "https://www.nytimes.com/puzzles/tiles",
            "vertex": "https://www.nytimes.com/puzzles/vertex"
        }
    }

    with open('data.json', 'w') as f:
        json.dump(master_data, f, indent=4)
    print("✅ All Game Data saved to data.json!")

if __name__ == "__main__":
    main()
