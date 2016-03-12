
# Run this file from JYthon Prompt (need to install jython)

import sys


jars = [
    "../Lib/lucene-core-3.6.1.jar",
    "../Lib/apache-lucene.jar"
    ]


for jar in jars:
    sys.path.append(jar)

print(sys.path)

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexReader
from org.apache.lucene.queryParser import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
import csv


query_list = []
final_products_list = []
data = csv.reader(open('../Intermediate_files/output_query.csv', 'rb'))

for row in data:
    query_list.append(row[0])
    #print(row[0])

# 1. open the index
analyzer = StandardAnalyzer(Version.LUCENE_36)
#index = SimpleFSDirectory(File("../Dataset/INDEX_FINAL1"))
index = SimpleFSDirectory(File("F:/INDEX_FINAL1/INDEX_FINAL1"))
reader = IndexReader.open(index)
n_docs = reader.numDocs()
print("Index contains %d documents." % n_docs)


#query_list = ["LG 42LD550","Sony E9000ES","Denon 4802","Sony STR-K840P.."]
# 2. parse the query from the command line
queryparser = QueryParser(Version.LUCENE_36, "product_desc", analyzer)
for i in range(0,len(query_list)):
    query_list[i] = query_list[i].replace('/','')
    query_list[i] = query_list[i].replace(')','')
    query_list[i] = query_list[i].replace('(','')
    query_list[i] = query_list[i].replace(':','')
    query_list[i] = query_list[i].replace('?','')

    query = queryparser.parse(query_list[i])
    searcher = IndexSearcher(reader)
    hits = searcher.search(query, n_docs).scoreDocs
    print "Found %d hits:" % len(hits)
    prod_list_str = ""
    doc_length = min(10, len(hits))
    print query_list[i],":","\n"
    prod_list_str=""
    for i in range(0,doc_length):
    	doc = searcher.doc(hits[i].doc)
    	prod_list_str+=doc.get("product_id")+" "
    final_products_list.append(prod_list_str)
    print(prod_list_str)


with open("../Intermediate_files/prod_ids.csv", "w") as output:
	writer = csv.writer(output, lineterminator='\n')
	for val in final_products_list:
		writer.writerow([val])
# 5. close resources
searcher.close()