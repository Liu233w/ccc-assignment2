import requests
import couchdb
from urllib.parse import urlencode, urlunparse
from collections import namedtuple
from redis import Redis

TwitterUrl = namedtuple(
    typename='TwitterUrl',
    field_names='scheme netloc path params query fragment',
    defaults=['https', 'api.twitter.com', '', '', '', ''])


def auth(couch: couchdb.Server, redis: Redis):
    token = redis.get('token')
    if token:
        token = token.decode('utf-8')
    if not token:
        tokens = couch["tokens"].find({
            "selector": {
                "_id": {
                    "$gt": None
                }
            },
            "limit": 1
        })
        token = list(tokens)[0]["token"]
        redis.set('token', token, 86400)

    return token


def create_url(endpoint, params):
    query = urlencode(params)
    url_object = TwitterUrl(path=endpoint, query=query)
    url = urlunparse(url_object)
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get(endpoint, params, couch, redis):
    bearer_token = auth(couch, redis)
    url = create_url(endpoint, params)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    return json_response
