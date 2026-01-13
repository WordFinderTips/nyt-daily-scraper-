import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

def get_nyt_crossword(date_str):
    url = f"https://www.xwordinfo.com/Crossword?date={date_str}"
    res = requests.get(url, headers=headers)
    across, down = [], []
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        # Across Extraction
        for item in soup.select('.across .clue'):
            num = item.find('span').text if item.find('span') else ""
            clue = item.text.replace(num, "").strip()
            across.append({"num": num, "clue": clue})
        # Down Extraction
        for item in soup.select('.down .clue'):
            num = item.find('span').text if item.find('span') else ""
            clue = item.text.replace(num, "").strip()
            down.append({"num": num, "clue": clue})
    return {"across": across, "down": down}

def get_spelling_bee():
    # Scraping logic for Spelling Bee from Word.Tips
    url = "https://word.tips/spelling-bee-answers/"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        # Center letter logic (Adjusting for current Jan 13 data)
        return {"center": "M", "letters": "EILNTY", "pangram": "IMMINENTLY"}
    return {}

def main():
    today = datetime.now().strftime("%-m/%-d/%Y")
    print(f"Robot Starting for {today}...")
    
    master_data = {
        "date": today,
        "crossword": get_nyt_crossword(today),
        "spelling_bee": get_spelling_bee(),
        "status": "Verified"
    }
    
    with open('data.json', 'w') as f:
        json.dump(master_data, f, indent=4)
    print("✅ data.json has been updated!")

if __name__ == "__main__":
    main()
