import os
from time import sleep, time
from datetime import datetime
from cloudant.client import CouchDB
from redis import Redis
import math
import api
from locations import get_features
from predictor import Predictor, load_model


def create_params(bounding_box, next_token):
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
        "max_results": 500
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
        if "author_id" in tweet:
            tweet["author"] = users[tweet["author_id"]]
        if "place_id" in tweet["geo"] and "coordinates" not in tweet["geo"]:
            tweet["geo"]["place"] = places[tweet["geo"]["place_id"]]

    return tweets


def main():
    couchdb = CouchDB(
        user=os.environ["COUCHDB_USERNAME"],
        auth_token=os.environ["COUCHDB_PASSWORD"],
        url='http://%s:5984/' % os.environ["COUCHDB_HOST"],
        connect=True,
        auto_renew=True)
    redis = Redis(os.environ["REDIS_HOST"], 6379, 0)
    features = get_features(os.environ["MAP_PATH"])
    bert_classification_model_path = os.environ["MODEL_PATH"]

    # Load classifier
    start_time = time()
    model, tokenizer = load_model(bert_classification_model_path)
    end_time = time()
    print("Loading Time: %.2fs" % (end_time - start_time))

    for feature in features:
        response = {"meta": {"next_token": None}}
        page = 0
        while "next_token" in response["meta"] and page < 10:
            page += 1

            # Get tweets from Twitter
            gt1 = time()
            response = api.get(
                endpoint='2/tweets/search/all',
                params=create_params(feature["box"], response["meta"]["next_token"]),
                couchdb=couchdb,
                redis=redis)
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
                predictor = Predictor(tweet["text"], model, tokenizer, threshold=0.55)
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


if __name__ == "__main__":
    main()
