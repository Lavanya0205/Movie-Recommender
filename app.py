import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# ===============================
# Load model
# ===============================
with open("content_based_model.pkl", "rb") as f:
    model_data = pickle.load(f)

cosine_sim = model_data['cosine_sim']
movie_titles = model_data['movie_titles']
movie_indices = model_data['movie_indices']
movie_posters = model_data.get('movie_posters', None)  # Optional poster URLs

# ===============================
# Function to get recommendations
# ===============================
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movie_indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    movie_indices_list = [i[0] for i in sim_scores]
    return movie_titles.iloc[movie_indices_list].tolist()

# ===============================
# Streamlit Config
# ===============================
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide", page_icon="🎥")

# ===============================
# Header
# ===============================
st.markdown(
    """
    <h1 style='text-align: center; color: #FF4B4B; font-size: 40px;'>🎬 Movie Recommendation System</h1>
    <p style='text-align: center; font-size: 18px; color: #555;'>Find top 5 movies similar to your favorite one!</p>
    """, unsafe_allow_html=True)
st.divider()

# ===============================
# Sidebar for movie selection
# ===============================
st.sidebar.header("🎯 Choose a Movie")
selected_movie = st.sidebar.selectbox(
    "Scroll or type to select a movie:",
    movie_titles.sort_values(),
    index=0
)

# ===============================
# Button to get recommendations
# ===============================
if st.button("🍿 Recommend Similar Movies"):
    recommendations = get_recommendations(selected_movie)
    st.success(f"Top 5 movies similar to **{selected_movie}**:")

    # Horizontal scrollable cards
    scroll_cols = st.columns(len(recommendations))
    for i, movie in enumerate(recommendations):
        with scroll_cols[i]:
            if movie_posters and movie in movie_posters:
                st.image(movie_posters[movie], use_column_width=True)
            st.markdown(f"**{movie}**")
            st.caption(f"Rank #{i+1}")
else:
    st.info("ℹ️ Select a movie from the sidebar and click 'Recommend Similar Movies'.")

# ===============================
# Footer
# ===============================
st.divider()

