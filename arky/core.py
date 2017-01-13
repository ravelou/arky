# -*- encoding: utf8 -*-
from . import StringIO, __PY3__, __FEES__, slots, base58, api, ark, testnet, ArkyDict
from .bitcoin.core import key
import struct, hashlib, binascii

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

# generate bitcon keygen and store network info into it
# if network is not provided, ark network is automatically selected
def getKeys(secret, network=None):
	keys = key.CECKey()
	keys.network = ark if network == None else network
	keys.set_compressed(keys.network.get("compressed", True)) # compressed = True by default
	seed = hashlib.sha256(secret.encode("utf8") if not isinstance(secret, bytes) else secret).digest()
	keys.set_secretbytes(secret=seed)
	return keys

# return ARK address from keys defined by getKeys
def getAddress(keys):
	ripemd160 = hashlib.new('ripemd160', keys.public).digest()[:21]
	seed = keys.network.pubKeyHash + ripemd160
	return base58.b58encode_check(seed)

# return WIF address from keys defined by getKeys
def getWIF(keys):
	compressed = keys.network.get("compressed", True)
	seed = keys.network.wif + keys.private[:32] + (b"\x01" if compressed else b"")
	print(len(seed), binascii.hexlify(seed))
	return base58.b58encode_check(seed)

# return a transaction as a bytes serie for the ARK network
def getBytes(transaction):
	# create a buffer
	buf = StringIO()

	# write type as byte in buffer
	pack("!b", buf, (transaction.type,))
	# write timestamp as integer in buffer (see if uint is better)
	pack("!i", buf, (int(transaction.timestamp),))
	# write senderPublicKey as bytes in buffer
	pack_bytes(buf, transaction.senderPublicKey)

	if hasattr(transaction, "requesterPublicKey"):
		pack_bytes(buf, transaction.requesterPublicKey)

	if hasattr(transaction, "recipientId"):
		recipientId = base58.b58decode_check(transaction.recipientId)
	else:
		recipientId = b"\x00"*21
	pack_bytes(buf,recipientId)

	if hasattr(transaction, "vendorField"):
		n = len(transaction.vendorField)
		vendorField = transaction.vendorField + b"\x00"*(64-n)
	else:
		vendorField = b"\x00"*64
	pack_bytes(buf, vendorField)

	pack("!q", buf, (transaction.amount,))

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


class Transaction(api.Transaction):

	id = property(lambda obj: int("0x"+hashlib.sha256(obj.getBytes()).hexdigest()[-8:][::-1], base=16), None, None, "")
	hash = property(lambda obj: hashlib.sha256(getBytes(obj)).digest(), None, None, "")

	def __init__(self, **kwargs):
		self.type = kwargs.get("type", 0)
		self.amount = kwargs.get("amount", 0)
		self.timestamp = slots.getTime()
		self.asset = ArkyDict()

	def __setattr__(self, attr, value):
		if attr == "secret":
			keys = getKeys(value)
			object.__setattr__(self, "key_one", keys)
			object.__setattr__(self, "address", getAddress(keys))
			object.__setattr__(self, "senderPublicKey", keys.public)
		if attr == "secondSecret":
			object.__setattr__(self, "key_two", getKeys(value))
		elif attr == "type":
			if value == 1: self.fee = __FEES__.secondsignature
			elif value == 2: self.fee = __FEES__.delegate
			elif value == 3: self.fee = __FEES__.vote
			elif value == 4: self.fee = __FEES__.multisignature
			object.__setattr__(self, attr, value)
		else:
			object.__setattr__(self, attr, value)

	def sign(self, secret=None):
		if secret != None: self.secret = secret
		stamp = self.key_one.sign(self.hash)
		object.__setattr__(self, "signature", stamp)
		return stamp

	def secondSign(self, secondSecret=None):
		if secondSecret != None: self.secondSecret = secondSecret
		stamp = self.key_two.sign(self.hash)
		object.__setattr__(self, "signSignature", stamp)
		return stamp

	def __del__(self):
		if hasattr(self, "key_one"): delattr(self, "key_one")
		if hasattr(self, "key_two"): delattr(self, "key_two")
