#TOMY 1801431662

import numpy as np

K = [[5,8],[17,3]]
Kinv = [[9,2],[1,15]]

def cvtText2Matrix(text):
    temp = np.zeros(len(text))
    text = text.upper()
    for i in range(len(text)):
        temp[i] = ord(text[i])-ord("A")
    return temp.reshape((len(text)/len(K),len(K)))
    
def HillEncrypt(plaintext):
    if(len(plaintext)%len(K) == 0):
        P = cvtText2Matrix(plaintext)
        C = np.dot(P,K)%26
        ciphertext = ""
        for i in range(0,len(plaintext)/len(K)):
            for j in range(0,len(K)):
                ciphertext += chr(int(C[i][j]+ord("A")))
        print ciphertext
    else:
        print "Length must be multiple of",len(K)

def HillDecrypt(ciphertext):
    if(len(ciphertext)%len(K) == 0):
        C = cvtText2Matrix(ciphertext)
        P = np.dot(C,Kinv)%26

        plaintext = ""
        for i in range(0,len(ciphertext)/len(K)):
            for j in range(0,len(K)):
                plaintext += chr(int(P[i][j]+ord("A")))
        print plaintext
    else:
        print "Length must be multiple of",len(K)
