import urllib.request
import os

os.makedirs('data', exist_ok=True)

def download(url, filename):
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Successfully downloaded {filename} Size: {os.path.getsize(filename)/(1024*1024):.2f} MB")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

# Movies
movie_url = "https://raw.githubusercontent.com/vamshi121/TMDB-5000-Movie-Dataset/main/tmdb_5000_movies.csv"
movie_credits_url = "https://raw.githubusercontent.com/vamshi121/TMDB-5000-Movie-Dataset/main/tmdb_5000_credits.csv"
download(movie_url, "data/tmdb_5000_movies.csv")
download(movie_credits_url, "data/tmdb_5000_credits.csv")

# Anime
anime_url = "https://raw.githubusercontent.com/MayankMkh/Anime-Recommendation-System/main/anime.csv"
download(anime_url, "data/anime.csv")
