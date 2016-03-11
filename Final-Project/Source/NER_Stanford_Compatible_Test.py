import os
import string
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
        # if text in stop:
        #     indexes.append(i)
        #     continue
        text = BeautifulSoup(text,"lxml").get_text()
        text = "".join([ch for ch in text if ch not in string.punctuation])
        if not text:
            indexes.append(i)
    df.drop(df.index[indexes],inplace=True)
    df = df.reset_index(drop=True)
    return df

def cleanHTMLTags(df):
    df['token']=df['token'].replace(to_replace='<', value='', regex = True)
    df['token']=df['token'].replace(to_replace='>', value='', regex = True)
    return df

def verticalizeTextItems(df):
    rows = []
    df.apply(lambda row: [rows.append([row['docid'], txt, index, row['occurence']]) for index, txt in enumerate(row.text)], axis=1)
    df = pd.DataFrame(rows, columns=['docid','token','tokenid','occurence'])
    return df

def verticalizeTestData(df):
    rows = []
    df.apply(lambda row: [rows.append([row['docid'], txt, index]) for index, txt in enumerate(row.text)], axis=1)
    df = pd.DataFrame(rows, columns=['docid','token','oldtokenid'])
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

def predictLabelStanford(test_data, preTrained = False):
    path_stanford = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '\StanfordNER\\'

    if(preTrained == True):
        path_to_model = path_stanford + '\english.all.3class.distsim.crf.ser.gz'
    else:
        path_to_model = path_stanford + '\stanford.ner.model.products.gz'

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
        op['tokenid'] = pd.Series([x for x in range(len(op.index))], index=op.index)
        prediction=prediction.append(op,ignore_index=True)
    return prediction

def getProductOccurence(prediction):
    final_list = pd.DataFrame(columns=['docid','occurences'])
    seperator ="-"
    l = []
    lproduct = []
    i = 0
    prev_docid = ''
    while(i < len(prediction['pred_label'])):
        curr_docid = prediction['docid'][i]
        label = prediction['pred_label'][i]
        if(i>0 and curr_docid != prev_docid ):
            final_list=processTextItem(l, lproduct, prev_docid, final_list)
            l.clear()
            lproduct.clear()
        if(label in ('prod' ,'ORGANIZATION')):
            start_index = prediction['tokenid'][i]
            product = ''
            token = prediction['token'][i]
            end_index = start_index
            while((label in ('prod' ,'ORGANIZATION') and curr_docid == prev_docid) or start_index == end_index):
                prev_docid = curr_docid
                product += token+" "
                i = i+1
                if(i==len(prediction)):
                    l.append(str(int(start_index))+seperator+str(int(end_index)))
                    lproduct.append(product)
                    break
                curr_docid = prediction['docid'][i]
                end_index = prediction['tokenid'][i] if (curr_docid == prev_docid or end_index == 0) else prediction['tokenid'][i-1]+1
                label = str(prediction['pred_label'][i])
                token = prediction['token'][i]
            l.append(str(int(start_index))+seperator+str(int(end_index)))
            product += " "+prediction['token'][i]
            lproduct.append(product)
        else:
            i = i+1
            prev_docid = curr_docid
    final_list=processTextItem(l, lproduct, prediction['docid'][i-1], final_list)
    return final_list

def processTextItem(l, lproduct, textItemID, final_list):
    if(len(l) > 0):
        op = pd.DataFrame(l, columns=['occurences'])
        op['product'] = lproduct
        op['docid'] = pd.Series([textItemID for x in range(len(op.index))], index=op.index)
        final_list=final_list.append(op, ignore_index=True)
    return final_list

path_dataset = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '\Dataset'
with open(path_dataset+ r'\testing-annotated-text.json') as data_file:
    test_data = json.load(data_file)

test_data = pd.DataFrame(list(test_data['TextItem'].items()))

test_data.columns = ['docid', 'text']

test_data = verticalizeTestData(test_data)

test_data = cleanHTMLTags(test_data)

test_data = test_data[['docid','token']]

path_stanford = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '\StanfordNER\\'

#Prediction on our trained model
pred_data = predictLabelStanford(test_data)
pred_data = getProductOccurence(pred_data)
print(pred_data)
pred_occurences = pred_data[['docid','occurences']]
pred_products = pred_data[['product']]
pred_occurences.to_csv(path_stanford + 'ner_stanford_pred_comp_occurences', sep=' ', header=False , index=False)
pred_products.to_csv(path_stanford + 'ner_stanford_pred_comp_products', sep='|', header=False , index=False)

# Prediction on stanford pretrained model
pred_data = predictLabelStanford(test_data, preTrained=True)
pred_data = getProductOccurence(pred_data)
print(pred_data)
pred_occurences = pred_data[['docid','occurences']]
pred_products = pred_data[['product']]
pred_occurences.to_csv(path_stanford+'ner_stanford_pred_compPreTrain_occurences', sep=' ', header=False , index=False)
pred_products.to_csv(path_stanford+'ner_stanford_pred_compPreTrain_products', sep='|', header=False , index=False)