import pandas as pd
import json
import csv

#Process products file to be done once
with open("../Dataset/products.json") as data_file1:
     products = json.load(data_file1)

print(products)
product_Items = pd.DataFrame(list(products['Product'].items()))
product_Items.columns = ['prod_id', 'data']
products = product_Items['prod_id','data']
print(type(product_Items['data']))
product_Items['Name']= product_Items.apply (lambda row: row['data'][0],axis=1)
product_Items = product_Items.drop('data',1)

print(product_Items)
print(product_Items['Name'])
# Write this to csv file so it can be processed by Jython file
product_Items.to_csv('../Intermediate_files/products_list', sep=' ', header=False , index=False)

