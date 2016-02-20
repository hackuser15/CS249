# import json
# import csv
#
# employee_parsed = json.loads('training-annotated-text.json')
# emp_data = employee_parsed['TextItem']
# open a file for writing
# csvdata = open('training-annotated-text.csv', 'w')
# create the csv writer object
# csvwriter = csv.writer(csvdata)
# count = 0
# for emp in emp_data:
#       if count == 0:
#              header = emp.keys()
#              csvwriter.writerow(header)
#              count += 1
#       csvwriter.writerow(emp.values())
# csvdata.close()

import csv
import json
from pprint import pprint
data = []
with open('training-annotated.json') as jsonfile:
    x = json.load(jsonfile)
#print(data)
#emp_data = x['TextItem']
3#print(emp_data)
#pprint(x)
#print(' '.join(x["TextItem"]["0c1edc5b2ed5abb25e25b966ccdb01d2"]))
#f = csv.writer(open("test1.csv", "w"))
with open('test.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['TextItem','Value'])
    for ele in x.values():
        for key, value in ele.items():
            print (key, ' '.join(value))
            writer.writerow([key,' '.join(value)])
        #f.writerow(key+value)
        #spamwriter.writerow()

    #print(ele)
#f = csv.writer(open("test1.csv", "w"))
# Write CSV Header, If you dont need that, remove this line
#f.writerow(["TextItem"])

#for x1 in x:
#    f.writerow(x1["TextItem"])

#f.close()