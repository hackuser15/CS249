
1. The modified training dataset is present in training-annotate-text.json & testing dataset is present in testing-annotated-text.json.
   Both these files are present in Dataset folder.

Packages to be installed/built for this project:
Lucene Index Creation

Since the index creation takes a lot of time, we created it locally and uploaded it to Dropbox.

1. Download the Lucene index of product catalog from the following link
   https://www.dropbox.com/s/61p7ficpr49r4ea/INDEX_FINAL1.zip?dl=0
2. Place this index in the Dataset directory

Jython
Download and install Jython 2.7(as we need it for integration of Apache Lucene)
Note : Due to known issues of Jython incompatibility with Python IDEs like Pycharm, we need to install it and use it
separately as described below.

PyStruct
1. To install pystruct, you need cvxopt, cython and scikit-learn (which requires numpy and scipy).
   The easiest way to install pystruct is using pip:
   pip install pystruct
2. Additional instructions to install PyStruct(for different OS') is given at: https://pystruct.github.io/installation.html

Steps to run Mallet Model:

1. Run the mallet_preprocess_data.py file from the Source directory. (Mallet jar is already provided)
2. Run the train_model.sh shell script from Scripts directory to train the mallet model.
3. Run the test_model.sh script to create the test results.
4. Run the Generate_output.py script present in the Source folder.
4. Copy query.py to the Jython home dir
5. In query.py, modify the code lines number 13 & 14 by specifying the the absolute path as per your system to Final-Project/Lib/apache-lucene.jar &
   and Final-Project/Lib/lucene-core-3.6.1.jar
6. Modify lines 35 & 75 to give absolute file path up to the Intermediate_files directory in this project.
7. cd to Jython Home & execute : java -jar jython.jar query.py
8. Run the Final_output_generation.sh script present in Final-Project/Scripts/Final_output_generation.sh .
9. Compare the results with the ones in testing-disambiguated-product-mentions.xlsx present in Dataset folder.


Steps for Pystruct model:

1. Run the preprocess_data.py file from the Source directory.
1. Run the PyStructSSVM.py file from the Source directory.
2. Run the Generate_output_PyStruct.py file from the Source directory.
4. Copy query.py to the Jython home dir
5. In query.py, modify the code lines number 13 & 14 by specifying the the absolute path as per your system to Final-Project/Lib/apache-lucene.jar &
   and Final-Project/Lib/lucene-core-3.6.1.jar
6. Modify lines 35 & 75 to give absolute file path up to the Intermediate_files directory in this project.
7. cd to Jython Home & execute : java -jar jython.jar query.py
8. Run the Final_output_generation.sh script present in Final-Project/Scripts/Final_output_generation.sh .
9. Compare the results with the ones in testing-disambiguated-product-mentions.xlsx present in Dataset folder.



Steps for Stanford NER:

1. Run the NER_Stanford_Compatible_Train.py file from the Source directory.
2. Run the train_stanford_ner.bat file in StanfordNER directory to train the stanford NER model (If not windows, run the command java -cp ".;stanford-ner.jar;.\lib\*" edu.stanford.nlp.ie.crf.CRFClassifier -prop my_ner.prop
)
3. Run the NER_Stanford_Compatible_Test.py in source directory to create the test results.
4. Copy query.py to the Jython home dir
5. In query.py, modify the code lines number 13 & 14 by specifying the the absolute path as per your system to Final-Project/Lib/apache-lucene.jar &
   and Final-Project/Lib/lucene-core-3.6.1.jar
6. Modify lines 35 & 75 to give absolute file path up to the Intermediate_files directory in this project.
7. cd to Jython Home & execute : java -jar jython.jar query.py
8. Run the Final_output_generation.sh script present in Final-Project/Scripts/Final_output_generation.sh .
9. Compare the results with the ones in testing-disambiguated-product-mentions.xlsx present in Dataset folder.
