import requests
import json
import re
from datetime import datetime
from urllib.parse import quote

# ScrapingBee API Key yahan dalain
API_KEY = '0H648XHAU6JCPP1O6QGWSH4TDA2AUZGIGAQ3BJXTV2E4V7QXJP46BRD1BFQFPCIY5KMVUNNIGPISV9O7'

def get_via_scrapingbee(target_url):
    api_url = "https://app.scrapingbee.com/api/v1/"
    # Hum 'render_js': 'true' use karenge taake dynamic data load ho jaye
    params = {
        'api_key': API_KEY,
        'url': target_url,
        'render_js': 'true', 
        'country_code': 'us'
    }
    try:
        res = requests.get(api_url, params=params, timeout=60)
        if res.status_code == 200:
            return res.text
        else:
            print(f"Error {res.status_code}: {res.text}")
    except Exception as e:
        print(f"Network Error: {e}")
    return None

def extract_game_data(html):
    if not html: return {}
    
    # Pattern 1: window.gameData
    match = re.search(r'window\.gameData\s*=\s*(\{.*?\})(?=;|</script>)', html, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except: pass

    # Pattern 2: Scripts with JSON content
    match = re.search(r'{"today":\{.*?\}\}', html)
    if match:
        try:
            return json.loads(match.group(0))
        except: pass

    return {}

def main():
    print("🚀 Starting Advanced Extraction...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    games_to_fetch = {
        "spelling_bee": "https://www.nytimes.com/puzzles/spelling-bee",
        "connections": "https://www.nytimes.com/puzzles/connections",
        "strands": "https://www.nytimes.com/puzzles/strands",
        "wordle": "https://www.nytimes.com/games/wordle"
    }
    
    final_games_data = {}

    for game, url in games_to_fetch.items():
        print(f"Fetching {game}...")
        html = get_via_scrapingbee(url)
        data = extract_game_data(html)
        
        # Structure cleanup
        if game in ["spelling_bee", "strands"]:
            final_games_data[game] = data.get('today', data)
        elif game == "connections":
            final_games_data[game] = data.get('categories', data)
        else:
            final_games_data[game] = data

    master_json = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": today,
        "games": final_games_data,
        "status": "Success" if any(final_games_data.values()) else "Data Extraction Failed"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print("✅ data.json has been updated with deep scraping.")

if __name__ == "__main__":
    main()
