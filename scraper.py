import requests
import json
import re
from datetime import datetime

# ScrapingBee API Key yahan dalain
API_KEY = '0H648XHAU6JCPP1O6QGWSH4TDA2AUZGIGAQ3BJXTV2E4V7QXJP46BRD1BFQFPCIY5KMVUNNIGPISV9O7'

def get_via_scrapingbee(target_url):
    api_url = "https://app.scrapingbee.com/api/v1/"
    params = {
        'api_key': API_KEY,
        'url': target_url,
        'premium_proxy': 'true',
        'country_code': 'us',
        'render_js': 'false' # Hum raw HTML par parse karenge jo faster hai
    }
    try:
        res = requests.get(api_url, params=params, timeout=45)
        if res.status_code == 200:
            return res.text
        else:
            print(f"Error {res.status_code}: {res.text}")
    except Exception as e:
        print(f"Network Error: {e}")
    return None

def extract_game_data(html):
    if not html: return {}
    
    # Method 1: Standard window.gameData
    match = re.search(r'window\.gameData\s*=\s*(\{.*?\})(?=;|</script>)', html, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except: pass

    # Method 2: Connection logic (Sometimes stored in a different script tag)
    match = re.search(r'{"categories":.*?"id":.*?\}', html)
    if match:
        try:
            return json.loads(match.group(0))
        except: pass

    return {}

def main():
    print("🚀 Starting Advanced Extraction...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Games dictionary
    results = {
        "spelling_bee": "https://www.nytimes.com/puzzles/spelling-bee",
        "connections": "https://www.nytimes.com/puzzles/connections",
        "strands": "https://www.nytimes.com/puzzles/strands"
    }
    
    final_games_data = {}

    for game, url in results.items():
        print(f"Fetching {game}...")
        html = get_via_scrapingbee(url)
        data = extract_game_data(html)
        
        # Spelling Bee aur Strands ke liye 'today' object nikalna
        if game in ["spelling_bee", "strands"]:
            final_games_data[game] = data.get('today', data)
        else:
            final_games_data[game] = data

    master_json = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": today,
        "games": final_games_data,
        "status": "Success" if any(final_games_data.values()) else "Data Empty"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print("✅ data.json has been rewritten.")

if __name__ == "__main__":
    main()
