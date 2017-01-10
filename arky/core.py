# -*- encoding: utf8 -*-
from . import StringIO, __PY3__, __FEES__, slots, ArkObject

from nacl.bindings.crypto_sign import crypto_sign_seed_keypair, crypto_sign
import struct, base58, hashlib
# array,

unpack =     lambda fmt, fileobj: struct.unpack(fmt, fileobj.read(struct.calcsize(fmt)))
pack =       lambda fmt, fileobj, value: fileobj.write(struct.pack(fmt, *value))
pack_bytes = lambda f,v: pack("!"+"%ss"%len(v), f, (v,)) if __PY3__ else \
             lambda f,v: pack("!"+"c"*len(v), f, v)

def getKeys(secret):
	keys = ArkObject()
	seed = hashlib.sha256(secret.encode() if not isinstance(secret, bytes) else secret).digest()
	keys.public, keys.private = crypto_sign_seed_keypair(seed)
	return keys

def getBytes(transaction):
	buf = StringIO()

	pack("!b", buf, (transaction.type,))
	pack("!i", buf, (transaction.timestamp,))
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
	if typ == 1: # signature
		pack_bytes(buf, transaction.asset.signature)
	elif typ == 2: # delegate
		pack_bytes(buf, transaction.asset.delegate.username)
	elif typ == 3 and hasattr(transaction.asset, "vote"): # vote
		pack_bytes(buf, b"".join(transaction.asset.vote))
	elif typ == 4: # multi sigature
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


class Transaction(ArkObject):

	adress = property(lambda obj: base58.b58encode_check(obj.senderPublicKey) + "A", None, None, "")

	def __init__(self, **kwargs):
		self.type = kwargs.get("type", 1)
		self.amount = kwargs.get("amount", 0)
		self.timestamp = slots.getTime()
		self.asset =  ArkObject()

	def __setattr__(self, attr, value):
		if hasattr(self, "_bytes"): delattr(self, "_bytes")
		if hasattr(self, "_hash"): delattr(self, "_hash")

		if attr == "secret":
			keys = getKeys(value)
			ArkObject.__setattr__(self, "senderPublicKey", keys.public)
			self.sign(keys.private)
		elif attr == "secondSecret":
			self.secondSign(getKeys(value).private)
		elif attr == "type":
			if value == 1: self.fee = __FEES__.secondsignature
			elif value == 2: self.fee = __FEES__.delegate
			elif value == 3: self.fee = __FEES__.vote
			elif value == 4: self.fee = __FEES__.multisignature
			ArkObject.__setattr__(self, attr, value)
		else:
			ArkObject.__setattr__(self, attr, value)

	def getBytes(self):
		if not hasattr(self, "_bytes"):
			ArkObject.__setattr__(self, "_bytes", getBytes(self))
		return getattr(self, "_bytes")

	def getId(self):
		h = hashlib.sha256(self.getBytes()).hexdigest()[-8:]
		return int("0x"+h[-1:0:-1]+h[0:1], base=16)

	def check(self):
		pass

	def doubleCheck(self):
		pass

	def getHash(self):
		if not hasattr(self, "_hash"):
			ArkObject.__setattr__(self, "_hash", hashlib.sha256(self.getBytes()).digest())
		return getattr(self, "_hash")

	def sign(self, private):
		ArkObject.__setattr__(self, "signature", crypto_sign(self.getHash(), private))

	def secondSign(self, private):
		ArkObject.__setattr__(self, "signSignature", crypto_sign(self.getHash(), private))

# function sign(transaction, keys) {
# 	var hash = getHash(transaction);

# 	var signature = keys.sign(hash).toDER().toString("hex");

# 	if (!transaction.signature) {
# 		transaction.signature = signature;
# 	}
# 	return signature;

# }

# function secondSign(transaction, keys) {
# 	var hash = getHash(transaction);

# 	var signature = keys.sign(hash).toDER().toString("hex");

# 	if (!transaction.signSignature) {
# 		transaction.signSignature = signature;
# 	}
# 	return signature;
# }

