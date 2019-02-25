ROOT_ID=0

def clean_data(data):
    data=data.lower()
    return data

def frequency_analysis(data):
    d={}
    for c in data:
        if c in d:
            d[c]+=1
        else:
            d[c]=1

    return d

def create_tree(left,right,frequency,label):
    global ROOT_ID
    ROOT_ID+=1
    return {"root_id":ROOT_ID,
            "left":left,
            "right":right,
            "frequency":frequency,
            "label":label}

def transform_into_forest(dct):
    forest=[]
    for k,v in dct.items():
        forest.append( create_tree(None,None,v,k ) )

    return forest

def index_by_root_id(forest):
    dct={}
    for tree in forest:
        dct[ tree["root_id"] ] = {"left":tree["left"],
                                  "right":tree["right"],
                                  "frequency":tree["frequency"],
                                  "label":tree["label"]} 
    return dct

def huffman(data):
    global ROOT_ID
    ROOT_ID=0
    
    dct = frequency_analysis(data)
    forest = transform_into_forest(dct)

    l = forest.copy()
    l = sorted( l, key=lambda item: item["frequency"] )
    while(len(l)>1):
        e1,e2 = l[0:2]
        l.append( create_tree(e1["root_id"],
                              e2["root_id"],
                              e1["frequency"] + e2["frequency"],
                              e1["label"]+e2["label"]) )
        forest.append( l[-1] )
        l=l[2:]
        l = sorted( l, key=lambda item: item["frequency"] )

    return index_by_root_id(forest)

def open_data(filepath):
    with open(filepath) as f:
        data = f.read()
    data = clean_data(data)
    return data

def unique_symbols(data):
    s=set({})
    for c in data:
        s.add(c)
    return s

def get_height(symbol,huff_tree):
    root_id=len(huff_tree)
    el = huff_tree[root_id]
    h=0
    while el["left"] is not None or el["right"] is not None:
        left = huff_tree[el["left"]]
        right = huff_tree[el["right"]]

        if symbol in left["label"]:
            el = left
        elif symbol in right["label"]:
            el = right
        else:
            raise Exception("Symbol %s is not in the tree!" % (symbol,))
        h+=1

    return h
        

def bits_for_each(data,huff_tree):
    s = unique_symbols(data)
    bits_per_symbol={}
    for c in s:
        bits_per_symbol[c] = get_height(c,huff_tree)

    return bits_per_symbol

def encoded_length(data,huff_tree):
    bfe = bits_for_each(data,huff_tree)
    length=0
    for c in data:
        length+=bfe[c]
        
    return length

def main():
    data = open_data("vents.txt")
    huff_tree = huffman(data)

    print("Huffman uses %d bits to encode the text\n"
          "Original had %d bits" % (encoded_length(data,huff_tree),
                                    len(data)*8) )
    

if __name__=='__main__':
    main()
