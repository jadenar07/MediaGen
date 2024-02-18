import streamlit as st
import requests
import streamlit_extras.tags
from PIL import Image
from streamlit_lottie import st_lottie
import streamlit_extras
import base64
import random
import hashlib

st.set_page_config(page_title="MediaGen", layout="wide")
api_key = 'be830a8939c7d58efe26666a97b8dbad'

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://lottie.host/5f4c797e-bb93-4dba-a65a-51a9d8241081/FQVF1NRnzw.json")


with st.sidebar:
    selected = st.radio(
        "Main Menu",
        options=['Home', 'Movies', 'TV Shows', 'Top Rated TV Shows', 'Top Rated Movies'],
        key="main_menu_radio"  # Unique key for the radio widget
    )

home_col1, home_col2, home_col3 = st.columns(3)
if selected == "Home":
        st_lottie(lottie_coding, height=500)
        st.markdown(
            """
            <style>
            .stImage {
                display: block;
                margin-left: auto;
                margin-right: auto;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<h1 style='text-align: center;'>MediaGen</h1>", unsafe_allow_html=True)
elif selected == 'Movies':
    movie_title = st.text_input("Enter the movie title: ")
    movie_search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}&page=1&include_adult=false"

    response = requests.get(movie_search_url)
    if response.status_code == 200:
        orig_movie = response.json()
        if orig_movie['total_results'] > 0:
            results = orig_movie['results']
            for movie in results:
                movie_id = movie['id']
                movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
                details_response = requests.get(movie_details_url)

                if details_response.status_code == 200:
                    cast_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
                    rec_movie_data = details_response.json()
                    poster_path = rec_movie_data['poster_path']
                    movie_name = rec_movie_data['title']
                    genres = ", ".join([genre['name'] for genre in rec_movie_data['genres']])
                    plot = rec_movie_data['overview']
                    status = rec_movie_data['status']
                    score = float(rec_movie_data['vote_average'] * 10)
                    release_year = rec_movie_data['release_date'][:4] if rec_movie_data['release_date'] else "N/A"
                    cast_response = requests.get(cast_url)
                    col1, col2, col3 = st.columns(3)
                    production_companies = rec_movie_data.get('production_companies', [])

                    with col1:
                        st.image(f"https://image.tmdb.org/t/p/original{poster_path}")

                    with col2:
                        st.write(f"<h2>{movie_name}</h2>", unsafe_allow_html=True)
                        if production_companies:
                            company_tags = []
                            for company in production_companies:
                                company_name = company['name']
                                logo_path = company['logo_path']

                                if logo_path:
                                    logo_url = f"https://image.tmdb.org/t/p/original{logo_path}"

                                    tag = f"<img src='{logo_url}' alt='{company_name}' width='15' height='11'> {company_name}"
                                    company_tags.append(tag)

                            if company_tags:
                                comp = streamlit_extras.tags.tagger_component("Production Companies:", company_tags, color_name=['red']*len(company_tags))
                            else:
                                pass

                        else:
                            pass
                        genre_tags = streamlit_extras.tags.tagger_component("Genres:", genres.split(","))

                        st.write(f"<p><strong>Year:</strong> {release_year}</p>", unsafe_allow_html=True)
                        st.write(f"<p><strong>Status:</strong> {status}</p>", unsafe_allow_html=True)
                        st.write(f"<p>{plot}</p>", unsafe_allow_html=True)
                        st.write(f"<progress value='{score}' max='100'></progress>", unsafe_allow_html=True)
                        st.write(f"<p><strong>Vote Average:</strong> {round(rec_movie_data['vote_average'], 1)}</p>",
                                 unsafe_allow_html=True)


                    st.write("----")

                    with col3:
                        rev_expander = st.expander("Review")
                        sim_expander = st.expander("Similar Movies")

                        # Code to fetch reviews
                        review_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={api_key}"
                        review_response = requests.get(review_url)

                        with rev_expander:
                            if review_response.status_code == 200:
                                reviews_data = review_response.json()
                                reviews = reviews_data['results']

                                review_with_avatar = next((review for review in reviews if
                                                           review.get('author_details', {}).get('avatar_path')), None)

                                if review_with_avatar:
                                    author = review_with_avatar['author']
                                    avatar_path = review_with_avatar.get('author_details', {}).get('avatar_path')
                                    rating = review_with_avatar.get('author_details', {}).get('rating')
                                    summary = review_with_avatar.get('content')

                                    full_avatar_url = f"https://www.themoviedb.org/t/p/original{avatar_path}" if avatar_path else None
                                    if full_avatar_url:
                                        avatar_image = requests.get(full_avatar_url)
                                        if avatar_image.status_code == 200:
                                            circle_image_style = """
                                                <style>
                                                .circular-img {
                                                    border-radius: 50%;
                                                    overflow: hidden;
                                                    width: 50px; 
                                                    height: 50px; 
                                                }
                                                </style>
                                            """
                                            st.markdown(circle_image_style, unsafe_allow_html=True)

                                            encoded_image = base64.b64encode(avatar_image.content).decode()
                                            html_content = f'''
                                                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                                                    <img src="data:image/jpeg;base64,{encoded_image}" class="circular-img" style="width: 50px; height: 50px; margin-right: 10px;">
                                                    <div>
                                                        <p style="margin-bottom: 0;"><strong>{author}</strong></p>
                                                        <p style="margin-bottom: 0;">⭐ {rating}</p>
                                                    </div>
                                                </div>
                                            '''
                                            st.markdown(html_content, unsafe_allow_html=True)

                                            if len(summary) > 100:
                                                checkbox_key = f"read_more_checkbox_{hashlib.sha1(summary.encode()).hexdigest()}"
                                                show_full_summary = st.checkbox("Read more", key=checkbox_key)

                                                if not show_full_summary:
                                                    summary_50_words = ' '.join(summary.split()[:50])
                                                    summary_50_words += "..."
                                                    st.markdown(summary_50_words)
                                                else:
                                                    st.markdown(summary)
                                            else:
                                                st.markdown(summary)
                                else:
                                    st.write("No reviews available with avatars")
                            else:
                                st.write("Failed to fetch reviews")
                        with sim_expander:
                            url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={api_key}&language=en-US&page=1"

                            response = requests.get(url)

                            if response.status_code == 200:
                                similar_data = response.json()
                                similar_results = similar_data.get('results', [])

                                for movie in similar_results[0:3]:
                                    sim_path = movie.get('poster_path')
                                    similar_movie_image = f"https://image.tmdb.org/t/p/original{sim_path}"
                                    sim_title = movie.get('title')
                                    sim_date = movie.get('release_date')
                                    img_style = "border-radius: 15px; overflow: hidden;"

                                    st.markdown(
                                        f"""
                                                    <style>
                                                    .rounded-images {{
                                                        display: flex;
                                                        border-radius: 20px;
                                                        overflow: hidden;
                                                        width: auto;
                                                        height: auto;
                                                        padding: 5px;
                                                        margin-bottom: 10px;
                                                    }}
                                                    .rounded-images img {{
                                                        width: 100px;
                                                        height: 150px;
                                                        object-fit: cover;
                                                        margin-right: 10px;
                                                        {img_style}  /* Apply the image style here */
                                                    }}
                                                    </style>
                                                    <div class="rounded-images">
                                                        <img src="https://image.tmdb.org/t/p/original{sim_path}" alt="Movie Poster">
                                                        <div>
                                                            <p><strong>{sim_title}</strong></p>
                                                            <p>Release Date: {sim_date}</p>
                                                        </div>
                                                    </div>
                                                    """,
                                        unsafe_allow_html=True,
                                    )
                            else:
                                pass
elif selected == 'TV Shows':
    tv_title = st.text_input("Enter the movie title: ")
    tv_search_url = f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={tv_title}&page=1&include_adult=false"

    tv_requests = requests.get(tv_search_url)

    if tv_requests.status_code == 200:
        tv_shows_data = tv_requests.json()
        results = tv_shows_data.get('results', [])

        for show in results:
            show_id = show.get('id')
            overview = show.get('overview')
            poster_path = show.get('poster_path')
            release_date = show.get('first_air_date')
            title = show.get('name')
            score = show.get('vote_average')

            tv_col1, tv_col2, tv_col3 = st.columns(3)

            tv_show_details_url = f"https://api.themoviedb.org/3/tv/{show_id}?api_key={api_key}"
            tv_show_details = requests.get(tv_show_details_url)

            if tv_show_details.status_code == 200:
                show_details = tv_show_details.json()
                production_companies = show_details.get('production_companies', [])
                genres = show_details.get('genres', [])
                genre_names = [genre['name'] for genre in genres]
                genres_string = ", ".join(genre_names)
                episodes = show_details.get('episode_number')
                # seasons = show_details.get('seasons')
                in_production = show_details.get('in_production')
                still_on = 'Airing'
                off_air = 'Finished'

                with tv_col1:
                    st.image(f"https://image.tmdb.org/t/p/original{poster_path}")

                with tv_col2:
                    st.write(f"<h2>{title}</h2>", unsafe_allow_html=True)
                    if production_companies:
                        company_tags = []
                        for company in production_companies:
                            company_name = company['name']
                            logo_path = company['logo_path']

                            if logo_path:
                                logo_url = f"https://image.tmdb.org/t/p/original{logo_path}"

                                tag = f"<img src='{logo_url}' alt='{company_name}' width='15' height='11'> {company_name}"
                                company_tags.append(tag)

                        if company_tags:
                            comp = streamlit_extras.tags.tagger_component("Production Companies:", company_tags,
                                                                          color_name=['red'] * len(company_tags))
                        else:
                            pass

                    else:
                        pass
                    genre_tags = streamlit_extras.tags.tagger_component("Genres:", genres_string.split(","))

                    st.write(f"<p><strong>Release Date:</strong> {release_date}</p>", unsafe_allow_html=True)
                    if in_production == False:
                        st.write(f"<p><strong>Status:</strong> {off_air}</p>", unsafe_allow_html=True)
                    else:
                        st.write(f"<p><strong>Status:</strong> {still_on}</p>", unsafe_allow_html=True)
                    st.write(f"<p>{overview}</p>", unsafe_allow_html=True)
                    st.write(f"<progress value='{score*10}' max='100'></progress>", unsafe_allow_html=True)
                    st.write(f"<p><strong>Vote Average:</strong> {round(score, 1)}</p>",
                             unsafe_allow_html=True)

                st.write("----")
                with tv_col3:
                    rev_expander = st.expander("Review")
                    sim_expander = st.expander("Similar TV Shows")

                    review_url = f"https://api.themoviedb.org/3/tv/{show_id}/reviews?api_key={api_key}"
                    review_response = requests.get(review_url)

                    with rev_expander:
                        if review_response.status_code == 200:
                            reviews_data = review_response.json()
                            reviews = reviews_data['results']

                            review_with_avatar = next((review for review in reviews if
                                                       review.get('author_details', {}).get('avatar_path')), None)

                            if review_with_avatar:
                                author = review_with_avatar['author']
                                avatar_path = review_with_avatar.get('author_details', {}).get('avatar_path')
                                rating = review_with_avatar.get('author_details', {}).get('rating')
                                summary = review_with_avatar.get('content')

                                full_avatar_url = f"https://www.themoviedb.org/t/p/original{avatar_path}" if avatar_path else None
                                if full_avatar_url:
                                    avatar_image = requests.get(full_avatar_url)
                                    if avatar_image.status_code == 200:
                                        circle_image_style = """
                                                                            <style>
                                                                            .circular-img {
                                                                                border-radius: 50%;
                                                                                overflow: hidden;
                                                                                width: 50px; 
                                                                                height: 50px; 
                                                                            }
                                                                            </style>
                                                                        """
                                        st.markdown(circle_image_style, unsafe_allow_html=True)

                                        encoded_image = base64.b64encode(avatar_image.content).decode()
                                        html_content = f'''
                                                                            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                                                                                <img src="data:image/jpeg;base64,{encoded_image}" class="circular-img" style="width: 50px; height: 50px; margin-right: 10px;">
                                                                                <div>
                                                                                    <p style="margin-bottom: 0;"><strong>{author}</strong></p>
                                                                                    <p style="margin-bottom: 0;">⭐ {rating}</p>
                                                                                </div>
                                                                            </div>
                                                                        '''
                                        st.markdown(html_content, unsafe_allow_html=True)

                                        if len(summary) > 100:
                                            checkbox_key = f"read_more_checkbox_{hashlib.sha1(summary.encode()).hexdigest()}"
                                            show_full_summary = st.checkbox("Read more", key=checkbox_key)

                                            if not show_full_summary:
                                                summary_50_words = ' '.join(summary.split()[:50])
                                                summary_50_words += "..."
                                                st.markdown(summary_50_words)
                                            else:
                                                st.markdown(summary)
                                        else:
                                            st.markdown(summary)
                            else:
                                st.write("No reviews available with avatars")
                        else:
                            st.write("Failed to fetch reviews")

                    similar_url = f"https://api.themoviedb.org/3/tv/{show_id}/similar?api_key={api_key}&language=en-US&page=1"
                    similar_response = requests.get(similar_url)

                    with sim_expander:
                        if similar_response.status_code == 200:
                            similar_data = similar_response.json()
                            similar_results = similar_data.get('results', [])

                            similar_results = [tv_show for tv_show in similar_results if tv_show.get('id') != show_id]

                            if not similar_results:
                                st.write("No similar shows")
                            else:
                                for tv_show in similar_results[1:4]:
                                    sim_title = tv_show.get('name')
                                    sim_date = tv_show.get('first_air_date')
                                    sim_poster_path = tv_show.get('poster_path')
                                    img_style = "border-radius: 15px; overflow: hidden;"

                                    st.markdown(
                                        f"""
                                                       <style>
                                                       .rounded-images {{
                                                           display: flex;
                                                           border-radius: 20px;
                                                           overflow: hidden;
                                                           width: auto;
                                                           height: auto;
                                                           padding: 5px;
                                                           margin-bottom: 10px;
                                                       }}
                                                       .rounded-images img {{
                                                           width: 100px;
                                                           height: 150px;
                                                           object-fit: cover;
                                                           margin-right: 10px;
                                                           {img_style}  /* Apply the image style here */
                                                       }}
                                                       </style>
                                                       <div class="rounded-images">
                                                           <img src="https://image.tmdb.org/t/p/original{sim_poster_path}" alt="TV Show Poster">
                                                           <div>
                                                               <p><strong>{sim_title}</strong></p>
                                                               <p>First Air Date: {sim_date}</p>
                                                           </div>
                                                       </div>
                                                       """,
                                        unsafe_allow_html=True,
                                    )
                        else:
                            st.write("Failed to fetch similar shows")


elif selected == 'Top Rated Movies':
    top_movie_url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}&language=en-US&page=1"

    top_movie_requests = requests.get(top_movie_url)

    if top_movie_requests.status_code == 200:
        top_movies_data = top_movie_requests.json()
        original_results = top_movies_data.get('results', [])

        if 'shuffled_results' not in st.session_state:
            # Shuffle the list of top-rated movies only once
            st.session_state.shuffled_results = original_results.copy()
            random.shuffle(st.session_state.shuffled_results)

        for original, shuffled in zip(original_results, st.session_state.shuffled_results):
            # Use 'original' for displaying, 'shuffled' for shuffling
            overview = original.get('overview')
            poster_path = original.get('poster_path')
            release_date = original.get('release_date')
            title = original.get('title')
            score = float(original.get('vote_average') * 10)

            mov_col1, mov_col2, mov_col3 = st.columns(3)
            img_style = f"border-radius: 15px; overflow: hidden;"

            with mov_col1:
                st.markdown(
                    f'<img src="https://image.tmdb.org/t/p/original{poster_path}" style="{img_style}" width="300">',
                    unsafe_allow_html=True)
            with mov_col2:
                st.write(f"<p><strong>Title:</strong> {title}</p>", unsafe_allow_html=True)
                st.write(f"<p><strong>Year:</strong> {release_date}</p>", unsafe_allow_html=True)
                st.write(f"<p>{overview}</p>", unsafe_allow_html=True)
                st.write(
                    f"<progress value='{float(st.session_state.shuffled_results[0]['vote_average']) * 10}' max='100'></progress>",
                    unsafe_allow_html=True)
                st.write(f"<p><strong>Vote Average:</strong> {round(score/10, 1)}</p>",
                         unsafe_allow_html=True)

            # Add a line after each movie
            st.write("------")

        # Button to shuffle and display a new movie
        shuffle_button = st.button("Shuffle Movie")
        if shuffle_button:
            # Reshuffle the list and pick a new random movie
            random.shuffle(st.session_state.shuffled_results)

            st.markdown("<h2>Randomly Shuffled Movie</h2>", unsafe_allow_html=True)
            st.image(f"https://image.tmdb.org/t/p/original{st.session_state.shuffled_results[0]['poster_path']}", width=300)
            st.write(f"<p><strong>Title:</strong> {st.session_state.shuffled_results[0]['title']}</p>", unsafe_allow_html=True)
            st.write(f"<p><strong>Year:</strong> {st.session_state.shuffled_results[0]['release_date']}</p>", unsafe_allow_html=True)
            st.write(f"<p>{st.session_state.shuffled_results[0]['overview']}</p>", unsafe_allow_html=True)
            st.write(f"<progress value='{float(st.session_state.shuffled_results[0]['vote_average']) * 10}' max='100'></progress>",
                     unsafe_allow_html=True)
            st.write(f"<p><strong>Vote Average:</strong> {round(float(st.session_state.shuffled_results[0]['vote_average']), 1)}</p>",
                     unsafe_allow_html=True)

elif selected == 'Top Rated TV Shows':
    top_tv_url = f"https://api.themoviedb.org/3/tv/top_rated?api_key={api_key}&language=en-US&page=1"

    top_tv_requests = requests.get(top_tv_url)

    if top_tv_requests.status_code == 200:
        top_tv_data = top_tv_requests.json()
        original_results = top_tv_data.get('results', [])

        if 'shuffled_results' not in st.session_state:
            st.session_state.shuffled_results = original_results.copy()
            random.shuffle(st.session_state.shuffled_results)

        for original, shuffled in zip(original_results, st.session_state.shuffled_results):
            overview = original.get('overview')
            poster_path = original.get('poster_path')
            release_date = original.get('first_air_date')
            title = original.get('name')
            score = float(original.get('vote_average') * 10)

            tv_col1, tv_col2, tv_col3 = st.columns(3)
            img_style = f"border-radius: 15px; overflow: hidden;"

            with tv_col1:
                st.markdown(
                    f'<img src="https://image.tmdb.org/t/p/original{poster_path}" style="{img_style}" width="300">',
                    unsafe_allow_html=True)
            with tv_col2:
                st.write(f"<p><strong>Title:</strong> {title}</p>", unsafe_allow_html=True)
                st.write(f"<p><strong>Year:</strong> {release_date}</p>", unsafe_allow_html=True)
                st.write(f"<p>{overview}</p>", unsafe_allow_html=True)
                st.write(
                    f"<progress value='{float(st.session_state.shuffled_results[0]['vote_average']) * 10}' max='100'></progress>",
                    unsafe_allow_html=True)
                st.write(f"<p><strong>Vote Average:</strong> {round(score/10, 1)}</p>",
                         unsafe_allow_html=True)

            st.write("------")

        shuffle_button = st.button("Shuffle TV Show")
        if shuffle_button:
            random.shuffle(st.session_state.shuffled_results)

            st.markdown("<h2>Randomly Shuffled TV Show</h2>", unsafe_allow_html=True)
            st.image(f"https://image.tmdb.org/t/p/original{st.session_state.shuffled_results[0]['poster_path']}", width=300)
            st.write(f"<p><strong>Title:</strong> {st.session_state.shuffled_results[0]['name']}</p>", unsafe_allow_html=True)
            st.write(f"<p><strong>Year:</strong> {st.session_state.shuffled_results[0]['first_air_date']}</p>", unsafe_allow_html=True)
            st.write(f"<p>{st.session_state.shuffled_results[0]['overview']}</p>", unsafe_allow_html=True)
            st.write(f"<progress value='{float(st.session_state.shuffled_results[0]['vote_average']) * 10}' max='100'></progress>",
                     unsafe_allow_html=True)
            st.write(f"<p><strong>Vote Average:</strong> {round(float(st.session_state.shuffled_results[0]['vote_average']), 1)}</p>",
                     unsafe_allow_html=True)



hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)