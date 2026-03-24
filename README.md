<div align="center">
  <h1>🍿 Nexus AI Recommendation Engine</h1>
  <p><strong>A high-performance, dual-domain Machine Learning Recommendation System for Movies and Anime.</strong></p>

  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
  [![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
  [![UI](https://img.shields.io/badge/Frontend-Vanilla_JS_+_Tailwind-38bdf8.svg)](https://tailwindcss.com/)
</div>

<br>

> **Nexus AI** is a personal passion project of mine built to explore the fascinating intersection of Natural Language Processing and seamless web development. It leverages advanced **Content-Based Filtering** to algorithmically match and recommend movies and anime based on user affinity. 

<br>

## 📋 Table of Contents
1. [📸 Visual Showcase](#-visual-showcase)
2. [✨ Key Features](#-key-features)
3. [🚀 Architecture](#-architecture)
4. [⚙️ Installation & Setup](#️-installation--setup)
5. [🧠 Machine Learning Approach](#-machine-learning-approach)

---

## 📸 Visual Showcase
<p align="center"><i>A highlight of the Premium UI, dynamic search, and cinematic hover overlays built entirely in Vanilla JS and Tailwind CSS.</i></p>

<div align="center">
  <img src="screenshots/Screenshot%202026-03-25%20002219.png" width="800" style="border-radius: 12px; box-shadow: 0px 4px 15px rgba(0,0,0,0.2); margin-bottom: 20px;">
  <img src="screenshots/Screenshot%202026-03-25%20002235.png" width="800" style="border-radius: 12px; box-shadow: 0px 4px 15px rgba(0,0,0,0.2); margin-bottom: 20px;">
  <img src="screenshots/Screenshot%202026-03-25%20002259.png" width="800" style="border-radius: 12px; box-shadow: 0px 4px 15px rgba(0,0,0,0.2); margin-bottom: 20px;">
  <img src="screenshots/Screenshot%202026-03-25%20001944.png" width="800" style="border-radius: 12px; box-shadow: 0px 4px 15px rgba(0,0,0,0.2); margin-bottom: 20px;">
  <img src="screenshots/Screenshot%202026-03-25%20001956.png" width="800" style="border-radius: 12px; box-shadow: 0px 4px 15px rgba(0,0,0,0.2); margin-bottom: 20px;">
</div>

---

## ✨ Key Features
- ⚡ **Lightning Fast Inference**: Reduces standard 6-second API cold-starts to **0.5s** using `ThreadPool` concurrency, with **0.00s** latency on cached recurrent searches via `@lru_cache`.
- 🧬 **Dual ML Domains**: Independent vector spaces for `TMDB 5000 Movies` and the `MyAnimeList` datasets.
- 🏷️ **Granular Metadata Scrapers**: Dynamically scrapes live runtime, studios, genres, and release dates via REST integration with TMDB and Jikan APIs.
- 🎨 **Premium UI/UX**: Netflix-inspired glassmorphic overlays, responsive fluid grids, and a highly polished Light/Dark mode mechanic.
- 🐍 **Streamlit Prototype**: A robust Python-only interactive variant created specifically for rapid data-science demonstrations.

---

## 🚀 Architecture

```text
📦 nexus-ai-recommendation
├── 📁 api/
│   └── 📄 main.py              # FastAPI server (Endpoints, Caching, Live Scrapers)
├── 📁 data/                    # Raw CSV Datasets
├── 📁 frontend/                
│   └── 📄 index.html           # High-Performance Vanilla JS + Tailwind SPA
├── 📁 models/                  # Pickled ML models (Similarity Matrices, Pandas Dictionaries)
├── 📁 src/
│   └── 📄 train.py             # NLP Feature Engineering & Vectorization logic
├── 📄 streamlit_app.py         # Python-only Interactive UI
├── 📄 Kaggle_Notebook.ipynb    # Jupyter Notebook export for Kaggle Portfolio
└── 📄 requirements.txt         # Dependencies
```

---

## ⚙️ Installation & Setup

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/nexus-ai-recommendation.git
cd nexus-ai-recommendation
pip install -r requirements.txt
```

### 2. Synthesize the Models
*(Note: Skip this step if the compiled `.pkl` files already exist within the `/models` directory.)*
```bash
python src/train.py
```
This script acts as the core engine pipeline: it parses the raw CSV datasets, standardizes the NLP entities, executes the `CountVectorizer`, computes the `Cosine Similarity` matrices, and serializes the state to disk.

### 3. Launch Application (FastAPI + HTML Engine)
```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000
```
*(Navigate to **`http://localhost:8000`** in your browser)*

### 4. Launch Streamlit Prototype
```bash
streamlit run streamlit_app.py
```
*(Navigate to **`http://localhost:8501`** in your browser)*

---

## 🧠 Machine Learning Approach
A **Content-Based Filtering** architecture was selected due to the sparsity of organic user-item collaborative data. The pipeline workflow consists of:
1. **Extraction & Standardization**: Messy, stringified JSON arrays (e.g. `cast`, `crew`, `genres`, `synopsis`) are mapped and stripped of spaces (`Johnny Depp` -> `JohnnyDepp`) so the tokenizer treats people/studios as continuous, uniquely bounded tokens.
2. **Dimensionality Reduction**: `CountVectorizer` embeds the tokens holding a strict `5000` multi-dimensional limit with English `stop_words` stripped out.
3. **Similarity Calculation**: Vectors are cast into a `cosine_similarity` model mapping angular distance, yielding an instantaneous neighbor-search index.

---

<p align="center"><i>If you found this project interesting, feel free to ⭐ the repository!</i></p>
