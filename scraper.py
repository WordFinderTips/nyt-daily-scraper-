import requests
import json
import re
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_official_spelling_bee():
    url = "https://www.nytimes.com/puzzles/spelling-bee"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        # NYT ke page se JSON data nikalna
        match = re.search(r'window\.gameData = (\{.*?\})', res.text)
        if match:
            data = json.loads(match.group(1))
            today_data = data['today']
            return {
                "center": today_data['centerLetter'],
                "outer": today_data['outerLetters'],
                "pangrams": today_data['pangrams'],
                "answers": today_data['answers']
            }
    return None

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"Fetching official data for {today}...")
    
    bee_data = get_official_spelling_bee()
    
    master_json = {
        "date": today,
        "spelling_bee": bee_data,
        "status": "Official NYT Source"
    }
    
    # Ye file aapki GitHub Repo mein save hogi
    with open('data.json', 'w') as f:
        json.dump(master_json, f, indent=4)
    print("✅ data.json is ready for your Auto Blogger!")

if __name__ == "__main__":
    main()
