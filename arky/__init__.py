# -*- encoding: utf8 -*-
import sys

__PY3__ = True if sys.version_info[0] >= 3 else False
if __PY3__:
	from io import BytesIO as StringIO
	long = int
else:
	from StringIO import StringIO

try:
	from . import slots
except:
	pass


class ArkObject(object):

	def __getitem__(self, item):
		if hasattr(self, item):
			value = getattr(self, item)
			if isinstance(value, bytes):
				return value.hex()
		else:
			raise AttributeError()


class ArkyDict(dict):
	__setattr__ = lambda obj,*a,**k: dict.__setitem__(obj, *a, **k)
	__getattr__ = lambda obj,*a,**k: dict.__getitem__(obj, *a, **k)
	__delattr__ = lambda obj,*a,**k: dict.__delitem__(obj, *a, **k)


ark = ArkyDict()
ark.messagePrefix = "\x18Ark Signed Message:\n"
ark.bip32 = ArkyDict(public=0x0488b21e, private=0x0488ade4)
ark.pubKeyHash = 0x17
ark.wif = 0xaa

testnet = ArkyDict()
testnet.messagePrefix = "\x18Testnet Ark Signed Message:\n"
testnet.bip32 = ArkyDict(public=0x043587cf, private=0x04358394)
testnet.pubKeyHash = 0x6f
testnet.wif = 0xef

# ARK fees according to transactions in SATOSHI
__FEES__ = ArkyDict({
	"send": 10000000,
	"vote": 100000000,
	"delegate": 2500000000,
	"secondsignature": 500000000,
	"multisignature": 500000000,
	"dapp": 2500000000
})

