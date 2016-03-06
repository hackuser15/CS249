modelFile="CRF_malllet.crf"

tmpTestingFile="/Users/avneet/Desktop/CS249/Dataset/mallet_test_product"

MalletClassPath="/Users/avneet/Desktop/CS249/mallet-2.0.8RC3/class:/Users/avneet/Desktop/CS249/mallet-2.0.8RC3/lib/mallet-deps.jar"
if [ "$OS" == "Linux" ]; then MalletClassPath="../mallet-2.0.7/class:../mallet-2.0.7/lib/mallet-deps.jar"; fi

java -Xmx1024m -cp "$MalletClassPath" cc.mallet.fst.SimpleTagger --model-file $modelFile $tmpTestingFile >>  test_labels.tok
paste -d ' ' $tmpTestingFile test_labels.tok > Test_output
cut -d " " -f 1,3  Test_output > Test_result