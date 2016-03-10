
1. The modified training dataset is present in training-annotate-text.json & testing dataset is present in testing-annotated-text.json.
   Both these files are present in Dataset folder.

Lucene Index Creation
1. Download the Lucene index of product catalog from the following link
   https://www.dropbox.com/s/61p7ficpr49r4ea/INDEX_FINAL1.zip?dl=0
2. Place this index in the Dataset directory

Jython
Download and install Jython 2.7
Note : Due to known issues of Jython incompatibility with Python IDEs like Pycharm, we need to install it and use it
separately as described below.

   Steps to run Mallet Model
1. Run the mallet_preprocess_data.py file from the Source directory. (Mallet jar is already provided)
2. Run the train_model.sh shell script from Scripts directory to train the mallet model.
3. Run the test_model.sh script to create the test results.
4. Copy query.py to the Jython home dir
5. In query.py, modify the code lines number 13 & 14 by specifying the the absolute path as per your system to Final-Project/Lib/apache-lucene.jar &
   and Final-Project/Lib/lucene-core-3.6.1.jar
6. Modify lines 35 & 75 to give absolute file path up to the Intermediate_files directory in this project.
7. cd to Jython Home & execute : java -jar jython.jar query.py
8. Run the Final_output_generation.sh script present in Final-Project/Scripts/Final_output_generation.sh .
9. Compare the results with the ones in test-annotated-text.json


Steps for Pystruct


Steps for Stanford NER