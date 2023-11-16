import pickle
import gzip
import streamlit as st
import requests
import io

# Function to fetch data from a URL
def fetch_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Failed to load data from URL: {url}")
        return None

# Specify the URLs for movie data and similarity data
movie_data_url = 'movie_list.pkl'
similarity_data_url = 'similarity.pkl.gz'

# Load movie data
movie_data = fetch_data_from_url(movie_data_url)
if movie_data:
    try:
        movies = pickle.loads(movie_data)
    except Exception as e:
        st.error(f"Failed to load movie data from URL: {movie_data_url}\nError: {e}")
        st.stop()

# Load compressed similarity data from another repository
similarity_data = fetch_data_from_url(similarity_data_url)
if similarity_data:
    try:
        with gzip.decompress(similarity_data) as f:
            similarity = pickle.load(f)
    except Exception as e:
        st.error(f"Failed to load compressed similarity data from URL: {similarity_data_url}\nError: {e}")
        st.stop()

# Function to recommend movies based on similarity
def recommend(selected_movie):
    selected_movie_index = movies[movies['title'] == selected_movie].index

    if not selected_movie_index.empty:
        index = selected_movie_index[0]

        # Get similarity scores for the selected movie
        try:
            movie_similarity_scores = similarity[index]
        except IndexError:
            st.error(f"IndexError: Index {index} is out of bounds for the 'similarity' array.")
            return None

        # Sort movies based on similarity scores
        distances = sorted(list(enumerate(movie_similarity_scores)), reverse=True, key=lambda x: x[1])

        # Get top 5 recommendations (excluding the selected movie itself)
        top_recommendations = []
        for i in range(1, min(6, len(distances))):  # Start from 1 to exclude the selected movie
            try:
                recommended_index = distances[i][0]
                recommended_movie_name = movies.iloc[recommended_index]['title']
                recommended_movie_poster = movies.iloc[recommended_index]['poster_path']
                top_recommendations.append((recommended_movie_name, recommended_movie_poster))
            except IndexError:
                st.error(f"IndexError: Index {recommended_index} is out of bounds for the 'movies' array.")
                return None

        return top_recommendations
    else:
        st.error(f"Selected movie '{selected_movie}' not found.")
        return None

# Define the Streamlit app
def main():
    st.header('Movie Recommender System')
    movie_list = movies['title'].values
    selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

    if st.button('Show Recommendation'):
        recommended_movies = recommend(selected_movie)

        if recommended_movies:
            for recommended_movie_name, recommended_movie_poster in recommended_movies:
                st.text(recommended_movie_name)
                st.image(recommended_movie_poster)

# Run the Streamlit app
if __name__ == '__main__':
    main()
