import os
import string
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tag import StanfordNERTagger
from nltk.internals import find_jars_within_path
import numpy as np
import json
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def splitData(df):
    msk = np.random.rand(len(df)) < 0.8
    train = df[msk]
    test = df[~msk]
    return train, test

def cleanFrame(df):
    df['token']=df['token'].replace(to_replace='\n', value='', regex = True)
    indexes = []
    for i in range(0, len(df['token'])):
        text = df['token'][i]
        text = text.replace('\n','')
        text = text.lower()
        text = BeautifulSoup(text,"lxml").get_text()
        text = "".join([ch for ch in text if ch not in string.punctuation])
        if not text:
            indexes.append(i)
    df.drop(df.index[indexes],inplace=True)
    df = df.reset_index(drop=True)
    return df

def verticalizeTextItems(df):
    rows = []
    df.apply(lambda row: [rows.append([row['docid'], txt, index]) for index, txt in enumerate(row.text)], axis=1)
    df = pd.DataFrame(rows, columns=['docid','token','tokenid'])
    return df

def checkWithinRange(num,list):
    for x in list:
        elem = x.split('-')
        if len(elem) == 1:
            if num == int(elem[0]):
                return  True
        elif len(elem) == 2:
            start, end = map(int,elem)
            if start <= num <= end:
                return True
        else: # more than one hyphen
            return False
    return False

def assignProductLabel(row, product_terms):
    if(row['token'] in product_terms):
        return 'prod'
    else:
        return 'O'

def assignDummyProductLabel(row):
    return 'O'

def addBlanknLines(data):
    # Adding blank row after reach text item
    prev_docid = ''
    j=0
    for i, row in data.iterrows():
        curr_docid = row['docid']
        if(i > 0 and i < len(data)-1 and curr_docid != prev_docid):
            df = data[0:j]
            df = df.append({"docid": "","token":"","tokenid":"","label":"","dummy":""},ignore_index=True)
            df = df.append(data[j:])
            data = df
            j=j+1
        prev_docid = curr_docid
        j=j+1
    return data

path_dataset = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '\Dataset'
with open(path_dataset+ r'\training-annotated-text.json') as data_file:
    train_data = json.load(data_file)

train_data = pd.DataFrame(list(train_data['TextItem'].items()))

train_data.columns = ['docid', 'text']

train_data = verticalizeTextItems(train_data)

dsmb_textItems = pd.read_csv(path_dataset+ r'\training-disambiguated-product-mentions.csv')
dsmb_textItems.columns = ['id', 'documents']
dsmb_textItems = dsmb_textItems.drop('documents',1)
dsmb_textItems = dsmb_textItems['id'].apply(lambda x: pd.Series(x.split(':')))
dsmb_textItems.columns = ['docid', 'occurence']
dsmb_textItems = dsmb_textItems.groupby('docid', as_index=False).agg({'occurence': lambda x: list(x)})

# Creating set of products
product_terms = set()
for index, row in dsmb_textItems.iterrows():
    textItemId = row['docid']
    range_list = row['occurence']
    for r in range_list:
        elem = r.split('-')
        start, end = map(int,elem)
        df = train_data[train_data['docid'] == textItemId][start:end+1]
        l1 = [x for x in list(df['token']) if not x.isdigit()]
        product_terms.update(l1[0:])

product_terms.remove("'s")

train_data['label']= train_data.apply (lambda row: assignProductLabel (row, product_terms),axis=1)

train_data = cleanFrame(train_data)

train_data = train_data[['token','label']]

path_intermediate = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '\Intermediate_files\\'
train_data.to_csv(path_intermediate + 'ner_stanford_train_data', sep='\t', header=False , index=False)  #Training data for model
