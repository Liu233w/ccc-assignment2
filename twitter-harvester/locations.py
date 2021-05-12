import json


def get_features(filepath):
    features = []
    with open(filepath) as file:
        content = file.read()
        polygons = json.loads(content)
        features = polygons["features"]
        for feature in features:
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
            feature["bounding_box"] = box

        features = [
            {
                "name": feature["properties"]["name"],
                "box": feature["bounding_box"]
            }
            for feature in features
        ]

    return features
