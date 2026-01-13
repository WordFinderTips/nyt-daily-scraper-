import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

# Apni ScrapingBee API Key yahan dalein
API_KEY = '0H648XHAU6JCPP1O6QGWSH4TDA2AUZGIGAQ3BJXTV2E4V7QXJP46BRD1BFQFPCIY5KMVUNNIGPISV9O7'

def get_bee_answers(target_url):
    api_url = "https://app.scrapingbee.com/api/v1/"
    params = {
        'api_key': API_KEY,
        'url': target_url,
        'render_js': 'false' 
    }
    try:
        res = requests.get(api_url, params=params, timeout=30)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            words = []
            
            # WordTips ke Spelling Bee answers hamesha table (td) mein hote hain
            # Hum sirf wo words uthayenge jo uppercase hain aur menu ka hissa nahi
            for td in soup.find_all('td'):
                txt = td.get_text().strip()
                # Spelling Bee answers hamesha bare haroof (Caps) mein hote hain
                if txt.isupper() and len(txt) > 3 and " " not in txt:
                    words.append(txt)
            
            return list(dict.fromkeys(words)) # Duplicates khatam
        else:
            return [f"API Error: {res.status_code}"]
    except Exception as e:
        return [f"Error: {str(e)}"]

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Sirf Spelling Bee ka test (1 Credit)
    print("🚀 Fetching ONLY Table Data (Proof of Concept)...")
    url = "https://word.tips/spelling-bee-answers/"
    data = get_bee_answers(url)

    final_json = {
        "last_updated": now,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "real_answers": data if data else "Table not found - Check Logic",
        "status": "Success" if data else "Failed to find words"
    }

    with open('data.json', 'w') as f:
        json.dump(final_json, f, indent=4)
    print("✅ Check data.json for REAL words now!")

if __name__ == "__main__":
    main()
