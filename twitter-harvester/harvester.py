from time import time
import couchdb
from redis import Redis
import math
import api


def create_params():
    # Twitter's bounding box for Melbourne - might need to update
    bounding_box = [144.593741856, -38.433859306, 145.512528832, -37.5112737225]
    x_delta = bounding_box[2] - bounding_box[0]
    y_delta = bounding_box[3] - bounding_box[1]
    x_total = math.ceil(x_delta / 0.3)
    y_total = math.ceil(y_delta / 0.3)
    x = x_delta / x_total
    y = y_delta / y_total

    bounding_boxes = []
    for i in range(x_total):
        for j in range(y_total):
            bounding_boxes.append([
                bounding_box[0] + x * i,
                bounding_box[1] + x * j,
                bounding_box[0] + x * (i + 1),
                bounding_box[1] + x * (j + 1),
            ])

    bounding_box_query = "(%s)" % " OR ".join(
        map(lambda box: "bounding_box:[%s]" % " ".join(
            map(lambda point: "%.6f" % point, box)
        ), bounding_boxes))

    params = {
        # "start_time": "",
        # "end_time": "",
        "query": "lang:EN -place:melbourne %s" % bounding_box_query,  # max 1,024 characters
        "user.fields": "url",
        "expansions": "geo.place_id,author_id",
        "tweet.fields": "author_id,created_at,geo,id,source,text",
        "place.fields": "full_name,geo,place_type",
        "user.fields": "location,username",
        "max_results": 300
    }

    return params


def format_response(response):
    places = {}
    users = {}
    tweets = response["data"]

    if "includes" in response:
        if "places" in response["includes"]:
            places = {x["id"]: x for x in response["includes"]["places"]}
        if "users" in response["includes"]:
            users = {x["id"]: x for x in response["includes"]["users"]}

    for tweet in tweets:
        tweet["_id"] = tweet["id"]
        if "author_id" in tweet:
            tweet["author"] = users[tweet["author_id"]]
        if "place_id" in tweet["geo"] and "coordinates" not in tweet["geo"]:
            tweet["geo"]["place"] = places[tweet["geo"]["place_id"]]

    return tweets


def main():
    couch = couchdb.Server('http://admin:uJNh4NwrEt59o7@172.26.129.48:5984/')  # should come from os.environ param
    redis = Redis('172.26.134.58', 6379, 0)

    t1 = time()
    response = api.get(
        endpoint='2/tweets/search/all',
        params=create_params(),
        couch=couch,
        redis=redis)
    t2 = time()
    print("%.2fs to call" % (t2 - t1))

    if "data" not in response:
        # handle
        pass

    tweets = format_response(response)

    t1 = time()
    couch["twitter"].update(tweets)
    t2 = time()
    print("%.2fs to save" % (t2 - t1))


if __name__ == "__main__":
    main()
