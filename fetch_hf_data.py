import os
import subprocess
import sys

def install(package):
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])

for pkg in ["datasets", "pandas", "pyarrow"]:
    try:
        if pkg == "datasets":
            from datasets import load_dataset
        elif pkg == "pandas":
            import pandas as pd
        else:
            __import__(pkg)
    except ImportError:
        install(pkg)

import pandas as pd
from datasets import load_dataset

os.makedirs('data', exist_ok=True)

print("Downloading Movies Dataset (ashraq/tmdb-movie-metadata)...")
try:
    movies = load_dataset("ashraq/tmdb-movie-metadata", split="train")
    df_movies = movies.to_pandas()
    df_movies.to_csv("data/movies.csv", index=False)
    print(f"Saved movies.csv with {len(df_movies)} records.")
except Exception as e:
    print("Failed to download movies:", e)

print("Downloading Anime Dataset (cahya/anime-dataset)...")
try:
    anime = load_dataset("cahya/anime-dataset", split="train")
    df_anime = anime.to_pandas()
    df_anime.to_csv("data/anime.csv", index=False)
    print(f"Saved anime.csv with {len(df_anime)} records.")
except Exception as e:
    print("Failed to download anime dataset:", e)
