import requests
import json
import re
from datetime import datetime
from urllib.parse import quote

# ScrapingBee API Key yahan dalain
API_KEY = '0H648XHAU6JCPP1O6QGWSH4TDA2AUZGIGAQ3BJXTV2E4V7QXJP46BRD1BFQFPCIY5KMVUNNIGPISV9O7'

def get_via_scrapingbee(target_url):
    # Premium proxy aur JS wait use kar rahe hain taake data lazmi load ho
    api_url = "https://app.scrapingbee.com/api/v1/"
    params = {
        'api_key': API_KEY,
        'url': target_url,
        'premium_proxy': 'true',
        'country_code': 'us',
        'wait_for': 'window.gameData' 
    }
    try:
        res = requests.get(api_url, params=params, timeout=50)
        if res.status_code == 200:
            return res.text
        else:
            print(f"ScrapingBee Error {res.status_code}: {res.text}")
    except Exception as e:
        print(f"Network Error: {e}")
    return None

def extract_json_logic(html):
    if not html: return {}
    # Naya aur behtar pattern jo semicolon aur script tags ko handle karta hai
    patterns = [
        r'window\.gameData\s*=\s*(\{.*?\})(?=;|</script>)',
        r'window\.gameData\s*=\s*(\{.*?\});',
        r'window\.gameData\s*=\s*(\{.*?\})'
    ]
    for pattern in patterns:
        match = re.search(pattern, html, re.DOTALL)
        if match:
            try:
                data_str = match.group(1).strip()
                return json.loads(data_str)
            except Exception as e:
                print(f"JSON Parse Error: {e}")
                continue
    return {}

def main():
    print("🚀 Master Scraper starting with Advanced Parsing...")
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 1. Spelling Bee
    bee_html = get_via_scrapingbee("https://www.nytimes.com/puzzles/spelling-bee")
    bee_json = extract_json_logic(bee_html)
    
    # 2. Connections
    conn_html = get_via_scrapingbee("https://www.nytimes.com/puzzles/connections")
    conn_json = extract_json_logic(conn_html)

    # 3. Strands
    strands_html = get_via_scrapingbee("https://www.nytimes.com/puzzles/strands")
    strands_json = extract_json_logic(strands_html)

    # Master structure
    master_json = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": today,
        "games": {
            "spelling_bee": bee_json.get('today', {}),
            "connections": conn_json.get('categories', []),
            "strands": strands_json.get('today', {})
        }
    }

    # Status check
    if master_json["games"]["spelling_bee"]:
        master_json["status"] = "Success"
    else:
        master_json["status"] = "Failed - Data not found in HTML"

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print(f"✅ data.json updated with status: {master_json['status']}")

if __name__ == "__main__":
    main()
