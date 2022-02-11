# S1: generate large number (p)
# S2: Miller-rabin prime number test
# S3: Find number primitive root generator 'g' from p
# S4: Perform diffie Hellman key exchange with 'g' and prime to generate pk and sk and shared key
# S5: ElGamal Encryption (encoding)
# S5.1 break message up
# S5.2 Encode
# S6: Decryption
# S7: end

from numpy import byte
from sympy.ntheory.primetest import mr
import random
import secrets
from math import sqrt
from itertools import islice
# use primes up to 37 for 2^64 bit integers for miller rabin test
prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 31, 37]


# generate odd number
def generate_rand_number(min, max):
    return random.randrange(min, max, 2)


# use miller rabin to test if number is prime
def is_prime(min, max):

    while True:
        p = generate_rand_number(min, max)
        if mr(p, prime_list) == True:
            return p
# chosen prime p = 12015079137676779473


# From: https://www.geeksforgeeks.org/primitive-root-of-a-prime-number-n-modulo-n/
def findPrimefactors(s, n):

    # Print the number of 2s that divide n
    while (n % 2 == 0):
        s.add(2)
        n = n // 2

    # n must be odd at this po. So we can
    # skip one element (Note i = i +2)
    for i in range(3, int(sqrt(n)), 2):

        # While i divides n, print i and divide n
        while (n % i == 0):

            s.add(i)
            n = n // i

    # This condition is to handle the case
    # when n is a prime number greater than 2
    if (n > 2):
        s.add(n)


# uses Euler's Totient to find primitive root of a prime AKA 'g'
# From: https://www.geeksforgeeks.org/primitive-root-of-a-prime-number-n-modulo-n/
def find_generator(n):
    s = set()
    phi = n - 1
    findPrimefactors(s, phi)

    for r in range(2, phi+1):
        flag = False
        for it in s:
            if(pow(r, phi//it, n) == 1):
                flag = True
                break
        if (flag == False):
            return r

    return -1
# chosen 'g' for 'p' = 3


# Diffie_hellman key exchange protocol
def diffie_hellman():
    p = 12015079137676779473
    g = 3

    secret_alice = secrets.randbits(32)
    public_alice = pow(g, secret_alice, p)

    secret_bob = secrets.randbits(32)
    public_bob = pow(g, secret_bob, p)

    # alice secret key from bob
    sharedKey_alice = pow(public_bob, secret_alice, p)
    sharedKey_bob = pow(public_alice, secret_bob, p)
    print(sharedKey_alice)
    print(sharedKey_bob)
# alice sk: 1387309942, pk: 7811671445020318667, shared: 4579848827226567092
# bob sk: 239411270, pk: 2732429492559587050, shared: 4579848827226567092


# coverts given message to utf-8 bytes to relevant integers
def convert_message():
    string = "identifier generation indulgence"
    byte_format = string.encode('utf-8')
    int_format = int.from_bytes(byte_format, "little")
    return int_format


# converts integers from convert_message() to string and breaks them up into blocks
def split(n):
    list = []
    message = str(convert_message())
    for i in range(0, len(message), n):
        list.append(int(message[i:i+n]))
    print(str(list))


def encryption():
