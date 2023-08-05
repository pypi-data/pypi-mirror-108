import sys
import urllib.parse
import hashlib
import hmac
import base64
import requests
import time

class kraken_client():

    def __init__(self, api_key=False, api_sec=False):
        self.api_url = "https://api.kraken.com"
        print('New Kraken API client created')
        self.set_keys(api_key, api_sec)
    def keys_missing_handler(self):
        if not self.api_key or not self.api_sec : 
            print('api keys missing, could not connect')
            return False
        else : return True

    def set_keys(self,api_key = False, api_sec = False):
        # str(int(1000*time.time())) = str(int(1000*time.time()))
        if not api_key or not api_sec : 
            print('API Keys were not provided, will not connect to private API')
            return False
        if not self._keys_are_valid(api_key,api_sec):
            print('KEYS PROVIDED WERE NOT VALID !')
            print('You can retry setting them with set_keys(api_key,api_sec) attribute')
            api_key = False
            api_sec = False
            return False
        self.api_key = api_key
        self.api_sec = api_sec
        print("Provided keys are valid, client is connected to Kraken private API")

        return True

    def _requestCheck(self,api_key,api_sec):
        urlpath = '/0/private/TradeBalance'
        data = {"nonce": str(int(1000*time.time())),"asset": "EUR" }
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()
        mac = hmac.new(base64.b64decode(api_sec), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        sigdigest = sigdigest.decode()
        headers = {}
        headers['API-Key'] = api_key
        headers['API-Sign'] = sigdigest           
        req = requests.post((self.api_url + urlpath), headers=headers, data=data)
        return req.json() 
    def _error_in_response(self,response):
        if len(response['error']) > 0:
            print("Error during request checking: ",response['error'])
            return True
        elif 'result' in response.keys():
            return False

    def _keys_are_valid(self,api_key = False, api_sec = False):
        if not api_key or not api_sec : 
            print('please provide api_key and api_sec as arguments')
            return False
        balanceRequest = self._requestCheck(api_key,api_sec)
        if 'EAPI:Invalid key' in balanceRequest['error']:
            print('keys invalid !')
            return False
        elif len(balanceRequest['error']) > 0:
            print("Error during request checking: ",balanceRequest['error'])
            return False
        elif 'result' in balanceRequest.keys():
            return True
        return False

    def get_kraken_signature(self, urlpath, data):
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()
        mac = hmac.new(base64.b64decode(self.api_sec), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    def kraken_request(self,uri_path, data):
        headers = {}
        headers['API-Key'] = self.api_key
        headers['API-Sign'] = self.get_kraken_signature(uri_path, data )             
        req = requests.post((self.api_url + uri_path), headers=headers, data=data)
        return req

    def requestTradeBalance(self, asset = "EUR"):
        balanceRequest = self.kraken_request('/0/private/TradeBalance', {
            "nonce": str(int(1000*time.time())), 
            "asset": asset
        })
        if self._error_in_response(balanceRequest.json()):return False
        return balanceRequest.json()['result']  

    def requestAccountBalance(self):
        balanceRequest = self.kraken_request('/0/private/Balance', {"nonce": str(int(1000*time.time()))})
        if self._error_in_response(balanceRequest.json()):return False
        return balanceRequest.json()['result']  

    def requestTradesHistory(self,pair, since,proxies=False):
        """
        pair = "XDGEUR"
        since = timestamp in ns
        """
        print(proxies)
        try:
            raw_data = requests.get('https://api.kraken.com/0/public/Trades?pair='+ pair +'&since='+str(since), proxies=proxies)
            data = raw_data.json()['result'][pair]
            sinceID = raw_data.json()['result']['last']
        except:
            print("insert errors", sys.exc_info()[1],flush=True)
            data = 0
            sinceID = 0
            pass
        return data, sinceID

def hello(stringy):
    print(stringy)
  
class mod_call:
    def __call__(self,API_KEY=False,API_SEC=False):
        return kraken_client(API_KEY,API_SEC)

sys.modules[__name__] = mod_call()

# new_client = kraken_client(API_KEY,API_SEC)
# new_client._keys_are_valid(API_KEY, API_SEC)
# print(new_client.requestTradeBalance())
# print(new_client.requestAccountBalance())
# # print(new_client.requestTradesHistory("XDGEUR", 1619857401000000000,proxies=False))

