# -*- encoding:utf-8 -*-
from arky import core, api, slots
import os, sys, json, logging, binascii

# write your ip and port here
__IP__ = '45.63.114.19'
__PORT__ = '4000'

# screen command line
from optparse import OptionParser
parser = OptionParser()
parser.set_usage("usage: %prog arg1 ....argN [options]")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="print status messages to stdout")
parser.add_option("-t", "--testnet", action="store_true", dest="testnet", default=True, help="work with testnet delegate")
parser.add_option("-m", "--mainnet", action="store_false", dest="testnet", default=True, help="work with mainnet delegate")
(options, args) = parser.parse_args()

json_filename1 = "config.testnet.json"
json_filename2 = "config.main.json"

# deal with network
if options.testnet:
	forever_start = "forever start app.js --genesis genesisBlock.testnet.json --config config.testnet.json"
	json_filename = json_filename1
	db_table = "ark_testnet"
else:
	forever_start = "forever start app.js --genesis genesisBlock.main.json --config config.main.json"
	json_filename = json_filename2
	db_table = "ark_mainnet"

# deal with home directory
if "win" in sys.platform:
	home_path = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"])
	move_cmd = "move"
elif "linux" in sys.platform:
	home_path = os.environ["HOME"]
	move_cmd = "mv"

# first of all get delegate json data
# it automaticaly searches json configuration file in "/home/username/ark-node" folder
# if your install does not match this default one, you have to set ARKNODEPATH environement variable
json_folder = os.environ.get("ARKNODEPATH", os.path.join(home_path, "ark-node"))
json_path = os.path.join(json_folder, json_filename)

if not os.path.exists(json_path):
	sys.exit()

else:
	in_ = open(json_path)
	content = in_.read()
	in_.close()

	__JSON__ = json.loads(content.decode() if isinstance(content, bytes) else content)
	__SECRET__ = __JSON__["forging"]["secret"][0]
	__KEYRING__ = core.getKeys(__SECRET__)

	# move to ark node directory
	os.chdir(os.path.dirname(json_path))

#### set of command line
update_cmd = '''forever stopall
%(move)s "%(json1)s" "%(home)s"
%(move)s "%(json2)s" "%(home)s"
git pull
%(move)s "%(home)s/%(json1)s" .
%(move)s "%(home)s/%(json2)s" .
%(start)s''' % {
	"move": move_cmd,
	"home": home_path,
	"json1": json_filename1,
	"json2": json_filename2,
	"start": forever_start,
}

drop_cmd = '''droptable %(table)s
createtable %(table)s''' % {
	"table": db_table
}


#### set of functions
def update_node(droptable=False):
	if droptable:
		for line in drop_cmd.split("\n"):
			os.system(line.strip())
	for line in update_cmd.split("\n"):
		os.system(line.strip())

def getPublicKey():
	pubkey = binascii.hexlify(__KEYRING__.public)
	if isinstance(pubkey, bytes): return pubkey.decode()
	else: return pubkey

def isActiveDelegate():
	delegates = api.Delegate.getDelegates().get("delegates", [])
	search = [dlgt for dlgt in delegates if dlgt['publicKey'] == getPublicKey()]
	if not len(search): return False
	else: return search[0]['username']

def checkUpdate():
	curent_version = api.Peer.getPeerVersion().get("version", False)
	if curent_version:
		peers = api.Delegate.getPeersList().get("peers", [])
		search = [peer for peer in peers if peer['ip'] == __IP__]
		if not len(search):
			return False
		elif search[0]['version'] < curent_version:
			update_node()
			return True

def delegateIsForging():
	# check if it is active delegate
	dlgt = isActiveDelegate()
	if dlgt:
		# if delegate active (delegate rank < 51)
		pubkey = getPublicKey()
		# get last block forged by delegate (sorted by timestamp)
		blks = sorted([blk for blk in api.Block.getBlocks().get("blocks", []) if blk['generatorPublicKey'] == pubkey], key=lambda e:e['timestamp'])
		if len(blks):
			# last block time
			last_block_time = slots.getRealTime(blks[-1]['timestamp'])
			# UTC actual time
			utc_now = slots.datetime.datetime.now(slots.UTC)
			# if last block time is more than 17 min ago --> 2-3 missed block
			if abs((utc_now - last_block_time).total_seconds()/60) > 17:
				# not forging
				return False
			else:
				# forging
				return True
		else:
			return False
	else:
		# delegate rank > 51
		return None

if "update" in args:
	checkUpdate()

if "check" in args:
	is_forging = delegateIsForging()
	if is_forging == False:
		checkUpdate():
		os.system("forever stopall")
		os.system(forever_start)
