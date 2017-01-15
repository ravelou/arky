# -*- encoding:utf-8 -*-
from arky import ArkyDict
import arky.core as core
import requests, json, binascii

SESSION = requests.Session()
SESSION.headers.update({
	'Content-Type': 'application/json',
	'os': 'arkwalletapp',
	'version': '0.5.0',
	'port': '1',
	'nethash': "ce6b3b5b28c000fe4b810b843d20b971f316d237d5a9616dbc6f7f1118307fc6"
})

# send 1 ARK from secret to AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4
# createTransaction("AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", 100000000, null, "secret")
tx = core.Transaction(amount=100000000, recipientId="AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", secret="secret", vendorField="arky pulse")
tx.sign()
req = SESSION.post("http://node1.arknet.cloud:4000/peer/transactions", data=json.dumps({"transactions": [tx.serialize()]}))
print("json send:", json.dumps({"transactions": [tx.serialize()]}))
print("server resonse detail:", req.json())
