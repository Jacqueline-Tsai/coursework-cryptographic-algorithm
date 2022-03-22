import argparse
import sys

def caesar(ciphertext, key):
    plaintext = ''
    offset = ord('a') - ord('A')
    for i in ciphertext:
        plaintext += chr((ord(i)-65 - int(key))%26+65+offset)
    return plaintext

def playfair(ciphertext, key):
    plaintext = ''
    key2 = ''
    key_t = ''
    keyset = set(key)
    for i in range(len(key)):
        if key[i] in keyset:
            key_t += key[i]
            keyset.remove(key[i])


    row_size = 5
    for i in range(26):
        if not chr(65+i) in key_t and i != 9:
            key2 += chr(65+i)
    key_t += key2
    dict_key = {}
    for i in range(0,5):
        for j in range(0,5):
            dict_key[key_t[i*5+j]] = [i,j]
    
    for i in range(0, len(ciphertext), 2):
        row_1, col_1 = dict_key[ciphertext[i]][0], dict_key[ciphertext[i]][1]
        if i+1 < len(ciphertext):
            row_2, col_2 = dict_key[ciphertext[i+1]][0], dict_key[ciphertext[i+1]][1]
        if row_1 == row_2:
            plaintext += key_t[row_1 * row_size + (col_1 - 1) % row_size] + key_t[row_2 * row_size + (col_2 - 1) % row_size]
        elif col_1 == col_2:
            plaintext += key_t[((row_1 - 1) % row_size) * row_size + col_1] + key_t[((row_2 - 1) % row_size) * row_size + col_2]
        else:
            plaintext += key_t[row_1 * row_size + col_2] + key_t[row_2 * row_size + col_1] 
    plain = ''
    plain += plaintext[0]
    for i in range(1, len(plaintext)-1):
        if plaintext[i] == 'X':
            if i == len(plaintext)-1 or plaintext[i-1] == plaintext[i+1]:
                continue
                #plaintext = plaintext[:i] + plaintext[i+1:]
        else:
            plain += plaintext[i]
    if plaintext[len(plaintext)-1] != 'X':
        plain += plaintext[len(plaintext)-1]
        
    return plain.lower()


def vernam(ciphertext, key):
    plaintext = ""
    #get the autokey
    offset = 0
    init_key_len = len(key)
    while len(key) < len(ciphertext):
        for i in range(init_key_len):
            if len(key) >= len(ciphertext):
                break
            num = ((ord(ciphertext[offset * init_key_len + i])-65)^(ord(key[offset * init_key_len + i])-65)) % 26 + 65
            key += chr(num)
        offset += 1
    print(key)

    for cy, k in zip(ciphertext, key):
        num = ((ord(cy)-65)^(ord(k)-65)) % 26 + 65
        plaintext += chr(num)
    return plaintext.lower()
    

def railfence(ciphertext, key):
    key = int(key)
    plaintext = list(range(len(ciphertext)))
    row_len_list = list(range(key))
    cycle_len = (key-1) * 2
    cycles = int(len(ciphertext) / cycle_len)
    remain = len(ciphertext) % cycle_len
    #process full cycle
    for i in range(key):
        if i == 0:
            row_len_list[i] = cycles
        elif i == key-1:
            row_len_list[i] = cycles
        else:
            row_len_list[i] = 2*cycles
    #process remain cycle
    for i in range(remain):
        if i < key:
            row_len_list[i] += 1
        else:
            row_len_list[key-1 -(i-key+1)] += 1
    offset = cycle_len
    index, direction = 0, True
    start_index, cipher_index = 0, 0
    for size in row_len_list:
        if offset == 0:
            offset = cycle_len
        op_offset = cycle_len - offset
        
        index = start_index
        for i in range(size):
            plaintext[index] = ciphertext[cipher_index]
            cipher_index += 1
            if direction or op_offset == 0:
                index += offset
            else:
                index += op_offset
            direction = not direction
        start_index += 1
        direction = True
        offset -= 2
    plaintext_str = ''.join(plaintext)
    return plaintext_str.lower()

def row(ciphertext, key):
    key = str(key)
    plaintext = ''
    rows, cols = (len(ciphertext)-1)//len(key)+1, len(key)

    board_size = rows * cols
    remain = board_size % len(ciphertext)
    key_list = []
    for i in range(remain):
        key_list.append(int(key[len(key)-1-i]))
    key_list = sorted(key_list)
    for i in key_list:
        ciphertext = ciphertext[:i * rows-1] + '-' + ciphertext[i * rows-1:]
    board = [['' for j in range(cols)]for i in range(rows)]

    col_index = 0
    for i in key:
        index = int(i) - 1
        for j in range(rows):
            board[j][col_index] = ciphertext[index * rows + j]
        col_index += 1

    for i in range(rows):
        for j in range(cols):
            if board[i][j] != '-':
                plaintext += board[i][j]
    return plaintext.lower()


if __name__ == '__main__':
    argv = {}
    for i in range(2, len(sys.argv), 2):
        argv[sys.argv[i-1][-1]] = sys.argv[i]
    
    print(locals()[argv['m']](argv['i'].upper(), argv['k'].upper()))