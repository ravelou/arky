# -*- encoding: utf8 -*-
# created by Toons on 01/05/2017
import sys, binascii
import json, requests

__PY3__ = True if sys.version_info[0] >= 3 else False
if __PY3__:
	from io import BytesIO as StringIO
	long = int
else:
	from StringIO import StringIO


class ArkyDict(dict):
	__setattr__ = lambda obj,*a,**k: dict.__setitem__(obj, *a, **k)
	__getattr__ = lambda obj,*a,**k: dict.__getitem__(obj, *a, **k)
	__delattr__ = lambda obj,*a,**k: dict.__delitem__(obj, *a, **k)


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

# testnet headers for POST method
__HEADERS__ = {
	'Content-Type': 'application/json; charset=utf-8',
	'os': 'arkwalletapp',
	'version': '0.5.0',
	'port': '1',
	'nethash': "8b2e548078a2b0d6a382e4d75ea9205e7afc1857d31bf15cc035e8664c5dd038"
}

# ARK API url base
__URL_BASE__ = "http://node1.arknet.cloud:4000"

# GET generic method for ARK API
def get(api, dic={}, **kw):
	returnkey = kw.pop("returnKey", False)
	data = json.loads(requests.get(__URL_BASE__+api, params=dict(dic, **kw)).text)
	if data["success"] and returnkey: return ArkyDict(data[returnkey])
	else: return ArkyDict(data)
