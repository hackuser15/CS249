import numpy
import pandas as pd
import random
import json

input_data = pd.read_csv('training-disambiguated-product-mentions.csv')

df = pd.DataFrame(input_data)

df_test = df.sample(n=10)

df_train = df.loc[~df.index.isin(df_test)]

'''
test_list = df_test['id'].tolist()
print test_list

id_list = []
for str in test_list:
    id = str.split(':')
    id_list.append(id)

with open('training-annotated-text.json') as data_file:
    ann_textItems = json.load(data_file)

remove_list = []
for i in xrange(len(ann_textItems)):
    item = ann_textItems['TextItem'][i]
#    if ann_textItems[i]['TextItem'] in id_list:
        #ann_textItems.pop(i)
#        remove_list.append(i)
    print  item
#ann_textItems = pd.DataFrame(list(ann_textItems['TextItem'].items()))

ann_textItems.pop(remove_list)

'''
df_test.to_csv('test-disambiguated.csv',header=False,index=None)
df_train.to_csv('train_disambiguated.csv',header=False,index=None)
'''


with open('trial-training-data.json','w') as output:
    json.dump(ann_textItems, output)
'''