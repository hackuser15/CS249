import re

import nltk
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def lemmatize_tokens(stems, lemmatizer):
    lemmatized = []
    for item in stems:
        lemmatized.append(lemmatizer.lemmatize(item))
    return lemmatized

import string

def tokenize(text):
    text = BeautifulSoup(text,"lxml").get_text()
    text = "".join([ch for ch in text if ch not in string.punctuation])
    text = "".join([ch for ch in text if ch not in string.digits])
    #text = re.sub("[^a-zA-Z]", " ", text)
    #print(text)
    tokens = nltk.word_tokenize(text)
    #lemma = lemmatize_tokens(tokens, lemmatizer)
    #print(lemma)
    stems = stem_tokens(tokens, stemmer)
    return stems
import pandas as pd
import time
start_time = time.time()


data = pd.read_csv("test.csv")
q=data['Value']  # as a Series
v=data['Value'].values  # as a numpy array
f1 = open("test.csv","r").read()
list1=[]
list1.append(f1)
#vectorizer = CountVectorizer(input='content',ngram_range=(1, 1), min_df=1, max_features=500, tokenizer=tokenize, stop_words='english')
vectorizer = TfidfVectorizer(input='content',ngram_range=(1, 1), tokenizer=tokenize, stop_words='english')
#print(vectorizer)
# punctuations,numbers,lowercase,stemming,bigrams,html tags    ---> profanity,cotext,match word with dict,lentgh word > 2
#corpus = ['This is the firsts run <b>bold ? DONT document.','This is <u>the running  RAN second second document.','And the the the SECOND third one.','Is this the first document?']
X = vectorizer.fit_transform(v)
#print("tranform\n",X)
#analyze = vectorizer.build_analyzer()
#print("analyze\n",analyze)
print(vectorizer.get_feature_names())
print(X.toarray())
print(X.shape)

print("--- %s seconds ---" % (time.time() - start_time))