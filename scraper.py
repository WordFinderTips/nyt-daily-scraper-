import requests
import json
import re
from datetime import datetime

# Advanced Headers taake NYT ko lage ke real browser hai
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def get_nyt_game_data(url):
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            # NYT games ka sara data 'window.gameData' object mein hota hai
            match = re.search(r'window\.gameData\s*=\s*(\{.*?\});', response.text)
            if not match:
                # Alternate pattern check
                match = re.search(r'window\.gameData\s*=\s*(\{.*?\})', response.text)
            
            if match:
                return json.loads(match.group(1))
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    print("🚀 Starting Master Scraper...")
    
    # 1. Spelling Bee Official Data
    bee_raw = get_nyt_game_data("https://www.nytimes.com/puzzles/spelling-bee")
    bee_final = {}
    if bee_raw and 'today' in bee_raw:
        bee_final = {
            "center": bee_raw['today']['centerLetter'],
            "outer": bee_raw['today']['outerLetters'],
            "pangrams": bee_raw['today']['pangrams'],
            "answers": bee_raw['today']['answers']
        }

    # 2. Connections Official Data
    conn_raw = get_nyt_game_data("https://www.nytimes.com/puzzles/connections")
    conn_final = {}
    if conn_raw and 'categories' in conn_raw:
        conn_final = conn_raw['categories'] # Categories with answers

    # Final Master JSON
    master_json = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "spelling_bee": bee_final,
        "connections": conn_final,
        "status": "Success" if bee_final else "Failed to fetch Bee"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print("✅ Master data.json updated!")

if __name__ == "__main__":
    main()
