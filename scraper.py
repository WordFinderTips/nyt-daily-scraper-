import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

API_KEY = '0H648XHAU6JCPP1O6QGWSH4TDA2AUZGIGAQ3BJXTV2E4V7QXJP46BRD1BFQFPCIY5KMVUNNIGPISV9O7'

def get_data_safe(target_url):
    api_url = "https://app.scrapingbee.com/api/v1/"
    # Sirf raw HTML mangwa rahe hain, extract rules hata diye hain 400 error se bachne ke liye
    params = {
        'api_key': API_KEY,
        'url': target_url,
        'render_js': 'false' 
    }
    try:
        res = requests.get(api_url, params=params, timeout=30)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            # WordTips ke answers 'li' tags mein hote hain
            answers = [li.get_text().strip() for li in soup.find_all('li') if 3 < len(li.get_text()) < 30]
            return answers[:40]
        else:
            return [f"API Error: {res.status_code}"]
    except Exception as e:
        return [f"Error: {str(e)}"]

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Sirf 1 link par test karein taake mazeed credit zaya na hon
    # Jab ye chal jaye toh hum baqi links add kar lenge
    print("🚀 Fetching Spelling Bee Answers (1 Credit Test)...")
    bee_url = "https://word.tips/spelling-bee-answers/"
    bee_data = get_data_safe(bee_url)

    final_json = {
        "last_updated": now,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "spelling_bee_answers": bee_data,
        "status": "Check this JSON for real words now"
    }

    with open('data.json', 'w') as f:
        json.dump(final_json, f, indent=4)
    print("✅ Done! Check data.json")

if __name__ == "__main__":
    main()
