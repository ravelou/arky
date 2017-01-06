# -*- encoding: utf8 -*-
from . import ArkDict
import json

ark = ArkyDict()
ark.messagePrefix = "\x18Ark Signed Message:\n"
ark.bip32 = ArkDict(public=0x0488b21e, private=0x0488ade4)
ark.pubKeyHash = 0x17
ark.wif = 0xaa

testnet = ArkyDict()
testnet.messagePrefix = "\x18Testnet Ark Signed Message:\n"
testnet.bip32 = ArkDict(public=0x043587cf, private=0x04358394)
testnet.pubKeyHash = 0x6f
testnet.wif = 0xef
