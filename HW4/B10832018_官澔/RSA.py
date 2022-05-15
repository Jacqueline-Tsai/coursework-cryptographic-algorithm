from cmath import e
import math
import random
import argparse
import base64
prime_table = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,
    71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,
    167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,
    271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,
    389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,
    503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,
    631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,
    757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,
    883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]

def Exp_mod(x, y, n):
    exp = bin(y)[2:]
    value = x
 
    for i in range(1, len(exp)):
        value = pow(value, 2) % n
        if(exp[i:i+1]=='1'):
            value = (value*x) % n
    
    return value


def Produce_nbit_prime(n):
    has_appear = {}
    while True:
        ispass = True
        randnum = random.randrange(2**(n - 1) + 1, 2 ** n - 1)
        if str(randnum) in has_appear or randnum % 2 == 0:
            continue
        else:
            has_appear[str(randnum)] = True
        for p in prime_table:
            if randnum % p == 0:
                ispass = False
                break
        if ispass == True:
            if Miller_robin_test(randnum) == True:
                return randnum
def Miller_robin_test(n):
    exp = 0
    even = n-1
    while even & 1 == 0:
        even //= 2
        exp += 1
    assert(2**exp * even == n-1)

    def trialComposite(round_tester):
        if Exp_mod(round_tester, even, n) == 1:
            return False
        for i in range(exp):
            if Exp_mod(round_tester, 2**i * even, n) == n - 1:
                return False
        return True
    numberOfRabinTrials = 30
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, n)
        if trialComposite(round_tester):
            return False
    return True


def Produce_key():
    p = Produce_nbit_prime(512)
    q = Produce_nbit_prime(512)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 0
    for i in range(65537, 655379):
        if math.gcd(i, phi) == 1:
            e = i
            break
    d = pow(e, -1, phi)
    print("p = " + str(p))
    print("q = " + str(q))
    print("N = " + str(n))
    print("phi = " + str(phi))
    print("e = " + str(e))
    print("d = " + str(d))

#TODO: 這邊要處力plaintext > n的問題
def Encrypt(plaintext, n, e):
    n = int(n)
    e = int(e)
    m = plaintext.encode('ascii')
    plain_num = int.from_bytes(m, byteorder='little')
    
    cipher = Exp_mod( plain_num, e, n )
    cipher_bytes = cipher.to_bytes((cipher.bit_length() + 7) // 8, byteorder="little")
    base64_msg = base64.b64encode(cipher_bytes)
    print(str(base64_msg)[2:len(str(base64_msg)) - 1])

def Decrypt(ciphertext, n, d):
    n = int(n)
    d = int(d)
    cipher_bytes = base64.b64decode(ciphertext)
    cipher_num = int.from_bytes(cipher_bytes, byteorder='little')
    plain = Exp_mod( cipher_num, d, n)
    plain_bytes = plain.to_bytes((plain.bit_length() + 7) // 8, byteorder="little")
    plaintext = plain_bytes.decode('ascii')
    print(plaintext)

def CRT(ciphertext, p, q, d):
    p = int(p)
    q = int(q)
    d = int(d)
    e = pow(d, -1, (p-1) * (q-1))
    dp = pow(e, -1, p-1)
    dq = pow(e, -1, q-1)
    qinv = pow(q, -1, p)
    cipher_bytes = base64.b64decode(ciphertext)
    cipher_num = int.from_bytes(cipher_bytes, byteorder='little')
    mp = Exp_mod(cipher_num, dp, p)
    mq = Exp_mod(cipher_num, dq, q)
    h = (qinv * (mp - mq)) % p 
    plain = mq + h * q
    plain_bytes = plain.to_bytes((plain.bit_length() + 7) // 8, byteorder="little")
    plaintext = plain_bytes.decode('ascii')
    print(plaintext)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store_true')
    parser.add_argument('-e', dest = 'e', nargs='+')
    parser.add_argument('-d', dest = 'd', nargs = '+')
    parser.add_argument('-CRT', dest = 'CRT', nargs = '+')
    args = parser.parse_args()
    if args.i == True:
        Produce_key()
    elif args.e != None:
        msg = args.e[0]
        n = args.e[1]
        e = args.e[2]
        Encrypt(msg, n, e)
    elif args.d != None:
        Decrypt(args.d[0], args.d[1], args.d[2])
    elif args.CRT != None:
        CRT(args.CRT[0], args.CRT[1], args.CRT[2], args.CRT[3])
    
