import pickle
import streamlit as st
import requests


# Function to fetch the movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(selected_movie):
    # Get the index of the selected movie
    selected_movie_index = movies[movies['title'] == selected_movie].index

    if not selected_movie_index.empty:
        index = selected_movie_index[0]

        # Get similarity scores for the selected movie
        movie_similarity_scores = similarity[index]

        # Sort movies based on similarity scores
        distances = sorted(enumerate(movie_similarity_scores), reverse=True, key=lambda x: x[1])

        # Get top 5 recommendations (excluding the selected movie itself)
        top_recommendations = []
        for i in range(1, 6):  # Start from 1 to exclude the selected movie
            recommended_index = distances[i][0]
            recommended_movie_name = movies.iloc[recommended_index]['title']
            recommended_movie_poster = movies.iloc[recommended_index]['poster_path']
            top_recommendations.append((recommended_movie_name, recommended_movie_poster))

        return top_recommendations
    else:
        st.error(f"Selected movie '{selected_movie}' not found.")
        return None



st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Create columns
    col1, col2, col3, col4, col5 = st.columns(5)

    # Add content to columns
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
