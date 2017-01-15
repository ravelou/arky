# -*- encoding -*-
from arky.core import Transaction
from arky import api
import os, json, math, requests

# screen command line
from optparse import OptionParser
parser = OptionParser()
parser.set_usage("usage: %prog arg1 ....argN [options]")
parser.add_option("-v", "--verbose", action="store_false", dest="verbose", default=True, help="print status messages to stdout")
(options, args) = parser.parse_args()

# delegate automation work
__arky__ = "AR1LhtKphHSAPdef8vksHWaXYFxLPjDQNU"
__investments__ = "AYVLjVMLZzQnYbXeUy6HQaY4hECjvJRcA1"
__pythoners__ = "AZ8h8L4hUfS1Pi9fbZssNM1ePkn9p4NGxc"
__fees__ = "AVPhYstwXWwyTb3kat8MbjRasT92YLR5sV"
__daily_fees__ = 5./30 # daily server cost

# configure sesion for POST to ARK network
session = requests.Session()
session.headers.update({
	'Content-Type': 'application/json',
	'os': 'arkwalletapp',
	'version': '0.5.0',
	'port': '1',
	'nethash': "ce6b3b5b28c000fe4b810b843d20b971f316d237d5a9616dbc6f7f1118307fc6"
})


# to be improved using poloniex api...
def USD2ARK(value): return (value*34.)*100000000
def ARK2USD(value): return value/USD2ARK(1)

if len(args) == 1 and os.path.exists(args[0]):
	# do something
	in_ = open(args[0])
	content = in_.read()
	in_.close()
	conf = json.loads(content.decode() if isinstance(content, bytes) else content)

	secret = conf["forging"]["secret"][0]
	node = api.Account.getAccount(__arky__)

	# get forget crypto minus 3 times fees for transfer
	forged = int(node["account"]["balance"]) - (3*0.1*100000000)
	fees = math.floor(USD2ARK(__daily_fees__*7))
	forged -= fees
	pythoners = math.floor(forged*0.25)
	investments =  forged - pythoners

	# execute transfers
	for a,rid,vf in [(int(pythoners), __pythoners__, "arky to pythoners"),
                     (int(investments), __investments__, "arky investments"),
                     (int(fees), __fees__, "arky fees")]:

		print("Sending %.8f ARK to %s" % (a/100000000, rid))
		tx = Transaction(amount=a, recipientId=rid, vendorField=vf, secret=secret)
		tx.sign()
		print(session.post("http://node1.arknet.cloud:4000/peer/transactions", data=json.dumps({"transactions": [tx.serialize()]})).text)
		del tx

else:
	# command line error
	pass
