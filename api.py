import requests
import json
import os


class FigshareAPIClient(object):


    def __init__(self, access_token, endpoint):
        self._access_token = access_token
        self._endpoint = endpoint
        self._configure_session()


    def _configure_session(self):
        self._session = requests.Session()
        api_headers = {
                "Authorization": "token {}".format(self._access_token),
                "Content-Type": "application/json"
        }
        self._session.headers.update(api_headers)


    def create_article(self, article_metadata):
        pass


    def create_file(self, article_metadata):
        pass
