
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

1. Run the preprocess_data.py file from the Source directory. (Mallet jar is already provided)
2. Run the train_model.sh shell script from Scripts directory to train the mallet model(Please comment and uncomment as per OS).
3. Run the test_model.sh script to create the test results(Please comment and uncomment as per OS).
4. Run the Generate_output.py script present in the Source folder.
4. Copy query.py present present in Source directory to the Jython home dir
5. In query.py, modify the code lines number 8 & 9 by specifying the the absolute path as per your system to Final-Project/Lib/apache-lucene.jar &
   and Final-Project/Lib/lucene-core-3.6.1.jar
    Also  Modify following lines in query.py(as the path needs to be given based on your local filesystem)
    30 - Provide absolute path of this folder's Intermediate_files/output_query.csv
    39 - Provide absolute path of INDEX1(Lucene index) as downloaded from Dropbox as per link provided above
    70 - Provide absolute path of this project's Intermediate_files/prod_ids.csv
7. cd(change directory) to Jython Home & execute from the Terminal/command prompt : java -jar jython.jar query.py
8. Run the Final_output_generation.sh script present in Final-Project/Scripts/Final_output_generation.sh
9. Compare the results generated in Intermediate_files/Final_result.csv with the ones in testing-disambiguated-product-mentions.xlsx present in Dataset folder.


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



Steps for Stanford NER(Needs Java version 1.8 or higher):

1. Run the NER_Stanford_Compatible_Train.py file from the Source directory.
2. Run the shell script present in Scripts folder: stanford_train_model.sh(Please comment and uncomment as per OS).
3. Run the NER_Stanford_Compatible_Test.py in source directory to create the test results.
4. Copy query.py to the Jython home dir
5. In query.py, modify the code lines number 13 & 14 by specifying the the absolute path as per your system to Final-Project/Lib/apache-lucene.jar &
   and Final-Project/Lib/lucene-core-3.6.1.jar
6. Modify lines 35 & 75 to give absolute file path up to the Intermediate_files directory in this project.
7. cd to Jython Home & execute : java -jar jython.jar query.py
8. Run the Final_output_generation.sh script present in Final-Project/Scripts/Final_output_generation.sh .
9. Compare the results with the ones in testing-disambiguated-product-mentions.xlsx present in Dataset folder.
