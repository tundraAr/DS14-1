from typing import List, Set

import pandas as pd
from .utils import parse


class ContentBaseRecSys:

    def __init__(self, movies_dataset_filepath: str, distance_filepath: str):
        self.distance = pd.read_csv(distance_filepath, index_col='id')
        self.distance.index = self.distance.index.astype(int)
        self.distance.columns = self.distance.columns.astype(int)
        self._init_movies(movies_dataset_filepath)

    def _init_movies(self, movies_dataset_filepath) -> None:
        self.movies = pd.read_csv(movies_dataset_filepath, index_col='id')
        self.movies.index = self.movies.index.astype(int)
        self.movies['genres'] = self.movies['genres'].apply(parse)

    def get_title(self) -> List[str]:
        return self.movies['title_x'].values

    def get_genres(self) -> Set[str]:
        genres = [item for sublist in self.movies['genres'].values.tolist() for item in sublist]
        return set(genres)

    def get_lang(self) -> List[str]:
        language = self.movies['original_language'].unique().tolist()
        return language


    def recommendation(self, genre: str, language: str, title: str, top_k: int = 5) -> List[str]:
        """
        Returns the names of the top_k most similar movies with the movie "title"
        """
        # text1 = self.movies['overview'].fillna('')
        # title1 = self.movies['title_x']
        if language:
            if genre:
                # создаем датафрейм
                movies_min = pd.DataFrame({'title': self.movies['title_x'], 'text': self.movies['overview'], 'genres': self.movies['genres'], 'language': self.movies['original_language']})
                indices = pd.Series(movies_min.index, index=movies_min['title'])
                # print("indices равно: ", indices)
                # получаем индекс выбранного фильма
                idx = indices[title]
                # print("idx равно: ", idx)
                # Получаем оценки сходство попарно
                sim_scores = list(enumerate(self.distance[idx]))
                # Сортируем фильмы по показателям сходство
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                # Фильтруем датафрейм по выбранным жанру и языку
                # sim_scores = sim_scores[1:top_k + 1] # закоментировала 22.10
                movies = movies_min[movies_min['genres'].apply(lambda x: genre in x)]
                movies = movies[movies['language'] == language]
                # distances = self.distance
                l_d = [] # список с косинусными расстояниями от title до фильмов из отфильтрованного датасета
                for index in movies.index:
                    l_d.append(self.distance[index][idx])
                # вставляет колонку с косинусными расстояниями
                movies.insert(loc=0 , column='distance', value=l_d)
                # сортируем датафрейм по колонке с расстояниями по убыванию
                df = movies.sort_values(by='distance', ascending=False)
                # Создаем список лучших похожих фильмов
                if len(movies) > 0:
                    if len(movies) >= top_k: # проверяем длину итогового датафрейма, чтобы список не вышел за пределы индекса
                        movie_rec = list(df['title'].iloc[0:top_k])
                    else:
                        movie_rec = list(df['title'].iloc[0:len(movies)])
                    return movie_rec
                else:
                    # print("Условия слишком жесткие. Ничего не смогу рекомендовать")
                    return False
