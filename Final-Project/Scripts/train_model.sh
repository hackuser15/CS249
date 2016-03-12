modelFile="../Model/CRF_malllet.crf"

tmpTrainingFile="../Intermediate_files/mallet_train_product"

# FOR WINDOWS
#MalletClassPath="../Lib/mallet-2.0.7/class;../Lib/mallet-2.0.7/lib/mallet-deps.jar"

#FOR MAC
MalletClassPath="../Lib/mallet-2.0.7/class:../Lib/mallet-2.0.7/lib/mallet-deps.jar"

OS=`uname`
if [ "$OS" == "Linux" ]; then MalletClassPath="../mallet-2.0.7/class:../mallet-2.0.7/lib/mallet-deps.jar"; fi
# use a larger memory pool with param -Xmx1024m
echo "training model [$modelFile]"
java  -Xmx1024m  -cp "$MalletClassPath" cc.mallet.fst.SimpleTagger --train true --model-file $modelFile $tmpTrainingFile