import os
from time import sleep, time
from datetime import datetime, timedelta
from cloudant.client import CouchDB
from redis import Redis
import math
import api
from locations import load_features
from predictor import Predictor, load_model

os.environ["COUCHDB_USERNAME"] = "admin"
os.environ["COUCHDB_PASSWORD"] = "uJNh4NwrEt59o7"
os.environ["COUCHDB_HOST"] = "172.26.129.48"
os.environ["REDIS_HOST"] = "172.26.134.58"
os.environ["MAP_PATH"] = "/Users/robertsloan/repos/ccc-assignment2/flaskapp/frontend/src/assets/jsonfile/polygons.json"
os.environ["MODEL_PATH"] = "/Users/robertsloan/Desktop/BERT_classification_epoch_1.model"


def create_params(feature, next_token, backfill=False):

    # Combine boxes of max 25 miles
    box = feature["box"]
    x_delta = box[2] - box[0]
    y_delta = box[3] - box[1]
    x_total = math.ceil(x_delta / 0.3)
    y_total = math.ceil(y_delta / 0.3)
    x = x_delta / x_total
    y = y_delta / y_total

    boxes = []
    for i in range(x_total):
        for j in range(y_total):
            boxes.append([
                box[0] + x * i,
                box[1] + y * j,
                box[0] + x * (i + 1),
                box[1] + y * (j + 1),
            ])

    box_query = "(%s)" % " OR ".join(
        map(lambda box: "bounding_box:[%s]" % " ".join(
            map(lambda point: "%.6f" % point, box)
        ), boxes))

    # Get the start and end times
    start_time = None
    end_time = None
    if (backfill):
        start_time = datetime.fromtimestamp(feature["latest"])
        end_time = start_time + timedelta(days=30)
    else:
        end_time = datetime.fromtimestamp(feature["oldest"])
        start_time = end_time - timedelta(days=30)

    # Keep times within Twitter limits
    if end_time > datetime.utcnow() - timedelta(seconds=30):
        end_time = datetime.utcnow() - timedelta(seconds=30)
    if start_time < datetime(2017, 1, 1):
        start_time = datetime(2017, 1, 1)

    params = {
        "start_time": start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "end_time": end_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "query": "lang:EN -place:melbourne %s" % box_query,  # max 1,024 characters
        "user.fields": "url",
        "expansions": "geo.place_id,author_id",
        "tweet.fields": "author_id,created_at,geo,id,source,text",
        "place.fields": "full_name,geo,place_type",
        "user.fields": "location,username",
        "max_results": 10,
    }

    if next_token:
        params["next_token"] = next_token

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
        # Partition by date
        # date_string = datetime.fromisoformat(tweet["created_at"][:-1]).strftime("%Y-%m-%d")
        id = tweet["id"]
        tweet["_id"] = "%s:%s" % (1, id)
        try:
            if "author_id" in tweet:
                tweet["author"] = users[tweet["author_id"]]
            if "place_id" in tweet["geo"] and "coordinates" not in tweet["geo"]:
                tweet["geo"]["place"] = places[tweet["geo"]["place_id"]]
        except Exception as e:
            print('Error:', e, 'Tweet:', tweet)

    return tweets


def call_for_feature(feature, model, tokenizer, couchdb, redis, backfill=False):
    response = {"meta": {"next_token": None}}
    page = 0
    while "next_token" in response["meta"] and page < 10:
        next_token = response["meta"]["next_token"]
        print('Getting tweets for %s, token: %s...' % (feature["name"], next_token))
        page += 1

        # Get tweets from Twitter
        gt1 = time()
        try:
            response = api.get(
                endpoint='2/tweets/search/all',
                params=create_params(feature, next_token, backfill),
                couchdb=couchdb,
                redis=redis)
        except Exception as e:
            print(e)
            sleep(1)
            continue
        gt2 = time()
        print("%.2fs to get %s tweets in %s" % (
            gt2 - gt1,
            len(response["data"]) if "data" in response else 0,
            feature["name"]))

        if "data" not in response or len(response["data"]) == 0:
            continue

        tweets = format_response(response)

        # Add category prediction
        pt1 = time()
        for tweet in tweets:
            predictor = Predictor(
                tweet["text"], model, tokenizer, threshold=0.55)
            prediction = predictor.get_tweet_prediction()
            tweet["category"] = prediction
        pt2 = time()
        print("%.2fs to predict" % (pt2 - pt1))

        # Save to CouchDB
        t1 = time()
        couchdb["twitter"].bulk_docs(tweets)
        t2 = time()
        print("%.2fs to save" % (t2 - t1))

        sleep(1 - max(0, gt2 - t2))

    # TODO: if page >= 10: save url for later


def main():
    couchdb = CouchDB(
        user=os.environ["COUCHDB_USERNAME"],
        auth_token=os.environ["COUCHDB_PASSWORD"],
        url='http://%s:5984/' % os.environ["COUCHDB_HOST"],
        connect=True,
        auto_renew=True)
    redis = Redis(os.environ["REDIS_HOST"], 6379, 0)
    load_features(os.environ["MAP_PATH"], couchdb)

    # Load classifier
    start_time = time()
    model, tokenizer = load_model(os.environ["MODEL_PATH"])
    end_time = time()
    print("Loading Time: %.2fs" % (end_time - start_time))

    while True:
        feature = couchdb["features"].get_query_result(
            selector={"_id": {"$gt": None}},
            sort=[{"newest": "asc"}],
            limit=1
        ).all()[0]
        call_for_feature(feature, model, tokenizer,
                         couchdb, redis, backfill=False)

        feature_backfill = couchdb["features"].get_query_result(
            selector={"_id": {"$gt": None}},
            sort=[{"oldest": "desc"}],
            limit=1
        ).all()[0]
        call_for_feature(feature_backfill, model, tokenizer,
                         couchdb, redis, backfill=True)


if __name__ == "__main__":
    main()
