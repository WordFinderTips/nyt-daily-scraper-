import requests
import json
import re
from datetime import datetime
from urllib.parse import quote

# ScrapingBee API Key yahan dalain
API_KEY = '0H648XHAU6JCPP1O6QGWSH4TDA2AUZGIGAQ3BJXTV2E4V7QXJP46BRD1BFQFPCIY5KMVUNNIGPISV9O7'

def get_via_scrapingbee(target_url):
    # ScrapingBee API endpoint
    api_url = f"https://app.scrapingbee.com/api/v1/?api_key={API_KEY}&url={quote(target_url)}&render_js=false"
    try:
        res = requests.get(api_url, timeout=30)
        if res.status_code == 200:
            return res.text
    except Exception as e:
        print(f"Error fetching {target_url}: {e}")
    return None

def extract_nyt_json(html):
    if not html: return {}
    match = re.search(r'window\.gameData\s*=\s*(\{.*?\})', html)
    if match:
        return json.loads(match.group(1))
    return {}

def main():
    print("🚀 ScrapingBee Master Run Starting...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 1. Fetching NYT Games
    bee_html = get_via_scrapingbee("https://www.nytimes.com/puzzles/spelling-bee")
    conn_html = get_via_scrapingbee("https://www.nytimes.com/puzzles/connections")
    strands_html = get_via_scrapingbee("https://www.nytimes.com/puzzles/strands")
    wordle_html = get_via_scrapingbee("https://www.nytimes.com/games/wordle")

    # 2. Extracting Data
    bee_data = extract_nyt_json(bee_html).get('today', {})
    conn_data = extract_nyt_json(conn_html).get('categories', [])
    strands_data = extract_nyt_json(strands_html).get('clues', {})
    wordle_data = extract_nyt_json(wordle_html)

    # 3. LA Times (Simple Fetch as they are less strict)
    la_date = datetime.now().strftime("%y%m%d")
    la_url = f"https://games.arkadium.com/latimes-daily-crossword/data/{la_date}.json"
    la_res = requests.get(la_url, headers={'User-Agent': 'Mozilla/5.0'})
    la_data = la_res.json() if la_res.status_code == 200 else {"status": "LA Times API limit or error"}

    # Final Master JSON
    master_json = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": today,
        "nyt": {
            "spelling_bee": bee_data,
            "connections": conn_data,
            "strands": strands_data,
            "wordle": wordle_data
        },
        "la_times": la_data,
        "status": "All Data Collected via ScrapingBee"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print("✅ Success! data.json updated with all games.")

if __name__ == "__main__":
    main()
