import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Headers taake block na ho
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 Safari/537.36'
}

def get_nyt_data():
    date_str = datetime.now().strftime("%-m/%-d/%Y") # 1/13/2026
    url = f"https://www.xwordinfo.com/Crossword?date={date_str}"
    
    print(f"Fetching data for: {date_str}")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return "Blocked or Error"

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Across nikalna
    across_data = []
    # XWord Info ke Across clues nikalne ka logic
    # (Ye logic site ke HTML structure ke mutabiq hai)
    for clue_div in soup.select('.across .clue'):
        num = clue_div.find('span').text if clue_div.find('span') else ""
        text = clue_div.text.replace(num, "").strip()
        # Answer nikalna (Yahan aapko grid mapping karni hogi)
        across_data.append({"num": num, "clue": text})

    final_json = {"date": date_str, "across": across_data}
    
    with open('data.json', 'w') as f:
        json.dump(final_json, f, indent=4)
    print("✅ JSON Created!")

if __name__ == "__main__":
    get_nyt_data()
