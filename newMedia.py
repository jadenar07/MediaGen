import streamlit as st
import requests
from PIL import Image
from streamlit_lottie import st_lottie
import streamlit_extras.tags
import base64
import random

st.set_page_config(page_title="MediaGen", layout="wide")
api_key = 'be830a8939c7d58efe26666a97b8dbad'

def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_coding = load_lottieurl("https://lottie.host/5f4c797e-bb93-4dba-a65a-51a9d8241081/FQVF1NRnzw.json")

def create_sidebar():
    return st.sidebar.radio(
        "Main Menu",
        options=['Home', 'Movies', 'TV Shows', 'Top Rated Movies', 'Top Rated TV Shows'],
        key="main_menu_radio"
    )

def fetch_data(url):
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def display_production_companies(details):
    if details['production_companies']:
        company_tags = [
            f"<img src='https://image.tmdb.org/t/p/original{company['logo_path']}' alt='{company['name']}' width='15' height='11'> {company['name']}"
            for company in details['production_companies'] if company.get('logo_path')
        ]
        if company_tags:
            streamlit_extras.tags.tagger_component("Production Companies:", company_tags, color_name=['red'] * len(company_tags))
        else:
            st.write("No production company information available.")
    else:
        st.write("No production company information available.")

def display_genres(details):
    genres = [genre['name'] for genre in details['genres']]
    streamlit_extras.tags.tagger_component("Genres:", genres)

def display_review(review):
    author = review['author']
    avatar_path = review.get('author_details', {}).get('avatar_path')
    rating = review.get('author_details', {}).get('rating', 'N/A')
    summary = review.get('content')
    if avatar_path:
        avatar_url = f"https://www.themoviedb.org/t/p/original{avatar_path}" if avatar_path.startswith('/') else avatar_path
        st.image(avatar_url, width=50, caption=author)
        if rating:
            st.write(f"Rating: {rating}")
        if summary:
            st.write(summary)

def display_similar_content(content_list, content_type):
    for content in content_list[:3]:  # Display up to 3 similar contents
        col1, col2 = st.columns([1, 4])
        with col1:
            if 'poster_path' in content:
                st.image(f"https://image.tmdb.org/t/p/w200{content['poster_path']}", width=100, caption=content.get('release_date', '')[:4])
            else:
                st.write("No poster available")
        with col2:
            st.write(content['title'] if content_type == 'movie' else content['name'])

def display_movie_info(movie_details, api_key):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.image(f"https://image.tmdb.org/t/p/original{movie_details['poster_path']}")
    with col2:
        st.markdown(f"<h2>{movie_details['title']}</h2>", unsafe_allow_html=True)
        display_production_companies(movie_details)
        display_genres(movie_details)
        st.markdown(f"<p><strong>Year:</strong> {movie_details['release_date'][:4]}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Status:</strong> {movie_details['status']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p>{movie_details['overview']}</p>", unsafe_allow_html=True)
        st.progress(movie_details['vote_average'] / 10)
        st.write(f"Rating: {movie_details['vote_average']} / 10")
    with col3:
        with st.expander("Reviews"):
            reviews = fetch_data(f"https://api.themoviedb.org/3/movie/{movie_details['id']}/reviews?api_key={api_key}")
            if reviews and reviews['results']:
                display_review(reviews['results'][0])  # Display only one review
            else:
                st.write("No reviews available.")
        with st.expander("Similar Movies"):
            similar_movies = fetch_data(f"https://api.themoviedb.org/3/movie/{movie_details['id']}/similar?api_key={api_key}")
            if similar_movies and similar_movies['results']:
                display_similar_content(similar_movies['results'], 'movie')
            else:
                st.write("No similar movies found.")
    st.markdown("---")

def fetch_movie_details(movie_id, api_key):
    movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    return fetch_data(movie_details_url)

def display_movie_details(movie_data, api_key):
    for movie in movie_data:
        movie_details = fetch_movie_details(movie['id'], api_key)
        if movie_details:
            display_movie_info(movie_details, api_key)

def display_tv_show_details(tv_show_data, api_key):
    for show in tv_show_data:
        show_details = fetch_tv_show_details(show['id'], api_key)
        if show_details:
            display_tv_show_info(show_details, api_key)

def display_tv_show_info(show_details, api_key):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.image(f"https://image.tmdb.org/t/p/original{show_details['poster_path']}")
    with col2:
        st.markdown(f"<h2>{show_details['name']}</h2>", unsafe_allow_html=True)
        display_production_companies(show_details)
        display_genres(show_details)
        st.markdown(f"<p><strong>First Air Date:</strong> {show_details['first_air_date']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Status:</strong> {('Airing' if show_details['in_production'] else 'Ended')}</p>", unsafe_allow_html=True)
        st.markdown(f"<p>{show_details['overview']}</p>", unsafe_allow_html=True)
        st.progress(show_details['vote_average'] / 10)
        st.write(f"Rating: {show_details['vote_average']} / 10")
    with col3:
        with st.expander("Reviews"):
            reviews = fetch_data(f"https://api.themoviedb.org/3/tv/{show_details['id']}/reviews?api_key={api_key}")
            if reviews and reviews['results']:
                display_review(reviews['results'][0])  # Display only one review
            else:
                st.write("No reviews available.")
        with st.expander("Similar TV Shows"):
            similar_shows = fetch_data(f"https://api.themoviedb.org/3/tv/{show_details['id']}/similar?api_key={api_key}")
            if similar_shows and similar_shows['results']:
                display_similar_content(similar_shows['results'], 'tv')
            else:
                st.write("No similar TV shows found.")
    st.markdown("---")

def fetch_tv_show_details(show_id, api_key):
    tv_show_details_url = f"https://api.themoviedb.org/3/tv/{show_id}?api_key={api_key}"
    return fetch_data(tv_show_details_url)

def display_top_rated_entities(entity_type, api_key):
    top_rated_url = f"https://api.themoviedb.org/3/{entity_type}/top_rated?api_key={api_key}"
    top_rated_data = fetch_data(top_rated_url)
    if top_rated_data and top_rated_data['results']:
        if entity_type == 'movie':
            display_movie_details(top_rated_data['results'], api_key)
        elif entity_type == 'tv':
            display_tv_show_details(top_rated_data['results'], api_key)

selected = create_sidebar()

if selected == "Home":
    if lottie_coding:
        st_lottie(lottie_coding, height=500)
    else:
        st.error("Failed to load Lottie animation.")
    st.markdown("<h1 style='text-align: center;'>MediaGen</h1>", unsafe_allow_html=True)
elif selected == 'Movies':
    movie_title = st.text_input("Enter the movie title: ")
    if movie_title:
        movie_search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
        movie_data = fetch_data(movie_search_url)
        if movie_data and movie_data['results']:
            display_movie_details(movie_data['results'], api_key)
elif selected == 'TV Shows':
    tv_title = st.text_input("Enter the TV show title: ")
    if tv_title:
        tv_search_url = f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={tv_title}"
        tv_data = fetch_data(tv_search_url)
        if tv_data and tv_data['results']:
            display_tv_show_details(tv_data['results'], api_key)
elif selected == 'Top Rated Movies':
    display_top_rated_entities('movie', api_key)
elif selected == 'Top Rated TV Shows':
    display_top_rated_entities('tv', api_key)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stImage>img {
                border-radius: 5px;  # Slightly rounded corners for images
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
