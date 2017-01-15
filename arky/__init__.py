# -*- encoding: utf8 -*-
from collections import OrderedDict
import sys, binascii

__PY3__ = True if sys.version_info[0] >= 3 else False
if __PY3__:
	from io import BytesIO as StringIO
	long = int
else:
	from StringIO import StringIO


class ArkyDict(OrderedDict):
	__setattr__ = lambda obj,*a,**k: OrderedDict.__setitem__(obj, *a, **k)
	__getattr__ = lambda obj,*a,**k: OrderedDict.__getitem__(obj, *a, **k)
	__delattr__ = lambda obj,*a,**k: OrderedDict.__delitem__(obj, *a, **k)


# network options:
ark = ArkyDict()
ark.messagePrefix = b"\x18Ark Signed Message:\n"
ark.bip32 = ArkyDict(public=0x0488b21e, private=0x0488ade4)
ark.pubKeyHash = b"\x17"
ark.wif = b"\xaa"

testnet = ArkyDict()
testnet.messagePrefix = b"\x18Testnet Ark Signed Message:\n"
testnet.bip32 = ArkyDict(public=0x043587cf, private=0x04358394)
testnet.pubKeyHash = b"\x6f"
testnet.wif = b"\xef"


# ARK fees according to transactions in SATOSHI
__FEES__ = ArkyDict({
	"send": 10000000,
	"vote": 100000000,
	"delegate": 2500000000,
	"secondsignature": 500000000,
	"multisignature": 500000000,
	"dapp": 2500000000
})
