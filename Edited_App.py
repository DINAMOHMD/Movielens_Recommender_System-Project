import streamlit as st 
import pickle 
import pandas as pd 
from tmdbv3api import TMDb, Movie
from tmdbv3api.exceptions import TMDbException
from PIL import Image 
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components 
import requests

TMDB_API_KEY = '51187dabecd68561d591dbef4a5569e4'
tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY
movie_api = Movie()

# Load KNN model and data 
with open(r'KNN_model.pkl', 'rb') as f:
    KNN = pickle.load(f)

with open(r'data.pkl', 'rb') as f:
    X_reduced, movie_mapper, movie_inv_mapper, movie_titles = pickle.load(f)

# Load predictions and model 
predictions = pickle.load(open(r'all_prediction.Sav', 'rb'))

#Load image for UI 
img = Image.open(r"image_processing20210415-22559-wpekzo-removebg.png")

def find_similar_movies(movie_title, k=10):
    try:
        search_results = movie_api.search(movie_title)

        if len(search_results) == 0:
            st.write(f"No search results found for movie: {movie_title}")
            return []

        # Find the closest match or exact match
        for result in search_results:
            if result.title.lower() == movie_title.lower():
                movie_id = result.id
                break
        else:
            # If no exact match, take the first result as a fallback
            movie_id = search_results[0].id

        movie_ind = movie_mapper.get(movie_id)
        if movie_ind is None:
            st.write(f"Movie ID {movie_id} is not found in the dataset.")
            return []

        movie_vec = X_reduced[movie_ind].reshape(1, -1)

        neighbour = KNN.kneighbors(movie_vec, return_distance=False)
        neighbour_ids = [movie_inv_mapper[n] for n in neighbour[0] if n != movie_ind][:k]
        return neighbour_ids
    
    except TMDbException as e:
        st.write(f"TMDb API error occurred: {e}")
        return []
    except Exception as e:
        st.write(f"An error occurred: {e}")
        return []

def get_recommendations(user_id, top_k = 10):
    # print(f"Fetching recommendations for user ID: {user_id}")
    user_predictions = predictions[predictions['userId'] == user_id]
    # print(f"User predictions:\n{user_predictions}")
    user_predictions = user_predictions.sort_values(by='prediction', ascending=False).head(top_k)
    # print(f"Top {top_k} predictions:\n{user_predictions}")
    return user_predictions[['movieId', 'prediction']]

def normalize_title(movie_title):
    return movie_title.split(' (')[0].strip()   

def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}')
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
    except Exception as e:
        st.write(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Image"
   
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

# Streamlit UI 
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

def show_posters(num , similar_movies):
    num_cols = 3
    num_movies = similar_movies[:num]
    num_rows = (len(num_movies) // num_cols) + (1 if len(num_movies) % num_cols > 0 else 0)
    for row in range(num_rows):
                        cols = st.columns(num_cols)
                        for col in range(num_cols):
                            index = row * num_cols + col
                            if index < len(num_movies):
                                movie_id = num_movies[index]
                                poster_url = fetch_poster(movie_id)
                                movie_title = movie_titles.get(movie_id, "Unknown")
                                cols[col].image(poster_url, caption=movie_title)



# Main page 
def home_page():
    methods = ['Choose','User ID' , 'Movie Title']

    st.title("Movies Recommendation System")
    st.image(img , use_column_width=True)

    method_option = st.selectbox("Method of Recommendtion" , methods)

    if method_option == methods[2] :
        try:
            movie_selected = st.selectbox('Select a movie', ['Choose'] + list(movie_titles.values()))
            normalized_title = normalize_title(movie_selected)
            n = st.number_input('Number of movies:', min_value=6, max_value=20, step=1)
        
            if st.button("Recommend"):
                similar_movies = find_similar_movies(normalized_title)
                if not similar_movies:
                    st.write(f'No similar movies found for Movie "{normalized_title}".')
                else:
                    st.write("")
                    st.write("")
                    st. markdown("<h1 style='text-align: center; color:#A0CFD3;'> RECOMMENDED MOVIES 📈 </h1>", unsafe_allow_html=True)
                    st.write("")
                    st.write("") 
                    show_posters(n , similar_movies)

        except ValueError:
            st.write("Please enter a valid movie title.")

    elif method_option == methods[1]:

        user_id = st.number_input('Enter User ID', min_value= 1 , step=1)
        n = st.number_input('Number of movies:', min_value=6, max_value=20, step=1)
        
        if st.button('Recommend'):
            recommended_movies = get_recommendations(user_id , top_k = n )
            if recommended_movies.empty:
                st.write('No similar movies found for the given User ID')
            else:
                st.write("")
                st.write("")
                st. markdown("<h1 style='text-align: center; color:#A0CFD3;'> RECOMMENDED MOVIES 📈 </h1>", unsafe_allow_html=True)
                st.write("")
                st.write("") 
                show_posters(n , recommended_movies['movieId'].tolist())
            

home_page()

# Sidebar
with st.sidebar:
    selected = option_menu(
                menu_title="Menu",  
                options=["Home","Github-Repo"],  
                icons=["house", "github"], 
                menu_icon="cast",  
                default_index=0, 
                styles={
                "container": {"padding": "5!important", "background-color": "#0E1117" , "Font-family":"Consolas"},
                "icon": {"color": "#FFFFFF", "font-size": "25px"}, 
                "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px","Font-family":"Consolas"},
                "nav-link-selected": {"background-color": "#d25600"},
                }
                ) 
    
    if selected == "Home":
        st.empty()
     
    if selected == "Github-Repo":
        st.subheader("Check Out our Github Repository")
        
        button_html = """
        <div style='
        background-color:#629590; 
        cursor:pointer; 
        height:2.8rem;
        font-size:25px;
        font-weight:bolder;
        border-radius:5px;
        font-family: Consolas, sans-serif;
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
        display: flex;
        align-items:center;
        justify-content:center;'>
            <a href="https://github.com/DINAMOHMD/Movielens_Recommender_System-Project" 
            target="_blank" 
            style='color: white; 
                text-decoration:none;
                padding-top:6px;
                padding-bottom:5px;
                text-align:center;
                width: 100%;'>
            GITHUB
            </a>
        </div>
        """
        components.html(button_html, height=50)

