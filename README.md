# `Arky`

This package aims to provide python developpers a usefull interface to [ARK](https://ark.io/) platform.

## `arky.api`

```python
>>> import arky.api as api
>>> api.Account.getAccount("AR1LhtKphHSAPdef8vksHWaXYFxLPjDQNU") # arky delegate
{'account': {'publicKey': '0326f7374132b18b31b3b9e99769e323ce1a4ac5c26a43111472614bcf6c65a377', 'bal
ance': '1101375294113', 'unconfirmedBalance': '1101375294113', 'u_multisignatures': [], 'unconfirmed
Signature': 0, 'secondSignature': 0, 'address': 'AR1LhtKphHSAPdef8vksHWaXYFxLPjDQNU', 'secondPublicK
ey': None, 'multisignatures': []}, 'success': True}
```

## `arky.core`

```python
>>> import arky.core as core
>>> keys = core.getKeys("your secret passphrase")
>>> keys.public
b'\x03\xab\xfa\xd4\xa7dO@n\x8d\x9b\t\x83\x19B\'\xa0\x1e\x15\t{~\xae\x06n)\xb4"l\x89\xd6{\xd9'
>>> keys.public.hex()
'03abfad4a7644f406e8d9b0983194227a01e15097b7eae066e29b4226c89d67bd9'
>>> keys.private.hex()
'3081d3020101042026984bc4305c6c043e6fb3a1727dd055f17231b44982db1788699a154c5c4e9ca081853081820201013
02c06072a8648ce3d0101022100fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f300604010
004010704210279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798022100fffffffffffffffff
ffffffffffffffebaaedce6af48a03bbfd25e8cd0364141020101a12403220003abfad4a7644f406e8d9b0983194227a01e1
5097b7eae066e29b4226c89d67bd9'
>>> core.getAddress(keys)
'AebdUTUtzHhEUQmn8QU91k2VSTrDU3fn2z'
>>> keys.sign(hashlib.sha256("message".encode()).digest()).hex()
'304402206e955336706dd2e45216db9321f5647a807dffe8040d259f93cb9917bed95ac502201fce153afaac89220a084da
4a5d228e1e636997caab2b540b628755d4a5b0af2'
```

* TODO: private key WIF encode 
