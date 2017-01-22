# -*- encoding:utf-8 -*-
from arky import core, api, slots
import os, sys, json, logging, binascii

# screen command line
from optparse import OptionParser
parser = OptionParser()
parser.set_usage("usage: %prog arg1 ....argN [options]")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="print status messages to stdout")
parser.add_option("-t", "--testnet", action="store_true", dest="testnet", default=True, help="work with testnet delegate")
parser.add_option("-m", "--mainnet", action="store_false", dest="testnet", default=True, help="work with mainnet delegate")
parser.add_option("-i", "--ip", dest="ip", help="peer ip you want to check")
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

logging.basicConfig(filename=os.path.join(home_path, 'delegate.log'), format='%(levelname)s:%(message)s', level=logging.INFO)

if len(sys.argv) > 1:
	logging.info('### %s : delegate.py %s %s ###', slots.datetime.datetime.now(slots.UTC), args, options)
else:
	# add your ip here if you want to test from console...
	options.ip = '45.63.114.19'

#### set of command line
update_cmd = ('''forever stopall
%(move)s "%(json1)s" "%(home)s"
%(move)s "%(json2)s" "%(home)s"
git pull
%(move)s "%(home)s'''+os.sep+'''%(json1)s" .
%(move)s "%(home)s'''+os.sep+'''%(json2)s" .
%(start)s''') % {
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


def update_node(droptable=False):
	logging.info('Updading node:')
	if droptable:
		for line in [l.strip() for l in drop_cmd.split("\n")]:
			logging.info('EXECUTE> %s [%s]', line, os.popen(line).read().strip())
	for line in [l.strip() for l in update_cmd.split("\n")]:
		logging.info('EXECUTE> %s [%s]', line, os.popen(line).read().strip())

def getPublicKey():
	pubkey = binascii.hexlify(__KEYRING__.public)
	if isinstance(pubkey, bytes): return pubkey.decode()
	else: return pubkey

def isActiveDelegate():
	delegates = api.Delegate.getDelegates().get("delegates", [])
	search = [dlgt for dlgt in delegates if dlgt['publicKey'] == getPublicKey()]
	if not len(search):
		logging.info('%s is no longer active delegate', option.ip)
		return False
	else:
		dlgt = search[0]
		logging.info('%s is an active delegate rated %s with productivity at %s%%', dlgt['username'], dlgt['rate'], dlgt['productivity'])
		return dlgt['username']

def checkUpdate():
	curent_version = api.Peer.getPeerVersion().get("version", False)
	if curent_version:
		logging.info('current node version is %s', curent_version)
		peers = api.Peer.getPeersList().get("peers", [])
		search = [peer for peer in peers if peer['ip'] == options.ip]
		if not len(search):
			logging.info('%s seems not to be registered as a delegate', options.ip)
			return False
		elif search[0]['version'] < curent_version:
			logging.info('%s runs node version %', options.ip, search[0]['version'], curent_version)
			update_node()
			return True
		else:
			logging.info('%s runs node version %s', options.ip, curent_version)

def delegateIsForging():
	# check if it is active delegate
	dlgt = isActiveDelegate()
	if dlgt:
		# if delegate active (delegate rank < 51)
		pubkey = getPublicKey()
		# get last block forged by delegate (sorted by timestamp)
		blks = sorted([blk for blk in api.Block.getBlocks().get("blocks", []) if blk['generatorPublicKey'] == pubkey], key=lambda e:e['timestamp'])
		peer = [p for p in api.Peer.getPeersList().get("peers", []) if p['ip'] == options.ip]
		if len(blks) and len(peer):
			# blockchain height
			block_height = api.Block.getBlockchainHeight().get("height", -1)
			# peer height
			peer_height = peer[0]["height"]
			# last block time
			last_block_time = slots.getRealTime(blks[-1]['timestamp'])
			# UTC actual time
			utc_now = slots.datetime.datetime.now(slots.UTC)
			# if last block time is more than 17 min ago --> 2-3 missed block

			delay = (utc_now - last_block_time).total_seconds()/60
			h_diff = (block_height - peer_height)

			problem = (delay > 17) and (h_diff > 25)
			if problem:
				if delay > 17:
					logging.info('%s last block was forged %d minutes ago, it is not forging !', options.ip, delay)
				if h_diff > 25:
					logging.info('%s height is %d block late from the network height, it is not forging !', options.ip, h_diff)	
				return False
			else:
				logging.info('%s stands at height %s and its last block was forged %d minutes ago, it is forging', options.ip, peer_height, delay)
				return True
		else:
			logging.info('Can not find last block forged by %d in the last ones, it is not forging !', options.ip)
			return False
	else:
		# delegate rank > 51
		return None

if "update" in args:
	checkUpdate()

if "check" in args:
	logging.info('Checking if %s is forging :', options.ip)
	is_forging = delegateIsForging()
	if is_forging == False:
		logging.info('Checking if %s is up to date', options.ip)
		checkUpdate()
		logging.info('Restarting the node %s', options.ip)
		logging.info('EXECUTE> %s [%s]', "forever stopall", os.popen("forever stopall").read().strip())
		logging.info('EXECUTE> %s [%s]', forever_start, os.popen(forever_start).read().strip())

if len(sys.argv) > 1:
	logging.info('### end ###')
