import os
from time import sleep, time
from datetime import datetime, timedelta
from cloudant.client import CouchDB
from redis import Redis
import math
import api
from features import load_features
from predictor import Predictor, load_model


def create_params(feature, next_token, start_time, end_time):

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

    params = {
        "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end_time": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "query": "lang:EN -place:melbourne %s" % box_query,  # max 1,024 characters
        "user.fields": "url",
        "expansions": "geo.place_id,author_id",
        "tweet.fields": "author_id,created_at,geo,id,source,text",
        "place.fields": "full_name,geo,place_type",
        "user.fields": "location,username",
        "max_results": 300,
    }

    if next_token:
        params["next_token"] = next_token

    return params


def get_time_interval(feature, backfill) -> "tuple[datetime, datetime]":
    # Get the start and end times
    start_time = None
    end_time = None
    if not backfill:
        if (feature["newest"] is None):
            start_time = datetime.utcnow() - timedelta(days=30)
        else:
            start_time = datetime.fromtimestamp(feature["newest"])
        end_time = datetime.utcnow() - timedelta(seconds=30)
    else:
        if (feature["oldest"] is None):
            end_time = datetime.utcnow() - timedelta(days=30)
        else:
            end_time = datetime.fromtimestamp(feature["oldest"])
        start_time = end_time - timedelta(days=30)

    # Keep times within Twitter limits
    if start_time < datetime(2006, 4, 1):
        start_time = datetime(2006, 4, 1)

    return start_time, end_time


def update_location_info(feature, start_time: datetime, end_time: datetime, backfill: bool, couchdb: CouchDB):
    doc = couchdb["features"][feature["_id"]]
    if not backfill:
        doc["newest"] = int(end_time.timestamp())
    else:
        doc["oldest"] = int(start_time.timestamp())

    doc.save()


def format_response(response, feature):
    places = {}
    users = {}
    tweets = response["data"]

    if "includes" in response:
        if "places" in response["includes"]:
            places = {x["id"]: x for x in response["includes"]["places"]}
        if "users" in response["includes"]:
            users = {x["id"]: x for x in response["includes"]["users"]}

    for tweet in tweets:
        # Partition by year
        partition_key = datetime.fromisoformat(tweet["created_at"][:-1]).strftime("%Y%m")
        id = tweet["id"]
        tweet["_id"] = "%s:%s" % (partition_key, id)
        tweet["feature"] = {
            "_id": feature["_id"],
            "name": feature["name"],
            "loc_pid": feature["loc_pid"] if "loc_pid" in feature else None
        }
        try:
            if "author_id" in tweet:
                tweet["author"] = users[tweet["author_id"]]
            if "place_id" in tweet["geo"] and "coordinates" not in tweet["geo"]:
                tweet["geo"]["place"] = places[tweet["geo"]["place_id"]]
        except Exception as e:
            print("Error:", e, "Tweet:", tweet)

    return tweets


def call_for_feature(feature, model, tokenizer, couchdb, redis, backfill=False):
    response = {"meta": {"next_token": None}}
    start_time, end_time = get_time_interval(feature, backfill)

    page = 0
    while "next_token" in response["meta"] and page < 10:
        next_token = response["meta"]["next_token"]
        print("Getting tweets for %s between %s and %s%s" % (
            feature["name"],
            start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            ", next_token: %s..." % next_token if next_token else ""))
        page += 1

        # Get tweets from Twitter
        gt1 = time()
        try:
            response = api.get(
                endpoint="2/tweets/search/all",
                params=create_params(feature, next_token, start_time, end_time),
                couchdb=couchdb,
                redis=redis)
        except Exception as e:
            print(e)
            sleep(1)
            break
        gt2 = time()
        print("%.2fs to get %s tweets from %s" % (
            gt2 - gt1,
            len(response["data"]) if "data" in response else 0,
            feature["name"]))

        update_location_info(feature, start_time, end_time, backfill, couchdb)

        if "data" not in response or len(response["data"]) == 0:
            break

        tweets = format_response(response, feature)

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

    # TODO: if page >= 10: save url for later


def main():
    print("Connecting to services...")
    couchdb = CouchDB(
        user=os.environ["COUCHDB_USERNAME"],
        auth_token=os.environ["COUCHDB_PASSWORD"],
        url="http://%s:5984/" % os.environ["COUCHDB_HOST"],
        connect=True,
        auto_renew=True)
    redis = Redis(os.environ["REDIS_HOST"], 6379, 0)

    # Load features
    print("Loading features...")
    start_time = time()
    load_features(os.environ["MAP_PATH"], couchdb)
    print("Loading Time: %.2fs" % (time() - start_time))

    # Load classifier
    print("Loading classifier...")
    start_time = time()
    model, tokenizer = load_model(os.environ["MODEL_PATH"])
    print("Loading Time: %.2fs" % (time() - start_time))

    while True:
        backfill = False
        result = couchdb["features"].get_query_result(
            selector={
                "newest": {
                    "$or": [
                        {"$exists": False},
                        {"$lt": int((datetime.utcnow() - timedelta(days=1)).timestamp())}
                    ]
                }
            },
            sort=[{"newest": "asc"}],
            limit=1
        ).all()
        if len(result) == 0:
            backfill = True
            result = couchdb["features"].get_query_result(
                selector={"oldest": {"$or": [{"$exists": False}, None]}},
                limit=1
            ).all()
            if len(result) == 0:
                result = couchdb["features"].get_query_result(
                    selector={"oldest": {"$gt": datetime(2006, 4, 1).timestamp()}},
                    sort=[{"oldest": "desc"}],
                    limit=1
                ).all()

        if len(result) == 0:
            print("No jobs...")
            sleep(3600)
            continue

        feature = result[0]
        print("Calling %sfor feature: %s..." % (
            "backfill " if backfill else "",
            feature["_id"]))
        call_for_feature(feature, model, tokenizer,
                         couchdb, redis, backfill)


if __name__ == "__main__":
    main()
