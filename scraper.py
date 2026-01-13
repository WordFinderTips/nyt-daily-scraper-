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
        'country_code': 'us'
    }
    try:
        res = requests.get(api_url, params=params, timeout=40)
        if res.status_code == 200:
            return res.text
    except Exception as e:
        print(f"Fetch Error: {e}")
    return None

def extract_json(html):
    if not html: return {}
    # NYT game data nikalne ka pattern
    match = re.search(r'window\.gameData\s*=\s*(\{.*?\})', html)
    if match:
        try:
            return json.loads(match.group(1))
        except:
            return {}
    return {}

def main():
    print("🚀 Master Scraper running with ScrapingBee...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 1. Spelling Bee
    bee_html = get_via_scrapingbee("https://www.nytimes.com/puzzles/spelling-bee")
    bee_json = extract_json(bee_html)
    
    # 2. Connections
    conn_html = get_via_scrapingbee("https://www.nytimes.com/puzzles/connections")
    conn_json = extract_json(conn_html)

    # 3. Strands
    strands_html = get_via_scrapingbee("https://www.nytimes.com/puzzles/strands")
    strands_json = extract_json(strands_html)

    master_json = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": today,
        "games": {
            "spelling_bee": bee_json.get('today', {}),
            "connections": conn_json.get('categories', []),
            "strands": strands_json.get('today', {})
        },
        "status": "Success" if bee_json else "Failed"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print("✅ data.json Updated!")

if __name__ == "__main__":
    main()
