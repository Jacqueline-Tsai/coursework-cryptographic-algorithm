import sys, arguments, decrypt



def data_decryption_standard(input, key):
    input = bin(int(input, 16))[2:].zfill(64)
    key = bin(int(key, 16))[2:].zfill(64)
    keys = decrypt.generate_keys(key)
    input = decrypt.IP_permutation(input)
    
    left_half, right_half = input[:32], input[32:]
    for i in range(0, 16):#
        tmp1, tmp2 = decrypt.F(right_half, keys[i]), ""
        for j in range(32):
            tmp2 += str(int(left_half[j]) ^ int(tmp1[j]))
        left_half = right_half
        right_half = tmp2
    
    ans = decrypt.IP_reverse_permutation(right_half + left_half)
    ans = hex(int(ans, 2))[2:]
    return "0x" + "0"*(16-len(ans)) + ans.upper()

if __name__ == '__main__':
    argv = {}
    for i in range(2, len(sys.argv), 2):
        argv[sys.argv[i-1][-1]] = sys.argv[i]
 
    print(data_decryption_standard(argv['i'].upper(), argv['k'].upper()))