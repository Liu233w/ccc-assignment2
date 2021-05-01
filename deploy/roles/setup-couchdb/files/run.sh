#!/bin/bash

set -e

docker run\
  --name couchdb\
  --env COUCHDB_USER=${COUCH_DB_USER} \
  --env COUCHDB_PASSWORD=${COUCH_DB_PASS} \
  --env COUCHDB_SECRET=${COUCH_DB_SECRET} \
  --env ERL_FLAGS="-setcookie \"${COUCH_DB_SECRET}\" -name \"couchdb@${HOST_IP}\"" \
  -p 5984:5984 \
  -v /home/couchdb/data:/mnt/data/couchdb \
  ibmcom/couchdb3:${COUCH_DB_VERSION}