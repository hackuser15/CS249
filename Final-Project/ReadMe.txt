
1. The modified training dataset is present in training-annotate-text.json & testing dataset is present in testing-annotated-text.json.
   Both these files are present in Dataset folder.

Packages to be installed/built for this project:
Lucene Index Creation
1. Download the Lucene index of product catalog from the following link
   https://www.dropbox.com/s/61p7ficpr49r4ea/INDEX_FINAL1.zip?dl=0
2. Place this index in the Dataset directory
PyStruct
1. To install pystruct, you need cvxopt, cython and scikit-learn (which requires numpy and scipy).
   The easiest way to install pystruct is using pip:
   pip install pystruct
2. Additional instructions to install PyStruct(for different OS') is given at: https://pystruct.github.io/installation.html

   Steps to run Mallet Model
1. Run the mallet_preprocess_data.py file from the Source directory.
2. Run the train_model.sh shell script from Scripts directory to train the mallet model.
3. Run the test_model.sh script to create the test results.
4. cd to the Source dir & Run query.py as : java -jar ../Lib/jython.jar query.py
5. Run the Final_output_generation.sh script.
6. Compare the results with the ones in test-annotated-text.json


Steps for Pystruct
1. Run the PyStructSSVM.py file from the Source directory.
2. Run the Generate_output_PyStruct.py file from the Source directory.


Steps for Stanford NER