def CaesarEncrypt(move, plaintext):
    ciphertext = ""
    for i in range(len(plaintext)):
        if plaintext[i] != ' ':
            if plaintext[i] >= 'A' and plaintext[i] <= 'Z':
                ciphertext += chr((ord(plaintext[i])+move-ord('A'))%26 + ord('A'))
            elif plaintext[i] >= 'a' and plaintext[i] <= 'z':
                ciphertext += chr((ord(plaintext[i])+move-ord('a'))%26 + ord('a'))
            else:
                ciphertext += plaintext[i]
        else:
            ciphertext += ' '
    return ciphertext

def CaesarDecrypt(move, ciphertext):
    plaintext = CaesarEncrypt(-move, ciphertext)
    return plaintext
    
