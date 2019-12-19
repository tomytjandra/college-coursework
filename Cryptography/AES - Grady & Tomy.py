##Tomy 1801431662
##Grady 1801390403

from numpy import *

sBox = [[0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
        [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
        [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
        [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
        [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
        [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
        [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
        [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
        [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
        [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
        [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
        [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
        [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
        [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
        [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
        [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]]

invsBox = [[0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB],
            [0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB],
            [0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E],
            [0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25],
            [0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92],
            [0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84],
            [0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06],
            [0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B],
            [0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73],
            [0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E],
            [0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B],
            [0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4],
            [0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F],
            [0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF],
            [0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61],
            [0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D]]

mat = [["02","03","01","01"],
       ["01","02","03","01"],
       ["01","01","02","03"],
       ["03","01","01","02"]]

invmat = [["0E","0B","0D","09"],
          ["09","0E","0B","0D"],
          ["0D","09","0E","0B"],
          ["0B","0D","09","0E"]]

#change base number
def hex2Bin(hexa):
    return bin(int(hexa,16))[2:].zfill(8)

def bin2Hex(binary):
    return hex(int(binary,2))[2:].zfill(2).upper()

def hex2Dec(hex):
    return int(hex,16)

def dec2Hex(dec):
    return hex(dec)[2:].upper()

#change list structure
def transposeList(list1):
    return map(list, zip(*list1))

#change type data
def list2String(list):
    temp = ""
    for i in list:
        temp += str(i)
    return temp

def matrix2String(matrix):
    result = ""
    for i in range(len(matrix[0])):
        for j in range(len(matrix)):
            result += matrix[j][i]
    return result

def string2Matrix(string):
    result = []
    for i in range(4):
        tempList = []
        for j in range(4):
            temp = string[2*(4*i+j):2*(4*i+j)+2]
            tempList.append(temp)
        result.append(tempList)
    return transposeList(result)

#operation for mix column
def XOR(a,b):
    temp = ""
    if len(a) == len(b):
        for i in range(len(a)):
            temp += str((int(a[i])+int(b[i]))%2)
    return temp

def multiplyPoly(p,q):
    pb = list(hex2Bin(p))
    qb = list(hex2Bin(q))
    #convert string to int list
    pb = map(int,pb)
    qb = map(int,qb)
    
    p = poly1d(pb)
    q = poly1d(qb)
    m = poly1d([1,0,0,0,1,1,0,1,1])
    remCof = polydiv(polymul(p,q),m)[1].c%2
    return map(int,list(remCof))

def matrixOperation(rowAndCol):
    for i in range(0,len(rowAndCol),2):
        binary = list2String(multiplyPoly(rowAndCol[i],rowAndCol[i+1])).zfill(8)
        res = binary if i==0 else XOR(res,binary)
    return bin2Hex(res)
                   
#function for AES Encryption
def subByte(matrix):
    result = []
    for i in range(len(matrix)):
        tempList = []
        for j in range(len(matrix[0])):
            row = hex2Dec(matrix[i][j][0])
            col = hex2Dec(matrix[i][j][1])
            temp = dec2Hex(sBox[row][col])
            tempList.append(temp)
        result.append(tempList)
    return result

def shiftRows(matrix):
    result = []
    for i in range(4):
        tempList = []
        for j in range(4):
            tempList.append(matrix[i][(j+i)%4])
        result.append(tempList)
    return result

def mixColumns(matrix):
    result = []
    for i in range(4):
        tempOneCol = []
        for j in range(4):
            rowAndCol = []
            for k in range(4):
                rowAndCol.append(mat[i][k])
                rowAndCol.append(matrix[k][j])
            temp = matrixOperation(rowAndCol)
            tempOneCol.append(temp)
        result.append(tempOneCol)
    return result

def addRoundKey(matrix,key):
    result = []
    for i in range(4):
        tempList = []
        for j in range(4):
            temp = XOR(hex2Bin(matrix[i][j]), hex2Bin(key[i][j]))
            tempList.append(bin2Hex(temp))
        result.append(tempList)
    return result

#function for AES Decryption
def inverseSubByte(matrix):
    result = []
    for i in range(len(matrix)):
        tempList = []
        for j in range(len(matrix[0])):
            row = hex2Dec(matrix[i][j][0])
            col = hex2Dec(matrix[i][j][1])
            temp = dec2Hex(invsBox[row][col])
            tempList.append(temp)
        result.append(tempList)
    print result
    return result

def inverseShiftRows(matrix):
    result = []
    for i in range(4):
        tempList = []
        for j in range(4):
            tempList.append(matrix[i][(j-i)%4])
        result.append(tempList)
    print result
    return result

def inverseMixColumns(matrix):
    result = []
    for i in range(4):
        tempOneCol = []
        for j in range(4):
            rowAndCol = []
            for k in range(4):
                rowAndCol.append(invmat[i][k])
                rowAndCol.append(matrix[k][j])
            temp = matrixOperation(rowAndCol)
            tempOneCol.append(temp)
        result.append(tempOneCol)
    print result
    return result

def keyExpansion(matrix,rounds):
    rcon = [["01","00","00","00"],
            ["02","00","00","00"],
            ["04","00","00","00"],
            ["08","00","00","00"],
            ["10","00","00","00"],
            ["20","00","00","00"],
            ["40","00","00","00"],
            ["80","00","00","00"],
            ["1B","00","00","00"],
            ["36","00","00","00"]]
    tempMat = transposeList(matrix)
    lenMat = len(matrix)
    for i in range(rounds+1):
        RotWord = tempMat[lenMat-1]
        RotWord = RotWord[1:]
        RotWord.append(tempMat[lenMat-1][0])
        SubWord = subByte([RotWord])
        Z = []
        for j in range(len(SubWord[0])):
            Z.append(bin2Hex(XOR(hex2Bin(SubWord[0][j]),hex2Bin(rcon[i][j]))))
        for j in range(len(rcon[i])):
            temp = []
            for k in range(len(Z)):
                temp.append(bin2Hex(XOR(hex2Bin(Z[k]),hex2Bin(tempMat[j][k]))))
            tempMat[j] = temp
            Z = temp
    print transposeList(tempMat)
    return transposeList(tempMat)

def encryptAES(plaintext,key):
    matrix = string2Matrix(plaintext)
    key = string2Matrix(key)
    n = 10 #no. of rounds
    result = addRoundKey(matrix,key)
    for i in range(n):
        if i != n-1:
            result = addRoundKey(mixColumns(shiftRows(subByte(result))),keyExpansion(key,i))
        else:
            result = addRoundKey(shiftRows(subByte(result)),keyExpansion(key,i))
    return matrix2String(result)

def decryptAES(ciphertext,key):
    matrix = string2Matrix(ciphertext)
    key = string2Matrix(key)
    n = 10 #no. of rounds
    result = addRoundKey(matrix,keyExpansion(key,n-1))
    for i in range(n):
        print
        print result
        print
        if i!=n-1:
            result = inverseMixColumns(addRoundKey(inverseSubByte(inverseShiftRows(result)),keyExpansion(key,n-i-2)))
        else:
            result = addRoundKey(inverseSubByte(inverseShiftRows(result)),key)
        print result
    return matrix2String(result)

plaintext = "0123456789ABCDEFFEDCBA9876543210"
key = "0F1571C947D9E8590CB7ADD6AF7F6798"
ciphertext = encryptAES(plaintext,key)
plaintext = decryptAES(ciphertext,key)
print plaintext
print ciphertext