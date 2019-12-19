#CRYPTOGRAPHY: DES ALGORITHM
#1801420740 KELVIN ASCLEPIUS MINOR
#1801431662 TOMY
#LA05

import os

#VALIDASI INPUTAN
def is16Hexadecimal(string):
    flag = True
    if len(string) != 16:
        print "Your input must be 16 chars length"
        flag = False
    else:
        for i in range(16):
            if((str(string[i]) < '0' or str(string[i]) > '9')
               and (str(string[i]) < 'A' or str(string[i]) > 'F')
               and (str(string[i]) < 'a' or str(string[i]) > 'f')):
                print "Your input is not hexadecimal"
                flag = False
                break
    return flag

#CONVERT NUMBER SYSTEM
def hex2Bin(hexadecimal):
    return bin(int(hexadecimal, 16))[2:].zfill(16*4)

def bin2Hex(binary):
    return hex(int(binary,2))[2:-1].zfill(16) 

def bin2Dec(binary):
    return int(binary,2)

def dec2Bin(decimal):
    return bin(int(decimal))[2:].zfill(4)

#OPERASI EXCLUSIVE OR
def XOR_operation(binary1, binary2):
    result = ''
    if len(binary1)==len(binary2):
        for i in range(len(binary1)):
            result += str(int(binary1[i])^int(binary2[i]))
    return result

#PERMUTASI: UNTUK KURANGIN, TRANPOSISI, ATAU TAMBAHIN BIT
def permutation(source, table):
    length = len(table)
    target = ['' for i in range(length)]
    for i in range(0, length):
        target[i] = source[table[i]-1]      #-1 soalnya index array mulai dari 0
    target = ''.join(target)                #biar jadi string lagi
    return target

def sBox_Lookup(index,row,col):
    SBox = [[[14,  4,  13,  1,   2, 15,  11,  8,   3, 10,   6, 12,   5,  9,   0,  7,],
             [ 0, 15,   7,  4,  14,  2,  13,  1,  10,  6,  12, 11,   9,  5,   3,  8,],
             [ 4,  1,  14,  8,  13,  6,   2, 11,  15, 12,   9,  7,   3, 10,   5,  0,],
             [15, 12,   8,  2,   4,  9,   1,  7,   5, 11,   3, 14,  10,  0,   6, 13]],

            [[15,  1,   8, 14,   6, 11,   3,  4,   9,  7,   2, 13,  12,  0,   5, 10,],
             [ 3, 13,   4,  7,  15,  2,   8, 14,  12,  0,   1, 10,   6,  9,  11,  5,],
             [ 0, 14,   7, 11,  10,  4,  13,  1,   5,  8,  12,  6,   9,  3,   2, 15,],
             [13,  8,  10,  1,   3, 15,   4,  2,  11,  6,   7, 12,   0,  5,  14,  9]],

            [[10,  0,   9, 14,   6,  3,  15,  5,   1, 13,  12,  7,  11,  4,   2,  8,],
             [13,  7,   0,  9,   3,  4,   6, 10,   2,  8,   5, 14,  12, 11,  15,  1,],
             [13,  6,   4,  9,   8, 15,   3,  0,  11,  1,   2, 12,   5, 10,  14,  7,],
             [ 1, 10,  13,  0,   6,  9,   8,  7,   4, 15,  14,  3,  11,  5,   2, 12]],

            [[ 7, 13,  14,  3,   0,  6,   9, 10,   1,  2,   8,  5,  11, 12,   4, 15,],
             [13,  8,  11,  5,   6, 15,   0,  3,   4,  7,   2, 12,   1, 10,  14,  9,],
             [10,  6,   9,  0,  12, 11,   7, 13,  15,  1,   3, 14,   5,  2,   8,  4,],
             [ 3, 15,   0,  6,  10,  1,  13,  8,   9,  4,   5, 11,  12,  7,   2, 14]],

            [[ 2, 12,   4,  1,   7, 10,  11,  6,   8,  5,   3, 15,  13,  0,  14,  9,],
             [14, 11,   2, 12,   4,  7,  13,  1,   5,  0,  15, 10,   3,  9,   8,  6,],
             [ 4,  2,   1, 11,  10, 13,   7,  8,  15,  9,  12,  5,   6,  3,   0, 14,],
             [11,  8,  12,  7,   1, 14,   2, 13,   6, 15,   0,  9,  10,  4,   5,  3]],

            [[12,  1,  10, 15,   9,  2,   6,  8,   0, 13,   3,  4,  14,  7,   5, 11,],
             [10, 15,   4,  2,   7, 12,   9,  5,   6,  1,  13, 14,   0, 11,   3,  8,],
             [ 9, 14,  15,  5,   2,  8,  12,  3,   7,  0,   4, 10,   1, 13,  11,  6,],
             [ 4,  3,   2, 12,   9,  5,  15, 10,  11, 14,   1,  7,   6,  0,   8, 13]],

            [[ 4, 11,   2, 14,  15,  0,   8, 13,   3, 12,   9,  7,   5, 10,   6,  1,],
             [13,  0,  11,  7,   4,  9,   1, 10,  14,  3,   5, 12,   2, 15,   8,  6,],
             [ 1,  4,  11, 13,  12,  3,   7, 14,  10, 15,   6,  8,   0,  5,   9,  2,],
             [ 6, 11,  13,  8,   1,  4,  10,  7,   9,  5,   0, 15,  14,  2,   3, 12]],

            [[13,  2,   8,  4,   6, 15,  11,  1,  10,  9,   3, 14,   5,  0,  12,  7,],
             [ 1, 15,  13,  8,  10,  3,   7,  4,  12,  5,   6, 11,   0, 14,   9,  2,],
             [ 7, 11,   4,  1,   9, 12,  14,  2,   0,  6,  10, 13,  15,  3,   5,  8,],
             [ 2,  1,  14,  7,   4, 10,   8, 13,  15, 12,   9,  0,   3,  5,   6, 11]]]

    decimal = SBox[index][row][col]
    return dec2Bin(decimal)

#STEP 1
def create16Subkey(key):
    K = [['' for j in range(48)] for i in range(17)]
    K[0] = hex2Bin(key)
    
    #PERMUTATION PC1
    PC1_Table = [57,   49,    41,   33,    25,    17,    9,
                  1,   58,    50,   42,    34,    26,   18,
                 10,    2,    59,   51,    43,    35,   27,
                 19,   11,     3,   60,    52,    44,   36,
                 63,   55,    47,   39,    31,    23,   15,
                  7,   62,    54,   46,    38,    30,   22,
                 14,    6,    61,   53,    45,    37,   29,
                 21,   13,     5,   28,    20,    12,    4]

    Kplus = permutation(K[0], PC1_Table)

    C = [[] for i in range(17)]
    D = [[] for i in range(17)]
    C[0] = Kplus[:len(PC1_Table)/2]
    D[0] = Kplus[len(PC1_Table)/2:]

    leftShift_Table = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
    for i in range(1,17):
        C[i] = C[i-1][leftShift_Table[i-1]:]+C[i-1][0:leftShift_Table[i-1]]
        D[i] = D[i-1][leftShift_Table[i-1]:]+D[i-1][0:leftShift_Table[i-1]]

    #PERMUTATION PC2
    PC2_Table = [14,    17,   11,    24,     1,    5,
                  3,    28,   15,     6,    21,   10,
                 23,    19,   12,     4,    26,    8,
                 16,     7,   27,    20,    13,    2,
                 41,    52,   31,    37,    47,   55,
                 30,    40,   51,    45,    33,   48,
                 44,    49,   39,    56,    34,   53,
                 46,    42,   50,    36,    29,   32]

    lenPC2 = len(PC2_Table)
    for i in range(1,17):
        temp = C[i]+D[i]
        K[i] = permutation(temp, PC2_Table)

    return K

#STEP 2
def encrypt_decrypt(M,K,action):
    IP_Table = [58,    50,   42,    34,    26,   18,    10,    2,
                60,    52,   44,    36,    28,   20,    12,    4,
                62,    54,   46,    38,    30,   22,    14,    6,
                64,    56,   48,    40,    32,   24,    16,    8,
                57,    49,   41,    33,    25,   17,     9,    1,
                59,    51,   43,    35,    27,   19,    11,    3,
                61,    53,   45,    37,    29,   21,    13,    5,
                63,    55,   47,    39,    31,   23,    15,    7]

    M = hex2Bin(M)
    IP = permutation(M, IP_Table)
    #print "IP\t: "+IP

    L = [[] for i in range(17)]
    R = [[] for i in range(17)]
    L[0] = IP[:len(IP_Table)/2]
    R[0] = IP[len(IP_Table)/2:]

    E_Table = [32,     1,    2,     3,     4,    5,
                4,     5,    6,     7,     8,    9,
                8,     9,   10,    11,    12,   13,
               12,    13,   14,    15,    16,   17,
               16,    17,   18,    19,    20,   21,
               20,    21,   22,    23,    24,   25,
               24,    25,   26,    27,    28,   29,
               28,    29,   30,    31,    32,    1]

    P_Table = [16,   7,  20,  21,
               29,  12,  28,  17,
                1,  15,  23,  26,
                5,  18,  31,  10,
                2,   8,  24,  14,
               32,  27,   3,   9,
               19,  13,  30,   6,
               22,  11,   4,  25]

    for i in range(1,17):
        Btemp = ''
        SBtemp = ''
        SB = ''

        #LEFT
        L[i] = R[i-1]

        #RIGHT
        ER = permutation(R[i-1], E_Table)
        if action == "encrypt":
            B = XOR_operation(K[i],ER)
        elif action == "decrypt":
            B = XOR_operation(K[17-i],ER)

        for j in range(0,len(B),6):
            Btemp = B[j:j+6]
            Brow = bin2Dec(Btemp[0] + Btemp[5])
            Bcol = bin2Dec(Btemp[1:5])

            SBtemp = sBox_Lookup(j/6,Brow,Bcol) #j/6 karena stepnya 6, sedangkan indexnya mau: 0,1,2,...,7
            SB += SBtemp

        f = permutation(SB,P_Table)
        R[i] = XOR_operation(L[i-1],f)

        #if action == "encrypt":
        #    print "LR"+str(i)+"\t: "+L[i],R[i]
        #elif action == "decrypt":
        #    print "LR"+str(17-i)+"\t: "+L[i],R[i]

    IPinv_Table = [40,     8,   48,    16,    56,   24,    64,   32,
                   39,     7,   47,    15,    55,   23,    63,   31,
                   38,     6,   46,    14,    54,   22,    62,   30,
                   37,     5,   45,    13,    53,   21,    61,   29,
                   36,     4,   44,    12,    52,   20,    60,   28,
                   35,     3,   43,    11,    51,   19,    59,   27,
                   34,     2,   42,    10,    50,   18,    58,   26,
                   33,     1,   41,     9,    49,   17,    57,   25]
    
    IPinv = permutation(R[16]+L[16],IPinv_Table)
    C = bin2Hex(IPinv).upper()

    return C

def main():

    while True:
        os.system('cls')
        print "=================================="
        print "ENCRYPT-DECRYPT WITH DES ALGORITHM"
        print "=================================="
        print "1. Encrypt Plaintext"
        print "2. Decrypt Ciphertext"
        print "3. Exit"
        choose = raw_input("Choose: ")

        if(choose == "1"):
            while True:
                M = raw_input("Input Plaintext (16 hexadecimal) : ")
                if is16Hexadecimal(M):
                    break

            while True:
                Key = raw_input("Input Key (16 hexadecimal)\t : ")
                if is16Hexadecimal(Key):
                    break

            #STEP 1: CREATE SUBKEY
            K = create16Subkey(Key)
            #for i in range(len(K)):
            #    print "K"+str(i)+"\t: "+K[i]

            #STEP 2: ENCRYPT
            C = encrypt_decrypt(M,K,"encrypt")
            print "Encrypted Message: "+C+" (Ciphertext)"
            raw_input("Press Enter to continue...")
            
        elif(choose == "2"):
            while True:
                C = raw_input("Input Ciphertext (16 hexadecimal) : ")
                if is16Hexadecimal(C):
                    break

            while True:
                Key = raw_input("Input Key (16 hexadecimal)\t  : ")
                if is16Hexadecimal(Key):
                    break

            #STEP 1: CREATE SUBKEY
            K = create16Subkey(Key)
            #for i in range(len(K)):
            #    print "K"+str(i)+"\t: "+K[i]

            #STEP 2: DECRYPT
            M = encrypt_decrypt(C,K,"decrypt")
            print "Decrypted Message: "+M+" (Plaintext)"
            raw_input("Press Enter to continue...")
                
        elif(choose == "3"):
            print "Bye!"
            break
    
main()
