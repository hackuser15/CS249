#Code to find Named Entities using nltk
#Prints names of the named entities in 'training-annotated_subset.json' file
#Output: {'Charles Manson', 'Antennacraft', 'Currently', 'Bin Laden', 'WBNG', 'FWIU', 'TWC', 'UHF',
#           'R2R', 'JHG120', 'Quote', 'DWBNG', 'Hitler', 'WBNG Digital', 'Crazy', 'Ultra High'}

import json
import nltk

with open('training-annotated_subset.json') as data_file:
    textItems = json.load(data_file)

tokenized_sentences = textItems["TextItem"].values()
tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

entity_names = []
for tree in chunked_sentences:
    # Print results per sentence
    # print extract_entity_names(tree)

    entity_names.extend(extract_entity_names(tree))

# Print all entity names
#print entity_names

# Print unique entity names
print(set(entity_names))