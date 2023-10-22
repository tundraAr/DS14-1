import requests
from typing import Optional, List


class OMDBApi:

    def __init__(self, api_key: str):
        self.api_key = api_key
        # self.url = "http://img.omdbapi.com/"
        self.url = "http://www.omdbapi.com/"

    def _images_path(self, title: str) -> Optional[str]:
        # api_path = 'http: // img.omdbapi.com /?' + 'apikey='' + self.api_key + '&'
        endpoint = self.url
        # Замените DEMO_KEY ниже своим собственным ключом, если вы его сгенерировали.
        #api_key = "8eerWw2UIf7mr3FJVAtzWPgA7Ick118jbuB3cJ9e"
        query_params = {"apikey": self.api_key, "t": title}
        # Получаем данные из датасета
        response = requests.get(endpoint, params=query_params)
        if response.status_code == 200:
            movie = response.json()
            if len(movie) == 0:
                return False
            else:
                poster_url = movie['Poster']
                return poster_url
        else:
            print("Возникла ошибка. Ответ сервера: ", response)

    def get_posters(self, titles: List[str]) -> List[str]:
        posters = []
        for title in titles:
            path = self._images_path(title)
            if path:  # If image isn`t exist
                posters.append(path)
            else:
                posters.append('assets/none.jpeg')  # Add plug

        return posters
