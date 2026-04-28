import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np # Added to handle joining the matrix parts

# 🔐 Replace with your API key
API_KEY = "YOUR_API_KEY"


# ✅ Fetch poster using movie NAME (fixes ID issue)
@st.cache_data
def fetch_poster(movie_name):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"

        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()

        if data['results']:
            poster_path = data['results'][0].get('poster_path')

            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path

        return "https://via.placeholder.com/500x750?text=No+Poster"

    except Exception as e:
        print("Error:", e)
        return "https://via.placeholder.com/500x750?text=Error"


# ✅ Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))  # 🔥 FIXED

    return recommended_movies, recommended_posters


# ✅ Load data (REPLACED SINGLE LOAD WITH SPLIT JOINING LOGIC)
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load the parts you split locally and concatenate them
similarity_part1 = pickle.load(open('similarity_part1.pkl', 'rb'))
similarity_part2 = pickle.load(open('similarity_part2.pkl', 'rb'))
similarity = np.concatenate([similarity_part1, similarity_part2], axis=0)

# 🎨 UI
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie:",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])