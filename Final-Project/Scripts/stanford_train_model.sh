#FOR MAC
java -cp “.:../Lib/StanfordNER/stanford-ner.jar:../Lib/StanfordNER/lib/*" edu.stanford.nlp.ie.crf.CRFClassifier -prop ../Lib/StanfordNER/my_ner.prop

#FOR WINDOWS
#java -cp ".;../Lib/StanfordNER/stanford-ner.jar;../Lib/StanfordNER/lib/*" edu.stanford.nlp.ie.crf.CRFClassifier -prop ../Lib/StanfordNER/my_ner.prop