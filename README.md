# `Arky`

This package aims to provide python developpers a usefull interface to [ARK](https://ark.io/) platform.

## Install (for now not available on Pypi)

### Ubuntu

Open a shell and type: `sudo pip install arky`

### Windows

Run a command as Administrator and type : `pip install arky`

## `arky`

### `arky.api`

```python
>>> import arky.api as api
>>> api.Account.getAccount("AR1LhtKphHSAPdef8vksHWaXYFxLPjDQNU") # arky delegate
{'account': {'publicKey': '0326f7374132b18b31b3b9e99769e323ce1a4ac5c26a43111472614bcf6c65a377', 'bal
ance': '1101375294113', 'unconfirmedBalance': '1101375294113', 'u_multisignatures': [], 'unconfirmed
Signature': 0, 'secondSignature': 0, 'address': 'AR1LhtKphHSAPdef8vksHWaXYFxLPjDQNU', 'secondPublicK
ey': None, 'multisignatures': []}, 'success': True}
```

More on `arky.api` ?

```python
>>> help(api)
```

### `arky.core`

```python
>>> import arky.core as core
>>> keys = core.getKeys("secret")
>>> keys.public.hex()
'03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933'
>>> keys.wif
'SB3BGPGRh1SRuQd52h7f5jsHUg1G9ATEvSeA7L5Bz4qySQww4k7N'
>>> core.getAddress(keys)
'AJWRd23HNEhPLkK1ymMnwnDBX2a7QBZqff'
>>> tx = core.Transaction(amount=100000000, recipientId="AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4")
>>> tx.sign("secret")
>>> tx.serialize()
{'recipientId': 'AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4', 'timestamp': 20832330, 'amount': 100000000, 'a
sset': {}, 'senderPublicKey': '03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933', 
'fee': 10000000, 'signature': '304402201dbf20a62d3411c6d000b691edf3ed50c34baa96b94dedf70e2d512b9f917
8250220475869560dd9740e2c324972be3cb2690e5fdd27b1cccf6dcd8fb325f52f8f25', 'type': 0, 'id': '16683123
258705133772'}
```

Actualy, there is an issue with signature. `sendTransaction` uses a while loop to do several attempts :

```python
>>> tx = core.Transaction(amount=1234000000, recipientId="AR1LhtKphHSAPdef8vksHWaXYFxLPjDQNU")
>>> core.sendTransaction("secret", tx)
{'transactionId': '3684489509227507694', 'attempt': 5, 'success': True}
```

More on `arky.core` ?

```python
>>> help(core)
```

### `arky.util`

```python
>>> import arky.util as util
>>> util.getArkPrice("usd")
0.029411764705882353
>>> util.getPoloniexPair("BTCLSK")
0.00017798
>>> util.getKrakenPair("ETHEUR")
9.661
```
