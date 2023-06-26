import os

import streamlit as st
from dotenv import load_dotenv

from api.omdb import OMDBApi
from recsys import ContentBaseRecSys

TOP_K = 5
load_dotenv()

# API_KEY = os.getenv("API_KEY")
MOVIES = os.getenv("MOVIES")
DISTANCE = os.getenv("DISTANCE")

# omdbapi = OMDBApi(API_KEY)


recsys = ContentBaseRecSys(
    movies_dataset_filepath=MOVIES,
    distance_filepath=DISTANCE,
)

st.markdown(
    "<h1 style='text-align: center; color: black;'>Movie Recommender Service</h1>",
    unsafe_allow_html=True
)

selected_movie = st.selectbox(
    "Type or select a movie you like :",
    recsys.get_title()
)


if st.button('Show Recommendation'):
    st.write("Recommended Movies:")
    recommended_movie_names = recsys.recommendation(selected_movie, top_k=TOP_K)
    # recommended_movie_posters = omdbapi.get_posters(recommended_movie_names)
    movies_col = st.columns(TOP_K)
    for index, col in enumerate(movies_col):
        with col:
            st.subheader(recommended_movie_names[index])
            # st.image(recommended_movie_posters[index])
