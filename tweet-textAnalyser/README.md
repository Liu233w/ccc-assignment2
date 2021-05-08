## The `predict_tweets.py` script is an example for predicting one tweet at a time


The Steps to Classify a tweet defined on the `predict_tweets.py` script are as follows:
 - Import the `GetTweetPrediction.py` script
 - Define the path to the BERT_Classification_Model
 - Call `Load_Model` function with path to BERT_Classification_Model and get `model` and `tokenizer`
      ```
      def Load_Model(bert_classification_model_path):
          # Load Tokenizer and BERT Model
          logging.set_verbosity_error()
          tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', 
                                                  do_lower_case=True)

          model = BertForSequenceClassification.from_pretrained("bert-base-uncased",
                                                              num_labels=10,
                                                              output_attentions=False,
                                                              output_hidden_states=False)

          model.load_state_dict(torch.load(bert_classification_model_path, map_location=torch.device('cpu')))

          return model, tokenizer
      ```
 - Call `GetTweetPrediction.Get_Prediction(tweet_text, model, tokenizer).Get_Tweet_Prediction()` to classify tweet


NOTE: `tweet_text` is the tweet text you want to classify

The `GetTweetPrediction` script classifies the tweet_text into the defined 10 classes.

IF the prediction probability of the predicted class is less than the `threshold` value, it classifies the tweet as `OTHER` class.
