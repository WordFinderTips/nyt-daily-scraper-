import requests
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup # BeautifulSoup use kar rahe hain taake data safayi se nikle

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_wordtips_content(url):
    try:
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            # Word.Tips par answers aksar <strong> tags ya tables mein hote hain
            # Hum saare list items aur bold text nikal rahe hain
            results = []
            for item in soup.find_all(['li', 'strong']):
                text = item.get_text().strip()
                if 2 < len(text) < 100: # Sirf kaam ka text rakhne ke liye
                    results.append(text)
            return results[:30] # Top 30 points kafi hain
    except:
        return ["Link Error"]
    return []

def main():
    print("🚀 Scraping all Word.Tips Daily Links...")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Aapke diye hue links ka structure
    urls = {
        "nyt_crossword": "https://word.tips/todays-nyt-the-crossword-clues-answers-hints/",
        "nyt_mini": "https://word.tips/todays-nyt-mini-crossword-clues-answers/",
        "nyt_strands": "https://word.tips/todays-nyt-strands-hints-spangram-answers/",
        "nyt_connections": "https://word.tips/connections-hints-today/",
        "nyt_spelling_bee": "https://word.tips/spelling-bee-answers/",
        "nyt_pips": "https://word.tips/nyt-pips-todays-hints-answers/",
        "nyt_wordle": "https://word.tips/todays-wordle-answer/",
        "la_times_daily": "https://word.tips/crossword-solver/los-angeles-times-daily/",
        "la_times_mini": "https://word.tips/crossword-solver/los-angeles-times-mini/",
        "usa_today_daily": "https://word.tips/crossword-solver/usa-today/",
        "usa_today_quick": "https://word.tips/crossword-solver/usa-today-quick/"
    }
    
    master_data = {}
    for game_name, link in urls.items():
        print(f"Fetching {game_name}...")
        master_data[game_name] = fetch_wordtips_content(link)

    final_json = {
        "last_updated": now,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "puzzles_data": master_data,
        "status": "Success"
    }

    with open('data.json', 'w') as f:
        json.dump(final_json, f, indent=4)
    print(f"✅ All {len(urls)} links scraped into data.json")

if __name__ == "__main__":
    main()
