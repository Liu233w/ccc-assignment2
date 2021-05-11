import os

class Config:
  COUCHDB_URL = os.environ.get("COUCHDB_URL") or 'http://admin:uJNh4NwrEt59o7@172.26.129.48:5984'