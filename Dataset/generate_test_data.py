import numpy
import pandas as pd
import random


input_data = pd.read_csv('training-disambiguated-product-mentions.csv')

df = pd.DataFrame(input_data)

df_test = df.sample(n=10)

df_train = df.loc[~df.index.isin(df_test)]

df_test.to_csv('test-disambiguated',header=False,index=None)
df_train.to_csv('train_disambiguated',header=False,index=None)




