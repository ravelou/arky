# -*- encoding:utf-8 -*-
from arky import core, api, slots
import os, re, sys, json, logging, binascii

# screen command line
from optparse import OptionParser
parser = OptionParser()
parser.set_usage("usage: %prog arg1 ....argN [options]")
# parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="print status messages to stdout")
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
# move to ark node directory
os.chdir(os.path.dirname(json_path))

# command lines to update node
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

# command lines to recreate database
drop_cmd = '''droptable %(table)s
createtable %(table)s''' % {
	"table": db_table
}

# open the log file
logging.basicConfig(filename=os.path.join(home_path, 'delegate.log'), format='%(levelname)s:%(message)s', level=logging.INFO)


# deal if launch from command line
if len(sys.argv) > 1: logging.info('### %s : delegate.py %s %s ###', slots.datetime.datetime.now(slots.UTC), args, options)
# add my peer ip here for test purpose only...
else: options.ip = '45.63.114.19'

if not os.path.exists(json_path):
	logging.info('Can not find any peer ', slots.datetime.datetime.now(slots.UTC), args, options)
	sys.exit()

# get info from peer
in_ = open(json_path)
content = in_.read()
in_.close()
config = json.loads(content.decode() if isinstance(content, bytes) else content)
secret = config["forging"]["secret"][0]
keyring = core.getKeys(secret)
publicKey = binascii.hexlify(keyring.public)
if isinstance(publicKey, bytes): publicKey = publicKey.decode()

# get data from ARK api
peers = api.Peer.getPeersList().get("peers", False)
delegates = api.Delegate.getDelegates().get("delegates", False)
blocks = api.Block.getBlocks().get("blocks", False)
version = api.Peer.getPeerVersion().get("version", "0.0.0")
height = api.Block.getBlockchainHeight().get("height", False)

# get usefull info to analyse delegate
def isActiveDelegate():
	search = [dlgt for dlgt in delegates if dlgt['publicKey'] == publicKey]
	if not len(search): return False
	else: return search[0]

def getPeerByIp():
	search = [peer for peer in peers if peer["ip"] == options.ip]
	if not len(search): return False
	else: return search[0]

def getLastForgedBlock():
	search = [blck for blck in blocks if blck["generatorPublicKey"] == publicKey]
	if not len(search): return False
	else: return search[0]

# retrieve info from ark.log
class ArkLog:
	@staticmethod
	def getLastSyncTime():
		search = re.compile(".* ([0-9][0-9])-([0-9][0-9])-([0-9][0-9]) ([0-9][0-9]):([0-9][0-9]):([0-9][0-9]) .*")
		catch = os.popen('cat %s | grep "Finished sync" | tail -1' % os.path.join(json_folder, "logs", "ark.log")).read().strip()
		return slots.datetime.datetime(*search.match(catch).groups(), tzinfo=slots.UTC)

	@staticmethod
	def getBlockchainHeight():
		search = re.compile(".* height: ([0-9]*) .*")
		catch = os.popen('cat %s | grep "Received height" | tail -1' % os.path.join(json_folder, "logs", "ark.log")).read().strip()
		return search.match(catch).groups()[0]

	@staticmethod
	def getPeerHeight():
		search = re.compile(".* height: ([0-9]*) .*")
		catch = os.popen('cat %s | grep "Received new block id" | tail -1' % os.path.join(json_folder, "logs", "ark.log")).read().strip()
		return search.match(catch).groups()[0]

delegate = isActiveDelegate()
# info about delegate (False if not registered)
# {'publicKey': '0326f7374132b18b31b3b9e99769e323ce1a4ac5c26a43111472614bcf6c65a377', 
# 'productivity': 90.28, 
# 'missedblocks': 74, 
# 'approval': 97.36, 
# 'address': 'AR1LhtKphHSAPdef8vksHWaXYFxLPjDQNU', 
# 'vote': '12176985772856181', 
# 'producedblocks': 687, 
# 'username': 'arky', 
# 'rate': 33}

peer = getPeerByIp()
# if 'blockheader' not in peer --> not forging
# if 'height' not in peer --> not forging
# verion in peer to be compared with version
# {'port': 4000, 
# 'blockheader': {
# 	'totalFee': 110000000, 
# 	'blockSignature': '3044022065f2ec850891d9ec758bb87e0c5735d6504534c33d4d6c1d32dbd5fa808baf6e02201b356f0034aaa8e5e0944ff8d728aeb07ed49b6cc57ffdfc68276ad183d8e0f2', 
# 	'generatorPublicKey': '02033620fcdf599d28086311e6afe38e47c3bc19d21c794cdf1e84d86c641536d7', 
# 	'totalAmount': 1100562472, 
# 	'timestamp': 21087328, 
# 	'previousBlock': '13303588543971858952', 
# 	'reward': 200000000, 
# 	'version': 0, 
# 	'payloadLength': 2214, 
# 	'numberOfTransactions': 11, 
# 	'payloadHash': '33aef88d6f6c5409ff5901ccc9dd94333cd10961adf7dd8226060b7cbb89334d', 
# 	'height': 37220, 'id': '1931410963195578193'
# }, 'state': 2, 
# 'os': 'linux4.4.19-1-pve', 
# 'string': '137.74.79.185:4000', 
# 'ip': '137.74.79.185', 
# 'height': 37220, 
# 'version': '0.2.0'}

last_block = getLastForgedBlock()
# if False --> not forging
# {'totalForged': '200000000', 
# 'totalFee': 0, 
# 'blockSignature': '30450221009272f3dbe8af36db9c6f05e7044a6f0ae5a9002ec82aed458b83c9f95a04722602205808ef8c71b363197e763a0cb1819ee80dc3c232208ebc4c85fb034037db58f7', 
# 'generatorPublicKey': '03b15e462ac0505a8c524019096f8b550e15742336f5725f0de56df2669894b4e2', 
# 'confirmations': 1, 
# 'totalAmount': 0, 
# 'timestamp': 21090424, 
# 'numberOfTransactions': 0, 
# 'reward': 200000000, 
# 'version': 0, 
# 'payloadLength': 0, 
# 'previousBlock': '5019740463278951759', 
# 'generatorId': 'Aaoi7yd7d3MK3KZPKF49snLdbDBefQFPh2', 
# 'payloadHash': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 
# 'height': 37330, 
# 'id': '12753529974450248758'}

# if on linux platform, get data from ark.log
if "linux" in sys.platform:
	log_peer_height = ArkLog.getPeerHeight()
	print( log_peer_height)
	log_height = ArkLog.getBlockchainHeight()
	print( log_height)
	log_last_sync = ArkLog.getLastSyncTime()
	print( log_last_sync)

def isForging():
	if delegate:
		logging.info('%s is an active delegate : name=%s rate=%s productivity=%s%%', options.ip, delegate["username"], delegate["rate"], delegate['productivity'])
		if last_block:
			logging.info('%s is forging!', options.ip)
			return True
		else:
			logging.info('%s seems not to be forging, last block not found', options.ip)
			return False
	else:
		logging.info('%s is not an active delegate', options.ip)
		return False

def isUpToDate():
	test = config["version"] >= version
	if test:
		logging.info('%s runs last node version %s', options.ip, config["version"])
	else:
		logging.info('%s runs node version %s, %s is required', options.ip, config["version"], version)
	return test

def restartNode():
	logging.info('Restarting the node %s', options.ip)
	logging.info('EXECUTE> %s [%s]', "forever stopall", os.popen("forever stopall").read().strip())
	logging.info('EXECUTE> %s [%s]', forever_start, os.popen(forever_start).read().strip())

def updateNode(droptable=False):
	logging.info('Checking if %s is up to date', options.ip)
	if not isUpToDate():
		logging.info('Updading node:')
		if droptable:
			for line in [l.strip() for l in drop_cmd.split("\n")]:
				logging.info('EXECUTE> %s [%s]', line, os.popen(line).read().strip())
		for line in [l.strip() for l in update_cmd.split("\n")]:
			logging.info('EXECUTE> %s [%s]', line, os.popen(line).read().strip())

if "update" in args:
	updateNode()
	restartNode()

if "check" in args:
	logging.info('Checking if %s is forging :', options.ip)
	if not isForging():
		logging.info('Checking if %s is up to date', options.ip)
		if not isUpToDate():
			updateNode()
			restartNode()
		else:
			restartNode()

if len(sys.argv) > 1:
	logging.info('### end ###')
