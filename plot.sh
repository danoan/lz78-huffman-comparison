INPUT_DATA=$1

gnuplot -e "set xlabel 'Repetitions'; 
            set ylabel 'Bits'; 
            plot '${INPUT_DATA}' using 1:2 title 'LZ78', \
                 '${INPUT_DATA}' using 1:3 title 'Huffman';
	   set size 1.0, 0.6; 
           set terminal postscript portrait enhanced color dashed lw 1 'Helvetica' 14; 
           set output '${INPUT_DATA}.ps'; 
	   replot;
           set terminal x11; 
           set size 1,1;"
