import tweepy
from accounts import accounts

COORD = {
  'lat': [-43.00311, -12.46113],
  'lon': [113.6594, 153.61194],
}

token = accounts[0]

# Authenticate to Twitter
auth = tweepy.OAuthHandler(token['c_key'], token['c_secret'])
auth.set_access_token(token['a_key'], token['a_secret'])

# Create API object
api = tweepy.API(auth)

res = api.search('COVID-19')
print(res)