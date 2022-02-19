
import pandas as pd
import re
import numpy as np
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from gensim.models import Word2Vec
import pickle

w2v_model = Word2Vec.load('model.w2v')
model = load_model('model.h5')
with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)
with open('encoder.pkl', 'rb') as handle:
    encoder = pickle.load(handle)


#KERAS
SEQUENCE_LENGTH = 300
EPOCHS = 8
BATCH_SIZE = 1024

#SENTIMENT
POSITIVE = "POSITIVE"
NEGATIVE = "NEGATIVE"
NEUTRAL = "NEUTRAL"
SENTIMENT_THRESHOLDS = (0.4, 0.7)


def decode_sentiment(score, include_neutral=True):
    if include_neutral:
        label = NEUTRAL
        if score <= SENTIMENT_THRESHOLDS[0]:
            label = NEGATIVE
        elif score >= SENTIMENT_THRESHOLDS[1]:
            label = POSITIVE
        return label
    else:
        return NEGATIVE if score < 0.5 else POSITIVE


def predict(text, include_neutral=True):
    #Tokenize text
    x_text = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=SEQUENCE_LENGTH)
    #predict
    score = model.predict([x_text])[0]
    #decode sentiment
    label = decode_sentiment(score, include_neutral=include_neutral)
    return {"label": label, "score": float(score)}

df = pd.read_csv('tweets.csv')
clean_text1 = df['Tweets'].tolist()

def remove_emojis(text):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', text)

clean_text2 = []

for sentence in clean_text1:
    clean_text2.append(remove_emojis(sentence))


def removehtml(text):
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(CLEANR, '', text)
    return cleantext


clean_text3 = []

for sentence in clean_text2:
    clean_text3.append(removehtml(sentence))


clean_text4 = []

for sentence in clean_text3:
    clean_text4.append(re.sub(r'[^\w\s]', '', sentence))


def replace_words(text):
    text.replace("no", "dont")
    text.replace("not", "dont")
    return text


clean_text5 = []

for sentence in clean_text4:
    clean_text5.append(replace_words(sentence))


def to_low(text):
    new_text = text.lower()
    return new_text


clean_text6 = []

for sentence in clean_text4:
    clean_text6.append(to_low(sentence))


clean_text7 = []

for sentence in clean_text6:
    clean_text7.append(predict(sentence))

