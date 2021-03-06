import json
import sys
import pandas as pd
import csv

final_list = []
token_list = []
def processTextItem(l,textItemID,tokenStr):
    #print(token_str)
    if(len(l) > 0):
        r = l[0]
        s = token_str
        final_list.append(textItemID+":"+r)
        token_list.append(s)

# with open('/Users/avneet/Desktop/CS249/Dataset/testing-annotated-text.json') as data_file:
#     test_ann_textItems = json.load(data_file)
#
# test_ann_textItems = pd.DataFrame(list(test_ann_textItems['TextItem'].items()))
# test_ann_textItems.columns = ['id', 'text']

#Processing test_ids file
test_ids = pd.read_csv('../Intermediate_files/mallet_test_ids',sep=' ',skip_blank_lines=False,header = None)
test_ids.columns = ['docid']


##Processing output file generated by Mallet and Stanford NER
test_labels = pd.read_csv('../Intermediate_files/Test_result',sep=' ',skip_blank_lines=False,header = None)
test_labels.columns = ['token', 'label']

text_index = 0
index_str="";
seperator ="-"
l = []
token_str = ""
i = 0
#count = 0
while(i < len(test_labels['label'])):
    label = str(test_labels['label'][i])
    token = str(test_labels['token'][i])
    #print(label+":"+str(i)+ " "+str(test_labels['token'][i])+" "+str(text_index))
    if(label == 'nan'):
        #processTextItem(l, test_ann_textItems['id'][count],token_str)
        text_index = 0
        #l.clear()
        l = []
        i = i+1
        token_str = ""
        #count+=1
    elif(label == 'prod'):
        print("Found product in: ",test_ids['docid'][i]," at line = ",i, " ",str(test_labels['token'][i]))
        start_index = text_index
        end_index = text_index
        while(label == 'prod'):
            token = str(test_labels['token'][i])
            token_str+=token + " "
            end_index+=1
            text_index+=1
            i = i+1
            label = str(test_labels['label'][i])
        #l.append(str(start_index)+seperator+str(end_index-1)) - Modifying logic to include word right after product mention
        final_index = end_index-1
        if(label !='nan'):   #New logic of including prod+1 token
            token = str(test_labels['token'][i])
            token_str+=token
            final_index = end_index

        l.append(str(start_index)+seperator+str(final_index))
        processTextItem(l, test_ids['docid'][i-1], token_str)
        #l.clear()
        l = []
        token_str=""
    elif(label == 'O'):
        i+=1
        text_index += 1

#processTextItem(l, test_ann_textItems['id'][count],token_str)

with open("../Intermediate_files/output_textids.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in final_list:
        writer.writerow([val])

with open("../Intermediate_files/output_query.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in token_list:
        writer.writerow([val])