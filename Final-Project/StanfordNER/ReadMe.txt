Steps to run Stanford NER Model
1. Run the NER_Stanford_Compatible_Train.py file from the Source directory.
2. Run the train_stanford_ner.bat file in StanfordNER directory to train the stanford NER model (If not windows, run the command java -cp ".;stanford-ner.jar;.\lib\*" edu.stanford.nlp.ie.crf.CRFClassifier -prop my_ner.prop
)
3. Run the NER_Stanford_Compatible_Test.py in source directory to create the test results.
4. cd to the Source dir & Run query.py as : java -jar ../Lib/jython.jar query.py
5. Run the Final_output_generation.sh script.
6. Compare the results with the ones in test-annotated-text.json