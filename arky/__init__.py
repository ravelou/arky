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


# GET generic method for ARK API
def get(api, dic={}, **kw):
	returnkey = kw.pop("returnKey", False)
	data = json.loads(requests.get(__URL_BASE__+api, params=dict(dic, **kw)).text)
	if data["success"] and returnkey: return ArkyDict(data[returnkey])
	else: return ArkyDict(data)


class ArkyDict(dict):
	"""
Python dict with javascript behaviour.
>>> ad = ArkyDict()
>>> ad["key1"] = "value1"
>>> ad.key2 = "value2"
>>> ad
{'key2': 'value2', 'key1': 'value1'}
"""
	__setattr__ = lambda obj,*a,**k: dict.__setitem__(obj, *a, **k)
	__getattr__ = lambda obj,*a,**k: dict.__getitem__(obj, *a, **k)
	__delattr__ = lambda obj,*a,**k: dict.__delitem__(obj, *a, **k)


def swich(net=False):
	"""
Swich between mainnet and testnet
>>> swich(True) # use mainnet
>>> swich(False) # use testnet
"""
	global __NETWORK__, __URL_BASE__, __HEADERS__

	__NETWORK__ = ArkyDict()
	__HEADERS__ = ArkyDict()

	if net:
		# values are not all correct
		__URL_BASE__ = "http://node1.arknet.cloud:4000"
		__NETWORK__.update(
			messagePrefix = b"\x18Ark Signed Message:\n",
			bip32         = ArkyDict(public=0x043587cf, private=0x04358394),
			pubKeyHash    = b"\x6f",
			wif           = b"\xef",
		)
		__HEADERS__.update({
			'Content-Type': 'application/json; charset=utf-8',
			'os': 'arkwalletapp',
			'version': '0.5.0',
			'port': '1',
			'nethash': "ed14889723f24ecc54871d058d98ce91ff2f973192075c0155ba2b7b70ad2511"
		})

	else:
		__URL_BASE__ = "http://node1.arknet.cloud:4000"
		__NETWORK__.update(
			messagePrefix = b"\x18Testnet Ark Signed Message:\n",
			bip32         = ArkyDict(public=0x0488b21e, private=0x0488ade4),
			pubKeyHash    = b"\x17",
			wif           = b"\xaa",
		)
		__HEADERS__.update({
			'Content-Type': 'application/json; charset=utf-8',
			'os': 'arkwalletapp',
			'version': '0.5.0',
			'port': '1',
			'nethash': "8b2e548078a2b0d6a382e4d75ea9205e7afc1857d31bf15cc035e8664c5dd038"
		})

swich(False)


# ARK fees according to transactions in SATOSHI
__FEES__ = ArkyDict({
	"send": 10000000,
	"vote": 100000000,
	"delegate": 2500000000,
	"secondsignature": 500000000,
	"multisignature": 500000000,
	"dapp": 2500000000
})
