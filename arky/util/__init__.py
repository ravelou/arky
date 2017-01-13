# -*- encoding: utf8 -*-
# created by Toons on 01/05/2017
import json

# function getPoloniexPair(pair) {
#   var response = UrlFetchApp.fetch("https://poloniex.com/public?command=returnTicker");
#   var test = response.getContentText();
#   return parseFloat(JSON.parse(test)[pair].last);
# }

# function getKraken_XBTEUR()
# {
#   var response = UrlFetchApp.fetch("https://api.kraken.com/0/public/Ticker?pair=XBTEUR");
#   var myjson = JSON.parse(response.getContentText());
#   return parseFloat(myjson.result.XXBTZEUR.c[0]);
# }

# function getKraken_ICNEUR()
# {
#   var response = UrlFetchApp.fetch("https://api.kraken.com/0/public/Ticker?pair=ICNXBT");
#   var myjson = JSON.parse(response.getContentText());
#   return parseFloat(myjson.result.XICNXXBT.c[0])*getKraken_XBTEUR();
# }

# function getKraken_ETHEUR()
# {
#   var response = UrlFetchApp.fetch("https://api.kraken.com/0/public/Ticker?pair=ETHEUR");
#   var myjson = JSON.parse(response.getContentText());
#   return parseFloat(myjson.result.XETHZEUR.c[0]);
# }
