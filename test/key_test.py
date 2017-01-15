# from ecdsa import NIST384p, SigningKey
# from ecdsa.util import randrange_from_seed__trytryagain

# def make_key(seed):
# 	secexp = randrange_from_seed__trytryagain(seed, NIST384p.order)
# 	return SigningKey.from_secret_exponent(secexp, curve=NIST384p)

# key = make_key("secret")
# vkey = key.get_verifying_key()

# print( vkey.pubkey.point )

from hashlib import sha256
from bitcoin.signature import DERSignature
from bitcoin.core import _bignum
from ecdsa.keys import SigningKey, VerifyingKey
from ecdsa.curves import SECP256k1
from ecdsa import rfc6979
from six import b
import struct
import binascii

def test_deterministic(secret):
	data = binascii.unhexlify(
"000e2d340103a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de9331763\
4867b592574acee187f01a3aed0172a7cb0c7b0000000000000000000000000000000000000000000\
000000000000000000000000000000000000000000000000000000000000000000000000000000000\
00008096980000000000")
	sign = binascii.unhexlify(
"3045022100b9703cbc89dc0cb82d036536e07a703caeb345a2ef8fd01f1aec4b81c7a15416022022\
fe89619f2faab5cb2e33822aa129be14780d3798309bae3676964fa442bd6d")

	h = sha256(data+sign).digest()
	print(struct.unpack(">Q", h[:8]))
	print(struct.unpack("<Q", h[:8]))

	# secexp = int(sha256(secret).hexdigest(), 16)
	# priv = SigningKey.from_secret_exponent(secexp, SECP256k1, sha256)
	# pub = priv.get_verifying_key()

	# k = rfc6979.generate_k(SECP256k1.generator.order(), secexp, sha256, sha256(data).digest())
	# sig1 = priv.sign(data, k=k)
	# print(sig1.hex())
	# return DERSignature(sig1[:32], sig1[32:], 64)
	

test_deterministic(b"secret")

