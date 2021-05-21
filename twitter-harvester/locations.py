import json
from cloudant.client import CouchDB
from datetime import datetime
from hashlib import sha1


def load_features(filepath, couchdb: CouchDB):
    if "features" not in couchdb.all_dbs():
        couchdb.create_database("features", partitioned=False)
        couchdb["features"].create_query_index(fields=["newest"])
        couchdb["features"].create_query_index(fields=[{"oldest": "desc"}])

    poly_features = []
    with open(filepath) as file:
        content = file.read()
        polygons = json.loads(content)
        poly_features = polygons["features"]

    features = []
    for feature in poly_features:
        coords = feature["geometry"]["coordinates"]
        box = [None, None, None, None]

        for x in coords:
            for y in x:
                for z in y:
                    if box[0] is None or z[0] < box[0]:
                        box[0] = z[0]
                    if box[1] is None or z[1] < box[1]:
                        box[1] = z[1]
                    if box[2] is None or z[0] > box[2]:
                        box[2] = z[0]
                    if box[3] is None or z[1] > box[3]:
                        box[3] = z[1]

        id = sha1(json.dumps(box).encode('utf8')).digest().hex()
        features.append({
            "id": id,
            "name": feature["properties"]["name"],
            "box": box
        })

    docs = couchdb["features"].get_query_result(
        selector={
            "_id": {
                "$gt": None
            }
        }).all()

    known_ids = list(map(lambda doc: doc["_id"], docs))
    new_features = list(filter(lambda feature: feature["id"] not in known_ids, features))

    timestamp = int(datetime.utcnow().timestamp())
    new_docs = list(map(lambda feature: {
        "_id": feature["id"],
        "box": feature["box"],
        "name": feature["name"],
        "newest": timestamp,
        "oldest": timestamp
    }, new_features))
    couchdb["features"].bulk_docs(new_docs)

    return features
