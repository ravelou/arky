# -*- encoding: utf8 -*-
from . import StringIO, __PY3__, __FEES__, slots, ArkObject, base58, api, ark, testnet
from .bitcoin.core import key
import struct, hashlib

# add properties to bitcoin.key.CECKey class
# idea here is to generate public key and private key only on demand
# trough a simple attribute access syntax
key.CECKey.public = property(lambda cls: cls.get_pubkey(), None, None, "")
key.CECKey.private = property(lambda cls: cls.get_privkey(), None, None, "")

# read and write binary data
unpack =     lambda fmt, fileobj: struct.unpack(fmt, fileobj.read(struct.calcsize(fmt)))
pack =       lambda fmt, fileobj, value: fileobj.write(struct.pack(fmt, *value))
pack_bytes = lambda f,v: pack("!"+"%ss"%len(v), f, (v,)) if __PY3__ else \
             lambda f,v: pack("!"+"c"*len(v), f, v)

# generate bitcon keygen and store network nfo
def getKeys(secret, network=None):
	seed = hashlib.sha256(secret.encode("utf8") if not isinstance(secret, bytes) else secret).digest()
	keys = key.CECKey()
	keys.network = ark if network == None else network
	keys.set_compressed(keys.network.get("compressed", True))
	keys.set_secretbytes(secret=seed)
	return keys

def getAddress(keys):
	ripemd160 = hashlib.new('ripemd160', keys.public).digest()[:21]
	seed = keys.network.pubKeyHash + ripemd160
	return base58.b58encode_check(seed)

def getBytes(transaction):
	buf = StringIO()

	pack("!b", buf, (transaction.type,))
	pack("!i", buf, (int(transaction.timestamp),))
	pack_bytes(buf, transaction.senderPublicKey)

	if hasattr(transaction, "requesterPublicKey"):
		pack_bytes(buf, transaction.requesterPublicKey)

	if hasattr(transaction, "recipientId"):
		recipientId = base58.b58decode_check(transaction.recipientId[:-1])
	else:
		recipientId = b"\x00"*32
	pack_bytes(buf,recipientId)

	if hasattr(transaction, "vendorField"):
		n = len(transaction.vendorField)
		vendorField = transaction.vendorField + b"\x00"*(64-n)
	else:
		vendorField = b"\x00"*64
	pack_bytes(buf, vendorField)

	pack("!l", buf, (transaction.amount,))

	typ  = transaction.type
	if typ == 1 and "signature" in transaction.asset:
		pack_bytes(buf, transaction.asset.signature)
	elif typ == 2 and "delegate" in transaction.asset:
		pack_bytes(buf, transaction.asset.delegate.username)
	elif typ == 3 and "vote" in transaction.asset:
		pack_bytes(buf, b"".join(transaction.asset.vote))
	elif typ == 4 and "multisignature" in transaction.asset:
		pack("!b", buf, (transaction.asset.multisignature.min,))
		pack("!b", buf, (transaction.asset.multisignature.lifetime,))
		pack_bytes(buf, b"".join(transaction.asset.multisignature.keysgroup))

	if hasattr(transaction, "signature"):
		pack_bytes(buf, transaction.signature)
	
	if hasattr(transaction, "signSignature"):
		pack_bytes(buf, transaction.signSignature)

	result = buf.getvalue()
	buf.close()
	return result.encode() if not isinstance(result, bytes) else result


class Transaction(ArkObject, api.Transaction):

	def __init__(self, **kwargs):
		self.type = kwargs.get("type", 0)
		self.amount = kwargs.get("amount", 0)
		self.timestamp = slots.getTime()
		self.asset =  ArkObject()

	def __setattr__(self, attr, value):
		if hasattr(self, "_bytes"): delattr(self, "_bytes")
		if hasattr(self, "_hash"): delattr(self, "_hash")

		if attr == "secret":
			keys = getKeys(value)
			ArkObject.__setattr__(self, "key_one", keys)
			ArkObject.__setattr__(self, "address", getAddress(keys))
			ArkObject.__setattr__(self, "senderPublicKey", keys.public)
		if attr == "secondSecret":
			keys = getKeys(value)
			ArkObject.__setattr__(self, "key_two", keys)
		elif attr == "type":
			if value == 1: self.fee = __FEES__.secondsignature
			elif value == 2: self.fee = __FEES__.delegate
			elif value == 3: self.fee = __FEES__.vote
			elif value == 4: self.fee = __FEES__.multisignature
			ArkObject.__setattr__(self, attr, value)
		else:
			ArkObject.__setattr__(self, attr, value)

	def getId(self):
		h = hashlib.sha256(self.getBytes()).hexdigest()[-8:]
		return int("0x"+h[-1:0:-1]+h[0:1], base=16)

	def getBytes(self):
		if not hasattr(self, "_bytes"):
			ArkObject.__setattr__(self, "_bytes", getBytes(self))
		return getattr(self, "_bytes")

	def getHash(self):
		if not hasattr(self, "_hash"):
			ArkObject.__setattr__(self, "_hash", hashlib.sha256(self.getBytes()).digest())
		return getattr(self, "_hash")

	def sign(self):
		stamp = self.key_one.sign(self.getHash())
		ArkObject.__setattr__(self, "signature", stamp)
		if hasattr(self, "_bytes"): delattr(self, "_bytes")
		if hasattr(self, "_hash"): delattr(self, "_hash")
		return stamp

	def secondSign(self):
		stamp = self.key_two.sign(self.getHash())
		ArkObject.__setattr__(self, "signSignature", stamp)
		return stamp

	def __del__(self):
		if hasattr(self, "key_one"): delattr(self, "key_one")
		if hasattr(self, "key_two"): delattr(self, "key_two")
