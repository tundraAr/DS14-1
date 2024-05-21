import os
import streamlit as st
from dotenv import load_dotenv
from api import OMDBApi
from recsys import ContentBaseRecSys


st.set_page_config(layout="wide", page_title="Recommendation service")
st.sidebar.write("## Настрой свой фильтр для фильмов :gear:")


st.markdown(
"<h1 style='text-align: center; color: black;'>Сервис рекомендаций</h1>",
unsafe_allow_html=True
)
st.image(
"https://www.joblo.com/wp-content/uploads/2021/07/good-bad-badass-2.jpg", width=600
)


TOP_K = 5
load_dotenv()

MOVIES = os.getenv("MOVIES")
DISTANCE = os.getenv("DISTANCE")
API_KEY = os.getenv("API_KEY")

recsys = ContentBaseRecSys(
        movies_dataset_filepath=MOVIES,
        distance_filepath=DISTANCE,
)
omdbapi = OMDBApi(API_KEY)
set_title = recsys.get_title()
set_genres = recsys.get_genres()
set_lang = recsys.get_lang()

result_genre = st.sidebar.selectbox("Выбери жанр фильма", set_genres)
# st.write("Result:", result_genre)
result_lang = st.sidebar.selectbox("Выбери язык оригинала", set_lang)
result_title = st.sidebar.selectbox("Выбери название фильма", set_title)
# st.write("Result:", result_genre)
# st.write("Result:", result_lang)
# st.write("Result:", result_title)

# title='Pirates of the Caribbean: At World\'s End'
# title = 'Man of Steel'
title = result_title
# result_genre = 'Adventure'
# result_lang = 'it'
# recommended_movie_names = recsys.recommendation(result_genre, result_lang, title, top_k=TOP_K)
# lm = len(recommended_movie_names)

if st.button('Показать рекомендации'):
    # st.write("Рекомендации:")
    recommended_movie_names = recsys.recommendation(result_genre, result_lang, title, top_k=TOP_K)
    # st.write(recommended_movie_names)
    if recommended_movie_names:
        recommended_movie_posters = omdbapi.get_posters(recommended_movie_names)
        # st.write(recommended_movie_posters)
        if len(recommended_movie_names) >= TOP_K:
            movies_col = st.columns(TOP_K)
        else:
            movies_col = st.columns(len(recommended_movie_names))
        # st.write("movies_col", type(movies_col))
        for index, col in enumerate(movies_col):
            with col:
                st.subheader(recommended_movie_names[index])
                st.image(recommended_movie_posters[index])
    else:
        st.write("Условия слишком жесткие. Ничего не смогу рекомендовать")
