# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 22:41:05 2019

@author: ASUS
"""

#Crawling Data
import tweepy

access_token = '284914146-1melXoz4t4Lw7YjH5az1wWyN53O63uFAJd8CEMPG'
access_token_secret = 'csFlA3HRXxlaJG1TtpM8LXvcORjh2Knqxabr8oKGLiC2l'
consumer_key = '70kixlsVWJ4u9wtP0If1n41By'
consumer_secret = 'pZ7XJnia0TCWS689XmmUEcY6PoZuxR6MLODXaUvR4qeco03Dxc'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

tweets = api.user_timeline('@fadlizon', count=5, tweet_mode='extended')
for t in tweets:
    print(t.full_text)
    print()
    
#buat list dari twitter
def list_tweets(user_id, count, prt=False):
    tweets = api.user_timeline(
        "@" + user_id, count=count, tweet_mode='extended')
    tw = []
    for t in tweets:
        tw.append(t.full_text)
        if prt:
            print(t.full_text)
            print()
    return tw

#cleaning data yang gak dibutuhin
import numpy as np
import re
def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)        
    return input_txt

def _removeNonAscii(s): 
    return "".join(i for i in s if ord(i)<128)

def clean_text(text):
    #text = text.lower()
    #text = re.sub(r"ya", " ", text)
    #text = re.sub(r"di", "  ", text)
    #text = re.sub(r"ini", " ", text)
    #text = re.sub(r"itu", " ", text)
    #text = re.sub(r"ada", " ", text)
    #text = re.sub(r"dan", " ", text)
    text = re.sub(r"yang", " ", text)
    #text = re.sub(r"kamu", " ", text)
    text = _removeNonAscii(text)
    text = text.strip()
    return text

def clean_lst(lst):
    lst_new = []
    for r in lst:
        lst_new.append(clean_text(r))
    return lst_new

def clean_tweets(lst):
    
    # remove twitter Return handles (RT @xxx:)
    lst = np.vectorize(remove_pattern)(lst, "RT @[\w]*:")
    # remove twitter handles (@xxx)
    lst = np.vectorize(remove_pattern)(lst, "@[\w]*")
    # remove URL links (httpxxx)
    lst = np.vectorize(remove_pattern)(lst, "https?://[A-Za-z0-9./]*")
    # remove punctuation 
    lst = np.core.defchararray.replace(lst, "[^\w\s]+", "")
    # remove special characters, numbers, punctuations (except for #)
    lst = np.core.defchararray.replace(lst, "[^a-zA-Z#]", " ")
    return lst

#menerjemahkan kata ke bahasa inggris
from googletrans import Translator
translator = Translator()
#text = translator.translate('Filmnya sangat buruk').text
#print(text)

#analisis sentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
#analyser.polarity_scores("The movie is bad")
#analyser.polarity_scores(text)

def sentiment_analyzer_scores(text, engl=True):
    if engl:
        trans = text
    else:
        trans = translator.translate(text).text    
    
    score = analyser.polarity_scores(trans)
    lb = score['compound']
    if lb >= 0.05:
        return 1
    elif (lb > -0.05) and (lb < 0.05):
        return 0
    else:
        return -1

#analisis sentiment dalam bentuk diagram
import seaborn as sns
def anl_tweets(lst, title='Tweets Sentiment', engl=True ):
    sents = []
    for tw in lst:
        try:
            st = sentiment_analyzer_scores(tw, engl)
            sents.append(st)
        except:
            sents.append(0)
    ax = sns.distplot(
        sents,
        kde=False,
        bins=3)
    ax.set(xlabel='Negative                Neutral                 Positive',
           ylabel='#Tweets',
          title="Tweets of @"+title)
    return sents

#read file stopwords.txt
stop_words = []
f = open('./data/stopwords.txt', 'r')
for l in f.readlines():
    stop_words.append(l.replace('\n', ''))

f = open('./data//stopwords-id.txt', 'r')
for l in f.readlines():
    stop_words.append(l.replace('\n', ''))

additional_stop_words = ['t', 'will']
stop_words += additional_stop_words

#analisis wordcloud
#from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
#from nltk.stem.porter import *

def word_cloud(wd_list):
    stopwords = stop_words + list(STOPWORDS)
    all_words = ' '.join([text for text in wd_list])
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        width=1600,
        height=800,
        random_state=21,
        colormap='jet',
        max_words=50,
        max_font_size=200).generate(all_words)
    
    plt.figure(figsize=(12, 10))
    plt.axis('off')
    plt.imshow(wordcloud, interpolation="bilinear");

#Test Jalankan semua perintah
user_id = 'fadlizon'
count = 200

tw_fadlizon = list_tweets(user_id, count)
tw_fadlizon = clean_tweets(tw_fadlizon)
tw_fadlizon = clean_lst(tw_fadlizon)
tw_fadlizon_sent = anl_tweets(tw_fadlizon, user_id)

sentiment_analyzer_scores(tw_fadlizon[2])

word_cloud(tw_fadlizon)