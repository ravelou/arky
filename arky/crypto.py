# -*- encoding: utf8 -*-
from . import StringIO, __PY3__
from nacl.bindings.crypto_sign import crypto_sign_seed_keypair
crypto_sign_keypair_from_seed = crypto_sign_seed_keypair

import struct, array, base58

unpack =     lambda fmt, fileobj: struct.unpack(fmt, fileobj.read(struct.calcsize(fmt)))
pack =       lambda fmt, fileobj, value: fileobj.write(struct.pack(fmt, *value))
pack_bytes = lambda f,v: pack("!"+"%ss"%len(v), f, (v,)) if __PY3__ else
             lambda f,v: pack("!"+"c"*len(v), f, v)

def getBytes(packet):
	buf = StringIO()

	pack("!b", buf, (packet.type,)) # checked
	pack("!i", buf, (packet.timestamp,)) # checked
	pack_bytes(buf, packet.senderPublicKey) # checked -- pynacl returns public key as bytes

	if hasattr(packet, "requesterPublicKey"):
		pack_bytes(buf, packet.requesterPublicKey)

	if hasattr(packet, "recipientId"):
		recipientId = base58.b58decode(packet.requesterPublicKey)
	else:
		recipientId = b"\x00"*32
	pack_bytes(buf,recipientId)

	if hasattr(packet, "vendorField"):
		vendorField = packet.vendorField + b"\x00"*(64-len(vendorField))
	else:
		vendorField = b"\x00"*64
	pack_bytes(buf, vendorField)

	pack("!l", (packet.amount,))

	typ  = packet.type
	if typ == 1: # signature
		pack_bytes(buf, packet.asset.signature)
	elif typ == 2: # delegate
		pack_bytes(buf, packet.asset.delegate.username)
	elif typ == 3: # vote
		pass
	elif typ == 4: # multi sigature
		pass

	if hasattr(packet, "signature"):
		pack_bytes(buf, packet.signature)
	
	if hasattr(packet, "signSignature"):
		pack_bytes(buf, packet.signSignature)
	
	result = array.array("H", buf.getvalue())
	buf.close()

	return result