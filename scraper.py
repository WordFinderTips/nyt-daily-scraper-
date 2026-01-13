import requests
import json
import re
from datetime import datetime

# Apni ScrapingBee API Key
API_KEY = '0H648XHAU6JCPP1O6QGWSH4TDA2AUZGIGAQ3BJXTV2E4V7QXJP46BRD1BFQFPCIY5KMVUNNIGPISV9O7'

def main():
    api_url = "https://app.scrapingbee.com/api/v1/"
    target_url = "https://word.tips/spelling-bee-answers/"
    
    params = {
        'api_key': API_KEY,
        'url': target_url,
        'render_js': 'false' 
    }
    
    try:
        print("🚀 Brute Force Scraping started...")
        res = requests.get(api_url, params=params, timeout=30)
        html_content = res.text
        
        # Logic: WordTips ke answers 4 se 10 huroof ke uppercase words hote hain
        # Hum poore HTML mein se wo words dhoondenge jo sirf CAPS mein hain
        # Aur filter karenge taake menu items (WORDLE, SOLVER) na ayien
        all_caps_words = re.findall(r'\b[A-Z]{4,12}\b', html_content)
        
        # Stop words jo menu ka hissa hote hain
        stop_words = ["WORDLE", "SOLVER", "TIPS", "LOGIN", "GAMES", "MENU", "BLOG", "TODAY", "SEARCH", "HOME"]
        
        clean_words = [w for w in all_caps_words if w not in stop_words]
        final_list = list(dict.fromkeys(clean_words)) # Duplicates khatam

        master_json = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "date": "2026-01-14",
            "extracted_words": final_list if len(final_list) > 5 else "Still no data found",
            "status": "Final Brute Force"
        }

    except Exception as e:
        master_json = {"error": str(e), "status": "Failed"}

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print("✅ data.json force updated.")

if __name__ == "__main__":
    main()
