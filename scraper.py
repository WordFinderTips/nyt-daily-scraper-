import requests
import json
import re
from datetime import datetime
from urllib.parse import quote

# ScrapingBee API Key yahan dalain
API_KEY = '0H648XHAU6JCPP1O6QGWSH4TDA2AUZGIGAQ3BJXTV2E4V7QXJP46BRD1BFQFPCIY5KMVUNNIGPISV9O7'

def get_via_scrapingbee(target_url):
    # Hum 'premium_proxy' aur 'country_code=us' use kar rahe hain
    api_url = "https://app.scrapingbee.com/api/v1/"
    params = {
        'api_key': API_KEY,
        'url': target_url,
        'premium_proxy': 'true',
        'country_code': 'us',
        'wait_for': 'window.gameData' # Wait taake JS load ho jaye
    }
    try:
        res = requests.get(api_url, params=params, timeout=40)
        if res.status_code == 200:
            return res.text
        else:
            print(f"Error {res.status_code}: {res.text}")
    except Exception as e:
        print(f"Fetch Error: {e}")
    return None

def extract_json(html):
    if not html: return {}
    match = re.search(r'window\.gameData\s*=\s*(\{.*?\})', html)
    if not match:
        match = re.search(r'window\.gameData\s*=\s*(\{.*?)\s*</script>', html)
    if match:
        try:
            return json.loads(match.group(1).rstrip(';'))
        except:
            return {}
    return {}

def main():
    print("🚀 Ultra-Scraper starting...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 1. NYT Spelling Bee (Sub se pehle isay fix karte hain)
    bee_html = get_via_scrapingbee("https://www.nytimes.com/puzzles/spelling-bee")
    bee_data = extract_json(bee_html).get('today', {})

    # 2. NYT Connections
    conn_html = get_via_scrapingbee("https://www.nytimes.com/puzzles/connections")
    conn_data = extract_json(conn_html).get('categories', [])

    master_json = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": today,
        "nyt": {
            "spelling_bee": bee_data,
            "connections": conn_data
        },
        "status": "Success" if bee_data else "Failed - Proxy Blocked"
    }

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print("✅ data.json Updated!")

if __name__ == "__main__":
    main()
