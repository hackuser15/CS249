import json
import pandas as pd
import string
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import warnings
warnings.filterwarnings("ignore")

def assignProductLabel(row):
    if(row['token'] in product_terms):
        return 'prod'
    else:
        return 'O'
def assignDummyProductLabel(row):
    return 'O'

with open('D:\WINTER\Big_Data_Analytics_CS249\Project\Code\src\\training-annotated.json') as data_file:
    ann_textItems = json.load(data_file)
dsmb_textItems = pd.read_csv('D:\WINTER\Big_Data_Analytics_CS249\Project\Code\src\\training-disambiguated-product-mentions.csv')
dsmb_textItems = dsmb_textItems.drop('documents',1)
dsmb_textItems = dsmb_textItems['id'].apply(lambda x: pd.Series(x.split(':')))
dsmb_textItems.columns = ['docid', 'range']
dsmb_textItems = dsmb_textItems.groupby('docid', as_index=False).agg({'range': lambda x: list(x)})
#print(dsmb_textItems)

ann_textItems = pd.DataFrame(list(ann_textItems['TextItem'].items()))
ann_textItems.columns = ['docid', 'text']

rows = []
ann_textItems.apply(lambda row: [rows.append([row['docid'], txt, index]) for index, txt in enumerate(row.text)], axis=1)
ann_textItems_new = pd.DataFrame(rows, columns=['docid','token','tokenid'])
#print(ann_textItems_new)

# Creating set of products
product_terms = set()
for index, row in dsmb_textItems.iterrows():
    textItemId = row['docid']
    range_list = row['range']
    for r in range_list:
        elem = r.split('-')
        start, end = map(int,elem)
        #print(textItemId,"-",start,":",end)
        df = ann_textItems_new[ann_textItems_new['docid'] == textItemId][start:end+1]
        # l1 = list(df['token'])
        l1 = [x for x in list(df['token']) if not x.isdigit()]
        # print(textItemId,":",l1)
        product_terms.update(l1[0:])

ann_textItems_new['label']= ann_textItems_new.apply (lambda row: assignProductLabel (row),axis=1)
ann_textItems_new['dummy']= ann_textItems_new.apply (lambda row: assignDummyProductLabel (row),axis=1)

# Data cleaning
stop = stopwords.words('english')
indexes = []
for i in range(0, len(ann_textItems_new['token'])):
    text = ann_textItems_new['token'][i]
    text = text.lower()
    if text in stop:
        indexes.append(i)
        continue
    text = BeautifulSoup(text,"lxml").get_text()
    text = "".join([ch for ch in text if ch not in string.punctuation])
    if not text:
        indexes.append(i)
ann_textItems_new.drop(ann_textItems_new.index[indexes],inplace=True)
ann_textItems_new = ann_textItems_new.reset_index(drop=True)

ann_textItems_new.to_csv('abcd', sep=' ', header=False , index=True)  #Training data for model

# Adding blank row after reach text item
prev_docid = ''
j=0
for i, row in ann_textItems_new.iterrows():
    curr_docid = row['docid']
    if(i > 0 and i < len(ann_textItems_new)-1 and curr_docid != prev_docid):
        df = ann_textItems_new[0:j]
        df = df.append({"docid": "","token":"","tokenid":"","label":"","dummy":""},ignore_index=True)
        df = df.append(ann_textItems_new[j:])
        ann_textItems_new = df
        j=j+1
    prev_docid = curr_docid
    j=j+1

stanford_train = ann_textItems_new[['token','label']]
stanford_test = ann_textItems_new[['token','dummy']]

stanford_train.to_csv('ner_stanford_train_product_new2', sep=' ', header=False , index=True)  #Training data for model
stanford_test.to_csv('ner_stanford_test_product_new2', sep=' ', header=False , index=False)    #dummy data testing on training set