import requests
from cloudant.client import CouchDB
from urllib.parse import urlencode, urlunparse
from collections import namedtuple
from redis import Redis
from datetime import datetime, timedelta
from time import sleep
from random import random

TwitterUrl = namedtuple(
    typename='TwitterUrl',
    field_names='scheme netloc path params query fragment',
    defaults=['https', 'api.twitter.com', '', '', '', ''])


def auth(couchdb: CouchDB, redis: Redis, endpoint: str):
    # Select valid token
    now = datetime.utcnow().timestamp()
    min_window = (datetime.utcnow() - timedelta(minutes=15)).timestamp()

    complete = False
    while not complete:
        token = None
        while not token:
            result = couchdb["tokens"].get_query_result(
                selector={
                    # ensure less than x calls per window
                    endpoint: {
                        "$or": [
                            {"$exists": False},
                            {"total": {"$lt": 300}},
                            {"since": {"$lt": min_window}}
                        ]
                    },
                    # ensure less than one second per call
                    "last_used": {
                        "$or": [
                            {"$exists": False},
                            {"$lt": now - 2}
                        ]
                    }
                },
                sort=[{"last_used": "asc"}],
                limit=1).all()
            if len(result) == 0:
                print("No valid token, waiting...")
                sleep(1)
                continue
            else:
                token = result[0]

        doc = couchdb["tokens"][token["_id"]]
        doc.fetch()

        # Update last_used
        needs_new_window = endpoint not in doc or doc[endpoint]["since"] < min_window
        if needs_new_window:
            doc.update({
                "last_used": now,
                endpoint: {
                    "since": now,
                    "total": 1
                }
            })
        else:
            doc.update({
                "last_used": now,
                endpoint: {
                    **doc[endpoint],
                    "total": doc[endpoint]["total"] + 1
                }
            })

        try:
            doc.save()
            print("Using token: %s" % token["_id"])
            complete = True
        except Exception as e:
            print("CouchDB Token Error", e)
            sleep(random() * 0.3 + 0.1)
            continue

    return token["token"]


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
    bearer_token = auth(couchdb, redis, endpoint)
    url = create_url(endpoint, params)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    return json_response
