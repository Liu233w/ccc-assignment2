import tweepy
from accounts import accounts

token = accounts[0]

# Authenticate to Twitter
auth = tweepy.OAuthHandler(token['c_key'], token['c_secret'])
auth.set_access_token(token['a_key'], token['a_secret'])

# Create API object
api = tweepy.API(auth)

res = api.search('COVID-19')
print(res)