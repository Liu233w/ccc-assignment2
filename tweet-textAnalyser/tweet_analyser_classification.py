import tweepy
from accounts import accounts
from nltk.corpus import wordnet
import pandas as pd 
import numpy as np 

# Product Topics -----------------------------------------------------------------
# 1) Sport
# 2) IT
# 3) Cooking and Food
# 4) Education
# 5) Pet
# 6) Cosmetic and Fashion
# 7) Car 
# 8) House
# /Product Topics -----------------------------------------------------------------


# Topics
topics_list = ['sports', 'tech', 'food', 'pets', 'fashion', 'car', 'house']

def Get_Syns_List(topics):
    topic_syns_list = []
    for topic in topics:
        syns = wordnet.synsets(topic)
        syns_lists = [s.lemmas() for s in syns]
        flatten_syns_lists = set([item.name() for sublist in syns_lists for item in sublist])
        topic_syns_list.append(flatten_syns_lists)

    return topic_syns_list

all_topic_syns = Get_Syns_List(topics_list)

print(f'{all_topic_syns}\n')


# product_categories_df = pd.read_csv('shopmania.csv', header=None)
# # product_categories_df = pd.read_csv('pricerunner_aggregate.csv', header=None)
# product_categories = pd.DataFrame(set(product_categories_df[3]))
# for pr in set(product_categories[0]):
#     print(pr)


# sports = []
# tech = []
# food = []
# pets = []
# fashion = []
# car = []
# house = []

# for pr in product_categories[0]:
#     sports_list = ['sport', 'golf', 'ball']
#     tech_list = ['audio', 'video', 'cpu', 'mobile', 'bateries', 'dvd', 'gpu', 'cable', 'power', 'network', 'fan', 'keyboard', 'mouse', 'tablet', 'memory', 'micro']
#     food_list = ['food', 'cook']
#     pets_list = []
#     fashion_list = ['cloth', 'cosmetic', 'care', 'bath']
#     car_list = ['motor', 'car']
#     house_list = ['home', 'microwave', 'garden']






# Harvesting Tweets
'''
COORD = {
  'lat': [-43.00311, -12.46113],
  'lon': [113.6594, 153.61194],
}

token = accounts[0]

# Authenticate to Twitter
auth = tweepy.OAuthHandler(token['consumer_key'], token['consumer_secret'])
auth.set_access_token(token['access_token'], token['access_token_secret'])

# Create API object
api = tweepy.API(auth)

res = api.search('food')
print(res)
'''

