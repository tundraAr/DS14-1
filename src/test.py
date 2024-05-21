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


# тестирую метод получения рекомендаций по названию фильма
title='Pirates of the Caribbean: At World\'s End'
# title = 'The Dark Knight'
result_genre = 'Adventure'
result_lang = 'it'

# endpoint = self.url
# query_params = {"apikey": self.api_key, "t": title}
# response = requests.get(endpoint, params=query_params)
# if response.status_code == 200:
#     movie = response.json()
#     if len(movie) == 0:
#         return False
#     else:
#         poster_url = movie['Poster']
#         return poster_url

recommended_movie_names = recsys.recommendation(result_genre, result_lang, title, top_k=TOP_K)
recommended_movie_posters = omdbapi.get_posters(recommended_movie_names)

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
