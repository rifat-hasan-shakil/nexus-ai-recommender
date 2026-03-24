import urllib.request
import os

os.makedirs('data', exist_ok=True)

def download(url, filename):
    print(f"Downloading {filename} from {url}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Successfully downloaded {filename}. Size: {os.path.getsize(filename)/(1024*1024):.2f} MB")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

download("https://raw.githubusercontent.com/hamzamalik22/ai-movie-recommender/main/tmdb_5000_credits.csv", "data/tmdb_5000_credits.csv")
download("https://raw.githubusercontent.com/LeoRigasaki/Anime-dataset/main/data/raw/anime.csv", "data/anime.csv")
