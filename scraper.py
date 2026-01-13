import requests
import json
from datetime import datetime

# ScrapingBee API Key yahan dalein
API_KEY = '0H648XHAU6JCPP1O6QGWSH4TDA2AUZGIGAQ3BJXTV2E4V7QXJP46BRD1BFQFPCIY5KMVUNNIGPISV9O7'

def scrape_all_wordtips():
    # Hum sabse main links target kar rahe hain jo aapne diye thay
    urls = {
        "crossword": "https://word.tips/todays-nyt-the-crossword-clues-answers-hints/",
        "connections": "https://word.tips/connections-hints-today/",
        "spelling_bee": "https://word.tips/spelling-bee-answers/",
        "strands": "https://word.tips/todays-nyt-strands-hints-spangram-answers/",
        "la_times": "https://word.tips/crossword-solver/los-angeles-times-daily/"
    }

    master_results = {}
    
    # Aik ek karke links process honge. Trial account hai toh har link 1 credit lega.
    # Agar aapko sirf 1 credit kharch karna hai, toh sirf 1 URL rakhein.
    
    for name, target_url in urls.items():
        print(f"Scraping {name}...")
        
        api_url = "https://app.scrapingbee.com/api/v1/"
        params = {
            'api_key': API_KEY,
            'url': target_url,
            'render_js': 'false', # Credit bachane ke liye JS off
            'extract_rules': {
                "answers": {
                    "selector": "article li, article td", # WordTips ke answers hamesha yahan hote hain
                    "type": "list"
                }
            }
        }

        try:
            res = requests.get(api_url, params=params, timeout=30)
            if res.status_code == 200:
                data = res.json()
                # Faltu kachra saaf karne ke liye filter
                clean_list = [item for item in data.get('answers', []) if 2 < len(item) < 40]
                master_results[name] = clean_list[:30] # Top 30 answers
            else:
                master_results[name] = [f"Error: {res.status_code}"]
        except Exception as e:
            master_results[name] = [str(e)]

    return master_results

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Data fetch karein
    puzzles_data = scrape_all_wordtips()
    
    final_json = {
        "last_updated": now,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "source": "WordTips via ScrapingBee",
        "puzzles": puzzles_data
    }

    with open('data.json', 'w') as f:
        json.dump(final_json, f, indent=4)
    print("✅ data.json is now updated with real answers!")

if __name__ == "__main__":
    main()
