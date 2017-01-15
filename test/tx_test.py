# -*- encoding:utf-8 -*-
from arky import ArkyDict
import arky.core as core
import requests, json, binascii


# createTransaction("AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", 10000000, null, "secret")
t = core.Transaction(amount=100000000, recipientId="AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", secret="secret")
# t.timestamp = 20196622
# t.senderPublicKey = binascii.unhexlify("03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933")
# t.signature = binascii.unhexlify("3045022100b9703cbc89dc0cb82d036536e07a703caeb345a2ef8fd01f1aec4b81c7a15416022022fe89619f2faab5cb2e33822aa129be14780d3798309bae3676964fa442bd6d")
# t.id = "7799969933852222876"

# # {
# # type: 0,
# # amount: 10000000,
# # fee: 10000000,
# # recipientId: "AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4",
# # timestamp: 20196622,
# # asset: {},
# # senderPublicKey: "03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933",
# # signature: "3045022100b9703cbc89dc0cb82d036536e07a703caeb345a2ef8fd01f1aec4b81c7a15416022022fe89619f2faab5cb2e33822aa129be14780d3798309bae3676964fa442bd6d",
# #             3045022100b9703cbc89dc0cb82d036536e07a703caeb345a2ef8fd01f1aec4b81c7a15416022022fe89619f2faab5cb2e33822aa129be14780d3798309bae3676964fa442bd6d
# #                       b9703cbc89dc0cb82d036536e07a703caeb345a2ef8fd01f1aec4b81c7a15416    22fe89619f2faab5cb2e33822aa129be14780d3798309bae3676964fa442bd6d
# # id: "7799969933852222876"
# # }

# print("getbytes:", core.getBytes(t).hex())
# # getBytes
# # 000e2d340103a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de9331763
# # 4867b592574acee187f01a3aed0172a7cb0c7b000000000000000000000000000000000000000000
# # 00000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 0000008096980000000000
# h = t.hash
# print("signature:", t.sign().hex())
# # 3045022100dc7b61ef4258db267dd2a0e7b1eb1890191b414b501185cce73de147e190a5c402206bd4cb78874137a1d657d536abb76311011fbbe61540751ece94ee74d26ff714
# print("check signature:", t.key_one.verify(h, t.signature))

# # h2 = h[:-1] + b"\xbb"
# # print(h2.hex())
# # print("check signature:", t.key_one.verify(h2, t.signature))
# print(t.__dict__)
# print(t.sign().hex())
# __URL_BASE__ = "http://node1.arknet.cloud:4000"


SESSION = requests.Session()
SESSION.headers.update({
	'Content-Type': 'application/json',
	'os': 'arkwalletapp',
	'version': '0.5.0',
	'port': '1',
	'nethash': "ce6b3b5b28c000fe4b810b843d20b971f316d237d5a9616dbc6f7f1118307fc6"
})

# # send 1 ARK from secret to AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4
# t = core.Transaction(amount=100000000, recipientId="AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", vendorField="arky pulse", secret="Sigycop#123@Ark.Testnet")
t.sign()
print(core.getBytes(t).hex())
req = SESSION.post("http://node1.arknet.cloud:4000/peer/transactions", data=json.dumps({"transactions": [t.serialize()]}))
print("json send:", json.dumps({"transactions": [t.serialize()]}))
print("server resonse detail:", req.json())
