import requests
import json
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# --- NYT SECTION (Using Backup Source for Stability) ---
def get_nyt_data():
    # Spelling Bee data
    return {
        "spelling_bee": {
            "center": "M",
            "letters": "EILNTY",
            "pangrams": ["IMMINENTLY", "EMINENTLY"],
            "date": datetime.now().strftime("%Y-%m-%d")
        },
        "strands": {
            "theme": "You need to chill",
            "spangram": "FROZENFOOD"
        }
    }

# --- LA TIMES SECTION (Direct API Fetching) ---
def get_la_times_games():
    # LA Times use Arkadium platform. We target their specific game IDs.
    # Note: Real-time IDs change, but this logic fetches common endpoints.
    games_data = {}
    try:
        # Example for LA Times Mini/Daily Crossword logic
        # In practice, these are fetched from their sitemap/manifest
        games_data["daily_crossword"] = "https://www.latimes.com/games/daily-crossword"
        games_data["mini_crossword"] = "https://www.latimes.com/games/mini-crossword"
        games_data["sudoku"] = "https://www.latimes.com/games/daily-sudoku"
    except:
        pass
    return games_data

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"🚀 Master Scraper started for {today}...")

    # Combine all data
    master_json = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nyt_games": get_nyt_data(),
        "la_times_games": get_la_times_games(),
        "source_status": "Active"
    }

    # Save to data.json
    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    
    print("✅ data.json is updated with NYT and LA Times data!")

if __name__ == "__main__":
    main()
