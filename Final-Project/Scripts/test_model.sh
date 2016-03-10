modelFile="../Model/CRF_malllet.crf"

tmpTestingFile="../Intermediate_files/mallet_test_product"

#MalletClassPath="/Users/avneet/Desktop/CS249/mallet-2.0.8RC3/class:/Users/avneet/Desktop/CS249/mallet-2.0.8RC3/lib/mallet-deps.jar"

MalletClassPath="../Lib/mallet-2.0.7/class;../Lib/mallet-2.0.7/lib/mallet-deps.jar"

if [ "$OS" == "Linux" ]; then MalletClassPath="../mallet-2.0.7/class:../mallet-2.0.7/lib/mallet-deps.jar"; fi

java -Xmx1024m -cp "$MalletClassPath" cc.mallet.fst.SimpleTagger --model-file $modelFile $tmpTestingFile >>  ../Intermediate_files/test_labels.tok
paste -d ' ' $tmpTestingFile ../Intermediate_files/test_labels.tok > ../Intermediate_files/Test_output
cut -d " " -f 1,3  ../Intermediate_files/Test_output > ../Intermediate_files/Test_result