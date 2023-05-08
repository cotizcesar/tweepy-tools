import requests
import os
import json
import time

BEARER_TOKEN = 'bearer_token'
USERNAME = 'username'
MEDIA_FIELDS = 'url'

def get_user_id(username: str) -> int:
    result = str()

    if username:
        url = f'https://api.twitter.com/2/users/by/username/{username}'
        response = requests.get(url, headers={'Authorization': f'Bearer {BEARER_TOKEN}'})
        result = response.json()['data']['id']

    return result

def get_tweets_urls(user_id: str, max_results=100) -> list:
    result = list()
    query_params = dict()
    pagination_token = ''
    iterator = 1

    if user_id:
        url = f'https://api.twitter.com/2/users/{user_id}/tweets?&expansions=attachments.media_keys&media.fields={MEDIA_FIELDS}&max_results={max_results}'
        response = requests.get(url, headers={'Authorization': f'Bearer {BEARER_TOKEN}'})
        tweets = response.json()
        media_urls = tweets['includes']['media']

        for media in media_urls:
            if 'url' in media:
                _get_tweets_download(media['media_key'], media['url'])
        
        # GET next page
        pagination_token = tweets['meta'].get('next_token')
        query_params['pagination_token'] = tweets['meta'].get('next_token')

        while pagination_token:
            iterator = iterator + 1

            # Timers to respect twitter limits
            if iterator > 15:
                time.sleep(900)
                iterator = 0

            url = f'https://api.twitter.com/2/users/{user_id}/tweets?&expansions=attachments.media_keys&media.fields={MEDIA_FIELDS}&max_results={max_results}'
            response = requests.get(url, headers={'Authorization': f'Bearer {BEARER_TOKEN}'}, params=query_params)
            
            if response.status_code != 200:
                print(f"Error al obtener la siguiente página de resultados: {response.status_code}")
                break

            tweets = response.json()
            media_urls = tweets['includes']['media']
            pagination_token = tweets['meta'].get('next_token')
            query_params['pagination_token'] = tweets['meta'].get('next_token')

            for media in media_urls:
                if 'url' in media:
                    _get_tweets_download(media['media_key'], media['url'])

    return result

def _get_tweets_download(name, url):
    if url:
        response = requests.get(url)
        filename = f"{name}.jpg"
        with open(filename, "wb") as f:
            f.write(response.content)

    return None

user_id = get_user_id(USERNAME)
tweets_urls = get_tweets_urls(user_id)
