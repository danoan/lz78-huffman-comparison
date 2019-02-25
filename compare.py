import sys
import huffman as H
import LZ78 as L

def compare(data,rep_range,mode):
    for n in rep_range:
        t = data*n

        lz78_t = len(L.lz78_compresse_bin(t,mode))*8
        huff_t = H.encoded_length(t,H.huffman(t))

        yield (n,lz78_t,huff_t)

def gnuplot(data,rep_range,mode):
    outputFilepath = input("Enter output filepath:")
    skip=5
    c=0
    n=len(rep_range)
    with open(outputFilepath,"w") as f:
        f.write("#Repetitions\tLZ78(bits)\tHuffman(bits)\n")
        for e in compare(data,rep_range,mode):
            if c%skip==0:
                print("Writing %d of %d" % (c,n) )
            f.write("%d\t%d\t%d\n" % (e[0],e[1],e[2]) )
            c+=1
        
def main():
    if len(sys.argv)<3:
        print("Usage: %s Input_File_Path gnuplot(g)|compare(c) mode=utf-8" % (sys.argv[0],))
        exit()

    filepath = sys.argv[1]
    action = sys.argv[2]
    mode = sys.argv[3] if len(sys.argv)>3 else "utf-8"

    data=""
    with open(filepath,"rb") as f:
        print(mode)
        data=f.read().decode(mode,"replace")
    

    if action=="g":    
       gnuplot(data,range(1,20,1),mode)
    elif action=="c":
       for e in compare(data,range(1,2),mode):
          print(e)
    else:
       print("Action %s not regognized" % (action,) )


if __name__=='__main__':
    main()
