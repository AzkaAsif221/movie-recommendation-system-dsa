# 🎬 Movie Recommendation System (DSA Version)

This is a **Movie Recommendation System** redesigned from an AI-based project into a **pure Data Structures & Algorithms (DSA) project**.  
It recommends movies based on **watching context** and **preferred genres**, using Python and Streamlit for an interactive UI.

## 🚀 Features

- Top 3 movie recommendations based on:
  - Watching context (friends, family, solo)
  - Selected genres
- Interactive Streamlit UI
- Dataset insights with visualizations
- Fully DSA-driven logic (no ML)

## 🧠 Concepts Used (DSA)

- **Lists** → Store movie records
- **Dictionaries (Hash Maps)** → Fast lookup for genres & contexts
- **Sets** → Efficient genre matching (intersection)
- **Inverted Indexing** → Quick retrieval of relevant movies
- **Greedy Algorithm** → Score and rank movies
- **Sorting Algorithms** → Rank best matches
- **Linear Search & Time Complexity Analysis**

## 📂 Dataset

Dataset: `tmdb_movies_with_watching_context.csv`  
Contains columns:
- `title` → Movie title
- `Watched_With_Whom` → Context of watching (friends, family, etc.)
- `genre_list` → Comma-separated genres

---

## 🛠 Tech Stack

- Python
- Streamlit
- Pandas
- Plotly & Matplotlib
- Seaborn

---

## 💡 How to Run Locally
streamlit run app.py
