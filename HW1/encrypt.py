import sys

def caesar(plaintext, key):
    ciphertext = ""
    for c in plaintext:
        ciphertext += chr((ord(c)-97+int(key))%26+65)
    return ciphertext

def playfair(plaintext, key):
    key2, ciphertext = "", ""
    for i in range(26):
        if not chr(65+i) in key and i != 9:
            key2 += chr(65+i)
    key += key2
    key_matrix = [[key[i*5+j] for j in range(5)]for i in range(5)]
    key_row_column = [[] for i in range(26)]
    for i in range(25):        
        key_row_column[ord(key[i])-65] = [i//5, i%5]

    index = 0
    while index < len(plaintext):
        if index+1 == len(plaintext) or plaintext[index] == plaintext[index+1]:
            plaintext = plaintext[:index+1] + "x" + plaintext[index+1:]
        row1, column1, row2, column2 = key_row_column[ord(plaintext[index])-97][0], key_row_column[ord(plaintext[index])-97][1], key_row_column[ord(plaintext[index+1])-97][0], key_row_column[ord(plaintext[index+1])-97][1]
        if row1 == row2:
            ciphertext += key_matrix[row1][(column1+1)%5] + key_matrix[row2][(column2+1)%5]
        elif column1 == column2:
            ciphertext += key_matrix[(row1+1)%5][column1] + key_matrix[(row2+1)%5][column2]
        else:
            ciphertext += key_matrix[row1][column2] + key_matrix[row2][column1]
        index += 2

    return ciphertext
    
def vernam(plaintext, key):
    ciphertext, key = "", (key+plaintext)[:len(plaintext)]
    print(22^3, key)
    for i in range(len(plaintext)):
        num1, num2 = ord(plaintext[i])-97, ord(key[i])-97
        ciphertext += chr((num1 + num2)%26+65)
    return ciphertext
    
def rail_fence(plaintext, key):
    ciphertext = ""
    for i in range(0, len(plaintext), 2):
        ciphertext += plaintext[i].upper()
    for i in range(1, len(plaintext), 2):
        ciphertext += plaintext[i].upper()
    return ciphertext

def row_transposition(plaintext, key):
    ciphertext, tmp_key = "", ['' for i in range(len(key))]
    for i in range(len(key)):
        tmp_key[int(key[i])-1] = i
    key = tmp_key
    
    rows, columns = (len(plaintext)-1)//len(key)+1, len(key)
    matrix = [[plaintext[i*columns+j] for j in range(columns)]for i in range(rows)]
    for col in key:
        for row in range(rows):
            ciphertext += matrix[row][col].upper()
    return ciphertext

if __name__ == '__main__':
    argv = {}
    for i in range(2, len(sys.argv), 2):
        argv[sys.argv[i-1][-1]] = sys.argv[i]
    
    print(locals()[argv['m']](argv['i'], argv['k']))