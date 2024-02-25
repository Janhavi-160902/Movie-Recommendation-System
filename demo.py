import pickle
import streamlit as st
import pandas as pd
import requests

def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_lists = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:8]

        recommended_movies = []
        recommended_posters = []

        for i in movies_lists:
            movie_id = i[0]
            recommended_movies.append(movies.iloc[movie_id].title)

            # Fetch movie poster from TMDb API
            poster_url = fetch_poster(movies.iloc[movie_id].movie_id)
            recommended_posters.append(poster_url)

        return recommended_movies, recommended_posters
    except Exception as e:
        st.error(f"Error: {e}")
        return [], []

def fetch_poster(movie_id):
    try:
        api_key = "3755295bad2cdfe8c3dd1a88e50349b6"  # Replace with your TMDb API key
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=3755295bad2cdfe8c3dd1a88e50349b6&language=en-US"
        response = requests.get(url)
        data = response.json()

        if 'poster_path' in data:
            poster_path = data['poster_path']
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return poster_url
        else:
            return None
    except Exception as e:
        st.warning(f"Error fetching poster: {e}")
        return None

# Load data and similarity matrix
movies_list = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('MOVIE RECOMMENDATION SYSTEM')
selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)

    for movie, poster in zip(recommendations, posters):
        st.write(movie)
        if poster:
            st.image(poster, caption=movie, use_column_width=True)
        else:
            st.write("Poster not available")
