import pandas as pd
import streamlit as st
import pickle
import requests

# Constants
TOP_K = 10

# Load predictions and model
df = pd.read_csv(r'D:\Downloads\Downloads\ml-latest-small (1)\ml-latest-small\tags.csv')
# df = pd.read_csv('data.csv')
all_predictions = pickle.load(open(r'D:\Downloads\Downloads\all_prediction.Sav', 'rb'))
API_KEY_AUTH = "b8c96e534866701532768a313b978c8b"

# Function to fetch movie title based on movie_id
def fetch_movie_title(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY_AUTH}')
        if response.status_code == 200:
            data = response.json()
            title = data.get('title', 'Unknown Title')
            return title
        else:
            return None  # Return None if status code is not 200
    except:
        return None  # Return None if any exception occurs

# Function to fetch movie poster URL based on movie_id
def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY_AUTH}')
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                full_path = 'https://image.tmdb.org/t/p/w500/' + poster_path
                return full_path
            else:
                return "https://via.placeholder.com/500x750?text=No+Image+Available"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image+Available"
    except:
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Image"

# Function to fetch recommendations for a user
def get_recommendations(user_id, top_k=TOP_K):
    user_predictions = all_predictions[all_predictions['userId'] == user_id]
    user_predictions = user_predictions.sort_values(by='prediction', ascending=False).head(top_k)
    return user_predictions[['movieId', 'prediction']]

# Streamlit app configuration
st.set_page_config(layout="wide", page_title="Movie Recommendation System by User ID", page_icon="🎬")

# Custom CSS for dark theme
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
body {
    background-color: #000000;
    color: white;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Hide Streamlit menu and header
hide_decoration_bar_style = '''
<style>
header {visibility: hidden;}
</style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

# Main application code
st.title('Movie Recommendation System By User ID')

user_id = st.number_input('Enter User ID', min_value=1, step=1)

if st.button('Recommend'):
    recommended_movies = get_recommendations(user_id)
    
    st.write(f"Top {TOP_K} recommendations for user {user_id}:")
    
    num_cols = 5  # Number of columns in the grid layout
    num_movies = len(recommended_movies)
    num_rows = (num_movies // num_cols) + (1 if num_movies % num_cols > 0 else 0)

    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            index = row * num_cols + col
            if index < num_movies:
                movie_id = recommended_movies.iloc[index]['movieId']
                prediction_score = recommended_movies.iloc[index]['prediction']
                movie_title = fetch_movie_title(movie_id)  # Fetch movie title here
                poster_url = fetch_poster(movie_id)  # Fetch movie poster URL here

                with cols[col]:
                    if movie_title:
                        st.write(movie_title)  # Display movie title above the poster
                    st.image(poster_url, width=150)
                    st.write(f"Prediction Score: {prediction_score:.4f}")








# import pandas as pd
# import streamlit as st
# import pickle
# import requests

# # Constants
# TOP_K = 10

# # Load predictions and model
# all_predictions = pickle.load(open(r'D:\Downloads\Downloads\all_prediction.Sav', 'rb'))
# API_KEY_AUTH = "b8c96e534866701532768a313b978c8b"

# # Function to fetch movie title based on movie_id
# def fetch_movie_title(movie_id):
#     try:
#         response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY_AUTH}')
#         if response.status_code == 200:
#             data = response.json()
#             title = data.get('title', 'Unknown Title')
#             return title
#         else:
#             return None  # Return None if status code is not 200
#     except:
#         return None  # Return None if any exception occurs

# # Function to fetch movie poster URL based on movie_id
# def fetch_poster(movie_id):
#     try:
#         response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY_AUTH}')
#         if response.status_code == 200:
#             data = response.json()
#             poster_path = data.get('poster_path')
#             if poster_path:
#                 full_path = 'https://image.tmdb.org/t/p/w500/' + poster_path
#                 return full_path
#             else:
#                 return None  # Return None if no poster path is available
#         else:
#             return None  # Return None if status code is not 200
#     except:
#         return None  # Return None if any exception occurs

# Function to fetch recommendations for a user
# def get_recommendations(user_id, top_k=TOP_K):
#     user_predictions = all_predictions[all_predictions['userId'] == user_id]
#     user_predictions = user_predictions.sort_values(by='prediction', ascending=False).head(top_k)
#     return user_predictions[['movieId', 'prediction']]

# # Streamlit app configuration
# st.set_page_config(layout="wide", page_title="Movie Recommendation System", page_icon="🎬")

# # Custom CSS for dark theme
# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# body {
#     background-color: #000000;
#     color: white;
# }
# </style>
# """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# # Hide Streamlit menu and header
# hide_decoration_bar_style = '''
# <style>
# header {visibility: hidden;}
# </style>
# '''
# st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

# # Main application code
# st.title('Movie Recommendation System')

# user_id = st.number_input('Enter User ID', min_value=1, step=1)

# if st.button('Recommend'):
#     recommended_movies = get_recommendations(user_id)
    
#     st.write(f"Top {TOP_K} recommendations for user {user_id}:")
    
#     num_cols = 5  # Number of columns in the grid layout
#     num_movies = len(recommended_movies)
#     num_rows = (num_movies // num_cols) + (1 if num_movies % num_cols > 0 else 0)

#     for row in range(num_rows):
#         cols = st.columns(num_cols)
#         for col in range(num_cols):
#             index = row * num_cols + col
#             if index < num_movies:
#                 movie_id = recommended_movies.iloc[index]['movieId']
#                 prediction_score = recommended_movies.iloc[index]['prediction']
#                 movie_title = fetch_movie_title(movie_id)  # Fetch movie title here
#                 poster_url = fetch_poster(movie_id)  # Fetch movie poster URL here

#                 if poster_url:
#                     with cols[col]:
#                         if movie_title:
#                             st.write(movie_title)  # Display movie title above the poster
#                         else:
#                             st.write('Unknown Title')
#                         st.image(poster_url, width=150)
#                         st.write(f"Prediction Score: {prediction_score:.4f}")
