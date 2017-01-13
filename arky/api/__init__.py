# -*- encoding: utf8 -*-
# created by Toons on 01/05/2017
# only GET method is implemented, no POST or PUT for security reasons
from .. import ArkyDict
import json, requests

__URL_BASE__ = "http://node1.arknet.cloud:4000"

def get(api, dic={}, **kw):
	returnkey = kw.pop("returnKey", False)
	data = json.loads(requests.get(__URL_BASE__+api, params=dict(dic, **kw)).text)
	if data["success"] and returnkey: return ArkyDict(data[returnkey])
	else: return ArkyDict(data)


class Loader:

	@staticmethod
	def getLoadingStatus():
		return get('/api/loader/status')

	@staticmethod
	def getSynchronisationStatus():
		return get('/api/loader/status/sync')


class Block:

	@staticmethod
	def getBlock(blockId):
		return get('/api/blocks/get', id=blockId)

	@staticmethod
	def getBlocks():
		return get('/api/blocks')

	@staticmethod
	def getBlockchainFee():
		return get('/api/blocks/getFee')

	@staticmethod
	def getBlockchainHeight():
		return get('/api/blocks/getHeight')

	@staticmethod
	def getForgedByAccount(publicKey):
		return get('/api/delegates/forging/getForgedByAccount', generatorPublicKey=publicKey)


class Account:

	@staticmethod
	def getBalance(address):
		return get('/api/accounts/getBalance', address=address)

	@staticmethod
	def getPublicKey(address):
		return get('/api/accounts/getPublicKey', address=address)

	@staticmethod
	def getAccount(address):
		return get('/api/accounts', address=address)

	@staticmethod
	def getVotes(address):
		return get('/api/accounts/delegates', address=address)


class Delegate:

	@staticmethod
	def getDelegates():
		return get('/api/delegates')

	@staticmethod
	def getDelegate(username):
		return get('/api/delegates/get', username=username)

	@staticmethod
	def getVoters(publicKey):
		return get('/api/delegates/voters', publicKey=publicKey)


class Transaction(object):

	@staticmethod
	def getTransactionsList():
		return get('/api/transactions')

	@staticmethod
	def getTransaction(transactionId):
		return get('/api/transactions/get', id=transactionId)

	@staticmethod
	def getUnconfirmedTransaction(transactionId):
		return get('/api/transactions/unconfirmed/get', id=transactionId)

	@staticmethod
	def getUnconfirmedTransactions():
		return get('/api/transactions/unconfirmed')


class Peer:

	@staticmethod
	def getPeersList():
		return get('/api/peers')

	@staticmethod
	def getPeers(ip, port):
		return get('/api/peers', ip=ip, port=port)

	@staticmethod
	def getPeerVersion():
		return get('/api/peers/version')


class Multisignature:

	@staticmethod
	def getPendingMultiSignatureTransactions(publicKey):
		return get('/api/multisignatures/pending', publicKey=publicKey)

	@staticmethod
	def getAccountsOfMultisignature(publicKey):
		return post('/api/multisignatures/accounts', publicKey=publicKey)
