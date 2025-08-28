import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load content-based model
with open("content_based_model.pkl", "rb") as f:
    model_data = pickle.load(f)

cosine_sim = model_data['cosine_sim']
movie_titles = model_data['movie_titles']
movie_indices = model_data['movie_indices']

# Function to get recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movie_indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    movie_indices_list = [i[0] for i in sim_scores]
    return movie_titles.iloc[movie_indices_list].tolist()

# Streamlit UI
st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")
st.title("🎥 Movie Recommendation System")
st.markdown("#### Select a movie to get similar recommendations")

# Dropdown to select a movie
selected_movie = st.selectbox("Choose a Movie", movie_titles.sort_values())

# Show Recommendations
if st.button("Recommend Similar Movies"):
    recommendations = get_recommendations(selected_movie)
    st.success("Top 5 similar movies:")
    for i, movie in enumerate(recommendations, start=1):
        st.markdown(f"**{i}. {movie}**")
