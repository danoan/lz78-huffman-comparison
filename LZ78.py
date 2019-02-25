#encoding:utf-8
#!/usr/bin/python3

def base256(n,pad):
    if n==0:
        return [0]*pad
    x=n
    l=[]
    while x>0 :
        l.append(x%256)
        x = int(x/256)

    pad -= len(l)
    while pad > 0:
        l.append(0)
        pad-=1

    return l[-1::-1]

def positionList(T,s):
    for (i,x) in enumerate(T):
        if x==s:
            return i
    return -1

def positionDict(D,s): 
    return D.get(s,-1)

def position(X,s):
    if isinstance(X,list):
        return positionList(X,s)
    else:
        return positionDict(X,s)

def lz78_compresse(texte):
    resultat = []

    dico=[""]
    mot_courant = ""
    p=0
    for c in texte:
        if( position(dico,mot_courant+c)==-1 ):
            dico.append(mot_courant+c)
            mot_courant = ""
            
            resultat.append(p)
            resultat.append(c)
            
        else:
            mot_courant = mot_courant + c
            
        p = position(dico,mot_courant)

    if mot_courant!="":
        resultat.append(p)

    #print(dico)

    return resultat

def lz78_decompresse(code):
    dico=[""]

    i=0
    n = len(code)
    t=""
    while(i<n):
        p = code[i]
        i+=1
        if i>=n:
            t+=dico[p]
            break
        c = code[i]
        i+=1

        dico.append(dico[p]+c)
        t+=dico[-1]

    return t

def octets(T,mode):
    r = bytearray()
    for e in T:
        if isinstance(e, int):
            if not 0 <= e < 256:
                raise RuntimeError("*** Problème, l'entier {} n'est pas compris entre 0 et 255 !".format(e))
            r.append(e)
            
        elif isinstance(e, str):
            if len(e) != 1:
                raise RuntimeError("*** Problème, les caractères doivent être donnés un par un !")
            try:
                r.extend(e.encode(mode))
            except UnicodeEncodeError:
                raise RuntimeError("*** Problème, '{}' n'est pas un caractère '{}' !".format(repr(e),mode))
        else:
            raise RuntimeError("*** Problème, '{}' n'est ni un entier, ni un caractère !".format(repr(e)))
            sys.exit(-1)
    return r
    

def lz78_compresse_bin(texte,mode="utf-8"):
    resultat = []

    dico={"":0}
    mot_courant = ""
    p=0
    for c in texte:
        if( position(dico,mot_courant+c)==-1 ):
            bitsToUse = len( base256( len(dico)-1,0 ) )

            resultat.extend( base256(p,bitsToUse) )
            resultat.append(c)

            dico.update( {mot_courant+c:len(dico)} )
            mot_courant = ""
        else:
            mot_courant = mot_courant + c
            
        p = position(dico,mot_courant)

    if mot_courant!="":
        bitsToUse = len( base256( len(dico)-1,0 ) )
        resultat.extend( base256(p,bitsToUse) )

    return octets(resultat,mode)


def ascii(n):
    """transforme un octet en caractère ASCII"""
    try:
        return ( bytes([n]).decode(encoding="ASCII"), 1)
    except UnicodeDecodeError:
        raise RuntimeError("*** Problème, '{}' ne correspond pas à un caractère ASCII !".format(n))

def utf8(octets):
    """transforme un ou plusieurs octet en caractère UTF8"""
    moctets=1
    while moctets <=5:
        try:
            return ( octets[:moctets].decode(encoding="utf-8"), moctets )
        except UnicodeDecodeError:
            moctets+=1

    raise RuntimeError("*** Problème. Trouvé sequence que ne correspond pas à un caractère UTF8 ! %s" % (octets[:moctets],))

def decode(code,mode):
    if mode=="ascii":
        return ascii(code[0])
    elif mode=="utf-8":
        return utf8(code)
    else:
        raise RuntimeError("Encodage %s n'est pas implementée" % (mode,) )

def lz78_decompresse_bin(code,mode="utf-8"):
    dico=[""]

    i=0
    n = len(code)
    t=""
    while(i<n):
        p=0
        bitsToUse = len( base256( len(dico)-1,0 ) )
        while bitsToUse >0:
            p += code[i]*pow(256,bitsToUse-1)
            i+=1

            bitsToUse-=1
    
        if i>=n:
            t+=dico[p]
            break
            
        c,skip = decode( code[i:],mode )
        c=str(c)
        i+= skip

        dico.append(dico[p]+c)
        t+=dico[-1]

    return t
    
def test_lz78(texte):
    print("Chaine de depart: ", texte)
    c = lz78_compresse(texte)
    d = lz78_decompresse(c)
    print("Resultat compresse: ", c)
    print("Resultat decompresse: ", d)
    if(d==texte):
        print('OK')
    else:
        print('Resultat sont differentes')


def lz78_compresse_fichier(fichier):
    """compresse un fichier en utilisant l'algorithme LZ78
    Le résultat est stocké dans un fichier dont le nom est obtenu en ajoutant
    l'extension ".Z78" au nom de fichier donné.
    fichier: nom de fichier (chaine de caractère)
    """
    texte = open(fichier, mode="r").read()
    code = lz78_compresse_bin(texte)
    f = open(fichier + ".Z78", mode="wb")
    f.write(code)
    f.close()

    print("Fichier {} compressé avec succès.".format(fichier))
    print("avant : {} octets".format(len(texte)))
    print("après : {} octets".format(len(code)))

    return code


def lz78_decompresse_fichier(fichier):
    """decompresse un fichier en utilisant l'algorithme LZ78
    Le résultat est stocké dans un fichier dont le nom est obtenu en ajoutant
    l'extension ".A78" au nom de fichier donné.
    fichier: nom de fichier (chaine de caractère)
    """
    code = open(fichier, mode="rb").read()
    texte = lz78_decompresse_bin(code)
    f = open(fichier + ".A78", mode="w")
    f.write(texte)
    f.close()

    print("Fichier {} décompressé avec succès.".format(fichier))
    print("avant : {} octets".format(len(code)))
    print("après : {} octets".format(len(texte)))

    return texte



def main(): 
   m=open("tour-du-monde.txt").read()
   c=lz78_compresse_bin(m)
   d=lz78_decompresse_bin(c)
   print(m==d)
   
   

if __name__=='__main__':
    main()
