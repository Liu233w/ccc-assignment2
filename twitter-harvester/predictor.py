import re
import numpy as np
import torch.nn.functional as F
import torch
from transformers import BertForSequenceClassification, BertTokenizer, logging


class Predictor:
    def __init__(self, tweet_text, model, tokenizer, threshold):
        self.tweet_text = tweet_text
        self.model = model
        self.tokenizer = tokenizer
        self.threshold = threshold
        self.MAX_LEN = 128
        self.device = 'cpu'
        self.class_list = ['entertainment', 'business', 'technology', 'gaming', 'music', 'sports', 'politics', 'fashion', 'health', 'food']

    # Cleaning Tweet
    def clean_tweets(self, data):
        tweet_text_noLinks = (re.sub(r'(https:\/\/t\.co\/[\/\.a-z0-9]+)|(http:[\/\.a-z0-9]+)', ' ', (data).lower()))
        tweet_text_noPunc_noLinks = (re.sub(r'[,\.!?\/\;\:\#\\\'\"]', ' ', tweet_text_noLinks))
        tweet_text_noPunc_noLinks = re.sub(r'(\\n)|(\\t)|[\(\)\\]', ' ', tweet_text_noPunc_noLinks)
        tweet_text_noPunc_noLinks_noUser = re.sub(r'\@\w+', ' ', tweet_text_noPunc_noLinks)
        tweet_text_noPunc_noLinks_noUser = re.sub(r'\<.+\>', ' ', tweet_text_noPunc_noLinks_noUser)

        return tweet_text_noPunc_noLinks_noUser

    # Prediction Tweet
    def predict_tweet(self, prediction, Temp, class_list, threshold):
        softmax_preds = F.softmax(torch.tensor(prediction/Temp), dim=1)
        prediction = ''
        if float(max(softmax_preds[0])) > threshold:
            prediction = class_list[int(np.argmax(softmax_preds[0]))]
        else:
            prediction = 'OTHER'
        return prediction

    def get_tweet_prediction(self):
        # Encoding Tweet
        encoded_tweet_text = self.tokenizer.encode_plus(
            self.clean_tweets(self.tweet_text),
            add_special_tokens=True,
            return_attention_mask=True,
            pad_to_max_length=True,
            padding='max_length',
            max_length=self.MAX_LEN,
            return_tensors='pt',
            truncation=True
        )

        inputs = {
            'input_ids':      encoded_tweet_text['input_ids'],
            'attention_mask': encoded_tweet_text['attention_mask'],
        }

        # Get Predictions
        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs[0]
        logits = logits.detach().cpu().numpy()
        softmax_prediction = self.predict_tweet(logits, 1, self.class_list, self.threshold)

        return softmax_prediction


def load_model(bert_classification_model_path):
    # Load Tokenizer and BERT Model
    logging.set_verbosity_error()
    tokenizer = BertTokenizer.from_pretrained(
        "bert-base-uncased",
        do_lower_case=True)

    model = BertForSequenceClassification.from_pretrained(
        "bert-base-uncased",
        num_labels=10,
        output_attentions=False,
        output_hidden_states=False)

    model.load_state_dict(torch.load(bert_classification_model_path, map_location=torch.device('cpu')))

    return model, tokenizer
