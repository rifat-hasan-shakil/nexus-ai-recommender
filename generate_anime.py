import time
import requests
import pandas as pd
import os

os.makedirs('data', exist_ok=True)
anime_data = []

print("Fetching Anime data from Jikan API...")
for page in range(1, 41): # 40 pages * 25 = 1000 anime
    try:
        url = f"https://api.jikan.moe/v4/top/anime?page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get('data', [])
            for item in data:
                anime_data.append({
                    "anime_id": item.get('mal_id'),
                    "title": item.get('title'),
                    "genres": ", ".join([g['name'] for g in item.get('genres', [])]),
                    "type": item.get('type'),
                    "episodes": item.get('episodes'),
                    "score": item.get('score'),
                    "synopsis": str(item.get('synopsis')).replace('\n', ' ')
                })
            print(f"Fetched page {page} - Total anime: {len(anime_data)}")
        else:
            print(f"Failed on page {page} with status {response.status_code}")
        time.sleep(1)  # Respect rate limit
    except Exception as e:
        print(f"Error on page {page}: {e}")

df = pd.DataFrame(anime_data)
df.to_csv("data/anime.csv", index=False)
print(f"Saved {len(df)} anime to data/anime.csv. Size: {os.path.getsize('data/anime.csv')/(1024*1024):.2f} MB")
