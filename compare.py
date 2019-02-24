import huffman as H
import LZ78 as L

def compare(data,rep_range):
    for n in rep_range:
        t = data*n

        lz78_t = len(L.lz78_compresse_bin(t))*8
        huff_t = H.encoded_length(t,H.huffman(t))

        yield (n,lz78_t,huff_t)

def gnuplot(data,rep_range):
    outputFilepath = input("Enter output filepath:")
    skip=5
    c=0
    n=len(rep_range)
    with open(outputFilepath,"w") as f:
        f.write("#Repetitions\tLZ78(bits)\tHuffman(bits)\n")
        for e in compare(data,rep_range):
            if c%skip==0:
                print("Writing %d of %d" % (c,n) )
            f.write("%d\t%d\t%d\n" % (e[0],e[1],e[2]) )
            c+=1
        
def main():
    filepath = input("Enter filepath:")
    data=""
    with open(filepath) as f:
        data=f.read()
        
    gnuplot(data,range(1,20,1))

if __name__=='__main__':
    main()
