import requests
import json
import re
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_nyt_data(url):
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            # Game data nikalne ka pattern
            match = re.search(r'window\.gameData\s*=\s*(\{.*?\})(?=;|</script>)', res.text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
    except:
        return {}
    return {}

def get_la_times_crossword(path):
    # LA Times format: YYMMDD
    date_str = datetime.now().strftime("%y%m%d")
    url = f"https://games.arkadium.com/{path}/data/{date_str}.json"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json()
    except:
        return {"status": "LA Times Fetch Error"}
    return {}

def main():
    print("🚀 Scraping NYT (US) and LA Times...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 1. NYT Games
    bee = get_nyt_data("https://www.nytimes.com/puzzles/spelling-bee")
    strands = get_nyt_data("https://www.nytimes.com/puzzles/strands")
    conn = get_nyt_data("https://www.nytimes.com/puzzles/connections")

    # 2. LA Times Games
    la_daily = get_la_times_crossword("latimes-daily-crossword")
    la_mini = get_la_times_crossword("latimes-mini-crossword")

    master_json = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": today,
        "nyt_us_time": {
            "spelling_bee": bee.get('today', {}),
            "strands": strands.get('today', {}),
            "connections": conn.get('categories', [])
        },
        "la_times": {
            "daily_crossword": la_daily,
            "mini_crossword": la_mini
        },
        "status": "Success"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print("✅ data.json Updated with NYT and LA Times data!")

if __name__ == "__main__":
    main()
