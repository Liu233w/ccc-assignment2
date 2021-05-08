# The `predict_tweet.py` script is an example fpr predicting one tweet at a time


The Steps to Classify a tweet are as follows:
 - Import the `GetTweetPrediction` script
 - Define the path to the BERT_Classification_Model
 - Call `Load_Model` function with path to BERT_Classification_Model and get `model` and `tokenizer`
 - Call `GetTweetPrediction.Get_Prediction(tweet_text, model, tokenizer).Get_Tweet_Prediction()` to classify tweet


NOTE: `tweet_text` is the tweet text you want to classify

The `GetTweetPrediction` script classifies the tweet_text into the defined 10 classes.

IF the prediction probability of the predicted class is less than the `threshold` value, it classifies the tweet as `OTHER` class.
