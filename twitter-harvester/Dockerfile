FROM python:3.7-slim as final
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

COPY . .

ENV COUCHDB_HOST ''
ENV COUCHDB_USERNAME ''
ENV COUCHDB_PASSWORD ''
ENV REDIS_HOST ''
ENV MAP_PATH '/app/polygons.json'
ENV MODEL_PATH '/opt/bert.model'

ENTRYPOINT [ "python", "harvester.py" ]
