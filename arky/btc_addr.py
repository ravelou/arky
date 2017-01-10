#!/usr/bin/env python
import ctypes
import hashlib
import random

""" base58 encoding / decoding functions """
 
alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
base_count = len(alphabet)
        
def encode(num):
    """ Returns num in a base58-encoded string """
    encode = ''
    
    if (num < 0):
        return ''
    
    while (num >= base_count):    
        mod = num % base_count
        encode = alphabet[mod] + encode
        num = num // base_count
 
    if (num):
        encode = alphabet[num] + encode
 
    return encode
 
def decode(s):
    """ Decodes the base58-encoded string s into an integer """
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * alphabet.index(char)
        multi = multi * base_count
        
    return decoded

################################################################################
################################################################################
ssl_library = ctypes.cdll.LoadLibrary('libssl.so')

seed_method = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int)
bytes_method = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_int)
cleanup_method = ctypes.CFUNCTYPE(None)
add_method = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int, ctypes.c_double)
pseudorand_method = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int)
status_method = ctypes.CFUNCTYPE(None)

"""
typedef struct rand_meth_st
{
    void (*seed)(const void *buf, int num);
    int (*bytes)(unsigned char *buf, int num);
    void (*cleanup)(void);
    void (*add)(const void *buf, int num, int entropy);
    int (*pseudorand)(unsigned char *buf, int num);
    int (*status)(void);
} RAND_METHOD;
"""

class RAND_METHOD(ctypes.Structure):
    _fields_ = [
        ("seed", seed_method),
        ("bytes", bytes_method),
        ("cleanup", cleanup_method),
        ("add", add_method),
        ("pseudorand", pseudorand_method),
        ("status", status_method),
    ]

RAND_get_rand_method = ssl_library.RAND_get_rand_method
RAND_get_rand_method.restype = ctypes.POINTER(RAND_METHOD)
original = RAND_get_rand_method().contents
seed = None

@seed_method
def r_seed(buf, num):
    if not r_seed.seeded:
        r_seed.seeded = True
    else:
        print('not seed')
r_seed.seeded = False

@bytes_method
def r_bytes(buf, num):
    p = ctypes.cast(ctypes.pointer(ctypes.c_int(buf)), ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte))).contents
    for i in range(num):
        p[i] = random.randrange(0,255)
    return 1
 
@cleanup_method
def r_cleanup():
    r_seed.seeded = False

@add_method
def r_add(buf, num, entropy):
    pass

@pseudorand_method
def r_pseudorand(buf, num):
    pass

@status_method
def r_status():
    pass

def gen_ecdsa_pair():
    NID_secp160k1 = 708
    NID_secp256k1 = 714
    k = ssl_library.EC_KEY_new_by_curve_name(NID_secp256k1)

    if seed is not None:
        rmeth = RAND_METHOD()
        rmeth.seed = r_seed
        rmeth.bytes = r_bytes
        rmeth.cleanup = r_cleanup
        rmeth.add = r_add
        rmeth.pseudorand = r_pseudorand
        rmeth.status = r_status
        ssl_library.RAND_set_rand_method(ctypes.byref(rmeth))

    if ssl_library.EC_KEY_generate_key(k) != 1:
        raise Exception("internal error?")

    bignum_private_key = ssl_library.EC_KEY_get0_private_key(k)
    size = (ssl_library.BN_num_bits(bignum_private_key)+7)//8
    #print("Key size is {} bytes".format(size))
    storage = ctypes.create_string_buffer(size)
    ssl_library.BN_bn2bin(bignum_private_key, storage)
    private_key = storage.raw

    size = ssl_library.i2o_ECPublicKey(k, 0)
    #print("Pubkey size is {} bytes".format(size))
    storage = ctypes.create_string_buffer(size)
    ssl_library.i2o_ECPublicKey(k, ctypes.byref(ctypes.pointer(storage)))
    public_key = storage.raw

    ssl_library.EC_KEY_free(k)
    return public_key, private_key

def ecdsa_get_coordinates(public_key):
    x = bytes(public_key[1:33])
    y = bytes(public_key[33:65])
    return x, y

def generate_address(public_key):
    assert isinstance(public_key, bytes)

    x, y = ecdsa_get_coordinates(public_key)
    
    s = b'\x04' + x + y
    #print('0x04 + x + y:', ''.join(['{:02X}'.format(i) for i in s]))

    hasher = hashlib.sha256()
    hasher.update(s)
    r = hasher.digest()
    #print('SHA256(0x04 + x + y):', ''.join(['{:02X}'.format(i) for i in r]))

    hasher = hashlib.new('ripemd160')
    hasher.update(r)
    r = hasher.digest()
    #print('RIPEMD160(SHA256(0x04 + x + y)):', ''.join(['{:02X}'.format(i) for i in r]))

    # Since '1' is a zero byte, it won't be present in the output address.
    return '1' + base58_check(r, version=0)

def base58_check(src, version=0):
    src = bytes([version]) + src
    hasher = hashlib.sha256()
    hasher.update(src)
    r = hasher.digest()
    #print('SHA256(0x00 + r):', ''.join(['{:02X}'.format(i) for i in r]))

    hasher = hashlib.sha256()
    hasher.update(r)
    r = hasher.digest()
    #print('SHA256(SHA256(0x00 + r)):', ''.join(['{:02X}'.format(i) for i in r]))

    checksum = r[:4]
    s = src + checksum
    #print('src + checksum:', ''.join(['{:02X}'.format(i) for i in s]))

    return base58_encode(int.from_bytes(s, 'big'))

def test():
    global seed
    seed = input("Enter a seed (enter for Random): ")
    if len(seed) == 0:
        seed = None
    else:
        random.seed(seed)
    public_key, private_key = gen_ecdsa_pair()

    hex_private_key = ''.join(["{:02x}".format(i) for i in private_key])
    assert len(hex_private_key) == 64

    print("ECDSA private key (random number / secret exponent) = {}".format(hex_private_key))
    print("ECDSA public key = {}".format(''.join(['{:02x}'.format(i) for i in public_key])))
    print("Bitcoin private key (Base58Check) = {}".format(base58_check(private_key, version=128)))

    addr = generate_address(public_key)
    print("Bitcoin Address: {} (length={})".format(addr, len(addr)))


if __name__ == "__main__":
    test()