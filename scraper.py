import requests
import json
import re
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_nyt_game(game_name):
    url = f"https://www.nytimes.com/puzzles/{game_name}"
    try:
        response = requests.get(url, headers=headers, timeout=20)
        # window.gameData ke andar chhupa hua JSON nikalna
        match = re.search(r'window\.gameData\s*=\s*(\{.*?\})(?=;|</script>)', response.text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    except:
        return {}
    return {}

def get_la_times():
    date_id = datetime.now().strftime("%y%m%d")
    url = f"https://games.arkadium.com/latimes-daily-crossword/data/{date_id}.json"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            return res.json()
    except:
        return {"status": "LA Times Fetch Error"}
    return {}

def main():
    print("🚀 Extracting Real Data...")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. NYT Games (Spelling Bee, Connections, Strands)
    bee_raw = get_nyt_game("spelling_bee")
    conn_raw = get_nyt_game("connections")
    strands_raw = get_nyt_game("strands")

    # 2. Structure Final JSON
    master_json = {
        "last_updated": now,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "nyt_games": {
            "spelling_bee": bee_raw.get('today', {}),
            "connections": conn_raw.get('categories', []),
            "strands": strands_raw.get('today', {})
        },
        "la_times": get_la_times(),
        "status": "Success"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print(f"✅ Full Data Saved at {now}")

if __name__ == "__main__":
    main()
