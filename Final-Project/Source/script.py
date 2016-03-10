import sys
from java.io import File


jars = [
    "/Users/avneet/jython2.7.0/lucene-core-3.6.1.jar",
    "/Users/avneet/Desktop/CS249/LUC/apache-lucene.jar"  
    ]
for jar in jars:
	sys.path.append(jar)

from org.apache.lucene.index import Term
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.index import IndexReader

#import json
import csv



#CSV file to list creation
PROD_IDS = []
data = csv.reader(open('/Users/avneet/PycharmProjects/CS249_/Mallet/products_list', 'rb'), delimiter=" ")
PROD_IDS, PROD_DESC = [], []

for row in data:
    PROD_IDS.append(row[0])
    PROD_DESC.append(row[1])

# 1. create an index
index_path = File("/Users/avneet/Desktop/CS249/INDEX_FINAL1")
analyzer = StandardAnalyzer(Version.LUCENE_36)
index = SimpleFSDirectory(index_path)



#PROD_IDS = ["1ZzV6Py6F0E", "elNdHhbcAlM",
#          "gp2rsLWYjWc", "KGebVIgDDv0"]

#PROD_DESC = ["77 Kawasaki Kz650 Kz 650 Transmission Shift Fork A3  1977","Door Mirror 2001 Honda S2000 Lh Left Driver Side Electric","1971 - 1973 Nissan 1200 Ignition Coil Crane 730-0891 Nissan Ignition","Lexus 800 "]


config = IndexWriterConfig(Version.LUCENE_36, analyzer)
config.setOpenMode(IndexWriterConfig.OpenMode.CREATE_OR_APPEND)
writer = IndexWriter(index, config)

for i in range(0,len(PROD_IDS)):
	print(i)
	doc = Document()
	doc.add(Field("product_id", PROD_IDS[i], Field.Store.YES, Field.Index.ANALYZED))
	doc.add(Field("product_desc", PROD_DESC[i], Field.Store.YES, Field.Index.ANALYZED))
	writer.addDocument(doc)


writer.close()
index.close()
print("Index built")

