# -*- encoding:utf-8 -*-
from optparse import OptionParser
from arky import core, api
import os, sys, json, logging

# screen command line
parser = OptionParser()
parser.set_usage("usage: %prog arg1 ....argN [options]")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="print status messages to stdout")
parser.add_option("-t", "--testnet", action="store_true", dest="testnet", default=True, help="work with testnet delegate")
parser.add_option("-m", "--mainnet", action="store_false", dest="testnet", default=True, help="work with mainnet delegate")
(options, args) = parser.parse_args()

# deal with network
if options.testnet:
	forever_start = "forever start app.js --genesis genesisBlock.testnet.json --config config.testnet.json"
	json_filename = "config.testnet.json"
	db_table = "ark_testnet"
else:
	forever_start = "forever start app.js --genesis genesisBlock.mainnet.json --config config.mainnet.json"
	json_filename = "config.mainnet.json"
	db_table = "ark_mainnet"

# first of all get delegate json data
# it automaticaly searches json configuration file in "/home/username/ark-node" folder
# if your install does not match this default one, you have to set ARKNODEPATH environement variable
json_folder = os.environ.get("ARKNODEPATH", "~/ark-node")
json_path = os.path.join(json_folder, json_filename)

if not os.path.exists(json_path):
	sys.exit()

in_ = open(json_path)
content = in_.read()
in_.close()

__DELEGATE_JSON__ = json.loads(content.decode() if isinstance(content, bytes) else content)
__KEYRING__ = core.getKeys(__DELEGATE_JSON__["forging"]["secret"][0])

# move to ark node directory
os.chdir(os.path.dirname(json_path))

######## utility functions
def update_node(droptable=False):
	if droptable:
		os.system('''
droptable %(table)
createtable %(table)
''' % {
		"table": db_table
	})

	os.system('''
forever stopall
mv "%(json)" ~
git pull
mv "~/%(json)" ./
%(start)
''' % {
		"json": json_filename,
		"start": forever_start,
	})


# {
# 	"ip":"213.32.41.107",
# 	"port":4000,
# 	"string":"213.32.41.107:4000",
# 	"os":"linux4.4.0-42-generic",
# 	"version":"0.2.0",
# 	"state":2,
# 	"height":12556,
# 	"blockheader":{
# 		"id":"11614775520380764520",
# 		"height":12556,
# 		"version":0,
# 		"totalAmount":0,
# 		"totalFee":0,
# 		"reward":200000000,
# 		"payloadHash":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
# 		"timestamp":20828672,
# 		"numberOfTransactions":0,
# 		"payloadLength":0,
# 		"previousBlock":"10783891843168196769",
# 		"generatorPublicKey":"03628abd0a1a6dcd7a3b7e4d63375e2baa7f0f88e1530d36c58594f5356f77f964",
# 		"blockSignature":"304502210082b5568b3cf9c785c717a66da5033eab935e07edbccc36bffe04576f4758bd0f022038cb00a8f6d4943194261f9dd9ec2a51a9f5d58bd40a7a64c91e379475d199a3"
# 	}
# }

def checkNetworkHealth():
	data = api.Peer.getPeersList(returnkey="peers")
	pass


def isActiveDelegate(pubkey, data):
	return False



# date = re.compile('.*([0-9][0-9])-([0-9][0-9])-([0-9][0-9]) ([0-9][0-9]):([0-9][0-9]):([0-9][0-9]).*')

# last_forged = os.popen("cat /home/ark/ark-node/logs/ark.log | grep Forged | tail -n 1").read().strip()
# server_time = os.popen("date --rfc-3339=seconds").read().strip()

# tuple1 = date.match(server_time).groups()
# tuple2 = date.match(last_forged).groups()
# date1 = datetime.datetime(*(int(e) for e in tuple1))
# date2 = datetime.datetime(*(int(e) for e in tuple2))
# delta = date2 - date1
# delay = abs(delta.total_seconds())/60

# if delay > 20:
# 	# update node and restart
# 	pass
