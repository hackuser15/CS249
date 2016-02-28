modelFile="CRF1.crf"

tmpTrainingFile="/Users/avneet/Desktop/CS249/M/ner_stanford_train_product"

MalletClassPath="/Users/avneet/Desktop/CS249/mallet-2.0.8RC3/class:/Users/avneet/Desktop/CS249/mallet-2.0.8RC3/lib/mallet-deps.jar"
OS=`uname`
if [ "$OS" == "Linux" ]; then MalletClassPath="../mallet-2.0.7/class:../mallet-2.0.7/lib/mallet-deps.jar"; fi
# use a larger memory pool with param -Xmx1024m
echo "training model [$modelFile]"
java  -Xmx1024m  -cp "$MalletClassPath" cc.mallet.fst.SimpleTagger --train true --model-file $modelFile $tmpTrainingFile