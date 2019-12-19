from random import *

def isPrime(a):
    counter = 0
    for i in range(1,a+1):
        if a%i == 0:
            counter += 1
    if counter == 2:
        return True
    else:
        return False
    
def gcd(a,b):
    while b>0:
        r = a%b
        a = b
        b = r
    return a

def keyGen(p,q):
    n = p*q
    phi = (p-1)*(q-1)
    listE = []

    for i in range(2,phi):
        if(gcd(i,phi)==1):
            listE.append(i)

    e = listE[int(random()*len(listE))]
    e = 31
    for i in range(2,phi):
        if((i*e)%phi == 1):
            d = i
            break

    print "p:",p
    print "q:",q
    print "n:",n
    print "phi:",phi
    print "e:",e
    print "d:",d
    print "Public Key:","[",e,",",n,"]"
    print "Private Key:","[",d,",",n,"]"
    return d,e,n

def encryptRSA(e,n):
    m = input("Input Message (M): ")
    c = m**e%n
    return c

def decryptRSA(d,n):
    c = input("Input Ciphertext (C): ")
    m = c**d%n
    return m

def main():
    while True:
        p = input("p: ")
        q = input("q: ")
        if(isPrime(p) and isPrime(q) and p!=q):
            break
        elif(p==q):
            print "p must not equal to q"
        else:
            print "p and q must both prime"

    d,e,n = keyGen(p,q)
    ciphertext = encryptRSA(e,n)
    print ciphertext
    plaintext = decryptRSA(d,n)
    print plaintext

def genPrime(a,b):
    primeList = []
    for i in range(a,b+1):
        if(isPrime(i)):
            primeList.append(i)
    return primeList

def trialandErrorPQ(n):
    primeList = genPrime(1,n)
    for i in range(len(primeList)):
        for j in range(len(primeList)):
            if i<j:
                if(primeList[i]*primeList[j] == n):
                    p = primeList[i]
                    q = primeList[j]
                    break
    return p,q

print trialandErrorPQ(3599)
main()
