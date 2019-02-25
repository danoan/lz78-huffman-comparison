import sys
from pymodules import huffman as H
from pymodules import LZ78 as L

def _compare(data,rep_range,mode):
    for n in rep_range:
        t = data*n

        lz78_t = len(L.lz78_compresse_bin(t,mode))*8
        huff_t = H.encoded_length(t,H.huffman(t))

        yield (n,lz78_t,huff_t)

def compare(data,rep_range,outputFilepath,mode):
    out=""
    for e in _compare(data,rep_range,mode):
        out+="%s" % (e,)

    if outputFilepath=="stdout":
        print(out)
    else:
        with open(outputFilepath,"w") as f:
            f.write(out)
    
        
def gnuplot(data,rep_range,outputFilepath,mode):
    n=len(rep_range)
    out="#Repetitions\tLZ78(bits)\tHuffman(bits)\n"
    for e in _compare(data,rep_range,mode):
        out+="%d\t%d\t%d\n" % (e[0],e[1],e[2])

    if outputFilepath=="stdout":
        print(out)
    else:
        with open(outputFilepath,"w") as f:
            f.write(out)
        
def main():
    if len(sys.argv)<3:
        print("Usage: %s Input_File_Path gnuplot(g)|compare(c) Output_File_Path=stdout mode=utf-8" % (sys.argv[0],),file=sys.stderr)
        exit()

    filepath = sys.argv[1]
    action = sys.argv[2]
    outpath = sys.argv[3] if len(sys.argv)>3 else "stdout"    
    mode = sys.argv[4] if len(sys.argv)>4 else "utf-8"

    data=""
    with open(filepath,"rb") as f:
        data=f.read().decode(mode,"replace")
    

    if action=="g":    
       gnuplot(data,range(1,20,1),outpath,mode)
    elif action=="c":
       compare(data,range(1,2),outpath,mode)
    else:
       print("Action %s not regognized" % (action,),file=stderr )


if __name__=='__main__':
    main()
