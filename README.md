# `Arky`

This package aims to provide python developpers a usefull interface with [ARK](https://ark.io/) platform.

## `arky` API

```python
>>> import arky.api as api
>>> account = api.Account()
>>> account.getAccount("232u2FdD2vGayU9GECAJsjMkwmAfGDgehyRDtfZzgfvwszUhB2A") # arky delegate
{'account': {'multisignatures': [], 'u_multisignatures': [], 'unconfirmedSignature': 0, 'unconfirmed
Balance': '197743137231', 'secondSignature': 0, 'balance': '197743137231', 'secondPublicKey': None, 
'publicKey': '884fc5264de5a23ba1a673bf2d5e102511932bf2e83ff99e49112dc65f213ee5', 'address': '232u2Fd
D2vGayU9GECAJsjMkwmAfGDgehyRDtfZzgfvwszUhB2A'}, 'success': True}
```
