# -------------------- Imports --------------------
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------- Page Config --------------------
st.set_page_config(page_title="Movie Recommendation System (DSA)", layout="wide")

# -------------------- Load Dataset --------------------
DATA_PATH = r"G:\Documents\All Data 3 Semster\DSA project\tmdb_movies_with_watching_context.csv"
df = pd.read_csv(DATA_PATH)

df = df[['title', 'Watched_With_Whom', 'genre_list']]
df.dropna(inplace=True)

# -------------------- Clean Data --------------------
df['title'] = df['title'].str.strip()
df['Watched_With_Whom'] = df['Watched_With_Whom'].str.lower().str.strip()
df['genre_list'] = df['genre_list'].str.lower().apply(lambda x: [g.strip() for g in x.split(',')])

# -------------------- DSA: Movie Database --------------------
movie_db = []  # LIST of DICTIONARIES

for _, row in df.iterrows():
    movie_db.append({
        "title": row["title"],
        "genres": set(row["genre_list"]),  # SET
        "watch": row["Watched_With_Whom"]
    })

# -------------------- DSA: Inverted Index (HASH MAP) --------------------
genre_index = {}
watch_index = {}

for movie in movie_db:
    for genre in movie["genres"]:
        genre_index.setdefault(genre, []).append(movie)
    watch_index.setdefault(movie["watch"], []).append(movie)

# -------------------- Recommendation Algorithm (GREEDY) --------------------
def recommend_movies(selected_genres, selected_watch):
    scores = {}  # HASH MAP

    relevant_movies = watch_index.get(selected_watch, [])

    for movie in relevant_movies:
        match_score = len(movie["genres"].intersection(selected_genres))  # SET INTERSECTION
        if match_score > 0:
            scores[movie["title"]] = match_score

    # SORTING (DSA)
    ranked_movies = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_movies[:3]

# -------------------- Styling --------------------
st.markdown("""
<style>
.header-box {
    background-color: #2d2d2d;
    color: white;
    padding: 15px 20px;
    border-radius: 8px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box">🎬 Movie Recommendation System (DSA)</div>', unsafe_allow_html=True)

# -------------------- Navbar --------------------
selected = option_menu(
    menu_title=None,
    options=["Movie Recommendation", "Dataset Insights", "Algorithm Explanation"],
    icons=["film", "bar-chart", "cpu"],
    orientation="horizontal",
    styles={
        "container": {"background-color": "#1e1e1e"},
        "icon": {"color": "white"},
        "nav-link": {"color": "lightgray"},
        "nav-link-selected": {"background-color": "#6c5ce7", "color": "white"}
    }
)

# -------------------- Movie Recommendation --------------------
if selected == "Movie Recommendation":
    st.subheader("🔍 Select Watching Context & Genres")

    watched_options = sorted(df['Watched_With_Whom'].unique())
    genre_options = sorted(genre_index.keys())

    selected_watch = st.selectbox("Watching With:", watched_options)
    selected_genres = st.multiselect("Preferred Genres:", [g.title() for g in genre_options])

    if st.button("🎯 Recommend Movies"):
        if not selected_genres:
            st.warning("Please select at least one genre.")
        else:
            results = recommend_movies(
                set(g.lower() for g in selected_genres),
                selected_watch
            )

            if results:
                st.success("🔥 Top 3 Movie Recommendations")
                for i, (title, score) in enumerate(results, 1):
                    st.write(f"**{i}. {title}** — Match Score: {score}")
            else:
                st.info("No matching movies found.")

# -------------------- Dataset Insights --------------------
elif selected == "Dataset Insights":
    st.subheader("📊 Dataset Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Movies", len(movie_db))
    col2.metric("Unique Genres", len(genre_index))
    col3.metric("Watching Contexts", len(watch_index))

    genre_count = {g: len(movies) for g, movies in genre_index.items()}
    genre_df = pd.DataFrame(genre_count.items(), columns=["Genre", "Count"])

    fig = px.bar(genre_df, x="Count", y="Genre", orientation="h", height=500)
    st.plotly_chart(fig, use_container_width=True)

# -------------------- Algorithm Explanation --------------------
elif selected == "Algorithm Explanation":
    st.subheader("🧠 Data Structures & Algorithms Used")

    st.markdown("""
### 📌 Data Structures
- **List** → Store movie records  
- **Dictionary (Hash Map)** → Fast lookup for genres & contexts  
- **Set** → Efficient genre matching  

### 📌 Algorithms
- **Greedy Algorithm** → Maximize genre match score  
- **Linear Search** → Scan relevant movies  
- **Sorting Algorithm** → Rank movies by score  

### ⏱ Time Complexity
| Operation | Complexity |
|---------|-----------|
| Data Loading | O(n) |
| Genre Indexing | O(n × g) |
| Recommendation | O(n) |
| Sorting | O(n log n) |

### ✅ Why DSA over ML?
- Transparent logic  
- No black-box models  
- Faster for small/medium datasets  
- Easy to explain in viva
""")
