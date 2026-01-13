import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

def clean_data(url, game_type):
    try:
        res = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(res.text, 'html.parser')
        results = []
        
        # Article area target karein
        content = soup.find('article')
        if not content: return []

        if "spelling_bee" in game_type:
            # Spelling bee ke table cells se words nikalna
            for td in content.find_all('td'):
                txt = td.get_text().strip()
                if len(txt) > 3 and txt.isalpha(): results.append(txt.upper())
        
        elif "connections" in game_type:
            # Connections ki categories (aksar bold ya specific class mein hoti hain)
            for li in content.find_all('li'):
                if ':' in li.get_text(): results.append(li.get_text().strip())

        else:
            # Crossword Clues target karein
            for item in content.find_all(['li', 'div'], class_=re.compile(r'clue|answer|item')):
                txt = item.get_text().strip()
                if len(txt) > 5: results.append(txt)
            
            # Agar upar wala fail ho toh general cleaning
            if not results:
                for li in content.find_all('li'):
                    txt = li.get_text().strip()
                    if "Crossword Clue" in txt or "Answer:" in txt:
                        results.append(txt.replace('\n', ' ').replace('\t', ' '))

        return list(dict.fromkeys(results))[:50]
    except:
        return []

def main():
    import re
    print("🚀 Running Laser Scraper on all links...")
    urls = {
        "nyt_crossword": "https://word.tips/todays-nyt-the-crossword-clues-answers-hints/",
        "nyt_mini": "https://word.tips/todays-nyt-mini-crossword-clues-answers/",
        "nyt_strands": "https://word.tips/todays-nyt-strands-hints-spangram-answers/",
        "nyt_connections": "https://word.tips/connections-hints-today/",
        "nyt_spelling_bee": "https://word.tips/spelling-bee-answers/",
        "nyt_wordle": "https://word.tips/todays-wordle-answer/",
        "la_times_daily": "https://word.tips/crossword-solver/los-angeles-times-daily/",
        "usa_today_daily": "https://word.tips/crossword-solver/usa-today/"
    }
    
    final_data = {}
    for name, link in urls.items():
        print(f"Cleaning {name}...")
        final_data[name] = clean_data(link, name)

    output = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "puzzles": final_data
    }

    with open('data.json', 'w') as f:
        json.dump(output, f, indent=4)
    print("✅ Success! Clean data saved.")

if __name__ == "__main__":
    main()
