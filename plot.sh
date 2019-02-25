mkdir out

INPUT_FILEPATH=$1

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

python3 compare.py $INPUT_FILEPATH g temp.data $MODE

gnuplot -e "set xlabel 'Repetitions'; 
            set ylabel 'Bits'; 
            plot 'temp.data' using 1:2 title 'LZ78', \
                 'temp.data' using 1:3 title 'Huffman';
	   set size 1.0, 0.6; 
           set terminal postscript portrait enhanced color dashed lw 1 'Helvetica' 14; 
           set output 'out/${OUTPUT_FILEPATH}'; 
	   replot;
           set terminal x11; 
           set size 1,1;"

rm temp.data
