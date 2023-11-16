import pickle
import streamlit as st
import gdown

# Function to fetch data from a URL
def fetch_data_from_url(url):
    response = gdown.download(url, output='./data.pkl', quiet=False)
    if response:
        return response
    else:
        st.error(f"Failed to load data from URL: {url}")
        return None

# Specify the URLs for movie data and similarity data
movie_data_url = 'movie_list.pkl'
similarity_data_url = 'https://drive.google.com/uc?id=18IVlSYFX5CywLXfJP1gp-AtN_GPSsgZN'

# Download movie data
movie_data = fetch_data_from_url(movie_data_url)
if movie_data:
    movies = pickle.load(open('./data.pkl', 'rb'))

# Download similarity data
similarity_data = fetch_data_from_url(similarity_data_url)
if similarity_data:
    similarity = pickle.load(open('./data.pkl', 'rb'))

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

# Run the Streamlit app
if __name__ == '__main__':
    main()
