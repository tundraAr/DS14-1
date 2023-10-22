import os

import streamlit as st
from dotenv import load_dotenv
# from src.recsys.base import ContentBaseRecSys
from api import OMDBApi
from recsys import ContentBaseRecSys
from streamlit_extras.no_default_selectbox import selectbox

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
st.write("Result:", result_genre)
st.write("Result:", result_lang)
st.write("Result:", result_title)

# тестирую метод получения рекомендаций по названию фильма
# title='Pirates of the Caribbean: At World\'s End'
# title = 'The Dark Knight'
title = result_title
# st.write("Название фильма:", title)

# st.button("Recommendation", type="primary")
if st.button('Показать рекомендации'):
    # st.write("Рекомендации:")
    recommended_movie_names = recsys.recommendation(title, result_genre, result_lang, top_k=TOP_K)
    # stnded.write(recommended_movie_names)
    recommended_movie_posters = omdbapi.get_posters(recommended_movie_names)
    # st.write(recommended_movie_posters)
    movies_col = st.columns(TOP_K)
    # st.write("movies_col", type(movies_col))
    for index, col in enumerate(movies_col):
        with col:
            st.subheader(recommended_movie_names[index])
            st.image(recommended_movie_posters[index])


# # print(recsys)
# recommended_movie_names = list(recsys.recommendation(title, top_k=TOP_K))
# print("Рекомендации: ", recommended_movie_names)
# recommended_movie_posters = omdbapi.get_posters(recommended_movie_names)

# тестирую функцию получения адреса постера к фильму из базы https://www.omdbapi.com/

# получаю class метода
# poster_class = OMDBApi(
#     api_key=API_KEY
# )
# # получаю путь к постеру
# poster = poster_class._images_path(title)
# if poster == False:
#     print("Ссылки на постер нет")
# else:
#     print(poster)
