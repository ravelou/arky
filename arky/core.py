# -*- encoding: utf8 -*-
# docstring according to https://www.python.org/dev/peps/pep-0257

from bitcoin.core import key
from ecdsa.keys import SigningKey, VerifyingKey
from ecdsa.curves import SECP256k1
from ecdsa import rfc6979

from . import StringIO, __PY3__, __FEES__, slots, base58, api, ark, testnet, ArkyDict
import struct, hashlib, binascii, json

class NoSecretDefinedError(Exception): pass
class NoSenderDefinedError(Exception): pass
class NotSignedTransactionError(Exception): pass

# read value binary data from buffer
unpack = lambda fmt, fileobj: struct.unpack(fmt, fileobj.read(struct.calcsize(fmt)))
# write value binary data into buffer
pack =  lambda fmt, fileobj, value: fileobj.write(struct.pack(fmt, *value))
# write bytes as binary data into buffer
pack_bytes = lambda f,v: pack("<"+"%ss"%len(v), f, (v,)) if __PY3__ else \
             lambda f,v: pack("<"+"c"*len(v), f, v)


def toBip66(sig):
	"""
Convert a bytes signature into a DER one.

Argument:
sig (bytes) -- a signature

Returns bytes
"""
	halfsize = len(sig)//2
	r, s = sig[:halfsize], sig[halfsize:]
	r_size = len(r); s_size = len(s)
	der_size = 6 + r_size + s_size
	# 0x30 [total-length] 0x02 [R-length] [R] 0x02 [S-length] [S]
	return b"\x30" + struct.pack("<b", der_size-2) + \
	       b"\x02" + struct.pack("<b", r_size+1) + r + \
	       b"\x02" + struct.pack("<b", s_size) + s

def getKeys(secret="passphrase", seed=None, network=None):
	"""
Generate `keys` containing `network`, `public` and `private` key as attribute.
`secret` or `seed` have to be provided, if `network` is not, `ark` is
automatically selected.

Keyword arguments:
secret (str or bytes) -- a human pass phrase
seed (byte)           -- a sha256 sequence bytes
network (object)      -- a python object

Returns ArkyDict
"""
	network = ark if network == None else network # use ark network by default
	seed = hashlib.sha256(secret.encode("utf8") if not isinstance(secret, bytes) else secret).digest() if not seed else seed

	keys = ArkyDict()
	# save network option
	keys.network = network
	# save private key ?
	keys.private = seed
	# generate public key
	cec_key = key.CECKey()
	cec_key.set_compressed(network.get("compressed", True))
	cec_key.set_secretbytes(secret=seed)
	keys.public = cec_key.get_pubkey()
	# generate signing object
	secret_exposent = int(binascii.hexlify(seed), 16)
	keys.signingKey = SigningKey.from_secret_exponent(secret_exposent, SECP256k1, hashlib.sha256)
	keys.checkingKey = keys.signingKey.get_verifying_key()
	keys.secret_exposent = secret_exposent

	return keys

def getSignature(data, keys):
	return keys.signingKey.sign(data, k=rfc6979.generate_k(
		SECP256k1.generator.order(),
		keys.secret_exposent,
		hashlib.sha256,
		hashlib.sha256(data).digest()
	))

def getAddress(keys):
	"""
Computes ARK address from keyring.

Argument:
keys (bitcoin.core.key.CECKey) -- keyring returned by `getKeys`

Returns str
"""
	network = keys.network
	ripemd160 = hashlib.new('ripemd160', keys.public).digest()[:21]
	seed = network.pubKeyHash + ripemd160
	return base58.b58encode_check(seed)

def getWIF(keys):
	"""
Computes WIF address from keyring.

Argument:
keys (bitcoin.core.key.CECKey) -- keyring returned by `getKeys`

Returns str
"""
	network = keys.network
	compressed = network.get("compressed", True)
	seed = network.wif + keys.private[:32] + (b"\x01" if compressed else b"")
	return base58.b58encode_check(seed)

def getBytes(transaction):
	"""
Computes transaction object as bytes data.

Argument:
transaction (arky.core.Transaction) -- transaction object

Returns bytes
"""
	buf = StringIO() # create a buffer

	# write type as byte in buffer
	pack("<b", buf, (transaction.type,))
	# write timestamp as integer in buffer (see if uint is better)
	pack("<i", buf, (int(transaction.timestamp),))
	# write senderPublicKey as bytes in buffer
	try:
		pack_bytes(buf, transaction.senderPublicKey)
	except AttributeError:
		raise NoSenderDefinedError("%r does not belong to any ARK account" % self)

	if hasattr(transaction, "requesterPublicKey"):
		pack_bytes(buf, transaction.requesterPublicKey)

	if hasattr(transaction, "recipientId"):
		# decode reciever adress public key
		recipientId = base58.b58decode_check(transaction.recipientId)
	else:
		# put a blank
		recipientId = b"\x00"*21
	pack_bytes(buf,recipientId)

	if hasattr(transaction, "vendorField"):
		# put vendor field value (64 bytes limited)
		n = min(64, len(transaction.vendorField))
		vendorField = transaction.vendorField[:n].encode() + b"\x00"*(64-n)
	else:
		# put a blank
		vendorField = b"\x00"*64
	pack_bytes(buf, vendorField)

	# write amount value
	pack("<Q", buf, (transaction.amount,))

	# more test to confirm the good bytification of type 1 to 4...
	typ  = transaction.type
	if typ == 1 and "signature" in transaction.asset:
		pack_bytes(buf, transaction.asset.signature)
	elif typ == 2 and "delegate" in transaction.asset:
		pack_bytes(buf, transaction.asset.delegate.username)
	elif typ == 3 and "vote" in transaction.asset:
		pack_bytes(buf, b"".join(transaction.asset.vote))
	elif typ == 4 and "multisignature" in transaction.asset:
		pack("<b", buf, (transaction.asset.multisignature.min,))
		pack("<b", buf, (transaction.asset.multisignature.lifetime,))
		pack_bytes(buf, b"".join(transaction.asset.multisignature.keysgroup))

	if hasattr(transaction, "signature"):
		pack_bytes(buf, transaction.signature)
	
	if hasattr(transaction, "signSignature"):
		pack_bytes(buf, transaction.signSignature)

	result = buf.getvalue()
	buf.close()
	return result.encode() if not isinstance(result, bytes) else result


class Transaction(api.Transaction):

	def __init__(self, **kwargs):
		self.type = kwargs.pop("type", 0)
		self.amount = kwargs.pop("amount", 0)
		self.timestamp = slots.getTime()
		self.asset = kwargs.pop("asset", ArkyDict())
		for attr,value in kwargs.items():
			setattr(self, attr, value)

	def __setattr__(self, attr, value):
		if attr == "secret":
			keys = getKeys(value)
			object.__setattr__(self, "key_one", keys)
			object.__setattr__(self, "address", getAddress(keys))
			object.__setattr__(self, "senderPublicKey", keys.public)
		elif attr == "secondSecret":
			object.__setattr__(self, "key_two", getKeys(value))
		elif attr == "type":
			if value == 0:   self.fee = __FEES__.send
			elif value == 1: self.fee = __FEES__.secondsignature
			elif value == 2: self.fee = __FEES__.delegate
			elif value == 3: self.fee = __FEES__.vote
			elif value == 4: self.fee = __FEES__.multisignature
			object.__setattr__(self, attr, value)
		else:
			object.__setattr__(self, attr, value)

	def __del__(self):
		if hasattr(self, "key_one"): delattr(self, "key_one")
		if hasattr(self, "key_two"): delattr(self, "key_two")

	def sign(self, secret=None):
		if secret != None: self.secret = secret
		elif not hasattr(self, "key_one"): raise NoSecretDefinedError("No secret defined for %r" % self)
		stamp = getSignature(getBytes(self), getattr(self, "key_one"))
		object.__setattr__(self, "signature", toBip66(stamp))
		object.__setattr__(self, "id", str(struct.unpack("<Q", hashlib.sha256(getBytes(self)).digest()[:8])[0]))

	def seconSign(self, secondSecret=None):
		if not hasattr(self, "signature"): raise NotSignedTransactionError("%r must be signed first" % self)
		if secondSecret != None: self.secondSecret = secondSecret
		elif not hasattr(self, "key_two"): raise NoSecretDefinedError("No second secret defined for %r" % self)
		stamp = getSignature(getBytes(self), getattr(self, "key_two"))
		object.__setattr__(self, "signSignature", toBip66(stamp))
		object.__setattr__(self, "id", str(struct.unpack("<Q", hashlib.sha256(getBytes(self)).digest()[:8])[0]))

	def serialize(self):
		data = ArkyDict()
		for attr in [a for a in [
			"id", "timestamp", "type", "fee", "amount", 
			"recipientId", "senderPublicKey", "requesterPublicKey", "vendorField",
			"asset", "signature", "signSignature"
		] if hasattr(self, a)]:
			value = getattr(self, attr)
			if isinstance(value, bytes):
				value = binascii.hexlify(value)
				if isinstance(value, bytes):
					value = value.decode()
			elif attr in ["amount", "timestamp", "fee"]: value = int(value)
			setattr(data, attr, value)
		return data
