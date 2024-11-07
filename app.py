import pickle
import streamlit as st
import requests
import pandas as pd


# - This function takes a movie_id as input.
# - It sends an HTTP request to The Movie Database (TMDb) API to fetch movie details using the Provided API key.  
# - Returns the full URL to the poster image.

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# - This function takes a movie title as input.
# - Finds the index of the selected movie in the movies DataFrame.
# - Uses a similarity matrix to find the top 5 similar movies based on similarity scores.
# - For each recommended movie, it:
#    - Fetches the movie_id to get the poster image.
#    - Adds the movie's title and poster URL to separate lists.
# - Returns the lists of recommended movie names and poster URLs.

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].show_id
        # recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    # return recommended_movie_names,recommended_movie_posters
    return recommended_movie_names


# Title
st.header('Movie Recommender System Using Machine Learning')
# load {Movie List] as well as [Vec]
movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))

# fetch all title to show as [Selectbox]
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# OnCLick
# - When the button is clicked, the recommend function is called with the selected movie.
# - The returned movie titles and poster URLs are displayed in five columns (st.columns(5)) for visual alignment.
# - Each column shows a movie title and its corresponding poster image (st.text and st.image).

if st.button('Show Recommendation'):
    # recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    recommended_movie_names = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        # st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        # st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        # st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        # st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        # st.image(recommended_movie_posters[4])