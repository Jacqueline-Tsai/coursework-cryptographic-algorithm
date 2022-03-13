import sys

def caesar(plaintext, key):
    ciphertext = ""
    for c in plaintext:
        ciphertext += chr((ord(c)-65+int(key))%26+65)
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
            plaintext = plaintext[:index+1] + "X" + plaintext[index+1:]
        row1, column1, row2, column2 = key_row_column[ord(plaintext[index])-65][0], key_row_column[ord(plaintext[index])-65][1], key_row_column[ord(plaintext[index+1])-65][0], key_row_column[ord(plaintext[index+1])-65][1]
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
    for i in range(len(plaintext)):
        num1, num2 = ord(plaintext[i])-65, ord(key[i])-65
        ciphertext += chr((num1 ^ num2)%26+65)
    return ciphertext
    
def railfence(plaintext, key):
    ciphertext, ciphertext_list, direction, index = "", ["" for i in range(int(key))], -1, 0

    for c in plaintext:
        ciphertext_list[index] += c
        if index==0 or index==int(key)-1:
            direction = 0-direction
        index += direction
    for text in ciphertext_list:
        ciphertext += text
    
    return ciphertext

def row(plaintext, key):
    ciphertext, tmp_key = "", ['' for i in range(len(key))]
    for i in range(len(key)):
        tmp_key[int(key[i])-1] = i
    key = tmp_key
    
    rows, columns = (len(plaintext)-1)//len(key)+1, len(key)
    matrix = [[plaintext[i*columns+j] for j in range(columns)]for i in range(rows)]
    for col in key:
        for row in range(rows):
            ciphertext += matrix[row][col]
    return ciphertext

if __name__ == '__main__':
    argv = {}
    for i in range(2, len(sys.argv), 2):
        argv[sys.argv[i-1][-1]] = sys.argv[i]
    
    print(locals()[argv['m']](argv['i'].upper(), argv['k'].upper()))