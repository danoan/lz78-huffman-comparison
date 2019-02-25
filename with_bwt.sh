INPUT_FILE=$1
MODE=$2

./sua.out $INPUT_FILE temp.txt
python3 compare.py temp.txt c $MODE
