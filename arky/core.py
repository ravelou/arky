# -*- encoding: utf8 -*-
from . import StringIO, __PY3__, __FEES__, slots, base58, api, ark, testnet, ArkyDict #, ArkyCECKey
from bitcoin.signature import DERSignature
from bitcoin.core import _bignum, key
import struct, hashlib, binascii

# read value binary data
unpack = lambda fmt, fileobj: struct.unpack(fmt, fileobj.read(struct.calcsize(fmt)))
# write value binary data
pack =  lambda fmt, fileobj, value: fileobj.write(struct.pack(fmt, *value))
# write bytes as binary data
pack_bytes = lambda f,v: pack("<"+"%ss"%len(v), f, (v,)) if __PY3__ else \
             lambda f,v: pack("<"+"c"*len(v), f, v)

def getKeys(secret="passphrase", seed=None, network=None):
	# Generate bitcon keygen and store network info into it.
	# If network is not provided, ark network is automatically selected.
	network = ark if network == None else network # use ark network by default
	keys = key.CECKey()
	keys.network = network
	keys.private = hashlib.sha256(secret.encode("utf8") if not isinstance(secret, bytes) else secret).digest() if not seed else seed
	keys.set_compressed(network.get("compressed", True)) # compressed = True by default
	keys.set_secretbytes(secret=keys.private)
	keys.public = keys.get_pubkey()
	return keys

def getAddress(keys):
	# return ARK address from keys defined by getKeys.
	network = keys.network
	ripemd160 = hashlib.new('ripemd160', keys.public).digest()[:21]
	seed = network.pubKeyHash + ripemd160
	return base58.b58encode_check(seed)

def getWIF(keys):
	# return WIF address from keys defined by getKeys.
	network = keys.network
	compressed = network.get("compressed", True)
	seed = network.wif + keys.private[:32] + (b"\x01" if compressed else b"")
	return base58.b58encode_check(seed)

def getBytes(transaction):
	# return a transaction as a bytes serie for the ARK network
	buf = StringIO() # create a buffer

	# write type as byte in buffer
	pack("<b", buf, (transaction.type,))
	# write timestamp as integer in buffer (see if uint is better)
	pack("<i", buf, (int(transaction.timestamp),))
	# write senderPublicKey as bytes in buffer
	pack_bytes(buf, transaction.senderPublicKey)

	if hasattr(transaction, "requesterPublicKey"):
		pack_bytes(buf, transaction.requesterPublicKey)

	if hasattr(transaction, "recipientId"):
		# decode reciever adress public key
		recipientId = base58.b58decode_check(transaction.recipientId)
	else:
		# put a blank
		recipientId = b"\x00"*22
	pack_bytes(buf,recipientId)

	if hasattr(transaction, "vendorField"):
		# put vendor field value (64 bytes limited)
		n = min(64, len(transaction.vendorField))
		vendorField = transaction.vendorField[:n] + b"\x00"*(64-n)
	else:
		# put a blank
		vendorField = b"\x00"*64
	pack_bytes(buf, vendorField)

	# write amount value
	pack("<Q", buf, (transaction.amount,))

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

	id = property(lambda obj: _bignum.bin2bn(hashlib.sha256(getBytes(obj)).digest()[-8:][::-1]), None, None, "")
	hash = property(lambda obj: hashlib.sha256(getBytes(obj)).digest(), None, None, "")

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

	def sign(self, secret=None):
		if secret != None: self.secret = secret
		print(self.hash.hex())
		stamp = self.key_one.sign(self.hash)
		object.__setattr__(self, "signature", stamp)
		return stamp

	def secondSign(self, secondSecret=None):
		if not hasattr("signature"): raise Exception()
		if secondSecret != None: self.secondSecret = secondSecret
		stamp = self.key_two.sign(self.hash)
		object.__setattr__(self, "signSignature", stamp)
		return stamp

	def __del__(self):
		if hasattr(self, "key_one"): delattr(self, "key_one")
		if hasattr(self, "key_two"): delattr(self, "key_two")
