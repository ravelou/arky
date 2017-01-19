# -*- encoding:utf-8 -*-
from arky import ArkyDict
import arky.core as core
import requests, json, binascii

SESSION = requests.Session()
SESSION.headers.update({
	'Content-Type': 'application/json; charset=utf-8',
	'os': 'arkwalletapp',
	'version': '0.5.0',
	'port': '1',
	'nethash': "ce6b3b5b28c000fe4b810b843d20b971f316d237d5a9616dbc6f7f1118307fc6"
})

for rid in ["AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4"]*10:
	tx = core.Transaction(amount=200000000, recipientId=rid, vendorField ="Transaction done by arky Python API")
	tx.sign("secret")
	_s = tx.serialize()
	dump = json.dumps({"transactions": [_s]})
	print(_s["signature"])
	success = False
	print(">>> sending to %s : " % rid, end="")
	req = SESSION.post("http://node1.arknet.cloud:4000/peer/transactions", data=dump)
	success = req.json()['success'] #print("server resonse detail:", req.json())
	print("[FAILED]" if not success else "[OK]")

# {"transactions": [{"signature": "3045022063bd927dadbbd730e7299fe1982c04864ce3a32c8c8e146df9dc5f51d3ccf19d022100af95bf693dd68cc1ab1e5ea174f60beffbf1fc28bf3374428684256dc83cd26c", "vendorField": "Transaction done by arky Python API", "type": 0, "amount": 200000000, "fee": 10000000, "timestamp": 20609592, "id": "12970648658463931032", "asset": {}, "recipientId": "AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", "senderPublicKey": "03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933"}]}
# >>> sending to AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4 : [FAILED]
# {"transactions": [{"signature": "3045022063bd927dadbbd730e7299fe1982c04864ce3a32c8c8e146df9dc5f51d3ccf19d022100af95bf693dd68cc1ab1e5ea174f60beffbf1fc28bf3374428684256dc83cd26c", "vendorField": "Transaction done by arky Python API", "type": 0, "amount": 200000000, "fee": 10000000, "timestamp": 20609592, "id": "12970648658463931032", "asset": {}, "recipientId": "AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", "senderPublicKey": "03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933"}]}
# >>> sending to AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4 : [FAILED]
# {"transactions": [{"signature": "3045022063bd927dadbbd730e7299fe1982c04864ce3a32c8c8e146df9dc5f51d3ccf19d022100af95bf693dd68cc1ab1e5ea174f60beffbf1fc28bf3374428684256dc83cd26c", "vendorField": "Transaction done by arky Python API", "type": 0, "amount": 200000000, "fee": 10000000, "timestamp": 20609592, "id": "12970648658463931032", "asset": {}, "recipientId": "AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", "senderPublicKey": "03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933"}]}
# >>> sending to AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4 : [FAILED]
# {"transactions": [{"signature": "304402205ff9c663017877487f82528533e6e9b26179cf3510bda8429878d90b92e03e000220385af14e54c21b6df4c08cc4cebc71c1a91477c5d4e5fc925b8eb68bab38a5e1", "vendorField": "Transaction done by arky Python API", "type": 0, "amount": 200000000, "fee": 10000000, "timestamp": 20609593, "id": "15472778150135709149", "asset": {}, "recipientId": "AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", "senderPublicKey": "03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933"}]}
# >>> sending to AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4 : [OK]
# {"transactions": [{"signature": "304402205ff9c663017877487f82528533e6e9b26179cf3510bda8429878d90b92e03e000220385af14e54c21b6df4c08cc4cebc71c1a91477c5d4e5fc925b8eb68bab38a5e1", "vendorField": "Transaction done by arky Python API", "type": 0, "amount": 200000000, "fee": 10000000, "timestamp": 20609593, "id": "15472778150135709149", "asset": {}, "recipientId": "AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", "senderPublicKey": "03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933"}]}
# >>> sending to AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4 : [OK]
# {"transactions": [{"signature": "3045022100f7a19ae19b990e2703a043c7ef701858e080fd5af61b5d57dc9f037a1a5fb97f02205b4e05628dc972d99dc5e9f05bb6e22dda27b4e5e097a5794c92e739a8a67281", "vendorField": "Transaction done by arky Python API", "type": 0, "amount": 200000000, "fee": 10000000, "timestamp": 20609594, "id": "8314833946284460725", "asset": {}, "recipientId": "AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", "senderPublicKey": "03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933"}]}
# >>> sending to AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4 : [OK]
# {"transactions": [{"signature": "3045022100f7a19ae19b990e2703a043c7ef701858e080fd5af61b5d57dc9f037a1a5fb97f02205b4e05628dc972d99dc5e9f05bb6e22dda27b4e5e097a5794c92e739a8a67281", "vendorField": "Transaction done by arky Python API", "type": 0, "amount": 200000000, "fee": 10000000, "timestamp": 20609594, "id": "8314833946284460725", "asset": {}, "recipientId": "AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", "senderPublicKey": "03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933"}]}
# >>> sending to AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4 : [FAILED]
# {"transactions": [{"signature": "3045022100db6933f1cc81049d5af1ef5813911bc1b673258a250d51a53ec1eceb0436ad8b0220025f5aa21078ed883dbb98c3d5357adeb0ff02f11e4f5dbe8c3d23d9f4e3e161", "vendorField": "Transaction done by arky Python API", "type": 0, "amount": 200000000, "fee": 10000000, "timestamp": 20609595, "id": "11263123143056466968", "asset": {}, "recipientId": "AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", "senderPublicKey": "03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933"}]}
# >>> sending to AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4 : [OK]
# {"transactions": [{"signature": "3045022100db6933f1cc81049d5af1ef5813911bc1b673258a250d51a53ec1eceb0436ad8b0220025f5aa21078ed883dbb98c3d5357adeb0ff02f11e4f5dbe8c3d23d9f4e3e161", "vendorField": "Transaction done by arky Python API", "type": 0, "amount": 200000000, "fee": 10000000, "timestamp": 20609595, "id": "11263123143056466968", "asset": {}, "recipientId": "AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", "senderPublicKey": "03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933"}]}
# >>> sending to AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4 : [FAILED]
# {"transactions": [{"signature": "3046022100bcc35796b1e7d592d8e6bcf0f230db9490300224e40f70471c7efc35b46ad2bb02210095072cf6e4de168bf0d52d68d67d32228a44763381932847e0b31fdb5ede0c54", "vendorField": "Transaction done by arky Python API", "type": 0, "amount": 200000000, "fee": 10000000, "timestamp": 20609596, "id": "6170630513735743577", "asset": {}, "recipientId": "AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4", "senderPublicKey": "03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933"}]}
# >>> sending to AQpqHHVFfEgwahYja9DpfCrKMyMeCuSav4 : [FAILED]