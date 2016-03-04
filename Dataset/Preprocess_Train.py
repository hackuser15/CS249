import json

import pandas as pd
import string
from bs4 import BeautifulSoup
import csv
from nltk.corpus import stopwords


def assignProductLabel(row):
    if(row['token'] in product_terms):
        return 'prod'
    else:
        return 'O'
def assignDummyProductLabel(row):
    return 'O'

with open('/Users/avneet/Desktop/CS249/Dataset/training-annotated-text.json') as data_file:
    ann_textItems = json.load(data_file)

with open('/Users/avneet/Desktop/CS249/Dataset/testing-annotated-text.json') as data_file:
    test_ann_textItems = json.load(data_file)


dsmb_textItems = pd.read_csv('/Users/avneet/Desktop/CS249/Dataset/training-disambiguated-product-mentions.csv')
dsmb_textItems = dsmb_textItems.drop('documents',1)
dsmb_textItems = dsmb_textItems['id'].apply(lambda x: pd.Series(x.split(':')))
dsmb_textItems.columns = ['docid', 'range']
dsmb_textItems = dsmb_textItems.groupby('docid', as_index=False).agg({'range': lambda x: list(x)})
#print(dsmb_textItems)

ann_textItems = pd.DataFrame(list(ann_textItems['TextItem'].items()))
ann_textItems.columns = ['docid', 'text']

test_ann_textItems = pd.DataFrame(list(test_ann_textItems['TextItem'].items()))
test_ann_textItems.columns = ['docid', 'text']



rows = []
ann_textItems.apply(lambda row: [rows.append([row['docid'], txt, index]) for index, txt in enumerate(row.text)], axis=1)
ann_textItems_new = pd.DataFrame(rows, columns=['docid','token','tokenid'])


rows = []
test_ann_textItems.apply(lambda row: [rows.append([row['docid'], txt, index]) for index, txt in enumerate(row.text)], axis=1)
test_ann_textItems_new = pd.DataFrame(rows, columns=['docid','token','tokenid'])

product_terms = set()
#print(dsmb_textItems)

for index, row in dsmb_textItems.iterrows():
    textItemId = row['docid']
    range_list = row['range']
    for r in range_list:
        elem = r.split('-')
        start, end = map(int,elem)
        #print(textItemId,"-",start,":",end)
        df = ann_textItems_new[ann_textItems_new['docid'] == textItemId][start:end+1]
        l1 = list(df['token'])
        #print(textItemId,":",l1)
        product_terms.update(l1[0:])

#print(ann_textItems_new)



ann_textItems_new['label']= ann_textItems_new.apply (lambda row: assignProductLabel (row),axis=1)
#ann_textItems_new['dummy']= ann_textItems_new.apply (lambda row: assignDummyProductLabel (row),axis=1)

test_ann_textItems_new['dummy'] = test_ann_textItems_new.apply (lambda row: assignDummyProductLabel (row),axis=1)

#stanford_train = ann_textItems_new[['token','label']]
#test_ann_textItems_new = test_ann_textItems_new[['token','dummy']]

#Data cleaning - train
stop = stopwords.words('english')
indexes = []
for i in range(0, len(ann_textItems_new['token'])):
    text = ann_textItems_new['token'][i]
    text = text.lower()
    if text in stop or text in string.punctuation:
        indexes.append(i)
        continue
    #text = BeautifulSoup(text,"lxml").get_text()
    text = "".join([ch for ch in text if ch not in string.punctuation])
    if not text:
        indexes.append(i)
ann_textItems_new.drop(ann_textItems_new.index[indexes],inplace=True)

#Data cleaning - test Will change indices?

#Inserting blank lines for training data
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


test_ids =[]
#Inserting blank lines for test data
prev_docid = ''
j=0
for i, row in test_ann_textItems_new.iterrows():
    curr_docid = row['docid']
    if(i > 0 and i < len(test_ann_textItems_new)-1 and curr_docid != prev_docid):
        test_ids.append(prev_docid)
        df = test_ann_textItems_new[0:j]
        df = df.append({"docid": "","token":"","tokenid":"","label":"","dummy":""},ignore_index=True)
        df = df.append(test_ann_textItems_new[j:])
        test_ann_textItems_new = df
        j=j+1
    prev_docid = curr_docid
    j=j+1


mallet_train = ann_textItems_new[['token','label']]
mallet_test = test_ann_textItems_new[['token','dummy']]

mallet_test_ids = test_ann_textItems_new['docid']
mallet_test_ids.to_csv('mallet_test_ids', sep=' ', header=False , index=False)  #Training data for model


mallet_train.to_csv('mallet_train_product', sep=' ', header=False , index=False)  #Training data for model
mallet_test.to_csv('mallet_test_product', sep=' ', header=False , index=False)    #dummy data testing on training set


# #Write test file textItemId's to file
# with open("output_textid.csv", "w") as output:
#     writer = csv.writer(output, lineterminator='\n')
#     for val in test_ids:
#         writer.writerow([val])
print(product_terms)