import sys, math, random, base64
number_of_bits, min_range_of_e = 1024, pow(2, 50) #1024, 2**50

def pow_by_square_and_multiply(x, n, p):
    # return x^n % p
    x, b, ans = x % p, bin(n)[3:], x
    for i in b:
        ans = (ans * ans) % p
        if i == '1':
            ans = (ans * x) % p
    return ans

def miller_rabin_test(n):
	s, d = 0, n - 1
	while d % 2 == 0:
		d >>= 1
		s += 1

	def trial_composite(a):
		if pow_by_square_and_multiply(a, d, n) == 1:
			return False
		for i in range(s):
			if pow_by_square_and_multiply(a, 2**i * d, n) == n-1:
				return False
		return True

	for i in range(20):
		a = random.randrange(2, n)
		if trial_composite(a):
			return False
	return True

def generate_n_bit_prime(n):
    first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293,307, 311, 313, 317, 331, 337, 347, 349]
    while True:
        ans = random.randrange(2**(n-1) + 1, 2**n - 1)
        valid = True
        for divisor in first_primes_list:
            if ans % divisor == 0:
                valid = False
                break
        if valid and miller_rabin_test(ans):
            return ans

def key_generation(n_bit):
    p, q = generate_n_bit_prime(n_bit), generate_n_bit_prime(n_bit)
    N, r = p * q, (p - 1) * (q - 1)
    e = random.randrange(min_range_of_e, r)  # e can not be too small
    while math.gcd(e, r) != 1:
        e = random.randrange(min_range_of_e, r)
    d = pow(e, -1, r)
    return p, q, N, r, e, d

def RSA(msg, N, key):
    msg, N, key = int.from_bytes(base64.b64decode(msg), 'big'), int(N), int(key)
    msg = pow_by_square_and_multiply(msg, key, N) 
    return base64.b64encode(msg.to_bytes(math.ceil(math.log2(msg)/8), 'big')).decode()

def RSA_by_chinese_remainder_theorem(msg, p, q, key):
    msg, p, q, key = int.from_bytes(base64.b64decode(msg), 'big'), max(int(p), int(q)), min(int(p), int(q)), int(key)
    m1 = pow_by_square_and_multiply(msg, key % (p-1), p)
    m2 = pow_by_square_and_multiply(msg, key % (q-1), q)
    q_inv = pow(q, -1, p)
    h = (q_inv * (m1 - m2)) % p
    msg = m2 + h * q
    return base64.b64encode(msg.to_bytes(math.ceil(math.log2(msg)/8), 'big')).decode()

def test():
    x, n, p = random.randrange(200, 500000000000000000), random.randrange(200, 500000000000000000), random.randrange(200, 500000000000000000)
    if pow_by_square_and_multiply(x, n, p) != pow(x, n, p): print(0)
    p, q, N, r, e, d = key_generation(number_of_bits)
    msg = generate_n_bit_prime(number_of_bits)
    msg = base64.b64encode(msg.to_bytes(math.ceil(math.log2(msg)/8), 'big')).decode()
    if RSA(RSA(msg, N, e), N, d) != msg: print(1)
    if RSA(RSA(msg, N, d), N, e) != msg: print(2)
    if RSA(msg, N, d) != RSA_by_chinese_remainder_theorem(msg, p, q, d): print(3)
    if RSA(msg, N, e) != RSA_by_chinese_remainder_theorem(msg, p, q, e): print(4)

if __name__ == '__main__':
    test()
    func = sys.argv[1][1:]
    argv = sys.argv[2:]
    if func == 'i':
        p, q, N, phi, e, d = key_generation(number_of_bits)
        print('p = ', p, '\nq = ', q, '\nN = ', N, '\nphi = ', phi, '\ne = ', e, '\nd = ', d)
    elif  func == 'e':
        print(RSA(argv[0], argv[1], argv[2]))
    elif  func == 'd':
        print(RSA(argv[0], argv[1], argv[2]))   
    elif  func == 'CRT':
        print(RSA_by_chinese_remainder_theorem(argv[0], argv[1], argv[2], argv[3]))
