import pickle
import streamlit as st
import requests
import io
from google_drive_downloader import GoogleDriveDownloader as gdd

# Function to fetch data from a URL
def fetch_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Failed to load data from URL: {url}")
        return None

# Specify the URLs for movie data and similarity data
movie_data_url = 'https://raw.githubusercontent.com/your_username/your_repository/main/movie_list.pkl'
similarity_data_google_drive_id = '1md2g6pH1V4s19t0oL_vwanLSqrpa4qMu'

# Download similarity data from Google Drive
gdd.download_file_from_google_drive(file_id=similarity_data_google_drive_id, dest_path='./similarity.pkl')

# Load movie data
movie_data = fetch_data_from_url(movie_data_url)
if movie_data:
    movies = pickle.load(io.BytesIO(movie_data))

# Load similarity data
similarity_data_path = './similarity.pkl'
similarity_data = fetch_data_from_url(similarity_data_path)
if similarity_data:
    similarity = pickle.load(io.BytesIO(similarity_data))

# Function to recommend movies based on similarity
def recommend(selected_movie):
    # Implement the recommendation logic here
    # ...

# Define the Streamlit app
def main():
    try:
        st.header('Movie Recommender System')
        movie_list = movies['title'].values
        selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

        if st.button('Show Recommendation'):
            recommended_movies = recommend(selected_movie)

            if recommended_movies:
                for recommended_movie_name, recommended_movie_poster in recommended_movies:
                    st.text(recommended_movie_name)
                    st.image(recommended_movie_poster)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        raise e  # This will print the full traceback in the Streamlit app logs

# Run the Streamlit app
if __name__ == '__main__':
    main()
