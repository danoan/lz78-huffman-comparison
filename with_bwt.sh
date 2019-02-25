mkdir out

INPUT_FILE=$1

if [ -z $2 ]
then
    OUTPUT_FILEPATH="stdout"
else
    OUTPUT_FILEPATH=$2
fi

if [ -z $3 ]
then 
    MODE="utf-8"
else
    MODE=$3
fi

if [ -z $4 ]
then 
   SUFFIX_ARRAY_LIB_PATH=""
else
   SUFFIX_ARRAY_LIB_PATH=$4
fi

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${SUFFIX_ARRAY_LIB_PATH}/lib
gcc cmodules/suffix-array.c -I${SUFFIX_ARRAY_LIB_PATH}/include -L${SUFFIX_ARRAY_LIB_PATH}/lib -ldivsufsort -o out/sua.out

./out/sua.out $INPUT_FILE temp.txt
python3 compare.py temp.txt c $OUTPUT_FILEPATH $MODE

rm temp.txt
