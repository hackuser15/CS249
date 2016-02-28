# NER using Stanford NLP - 3 class model Location, Person, Organization
# Download Stanford NER from http://nlp.stanford.edu/software/stanford-ner-2015-12-09.zip and place in project directory
# Set Environment Variable JAVA_HOME to point to java installation directory e.g. C:\Program Files\Java\jre1.8.0_66
# Output: [('Akshay', 'PERSON'), ('Shinde', 'PERSON'), ('is', 'O'), ('studying', 'O'), ('at', 'O'), ('University', 'ORGANIZATION'),
#           ('of', 'ORGANIZATION'), ('California', 'ORGANIZATION'), (',', 'O'), ('Los', 'LOCATION'), ('Angeles', 'LOCATION')]
import os
import string

import nltk
from nltk import word_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tag import StanfordNERTagger
from nltk.internals import find_jars_within_path
import json
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

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

rows = []
ann_textItems.apply(lambda row: [rows.append([row['docid'], txt, index, row['occurence']]) for index, txt in enumerate(row.text)], axis=1)
ann_textItems_new = pd.DataFrame(rows, columns=['docid','token','tokenid','occurence'])
ann_textItems_new['label']= ann_textItems_new.apply (lambda row: assignProductLabel (row),axis=1)
ann_textItems_new['dummy']= ann_textItems_new.apply (lambda row: assignDummyProductLabel (row),axis=1)
stop = stopwords.words('english')
indexes = [];
for i in range(0, len(ann_textItems_new['token'])):
    text = ann_textItems_new['token'][i]
    if text in stop:
        indexes.append(i)
        continue
    text = text.lower()
    text = BeautifulSoup(text,"lxml").get_text()
    text = "".join([ch for ch in text if ch not in string.punctuation])
    if not text:
        indexes.append(i)
ann_textItems_new.drop(ann_textItems_new.index[indexes],inplace=True)
stanford_train = ann_textItems_new[['token','label']]
stanford_test = ann_textItems_new[['token','dummy']]

stanford_train.to_csv('ner_stanford_train_products', sep='\t', header=False , index=False)  #Training data for model
stanford_test.to_csv('ner_stanford_test_products', sep='\t', header=False , index=False)    #dummy data testing on training set

path_stanford = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '\stanford-ner-2015-12-09'
# path_to_model = path_stanford + '\classifiers\english.all.3class.distsim.crf.ser.gz'
path_to_model = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '\stanford.ner-model.products.gz'   #This is the model we trained on products data
path_to_jar = path_stanford + '\stanford-ner.jar'
st = StanfordNERTagger(path_to_model, path_to_jar)

stanford_dir = st._stanford_jar.rpartition('\\')[0]

stanford_jars = find_jars_within_path(path_stanford)
st._stanford_jar = ';'.join(stanford_jars)
print(st._stanford_jar)
print(st.tag(nltk.word_tokenize(test_data['Value'][50])))














