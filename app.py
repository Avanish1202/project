import pickle
import streamlit as st
import requests
import io

# Function to fetch data from a local file or URL
def fetch_data(file_path):
    try:
        if file_path.startswith("http"):
            response = requests.get(file_path)
            response.raise_for_status()
            return io.BytesIO(response.content).read()
        else:
            with open(file_path, 'rb') as file:
                return file.read()
    except Exception as e:
        st.error(f"Failed to load data from: {file_path}\nError: {e}")
        return None

# Specify the file path or URL for movie data and similarity data
movie_data_path = 'movie_list.pkl'
similarity_data_path = 'https://www.dropbox.com/scl/fi/vs3b5hk78j10wvnecduwx/similarity.pkl?rlkey=7g1j2iuuvdwtl37ohyu8jnthx&dl=0'

# Load movie data
movie_data = fetch_data(movie_data_path)
if movie_data:
    try:
        movies = pickle.loads(movie_data)
    except Exception as e:
        st.error(f"Failed to load movie data from: {movie_data_path}\nError: {e}")
        st.stop()

# Load similarity data
similarity_data = fetch_data(similarity_data_path)
if similarity_data:
    try:
        similarity = pickle.loads(similarity_data)
    except Exception as e:
        st.error(f"Failed to load similarity data from: {similarity_data_path}\nError: {e}")
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
            st.stop()

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
                st.stop()

        return top_recommendations
    else:
        st.error(f"Selected movie '{selected_movie}' not found.")
        st.stop()

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
