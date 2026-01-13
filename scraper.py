import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_clean_answers(url):
    try:
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            results = []
            
            # Word.Tips ke articles mein answers aksar <li> ya tables mein hote hain
            # Hum sirf wo text uthayenge jo menu ka hissa nahi hai
            content_area = soup.find('article') or soup.find('main')
            if content_area:
                for item in content_area.find_all(['li', 'td']):
                    text = item.get_text().strip()
                    # Filtering: Menu items ko nikalne ke liye
                    if 2 < len(text) < 50 and "Solver" not in text and "Today" not in text:
                        results.append(text)
            
            return list(dict.fromkeys(results))[:40] # Duplicate khatam aur top 40
    except:
        return []
    return []

def main():
    print("🚀 Scraping Specific Answers from Word.Tips...")
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
    for name, link in urls.items():
        print(f"Processing {name}...")
        master_data[name] = fetch_clean_answers(link)

    final_json = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "puzzles": master_data
    }

    with open('data.json', 'w') as f:
        json.dump(final_json, f, indent=4)
    print("✅ data.json cleaned and updated!")

if __name__ == "__main__":
    main()
