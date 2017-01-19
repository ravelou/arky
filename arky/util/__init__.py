# -*- encoding: utf8 -*-
# created by Toons on 01/05/2017

import requests, json

def getPoloniexPair(pair):
	if "_" not in pair: pair = pair[:3] + "_" + pair[3:]
	return float(PoloniexTickers[pair]["last"])

def getArkPrice(curency):
	return float(cmp_ark["price"][curency])

def getKrakenPair(pair):
	data = json.loads(requests.get("https://api.kraken.com/0/public/Ticker?pair="+pair.upper()).text)
	A, B = pair[:3], pair[3:]
	A = ("Z" if A in ['USD', 'EUR', 'CAD', 'GPB', 'JPY'] else "X") + A
	B = ("Z" if B in ['USD', 'EUR', 'CAD', 'GPB', 'JPY'] else "X") + B
	try: return float(data["result"][A + B]["c"][0])
	except: return -1

def reload():
	global PoloniexTickers, cmp_ark
	PoloniexTickers = json.loads(requests.get("https://poloniex.com/public?command=returnTicker").text)
	try: cmp_ark = json.loads(requests.get("http://coinmarketcap.northpole.ro/api/v5/ARK.json").text)
	except: cmp_ark = {"price": {"usd":1/34}}

reload()
