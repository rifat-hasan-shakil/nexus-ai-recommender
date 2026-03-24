import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

os.makedirs('models', exist_ok=True)

print("--- Processing Movie Data ---")
movies = pd.read_csv('data/tmdb_5000_movies.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')
movies = movies.merge(credits, on='title')

# Keep relevant columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.dropna(inplace=True)

def convert(text):
    L = []
    try:
        for i in ast.literal_eval(text):
            L.append(i['name'])
    except: pass
    return L

def convert3(text):
    L = []
    counter = 0
    try:
        for i in ast.literal_eval(text):
            if counter < 3:
                L.append(i['name'])
                counter+=1
            else: break
    except: pass
    return L

def fetch_director(text):
    L = []
    try:
        for i in ast.literal_eval(text):
            if i['job'] == 'Director':
                L.append(i['name'])
                break
    except: pass
    return L

# Apply conversions
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['crew'] = movies['crew'].apply(fetch_director)

# Strip spaces from multi-word names so they become unique tags (e.g. "Johnny Depp" -> "JohnnyDepp")
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ","") for i in x])
movies['overview'] = movies['overview'].apply(lambda x: x.split() if isinstance(x, str) else [])

# Create a single 'tags' column containing all metadata
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
new_movies = movies[['movie_id', 'title', 'tags']].copy()
new_movies['tags'] = new_movies['tags'].apply(lambda x: " ".join(x).lower())

print("Vectorizing Movies...")
cv = CountVectorizer(max_features=5000, stop_words='english')
movie_vectors = cv.fit_transform(new_movies['tags']).toarray()
print("Calculating Cosine Similarity...")
movie_similarity = cosine_similarity(movie_vectors)

print("Saving Movie Models...")
# We save a dictionary to significantly reduce the size instead of a pandas dataframe
pickle.dump(new_movies.to_dict(), open('models/movie_dict.pkl', 'wb'))
pickle.dump(movie_similarity, open('models/movie_similarity.pkl', 'wb'))


print("\n--- Processing Anime Data ---")
anime = pd.read_csv('data/anime.csv')
anime.dropna(subset=['synopsis'], inplace=True)

anime['genres_list'] = anime['genres'].apply(lambda x: str(x).replace(" ", "").split(",") if pd.notnull(x) else [])
anime['synopsis_list'] = anime['synopsis'].apply(lambda x: str(x).split() if pd.notnull(x) else [])
anime['tags'] = anime['synopsis_list'] + anime['genres_list']

new_anime = anime[['anime_id', 'title', 'tags']].copy()
new_anime['tags'] = new_anime['tags'].apply(lambda x: " ".join(x).lower())

print("Vectorizing Anime...")
cv_anime = CountVectorizer(max_features=5000, stop_words='english')
anime_vectors = cv_anime.fit_transform(new_anime['tags']).toarray()
print("Calculating Cosine Similarity...")
anime_similarity = cosine_similarity(anime_vectors)

print("Saving Anime Models...")
pickle.dump(new_anime.to_dict(), open('models/anime_dict.pkl', 'wb'))
pickle.dump(anime_similarity, open('models/anime_similarity.pkl', 'wb'))

print("\nSuccess! All models trained and saved to the 'models/' directory.")
