import urllib.request
import os

os.makedirs('data', exist_ok=True)

urls = [
    "https://raw.githubusercontent.com/Ketanpawar/Anime-Recommendation-System/main/anime.csv",
    "https://raw.githubusercontent.com/Prasad-2900/Anime-Recommendation-System/main/anime.csv",
    "https://raw.githubusercontent.com/shikhondev/anime-recommendation-system/main/anime.csv",
    "https://raw.githubusercontent.com/Amil-Akkalkotkar/Anime-Recommendation-System/main/anime.csv",
    "https://raw.githubusercontent.com/taki0112/Anime-Recommendation/master/anime.csv",
    "https://raw.githubusercontent.com/indradenbakker/anime-recommendation/master/data/anime.csv"
]

for url in urls:
    print(f"Trying {url}...")
    try:
        urllib.request.urlretrieve(url, "data/anime.csv")
        size = os.path.getsize("data/anime.csv")
        if size > 100000: # > 100KB means it's likely valid
            print(f"Success! Size: {size/(1024*1024):.2f} MB")
            break
        else:
            print(f"File too small ({size} bytes). Possibly 404.")
    except Exception as e:
        print(e)
