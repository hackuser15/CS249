# NER using Stanford NLP - 3 class model Location, Person, Organization
# Download Stanford NER from http://nlp.stanford.edu/software/stanford-ner-2015-12-09.zip and place in project directory
# Set Environment Variable JAVA_HOME to point to java installation directory e.g. C:\Program Files\Java\jre1.8.0_66
# Output: [('Akshay', 'PERSON'), ('Shinde', 'PERSON'), ('is', 'O'), ('studying', 'O'), ('at', 'O'), ('University', 'ORGANIZATION'),
#           ('of', 'ORGANIZATION'), ('California', 'ORGANIZATION'), (',', 'O'), ('Los', 'LOCATION'), ('Angeles', 'LOCATION')]

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
    stop = stopwords.words('english')
    indexes = []
    for i in range(0, len(df['token'])):
        text = df['token'][i]
        text = text.lower()
        if text in stop:
            indexes.append(i)
            continue
        text = BeautifulSoup(text,"lxml").get_text()
        text = "".join([ch for ch in text if ch not in string.punctuation])
        if not text:
            indexes.append(i)
    df.drop(df.index[indexes],inplace=True)
    df = df.reset_index(drop=True)
    return df

def verticalizeTextItems(df):
    rows = []
    df.apply(lambda row: [rows.append([row['docid'], txt, index, row['occurence']]) for index, txt in enumerate(row.text)], axis=1)
    df = pd.DataFrame(rows, columns=['docid','token','tokenid','occurence'])
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

def assignProductLabel(row):
    if(checkWithinRange(row['tokenid'],row['occurence'])):
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

def predictLabelStanford(test_data):
    path_stanford = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '\stanford-ner-2015-12-09'
    # path_to_model = path_stanford + '\classifiers\english.all.3class.distsim.crf.ser.gz'
    path_to_model = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '\stanford.ner-model.products.gz'   #This is the model we trained on products data
    path_to_jar = path_stanford + '\stanford-ner.jar'

    st = StanfordNERTagger(path_to_model, path_to_jar)

    stanford_jars = find_jars_within_path(path_stanford)
    st._stanford_jar = ';'.join(stanford_jars)

    prediction = pd.DataFrame(columns=['docid','token','tokenid','pred_label'])
    docs = pd.Series(test_data['docid'].values.ravel()).unique()
    for doc in docs:
        op = st.tag(test_data[test_data['docid']==doc]['token'])
        op = pd.DataFrame(op, columns=['token','pred_label'])
        op['docid'] = pd.Series([doc for x in range(len(op.index))], index=op.index)
        prediction=prediction.append(op,ignore_index=True)
    return prediction

def getProductOccurence(prediction):
    final_list = pd.DataFrame(columns=['docid','occurences'])
    text_index = 0
    index_str="";
    seperator ="-"
    l = []
    i = 0
    prev_docid = ''
    while(i < len(prediction['pred_label'])):
        curr_docid = prediction['docid'][i]
        label = prediction['pred_label'][i]
        if(i>0 and curr_docid != prev_docid ):
            final_list=processTextItem(l, prev_docid, final_list)
            text_index = 0
            l.clear()
            i = i+1
            prev_docid = curr_docid
        elif(label == 'prod'):
            start_index = prediction['tokenid'][i]
            end_index = start_index
            while(label == 'prod' and curr_docid == prev_docid):
                prev_docid = curr_docid
                i = i+1
                curr_docid = prediction['docid'][i]
                end_index+=1
                text_index+=1
                label = str(prediction['pred_label'][i])
            l.append(str(start_index)+seperator+str(end_index-1))
        elif(label == 'O'):
            text_index +=1
            i = i+1
            prev_docid = curr_docid
    final_list=processTextItem(l, prediction['docid'][i-1], final_list)
    return final_list

def processTextItem(l, textItemID, final_list):
    if(len(l) > 0):
        r = l[0]
        final_list=final_list.append({"docid":textItemID,"occurences":r},ignore_index=True)
    return final_list

with open('training-annotated.json') as data_file:
    ann_textItems = json.load(data_file)

test_data = pd.read_csv('test.csv')

ann_textItems = pd.DataFrame(list(ann_textItems['TextItem'].items()))

ann_textItems.columns = ['docid', 'text']

dsmb_textItems = pd.read_csv('training-disambiguated-product-mentions.csv')
dsmb_textItems = dsmb_textItems.drop('documents',1)
dsmb_textItems = dsmb_textItems['id'].apply(lambda x: pd.Series(x.split(':')))
dsmb_textItems.columns = ['docid', 'occurence']
dsmb_textItems = dsmb_textItems.groupby('docid', as_index=False).agg({'occurence': lambda x: list(x)})

ann_textItems = pd.merge(ann_textItems, dsmb_textItems, on = 'docid')

train_textItems, test_textItems = splitData(ann_textItems)

train_data = verticalizeTextItems(train_textItems)
test_data = verticalizeTextItems(test_textItems)

train_data = cleanFrame(train_data)
test_data = cleanFrame(test_data)

train_data['label']= train_data.apply (lambda row: assignProductLabel (row),axis=1)
test_data['label']= test_data.apply (lambda row: assignProductLabel (row),axis=1)

# test_data = addBlanknLines(test_data)

train_data = train_data[['token','label']]
test_data = test_data[['docid','token','label']]

# train_data.to_csv('ner_train_data', sep='\t', header=False , index=False)  #Training data for model
test_data.to_csv('ner_test_data', sep='\t', header=False , index=False)    #dummy data testing on training set

#Prediction
pred_data = predictLabelStanford(test_data)
pred_data = getProductOccurence(pred_data)
print(pred_data)