# `Arky`

This package aims to provide python developpers a usefull interface to [ARK](https://ark.io/) platform.

## Install

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
>>> keys.private.hex()
'2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b'
>>> core.getAddress(keys)
'AJWRd23HNEhPLkK1ymMnwnDBX2a7QBZqff'
>>> core.getWIF(keys)
'SB3BGPGRh1SRuQd52h7f5jsHUg1G9ATEvSeA7L5Bz4qySQww4k7N'
>>> tx = core.Transaction(amount=100000000, recipientId="AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", secret="secret")
>>> tx.sign()
>>> core.getBytes(tx).hex()
'00d7f35e0103a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de93317634867b592574acee187f
01a3aed0172a7cb0c7b000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000e1f5050000000030450221006d06e5e3a3bb6f30cc398fa5ccb
d7a4d8bf72f3bf1a9e6b1a4f823cbb1f7920e0220714f5b69708bd6113fe03186e7364839294fcd6ba2d1c39d443df026435
b22cd'
```

More on `arky.core` ?

```python
>>> help(core)
```

## curent work

 * Transaction signature (first and second) 
