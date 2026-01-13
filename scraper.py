import requests
import json
import re
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
}

def get_nyt_game_api(game_name):
    # NYT ki internal API hit karne ki koshish
    url = f"https://www.nytimes.com/puzzles/{game_name}"
    try:
        res = requests.get(url, headers=headers, timeout=20)
        # Regex to find the game data inside the script tag
        pattern = r'window\.gameData\s*=\s*(\{.*?\})(?=;|</script>)'
        match = re.search(pattern, res.text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    except Exception as e:
        print(f"Error fetching {game_name}: {e}")
    return {}

def get_la_times_crossword():
    # LA Times Daily Crossword (Arkadium API)
    date_str = datetime.now().strftime("%y%m%d")
    url = f"https://games.arkadium.com/latimes-daily-crossword/data/{date_str}.json"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            return res.json()
    except:
        return {"status": "LA Times Error"}
    return {}

def main():
    print("🚀 Fetching Data via Hidden Endpoints...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    # NYT Games Extraction
    bee_data = get_nyt_game_api("spelling_bee")
    strands_data = get_nyt_game_api("strands")
    
    # LA Times Extraction
    la_data = get_la_times_crossword()

    master_json = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": today,
        "nyt_data": {
            "spelling_bee": bee_data.get('today', {}),
            "strands": strands_data.get('today', {})
        },
        "la_times": {
            "daily_crossword": la_data
        },
        "status": "Success" if (bee_data or la_data) else "All Sources Failed"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print("✅ data.json Updated!")

if __name__ == "__main__":
    main()
