import re
import torch.nn.functional as F
import torch
import numpy as np


class Get_Prediction:

    def __init__(self, tweet_text, model, tokenizer, threshold):
        self.tweet_text = tweet_text
        self.model = model
        self.tokenizer = tokenizer
        self.threshold = threshold
        self.MAX_LEN = 128
        self.device = 'cpu'
        self.class_list = ['entertainment', 'business', 'technology', 'gaming', 'music', 'sports', 'politics', 'fashion', 'health', 'food']


    # Cleaning Tweet
    def Clean_Tweets(self, data):
        tweet_text_noLinks = (re.sub(r'(https:\/\/t\.co\/[\/\.a-z0-9]+)|(http:[\/\.a-z0-9]+)', ' ', (data).lower()))
        tweet_text_noPunc_noLinks = (re.sub(r'[,\.!?\/\;\:\#\\\'\"]', ' ', tweet_text_noLinks))
        tweet_text_noPunc_noLinks = re.sub(r'(\\n)|(\\t)|[\(\)\\]', ' ', tweet_text_noPunc_noLinks)
        tweet_text_noPunc_noLinks_noUser = re.sub(r'\@\w+', ' ', tweet_text_noPunc_noLinks)
        tweet_text_noPunc_noLinks_noUser = re.sub(r'\<.+\>', ' ', tweet_text_noPunc_noLinks_noUser)

        return tweet_text_noPunc_noLinks_noUser

    # Prediction Tweet
    def Predict_Tweet(self, prediction, Temp, class_list, threshold):
        softmax_preds = F.softmax(torch.tensor(prediction/Temp), dim=1)
        prediction = ''
        if float(max(softmax_preds[0])) > threshold:
            prediction = class_list[int(np.argmax(softmax_preds[0]))]
        else:
            prediction = 'OTHER'
        return prediction


    def Get_Tweet_Prediction(self):
        # Encoding Tweet
        encoded_tweet_text = self.tokenizer.encode_plus(
            self.Clean_Tweets(self.tweet_text), 
            add_special_tokens=True, 
            return_attention_mask=True, 
            pad_to_max_length=True, 
            padding='max_length',
            max_length=self.MAX_LEN, 
            return_tensors='pt',
            truncation=True
        )

        inputs = {'input_ids':      encoded_tweet_text['input_ids'],
                  'attention_mask': encoded_tweet_text['attention_mask'],
                  }

        # Get Predictions
        with torch.no_grad():        
            outputs = self.model(**inputs)

        logits = outputs['logits']
        logits = logits.detach().cpu().numpy()
        softmax_prediction = self.Predict_Tweet(logits, 1, self.class_list, self.threshold)

        return softmax_prediction
