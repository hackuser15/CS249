# NER using Stanford NLP - 3 class model Location, Person, Organization
# Download Stanford NER from http://nlp.stanford.edu/software/stanford-ner-2015-12-09.zip
# Set Environment Variable JAVA_HOME to point to java installation directory e.g. C:\Program Files\Java\jre1.8.0_66
# Provide correct path_to_model and path_to_jar
# Output: [('Akshay', 'PERSON'), ('Shinde', 'PERSON'), ('is', 'O'), ('studying', 'O'), ('at', 'O'), ('University', 'ORGANIZATION'),
#           ('of', 'ORGANIZATION'), ('California', 'ORGANIZATION'), (',', 'O'), ('Los', 'LOCATION'), ('Angeles', 'LOCATION')]
import nltk
from nltk.tag import StanfordNERTagger
path_to_model = 'D:\WINTER\Big_Data_Analytics_CS249\Project\Code\stanford-ner-2015-12-09\classifiers\english.all.3class.distsim.crf.ser.gz'
path_to_jar = 'D:\WINTER\Big_Data_Analytics_CS249\Project\Code\stanford-ner-2015-12-09\stanford-ner.jar'
st = StanfordNERTagger(path_to_model, path_to_jar)

stanford_dir = st._stanford_jar.rpartition('\\')[0]
from nltk.internals import find_jars_within_path
stanford_jars = find_jars_within_path(stanford_dir)
st._stanford_jar = ';'.join(stanford_jars)

print(st.tag(nltk.word_tokenize('Akshay Shinde is studying at University of California, Los Angeles')))