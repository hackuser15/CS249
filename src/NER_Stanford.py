# NER using Stanford NLP - 3 class model Location, Person, Organization
# Download Stanford NER from http://nlp.stanford.edu/software/stanford-ner-2015-12-09.zip and place in project directory
# Set Environment Variable JAVA_HOME to point to java installation directory e.g. C:\Program Files\Java\jre1.8.0_66
# Output: [('Akshay', 'PERSON'), ('Shinde', 'PERSON'), ('is', 'O'), ('studying', 'O'), ('at', 'O'), ('University', 'ORGANIZATION'),
#           ('of', 'ORGANIZATION'), ('California', 'ORGANIZATION'), (',', 'O'), ('Los', 'LOCATION'), ('Angeles', 'LOCATION')]
import os
import nltk
from nltk.tag import StanfordNERTagger

path_stanford = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '\stanford-ner-2015-12-09'
path_to_model = path_stanford + '\classifiers\english.all.3class.distsim.crf.ser.gz'
path_to_jar = path_stanford + '\stanford-ner.jar'
st = StanfordNERTagger(path_to_model, path_to_jar)

# stanford_dir = st._stanford_jar.rpartition('\\')[0]
from nltk.internals import find_jars_within_path
stanford_jars = find_jars_within_path(path_stanford)
st._stanford_jar = ';'.join(stanford_jars)

print(st.tag(nltk.word_tokenize('Akshay Shinde is studying at University of California, Los Angeles')))