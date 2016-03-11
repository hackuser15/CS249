import json
import string
import nltk
import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from gensim.models import word2vec, Word2Vec
import warnings
warnings.filterwarnings("ignore")

dir = os.path.dirname(__file__)
train_anon_file = os.path.join(dir, os.pardir,'Dataset/training-annotated-text.json')
train_filename = os.path.join(dir, os.pardir,'Intermediate_files/mallet_train_product')
test_filename = os.path.join(dir, os.pardir,'Intermediate_files/mallet_test_product')
output_filename = os.path.join(dir, os.pardir,'Intermediate_files/PyStructOutput.csv')
stop = stopwords.words('english')

### Feature vector creation for input to PyStruct algorithm
def makeFeatureVec(words, labels,  model, item_id, keyword):
    index2word_set = set(model.index2word)
    train_all = []
    train = []
    label_all = []
    label = []
    prod_all = []
    prod = []
    item_id_test = []
    token_id = []
    token_id_all = []
    token_no = -1
    for i in range(0,words.shape[0]):
        token_no = token_no + 1
        check = words[i].lower()
        if check == "separator" or (i == words.shape[0]-1):
            if not label:
                label = []
                train = []
                prod = []
                continue
            tarr = np.array(train) #conv list to array
            larr = np.array(label) #conv list to array
            parr = np.array(prod) #conv list to array
            train_all.append(tarr)
            train = []
            label_all.append(larr)
            label = []
            prod_all.append(parr)
            prod = []
            if keyword == 'Test':
                item_id_test.append(item_id[i-1])
                token_id_all.append(token_id)
                token_no = -1
                token_id = []
        if check in index2word_set:
            prod.append(check)
            train.append(model[check])
            label.append(labels[i])
            token_id.append(token_no)
    train_data = np.array(train_all)
    label_data = np.array(label_all)
    prod_data = np.array(prod_all)
    token_id_all = np.array(token_id_all)
    return train_data,label_data,prod_data,item_id_test,token_id_all

### Clean Data
def cleanData(list):
    sent = []
    for text in list:
        text = " ".join(text)
        text = text.lower()
        text = BeautifulSoup(text,"lxml").get_text()
        text = "".join([ch for ch in text if ch not in string.punctuation])
        tokens = nltk.word_tokenize(text)
        cleaned = []
        for item in tokens:
            if not item.isdigit(): #item not in stop
                cleaned.append(item)
        sent.append(cleaned)
    return sent

### Read file and create a Word2Vec model
data = []
with open(train_anon_file) as jsonfile:
    x = json.load(jsonfile)
list = []
for ele in x.values():
    for key, value in ele.items():
        list.append(value)
sentences = cleanData(list)
# This part was used to build Word2Vec Model
# The parameters were set as follows, they can be manipulated to generate a different Word2Vec model
# num_features = 500    # Word vector dimensionality
# min_word_count = 3   # Minimum word count
# num_workers = 3       # Number of threads to run in parallel
# context = 10          # Context window size
# downsampling = 1e-3   # Downsample setting for frequent words
# model = word2vec.Word2Vec(sentences, sg=1, hs=1,sample=downsampling,
#                        workers=num_workers,size=num_features,window = context,
#                         min_count=min_word_count)
# We are using two models --> 249MF2,249MF4
model_name = "249MF4"
model = Word2Vec.load(model_name)

### Read the training and testing file and make feature vectors for tokens in them using Word2Vec model
### Also convert the output labels 'O' and 'prod' to 0's and 1's respectively.
### The conversion of input tokens and labels is done to feed input to PyStruct in the expected format
print("Reading the training and the testing files..")
data = pd.read_csv(train_filename,sep=' ',header=None,skip_blank_lines=False)
X_train = data[0]
y_train = data[1]
y_train.replace(to_replace='prod', value=1, inplace=True)
y_train.replace(to_replace='O', value=0, inplace=True)
y_train.fillna(0, inplace=True)
X_train.fillna('separator', inplace=True)
y_train = y_train.astype(int)
testfile = pd.read_csv(test_filename,sep=' ',header=None,skip_blank_lines=False)
item_id1 = testfile[0]
X_test1 = testfile[1]
y_test1 = testfile[2]
y_test = y_test1.replace(to_replace='prod', value=1)
y_test = y_test.replace(to_replace='O', value=0)
y_test = y_test.fillna(0)
X_test = X_test1.fillna('separator')
item_id = item_id1.dropna()
y_test = y_test.astype(int)
print("Making feature vectors for the training and testing files..")
train_data,train_label_data,train_prod_data,_,_ = makeFeatureVec(X_train, y_train, model,item_id, 'Train')
test_data,test_label_data,test_prod_data,dist_id,token_id_all = makeFeatureVec(X_test, y_test, model, item_id, 'Test')

### Apply PyStruct models
from pystruct.models import ChainCRF
from pystruct.learners import OneSlackSSVM
print("Training the model..")
model = ChainCRF()
ssvm = OneSlackSSVM(model=model, C=.1, max_iter=25)
ssvm.fit(train_data, train_label_data)
res = ssvm.predict(test_data)

### Prediction and creation of output result file
### Since the output values of labels in PyStruct models is always numeric
### We convert the 0's and 1's to 'O' and 'prod' respectively as required
print("Building the result file..")
test_output = pd.DataFrame()
test_output[0] = pd.Series(item_id1)
test_output[1] = pd.Series(X_test1)
test_output[2] = pd.Series(y_test1)
sLength = len(test_output[0])
for row in range(0,len(res)):
    tid = dist_id[row]
    idx = test_output[test_output[0] == tid].index.tolist()
    start_idx = np.min(idx)
    token_id_row = token_id_all[row]
    token_id_row = np.array(token_id_row)
    curres = test_prod_data[row]
    indices = np.where(res[row] > 0)
    for index in token_id_row[indices]:
        test_output.loc[start_idx+index,2] = 'prod'
        k = 1
        while True:
            if (start_idx+index+k) >= sLength-1:
                break
            s = test_output.loc[start_idx+index+k,1]
            if s == 'separator':
                break
            s = s.lower()
            if [ch for ch in s if ch in string.punctuation]:
                s = "".join([ch for ch in s if ch not in string.punctuation])
                if not s or len(s) <= 2:
                    break
            if s in stop or s.isdigit():
                break
            else:
                test_output.loc[start_idx+index+k,2] = 'prod'
                k = k + 1
cols = [1,2]
test_output.to_csv(output_filename,sep=' ',columns=cols,index=False,header=False,skip_blank_lines=False)
print("Intermediate file generated in the Intermediate folder (PyStructOutput.csv)")