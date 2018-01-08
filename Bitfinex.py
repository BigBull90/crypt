import requests,json
import json
import base64
import hashlib
import time
import hmac,calendar
import traceback
class BitFinex:
    XRP = 'XRPUSD'
    OMG = 'OMGUSD'
    def __init__(self,key,secret):
        self.key = key
        self.secret = bytes(secret)
    
    def __init__(self):
        "Add keys here"

    def __str__(self):
        return '[BitFinex] - ' + self.key

    def query(self,method,endpoint,authenticated=False,payload_object=None):
        base_url = 'https://api.bitfinex.com/v1/'
        if payload_object == None :
            payload_object = {}
        final_endpoint = base_url + endpoint
        timestamp = calendar.timegm(time.gmtime())
        payload_object['nonce'] = str(timestamp)
        payload_object['request'] = '/v1/' + endpoint
        payload_json = json.dumps(payload_object)
        payload = base64.b64encode(bytes(payload_json))
        m = hmac.new(self.secret, payload, hashlib.sha384)
        m = m.hexdigest()
        headers = {
            'X-BFX-APIKEY' : self.key,
            'X-BFX-PAYLOAD' : base64.b64encode(bytes(payload_json)),
            'X-BFX-SIGNATURE' : m
        }
        try :
            if method == 'GET' and authenticated == False:
                r = requests.get(base_url + endpoint,payload_object)
                return r.json()
            elif method =='GET' and authenticated == True:
                r = requests.get(final_endpoint,data={},headers=headers)
                return r.json()
            elif method == 'POST' :
                r = requests.post(final_endpoint,data={},headers=headers)
                return r.json()
        except :
            traceback.print_exc()
    
    def get_trades(self,ticker):
        suffix = 'trades/' + ticker
        return self.query('GET',suffix,authenticated=False)
    
    def get_order_book(self,ticker):
        suffix = 'book/' + ticker + '?limit_bids=200&limit_asks=200'
        return self.query('GET',suffix,authenticated=False)
    
    def wallet_balances(self):
        suffix = 'balances'
        return self.query('GET',suffix,authenticated=True)
    
    def create_sell_order(self,symbol,quantity,price):
        suffix = 'order/new'
        payload = {
               'request': '/v1/order/new',
               'symbol': symbol,
               'amount': quantity,
               'price': price,
               'exchange': 'bitfinex',
               'side': 'sell',
               'type': 'exchange limit',
               'ocoorder' : False,
               'use_all_available' : 0
            }
        return self.query('POST',suffix,authenticated=True,payload_object=payload)
    
    def create_buy_order(self,symbol,quantity,price):
        suffix = 'order/new'
        payload = {
               'request': '/v1/order/new',
               'symbol': symbol,
               'amount': quantity,
               'price': price,
               'exchange': 'bitfinex',
               'side': 'buy',
               'type': 'exchange limit',
               'ocoorder' : False,
               'use_all_available' : 0
            }
        return self.query('POST',suffix,authenticated=True,payload_object=payload)
    
    def get_active_orders(self):
        suffix = 'orders'
        return self.query('GET',suffix,authenticated=True)
    
    def cancel_all_orders(self):
        suffix = 'order/cancel/all'
        payload={}
        return self.query('POST',suffix,authenticated=True,payload_object=payload)
    
    def get_order(self,order_id):
        suffix = 'order/status'
        payload = {'id' : order_id}
        return self.query('POST',suffix,authenticated=True,payload_object=payload)
