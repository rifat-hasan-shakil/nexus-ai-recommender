from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pickle
import pandas as pd
import requests
import concurrent.futures
from functools import lru_cache

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

movies_dict = pickle.load(open('models/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
movie_similarity = pickle.load(open('models/movie_similarity.pkl', 'rb'))

anime_dict = pickle.load(open('models/anime_dict.pkl', 'rb'))
anime = pd.DataFrame(anime_dict)
anime_similarity = pickle.load(open('models/anime_similarity.pkl', 'rb'))

@lru_cache(maxsize=2000)
def fetch_movie_details(movie_id):
    link = f"https://www.themoviedb.org/movie/{movie_id}"
    poster = "https://via.placeholder.com/500x750?text=No+Poster"
    overview = "No description available."
    rating = "N/A"
    year = "N/A"
    category = "N/A"
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            poster = "https://image.tmdb.org/t/p/w500/" + poster_path
        imdb_id = data.get('imdb_id')
        if imdb_id: link = f"https://www.imdb.com/title/{imdb_id}/"
        overview = data.get('overview', "No description available.")
        if len(overview) > 400: overview = overview[:400] + "..."
        score = data.get('vote_average')
        if score: rating = f"{round(score, 1)}"
        
        release_date = data.get('release_date')
        if release_date: year = release_date.split('-')[0]
        
        genres = data.get('genres', [])
        if genres: category = ", ".join([g['name'] for g in genres[:2]])
    except:
        pass
    return poster, link, overview, rating, year, category

@lru_cache(maxsize=2000)
def fetch_anime_details(anime_id):
    link = f"https://myanimelist.net/anime/{anime_id}"
    poster = "https://via.placeholder.com/500x750?text=No+Poster"
    synopsis = "No synopsis available."
    rating = "N/A"
    year = "N/A"
    category = "N/A"
    run_time = "N/A"
    studios = "N/A"
    try:
        url = f"https://api.jikan.moe/v4/anime/{anime_id}"
        data = requests.get(url).json()
        item = data.get('data', {})
        images = item.get('images', {}).get('jpg', {})
        if 'large_image_url' in images: poster = images['large_image_url']
        synopsis = item.get('synopsis', "No synopsis available.")
        if len(synopsis) > 400: synopsis = synopsis[:400] + "..."
        score = item.get('score')
        if score: rating = f"{score}"
        
        aired = item.get('aired', {}).get('prop', {}).get('from', {})
        if aired and aired.get('year'): year = str(aired.get('year'))
        
        genres = item.get('genres', [])
        if genres: category = ", ".join([g['name'] for g in genres[:2]])
            
        dur = item.get('duration')
        if dur: run_time = dur.replace(' per ep', '').replace(' hr', 'h').replace(' min', 'm').strip()
        
        st_list = item.get('studios', [])
        if st_list: studios = st_list[0].get('name', 'N/A')
    except:
        pass
    return poster, link, synopsis, rating, year, category, run_time, studios

@app.get("/api/movies")
def get_movies():
    return {"movies": movies['title'].tolist()}

@app.get("/api/anime")
def get_anime():
    return {"anime": anime['title'].tolist()}

class RecommendRequest(BaseModel):
    title: str

@app.post("/api/recommend/movies")
def recommend_movies(req: RecommendRequest):
    movie_index = movies[movies['title'] == req.title].index[0]
    distances = movie_similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    def get_movie(i):
        movie_id = int(movies.iloc[i[0]].movie_id)
        title = movies.iloc[i[0]].title
        poster, link, overview, rating, year, category = fetch_movie_details(movie_id)
        return {"title": title, "poster": poster, "link": link, "overview": overview, "rating": rating, "year": year, "category": category}

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(get_movie, movies_list))
        
    return {"recommendations": results}

@app.post("/api/recommend/anime")
def recommend_anime_api(req: RecommendRequest):
    anime_index = anime[anime['title'] == req.title].index[0]
    distances = anime_similarity[anime_index]
    anime_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    def get_anime(i):
        anime_id = int(anime.iloc[i[0]].anime_id)
        title = anime.iloc[i[0]].title
        poster, link, synopsis, rating, year, category, run_time, studios = fetch_anime_details(anime_id)
        return {"title": title, "poster": poster, "link": link, "overview": synopsis, "rating": rating, "year": year, "category": category, "run_time": run_time, "studios": studios}
        
    results = [get_anime(i) for i in anime_list]
    return {"recommendations": results}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
