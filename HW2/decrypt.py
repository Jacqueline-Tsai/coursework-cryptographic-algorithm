import sys, math, arguments
def IP_permutation(input):
    ans = ""
    for i in range(64):
        ans += input[arguments.IP[i]-1]
    return ans

def IP_reverse_permutation(input):
    ans = ""
    for i in range(64):
        ans += input[arguments.IP_reverse[i]-1]
    return ans

def P_permutation(input):
    ans = ""
    for i in range(32):
        ans += input[arguments.P[i]-1]
    return ans

def generate_keys(key):
    tmp = ""
    for i in range(56):
        tmp += key[arguments.PC1[i]-1]
    left_half, right_half = tmp[:28], tmp[28:]
    keys = []
    for i in range(16):
        left_half = left_half[arguments.number_of_shit[i]:] + left_half[:arguments.number_of_shit[i]]
        right_half = right_half[arguments.number_of_shit[i]:] + right_half[:arguments.number_of_shit[i]]
        tmp = left_half + right_half
        tmp_key = ""
        for i in range(48):
            tmp_key += tmp[arguments.PC2[i]-1]
        keys += [tmp_key]
    return keys

def F(input, key):
    tmp = ""
    for i in range(48):
        tmp += input[arguments.E[i]-1]
    input = tmp
    tmp = ""
    for i in range(48):
        tmp += "0" if input[i]==key[i] else "1"
    input = tmp
    ans = ""
    for i in range(8):
        tmp = arguments.S_box[i][int(input[6*i]+input[6*i+5], 2)][int(input[6*i+1:6*i+5], 2)]
        ans += bin(tmp)[2:].zfill(4)
    ans = P_permutation(ans)
    return ans

def data_encryption_standard(input, key):
    input = bin(int(input, 16))[2:].zfill(64)
    key = bin(int(key, 16))[2:].zfill(64)
    keys = generate_keys(key)
    input = IP_permutation(input)
    
    left_half, right_half = input[:32], input[32:]
    for i in range(15, -1, -1):#
        tmp1, tmp2 = F(right_half, keys[i]), ""
        for j in range(32):
            tmp2 += "0" if left_half[j]==tmp1[j] else "1"
        left_half = right_half
        right_half = tmp2
    
    ans = IP_reverse_permutation(right_half + left_half)
    ans = hex(int(ans, 2))[2:]
    return "0x" + "0"*(16-len(ans)) + ans.upper()

if __name__ == '__main__':
    argv = {}
    for i in range(2, len(sys.argv), 2):
        argv[sys.argv[i-1][-1]] = sys.argv[i]
 
    print(data_encryption_standard(argv['i'].upper(), argv['k'].upper()))