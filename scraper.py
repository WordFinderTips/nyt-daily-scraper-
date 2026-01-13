import requests
import json
from datetime import datetime

# Apni ScrapingBee API Key
API_KEY = '0H648XHAU6JCPP1O6QGWSH4TDA2AUZGIGAQ3BJXTV2E4V7QXJP46BRD1BFQFPCIY5KMVUNNIGPISV9O7'

def main():
    # NYT Spelling Bee ki asli internal API
    target_url = "https://www.nytimes.com/puzzles/spelling-bee"
    api_url = "https://app.scrapingbee.com/api/v1/"
    
    params = {
        'api_key': API_KEY,
        'url': target_url,
        'premium_proxy': 'true',
        'country_code': 'us',
        'render_js': 'false' 
    }
    
    try:
        print("🚀 Fetching direct from NYT Source...")
        res = requests.get(api_url, params=params, timeout=40)
        html = res.text
        
        import re
        # NYT apna sara data is ek line mein rakhta hai
        match = re.search(r'window\.gameData\s*=\s*(\{.*?\})(?=;|</script>)', html, re.DOTALL)
        
        if match:
            raw_data = json.loads(match.group(1))
            today = raw_data.get('today', {})
            
            master_json = {
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "game": "Spelling Bee",
                "center_letter": today.get('centerLetter'),
                "outer_letters": today.get('outerLetters'),
                "word_list": today.get('answers'), # Ye hain asli 100% answers
                "pangrams": today.get('pangrams'),
                "status": "Success - Direct NYT Data"
            }
        else:
            master_json = {"status": "Failed", "reason": "Could not find gameData on NYT"}

    except Exception as e:
        master_json = {"error": str(e), "status": "Failed"}

    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print("✅ Final Data Saved.")

if __name__ == "__main__":
    main()
