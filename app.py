import pickle
import gzip
import streamlit as st
import io
import gdown

# Function to fetch data from a local file or download it from a URL
def fetch_data(file_path, url=None):
    if url:
        gdown.download(url, file_path, quiet=False)
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except Exception as e:
        st.error(f"Failed to load data from file: {file_path}\nError: {e}")
        st.stop()

# Specify the file paths for movie data and similarity data
movie_data_path = 'movie_list.pkl'
similarity_data_url = 'https://drive.google.com/uc?id=1md2g6pH1V4s19t0oL_vwanLSqrpa4qMu'
similarity_data_path = 'similarity.pkl.gz'

# Load movie data
movie_data = fetch_data(movie_data_path)
if movie_data:
    try:
        movies = pickle.loads(movie_data)
    except Exception as e:
        st.error(f"Failed to load movie data from file: {movie_data_path}\nError: {e}")
        st.stop()

# Load compressed similarity data
similarity_data = fetch_data(similarity_data_path, similarity_data_url)
if similarity_data:
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(similarity_data), mode='rb') as f:
            similarity = pickle.load(f)
    except Exception as e:
        st.error(f"Failed to load compressed similarity data from file: {similarity_data_path}\nError: {e}")
        st.stop()

# The rest of your code remains unchanged

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
