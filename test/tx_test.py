# -*- encoding:utf-8 -*-
import arky.core as core

# createTransaction("AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", 10000000, null, “secret”)
t = core.Transaction(amount=10000000, recipientId="AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", secret="secret")
t.timestamp = 20196622.0
# {
# type:				0,
# amount:			10000000,
# fee:				10000000,
# recipientId:		"AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4",
# timestamp:		20196622,
# asset:			{},
# senderPublicKey:	"03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933",
# signature:		"3045022100b9703cbc89dc0cb82d036536e07a703caeb345a2ef8fd01f1aec4b81c7a15416022022fe89619f2faab5cb2e33822aa129be14780d3798309bae3676964fa442bd6d",
# id:				"7799969933852222876"
# }

hash = t.hash
print("hash: ", t.hash.hex())

sign = t.sign()
print("\nsign: ", sign.hex())
# 000e2d340103a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de9331763
# 4867b592574acee187f01a3aed0172a7cb0c7b000000000000000000000000000000000000000000
# 00000000000000000000000000000000000000000000000000000000000000000000000000000000
# 00000080969800000000003045022100b9703cbc89dc0cb82d036536e07a703caeb345a2ef8fd01f
# 1aec4b81c7a15416022022fe89619f2faab5cb2e33822aa129be14780d3798309bae3676964fa442
# bd6d

print(t.key_one.verify(hash, sign))
print("\n" + core.getBytes(t).hex())
