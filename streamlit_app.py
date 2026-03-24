import streamlit as st
import pickle
import pandas as pd
import requests

# Set Page Config
st.set_page_config(page_title="AI Recommender Base", page_icon="🍿", layout="wide")

import concurrent.futures

# Deeply Premium CSS
st.markdown("""
<style>
    /* Global Component Styling */
    .stApp {
        background-color: #0b0c10;
        color: #f8f8f8;
    }
    
    /* Styling the select boxes and buttons */
    .stSelectbox label {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #f8f8f8 !important;
        margin-bottom: 10px !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #e50914, #b20710) !important;
        color: white !important;
        border-radius: 12px !important;
        height: 60px !important;
        font-weight: 900 !important;
        font-size: 20px !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(229, 9, 20, 0.3) !important;
        transition: all 0.3s ease !important;
        margin-top: 10px !important;
    }
    .stButton>button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 15px 30px rgba(229, 9, 20, 0.5) !important;
    }

    /* Custom CSS Card Overlay */
    .nexus-card {
        position: relative;
        cursor: pointer;
        border-radius: 1rem;
        overflow: hidden;
        aspect-ratio: 2/3;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: transform 0.4s ease;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .nexus-card:hover {
        transform: scale(1.05) translateY(-5px);
        z-index: 50;
        box-shadow: 0 20px 40px rgba(229,9,20,0.3);
    }
    .nexus-poster {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.7s ease;
    }
    .nexus-card:hover .nexus-poster {
        transform: scale(1.1);
    }
    .nexus-overlay {
        position: absolute;
        inset: 0;
        background: rgba(0,0,0,0.85);
        opacity: 0;
        transition: opacity 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 15px;
        backdrop-filter: blur(4px);
    }
    .nexus-card:hover .nexus-overlay {
        opacity: 1;
    }
    .nexus-title {
        color: white;
        font-weight: 900;
        font-size: 1.1rem;
        margin-bottom: 10px;
        line-height: 1.2;
    }
    .nexus-badge {
        background: rgba(234,179,8,0.2);
        color: #fbbf24;
        border: 1px solid rgba(234,179,8,0.5);
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 800;
        font-size: 0.7rem;
        display: inline-block;
        margin-bottom: 10px;
    }
    .nexus-link {
        background: rgba(229,9,20,0.2);
        color: #e50914;
        border: 1px solid rgba(229,9,20,0.5);
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 800;
        font-size: 0.7rem;
        text-decoration: none;
        display: inline-block;
        margin-left: 5px;
    }
    .nexus-link:hover {
        background: #e50914;
        color: white;
    }
    .nexus-synopsis {
        color: #d1d5db;
        font-size: 0.75rem;
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 6;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .nexus-footer-title {
        text-align: center;
        margin-top: 10px;
        font-weight: 800;
        font-size: 0.9rem;
        line-height: 1.2;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        color: white;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

# Free TMDB API Key for tutorial use
TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

@st.cache_resource(show_spinner="Loading machine learning models...")
def load_movie_data():
    movies_dict = pickle.load(open('models/movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    movie_similarity = pickle.load(open('models/movie_similarity.pkl', 'rb'))
    return movies, movie_similarity

@st.cache_resource(show_spinner="Loading machine learning models...")
def load_anime_data():
    anime_dict = pickle.load(open('models/anime_dict.pkl', 'rb'))
    anime = pd.DataFrame(anime_dict)
    anime_similarity = pickle.load(open('models/anime_similarity.pkl', 'rb'))
    return anime, anime_similarity

@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id):
    link = f"https://www.themoviedb.org/movie/{movie_id}"
    poster = "https://via.placeholder.com/500x750?text=No+Poster"
    overview = "No description available."
    rating = "N/A"
    year = "N/A"
    genres = "N/A"
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        data = requests.get(url).json()
        
        poster_path = data.get('poster_path')
        if poster_path:
            poster = "https://image.tmdb.org/t/p/w500/" + poster_path
            
        imdb_id = data.get('imdb_id')
        if imdb_id:
            link = f"https://www.imdb.com/title/{imdb_id}/"
            
        overview = data.get('overview', "No description available.")
        if len(overview) > 350:
            overview = overview[:350] + "..."
            
        score = data.get('vote_average')
        if score:
            rating = f"{round(score, 1)}"
            
        release_date = data.get('release_date')
        if release_date:
            year = release_date.split('-')[0]
            
        gen_list = data.get('genres', [])
        if gen_list:
            genres = ", ".join([g['name'] for g in gen_list[:3]])
    except:
        pass
    return poster, link, overview, rating, year, genres

@st.cache_data(show_spinner=False)
def fetch_anime_details(anime_id):
    link = f"https://myanimelist.net/anime/{anime_id}"
    poster = "https://via.placeholder.com/500x750?text=No+Poster"
    synopsis = "No synopsis available."
    rating = "N/A"
    year = "N/A"
    genres = "N/A"
    try:
        url = f"https://api.jikan.moe/v4/anime/{anime_id}"
        data = requests.get(url).json()
        item = data.get('data', {})
        
        images = item.get('images', {}).get('jpg', {})
        if 'large_image_url' in images:
            poster = images['large_image_url']
            
        synopsis = item.get('synopsis', "No synopsis available.")
        if len(synopsis) > 350:
            synopsis = synopsis[:350] + "..."
            
        score = item.get('score')
        if score:
            rating = f"{score}"
            
        aired = item.get('aired', {}).get('prop', {}).get('from', {})
        if aired and aired.get('year'):
            year = str(aired.get('year'))
            
        gen_list = item.get('genres', [])
        if gen_list:
            genres = ", ".join([g['name'] for g in gen_list[:3]])
    except:
        pass
    return poster, link, synopsis, rating, year, genres

def render_card(title, poster, link, overview, rating, year, genres):
    return f"""
    <div>
        <div class="nexus-card">
            <img src="{poster}" class="nexus-poster">
            <div class="nexus-overlay">
                <div>
                    <span class="nexus-badge">⭐ {rating}</span>
                    <a href="{link}" target="_blank" class="nexus-link">SOURCE ➔</a>
                </div>
                <div style="color: #9ca3af; font-size: 0.6rem; font-weight: 900; text-transform: uppercase; margin-bottom: 5px; border-bottom: 1px solid #374151; padding-bottom: 2px;">Synopsis</div>
                <p class="nexus-synopsis">{overview}</p>
            </div>
        </div>
        <div class="nexus-footer-title" title="{title.replace('"', '&quot;')}">{title}</div>
    </div>
    """

def recommend_movie(movie, movies, movie_similarity):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = movie_similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6] # Strict 5 items
    
    def get_html(i):
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster, link, overview, rating, year, genres = fetch_movie_details(movie_id)
        return render_card(title, poster, link, overview, rating, year, genres)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        html_cards = list(executor.map(get_html, movies_list))
        
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(html_cards[idx], unsafe_allow_html=True)

def recommend_anime(anime_title, anime, anime_similarity):
    anime_index = anime[anime['title'] == anime_title].index[0]
    distances = anime_similarity[anime_index]
    anime_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6] # Strict 5 items
    
    def get_html(i):
        anime_id = anime.iloc[i[0]].anime_id
        title = anime.iloc[i[0]].title
        poster, link, synopsis, rating, year, genres = fetch_anime_details(anime_id)
        return render_card(title, poster, link, synopsis, rating, year, genres)

    html_cards = [get_html(i) for i in anime_list]
        
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(html_cards[idx], unsafe_allow_html=True)


# ----------------- UI LAYOUT -----------------
st.markdown("<h1 style='text-align: center; font-weight: 900; font-size: 3.5rem; color: #fff; text-shadow: 0 4px 20px rgba(0,0,0,0.5);'>Nexus <span style='color: #e50914;'>AI</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0a0b0; font-weight: 300; font-size: 1.3rem; margin-bottom: 40px;'>Select a title. Discover a universe.</p>", unsafe_allow_html=True)

mode = st.sidebar.radio("CHOOSE DOMAIN", ("Movies", "Anime"))
st.sidebar.markdown("---")
st.sidebar.write("Built as a Machine Learning Portfolio showcasing Content-Based Filtering & APIs.")

if mode == "Movies":
    movies, movie_similarity = load_movie_data()
    selected_movie_name = st.selectbox("Search for a movie you love:", movies['title'].values)
    
    if st.button('Generate Recommendations', use_container_width=True):
        st.markdown("<hr>", unsafe_allow_html=True)
        with st.spinner('Calculating NLP vector distances...'):
            recommend_movie(selected_movie_name, movies, movie_similarity)

elif mode == "Anime":
    anime, anime_similarity = load_anime_data()
    selected_anime_name = st.selectbox("Search for an anime you love:", anime['title'].values)
    
    if st.button('Generate Recommendations', use_container_width=True):
        st.markdown("<hr>", unsafe_allow_html=True)
        with st.spinner('Calculating NLP vector distances...'):
            recommend_anime(selected_anime_name, anime, anime_similarity)
