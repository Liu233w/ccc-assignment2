#######################################################################################################
# This script is an example fpr predicting one tweet at a time
#
# - Import the `GetTweetPrediction` script
# - Define the path to the BERT_Classification_Model
# - Call `Load_Model` function with path to BERT_Classification_Model and get `model` and `tokenizer`
# - Call `GetTweetPrediction.Get_Prediction(tweet_text, model, tokenizer).Get_Tweet_Prediction()` to 
#     classify tweet
#
# NOTE: `tweet_text` is the tweet text you want to classify
# The `GetTweetPrediction` script classifies the tweet_text into the defined 10 classes.
# 
# IF the prediction probability of the predicted class is less than the `threshold` value, it classifies 
#   the tweet as `OTHER` class.
#######################################################################################################

import GetTweetPrediction
import time
from transformers import BertForSequenceClassification, BertConfig, AdamW, BertTokenizer, logging
import torch

# Define Data
tweet_text = "@LOLTrish hey  long time no see! Yes.. Rains a bit ,only a bit  LOL , I'm fine thanks , how's you ?"
bert_classification_model_path = '/Users/vihangajayalath/Desktop/UniMelb/Semester 4/Cluster and Cloud Computing/Assignment2/BERT_Classifier/BERT_classification_epoch_1.model'
threshold = 0.55

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


model, tokenizer = Load_Model(bert_classification_model_path)



# Predict
start_time = time.time()
prediction = GetTweetPrediction.Get_Prediction(tweet_text, model, tokenizer, threshold).Get_Tweet_Prediction()
print("\nPrediction: ",prediction)
end_time = time.time()
print("\nExecution Time: " + str(end_time - start_time))