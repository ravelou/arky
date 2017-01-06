# -*- encoding: utf8 -*-
# created by Toons on 01/05/2017

import json, requests

__URL_BASE__ = "http://node1.arknet.cloud:4000"


def get(api, dic={}, **kw):
	return json.loads(requests.get(__URL_BASE__+api, params=dict(dic, **kw)).text)

def post(api, dic={}, **kw):
	return json.loads(requests.post(__URL_BASE__+api, params=dict(dic, **kw)).text)

def put(api, dic={}, **kw):
	return json.loads(requests.put(__URL_BASE__+api, params=dict(dic, **kw)).text)


class Loader:

	def getLoadingStatus(self):
		return get('/api/loader/status')

	def getSynchronisationStatus(self):
		return get('/api/loader/status/sync')


class Block:

	def getBlock(self, blockId):
		return get('/api/blocks/get', id=blockId)

	def getBlocks(self):
		return get('/api/blocks')

	def getBlockchainFee(self):
		return get('/api/blocks/getFee')

	def getBlockchainHeight(self):
		return get('/api/blocks/getHeight')

	def getForgedByAccount(self, publicKey):
		return get('/api/delegates/forging/getForgedByAccount', generatorPublicKey=publicKey)


class Account:

	def openAccount(self, secret):
		return post('/api/accounts/open', secret=secret)

	def generatePublicKey(self, secret):
		return post('/api/accounts/generatePublicKey', secret=secret)

	def getBalance(self, address):
		return get('/api/accounts/getBalance', address=address)

	def getPublicKey(self, address):
		return get('/api/accounts/getPublicKey', address=address)

	def getAccount(self, address):
		return get('/api/accounts', address=address)

	def getVotes(self, address):
		return get('/api/accounts/delegates', address=address)

	def vote(self, secret, *delegates, secondSecret=None, publicKey=None):
		param = {"secret"=secret, "delegates"=delegates}
		if secondSecret: param["secondSecret"] = secondSecret
		if publicKey: param["publicKey"] = publicKey
		return put('/api/accounts/delegates', **param)


class Delegate:

	def enableDelegateOnAccount(self, secret, username, secondSecret=None):
		param = {"secret"=secret, "username"=username}
		if secondSecret: param["secondSecret"] = secondSecret
		return put('/api/delegates', **param)

	def getDelegates(self):
		return get('/api/delegates', **param)

	def getDelegate(self, username):
		return get('/api/delegates/get', username=username)

	def getVoters(self, publicKey):
		return get('/api/delegates/voters', publicKey=publicKey)

	def enableForging(self, secret):
		return post('/api/delegates/forging/enable', secret=secret)

	def disableForging(self, secret):
		return post('/api/delegates/forging/disable', secret=secret)

