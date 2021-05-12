import requests
from cloudant.client import CouchDB
from urllib.parse import urlencode, urlunparse
from collections import namedtuple
from redis import Redis

TwitterUrl = namedtuple(
    typename='TwitterUrl',
    field_names='scheme netloc path params query fragment',
    defaults=['https', 'api.twitter.com', '', '', '', ''])


def auth(couchdb: CouchDB, redis: Redis):
    token = redis.get('token')
    if token:
        token = token.decode('utf-8')
    if not token:
        token = couchdb["tokens"].get_query_result(
            selector={
                "_id": {
                    "$gt": None
                },
            },
            limit=1).all()[0]["token"]
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


def get(endpoint, params, couchdb, redis):
    bearer_token = auth(couchdb, redis)
    url = create_url(endpoint, params)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    return json_response
