import requests
import json

tickers = ["xrp","omg","bch","btc","ltc","qtm"]
def calc_arbitrage(ticker):
	coindelta_ticker = ticker
	if ticker=="qtm":
		coindelta_ticker = "qtum"
	currency = 58461.0
	currency_dollar = currency/63.8
	market_name = coindelta_ticker + "-inr"
	url = "https://api.bitfinex.com/v1/pubticker/" + ticker + "usd"

	coin_delta_url = "https://coindelta.com/api/v1/public/getticker/"

	koinex_url = "https://koinex.in/api/ticker"

	response = requests.request("GET", url)

	koinex_response = requests.request("GET", koinex_url)
	
	coindelta_response = requests.request("GET",coin_delta_url)

	bitfinex = json.loads(response.text)

	coindelta_response_json = json.loads(coindelta_response.text)
	try:
		koinex_response_json = json.loads(koinex_response.text)
	except:
		print "not found on koinex"

	for string in coindelta_response_json:
		if(string["MarketName"] == market_name):
			coindelta_price = float(string['Ask'])

	try:
		koinex_price = float(koinex_response_json['prices'][coindelta_ticker.upper()])
	except:
		koinex_price = 1
	bitfinex_price = float(bitfinex['last_price'])
	print coindelta_price, koinex_price, coindelta_price/koinex_price*100, koinex_price/coindelta_price*100
	dollars = currency/coindelta_price * bitfinex_price
	koinex = currency/coindelta_price * koinex_price
	koinex_arbitrage = (koinex_price - coindelta_price)/coindelta_price * 100
	arbitrage = (currency_dollar - dollars)/dollars * 100
	print " ------------\t " + ticker + " \t -----------"
	print "price in bitfinex : " + str(bitfinex_price)
	print "price in koinex : " + str(koinex_price)
	print "price in coindelta : " + str(coindelta_price) 
	print "Currency : " + str(currency)
	print "Currency in dollar : " + str(currency_dollar)
	print "Dollars : " + str(dollars)
	print "bitfinex arbitrage : " + str(arbitrage)
	print "koinex arbitrage : " + str(koinex_arbitrage)

def calc_profits(currency,ticker1,ticker2):
	url_ticker1 = "https://api.bitfinex.com/v1/pubticker/" + ticker1 + "usd"
	url_ticker2 = "https://api.bitfinex.com/v1/pubticker/" + ticker2 + "usd"

	coin_delta_url = "https://coindelta.com/api/v1/public/getticker/"
	bitfinex_dict = {}
	response = requests.request("GET", url_ticker1)
	bitfinex_dict[ticker1] = float(json.loads(response.text)['last_price'])

	coindelta_response = requests.request("GET",coin_delta_url)
	coindelta_response_json = json.loads(coindelta_response.text)
	coindelta_dict = {}
	for string in coindelta_response_json:
		if(string["MarketName"] == (ticker1+"-inr")):
			coindelta_dict[ticker1] = float(string['Ask'])
		elif(string["MarketName"] == (ticker2+"-inr")):
			coindelta_dict[ticker2] = float(string['Bid'])

	response = requests.request("GET", url_ticker2)
	bitfinex_dict[ticker2] = float(json.loads(response.text)['last_price'])
	print coindelta_dict
	result = currency/coindelta_dict[ticker1]*bitfinex_dict[ticker1]/bitfinex_dict[ticker2]*coindelta_dict[ticker2]
	print result
	
for i in tickers:
	calc_arbitrage(i)
#calc_profits(60000,"xrp","omg")