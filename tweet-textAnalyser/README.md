## The `predict_tweets.py` script is an example for predicting one tweet at a time

The scripts in this repository use Python3
Install the python packages of `requirements.txt` using `pip install -r requirements.txt` command.

The Steps to Classify a tweet defined on the `predict_tweets.py` script are as follows:
 - Import the `GetTweetPrediction.py` script
 - Define the path to the BERT_Classification_Model
 - Call `Load_Model` function with path to BERT_Classification_Model and get `model` and `tokenizer`
 - Call `GetTweetPrediction.Get_Prediction(tweet_text, model, tokenizer).Get_Tweet_Prediction()` to classify tweet




**NOTE**: `tweet_text` is the tweet text you want to classify

The `GetTweetPrediction` script classifies the tweet_text into the defined 10 classes.

IF the prediction probability of the predicted class is less than the `threshold` value, it classifies the tweet as `OTHER` class.


- The link to the BERT Classification Model: https://drive.google.com/drive/folders/1AJ85PaV6kTHsdB14ljZsy_uRIM3KncK_?usp=sharing

## Classes
 - entertainment
 - business
 - technology
 - gaming
 - music
 - sports
 - politics
 - fashion
 - health
 - food
 - OTHER
