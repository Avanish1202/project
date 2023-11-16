import pickle
import streamlit as st
import gzip
import io

# Function to fetch data from a local file
def fetch_data_from_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except Exception as e:
        st.error(f"Failed to load data from file: {file_path}\nError: {e}")
        return None

# Specify the file paths for movie data and similarity data
movie_data_path = 'movie_list.pkl'
similarity_data_path = 'similarity.pkl.gz'

# Load movie data
movie_data = fetch_data_from_file(movie_data_path)
if movie_data:
    try:
        movies = pickle.loads(movie_data)
    except Exception as e:
        st.error(f"Failed to load movie data from file: {movie_data_path}\nError: {e}")
        movies = None

# Load similarity data
similarity_data = fetch_data_from_file(similarity_data_path)
if similarity_data:
    try:
        # Use gzip to decompress the data before loading with pickle
        similarity = pickle.loads(gzip.decompress(similarity_data))
    except Exception as e:
        st.error(f"Failed to load similarity data from file: {similarity_data_path}\nError: {e}")
        similarity = None
# Function to recommend movies based on similarity
def recommend(selected_movie):
    selected_movie_index = movies[movies['title'] == selected_movie].index

    if not selected_movie_index.empty:
        index = selected_movie_index[0]

        # Log lengths of 'movies' and 'similarity' arrays
        st.write(f"Length of 'movies' array: {len(movies)}")
        st.write(f"Length of 'similarity' array: {len(similarity)}")

        # Check if the index is within bounds for both movies and similarity arrays
        if 0 <= index < len(movies) and 0 <= index < len(similarity):
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
            st.error(f"IndexError: Index {index} is out of bounds for either the 'movies' or 'similarity' array.")
            st.stop()
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
