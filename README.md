<div align="center">
  <img src="https://via.placeholder.com/800x200/0b0c10/e50914?text=Nexus+AI:+Recommendation+Engine" alt="Nexus AI Banner">
  
  <h1>🍿 Nexus AI Recommendation Engine</h1>
  <p><strong>A high-performance, dual-domain Machine Learning Recommendation System for Movies and Anime.</strong></p>

  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
  [![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
  [![UI](https://img.shields.io/badge/Frontend-Vanilla_JS_+_Tailwind-38bdf8.svg)](https://tailwindcss.com/)
</div>

---

## 📖 Overview
**Nexus AI** is a personal passion project of mine built to explore the fascinating intersection of Natural Language Processing and seamless web development. It is a portfolio-grade machine learning application that uses **Content-Based Filtering** (`CountVectorizer` and `Cosine Similarity`) to recommend movies and anime based on a user's favorite titles. 

Unlike basic prototypes, Nexus AI features a deeply optimized **FastAPI Backend**, an asynchronous in-memory caching system (`@lru_cache` + `ThreadPoolExecutor`), and two distinct frontends:
1. **Premium Web Application**: A flawless Vanilla JS Single Page Application (SPA) styled with Tailwind CSS, featuring glassmorphism, native search autocompletion, hover overlays, and dynamic Light/Dark mode.
2. **Streamlit App**: A sleek Python-based frontend that perfectly mimics the premium web app for rapid data-science demonstrations.

## 📸 Screenshots
Here is a highlight of the Premium UI, dynamic search, and cinematic hover overlays built entirely in Vanilla JS and Tailwind CSS!

<div align="center">
  <img src="screenshots/Screenshot%202026-03-25%20002219.png" width="800" style="border-radius: 10px; margin-bottom: 10px;">
  <img src="screenshots/Screenshot%202026-03-25%20002235.png" width="800" style="border-radius: 10px; margin-bottom: 10px;">
  <img src="screenshots/Screenshot%202026-03-25%20002259.png" width="800" style="border-radius: 10px; margin-bottom: 10px;">
  <img src="screenshots/Screenshot%202026-03-25%20001944.png" width="800" style="border-radius: 10px; margin-bottom: 10px;">
  <img src="screenshots/Screenshot%202026-03-25%20001956.png" width="800" style="border-radius: 10px; margin-bottom: 10px;">
</div>

---

## ✨ Key Features
- **Dual ML Domains**: Independent vector spaces for `TMDB 5000 Movies` and `MyAnimeList` datasets.
- **Lightning Fast Inference**: Reduces 6-second API cold-starts to `0.5s` using ThreadPool concurrency, and `0.00s` for cached searches.
- **Micro-Badges & Granular Metadata**: Dynamically scrapes live runtime, studios, genres, and release years via TMDB and Jikan APIs.
- **Cinematic UI**: Netflix-style hover-cards with glassmorphic overlays.

---

## 🚀 Architecture
```text
├── api/
│   └── main.py              # FastAPI server (Endpoints, Caching, Live TMDB/Jikan API Scraping)
├── data/                    # Raw CSV Datasets
├── frontend/                
│   └── index.html           # High-Performance Vanilla JS + Tailwind SPA
├── models/                  # Pickled ML models (Similarity Matrices, Pandas Dictionaries)
├── src/
│   └── train.py             # NLP Feature Engineering & Vectorization logic
├── streamlit_app.py         # Python-only Interactive UI
├── Kaggle_Notebook.ipynb    # Jupyter Notebook for Kaggle Portfolio
└── requirements.txt         # Dependencies
```

---

## ⚙️ Installation & Setup

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/nexus-ai-recommendation.git
cd nexus-ai-recommendation
pip install -r requirements.txt
```

### 2. Train the Models
*(Note: If the `models/` directory already contains the `.pkl` files, you can skip this step.)*
```bash
python src/train.py
```
This script will parse the raw CSV data, run the `CountVectorizer`, compute the `Cosine Similarity` matrix, and pickle the resulting structures to your hard drive.

### 3. Run the Backend (FastAPI + HTML Frontend)
To launch the core engine and the premium web application:
```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000
```
Open **`http://localhost:8000`** in your browser.

### 4. Run the Streamlit Prototype
To run the pure-Python UI variant:
```bash
streamlit run streamlit_app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 🧠 Machine Learning Approach
We adopted a **Content-Based Filtering** architecture because user-item collaborative filtering data was sparse.
1. **Feature Engineering**: We extracted strings from JSON arrays (e.g. `cast`, `crew`, `genres`, `synopsis`).
2. **Tag Generation**: Spaces were stripped from entity names (e.g., `Johnny Depp` -> `JohnnyDepp`) so that the NLP vectorizer treats specific people / studios as unique continuous tokens.
3. **Vectorization**: `sklearn.feature_extraction.text.CountVectorizer` was used with a strict 5000 max-features limit and English stop-words removed.
4. **Distance Calculation**: The `cosine_similarity` algorithm mapped the angular distances between the 5000-dimensional vectors, allowing the backend to immediately slice the top 5 nearest neighbors.

---

## 🤝 Contributing
Feel free to open issues or fork the repository to add Hybrid-Recommendation models or enhance the UI!
