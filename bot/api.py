import hashlib
import hmac
import json
import os
import requests
import time
from threading import Thread
from datetime import datetime
from utils import stop_bot
from requests.exceptions import ConnectionError

BASE_URL = 'https://www.bitmex.com/api/v1'

class BitmexApi:
    toggle_updates = False
    api_key = ''
    api_secret = ''
    balances = {}
    positions = {}

    @classmethod
    def authenticate(self, key, secret):
        self.api_key = key
        self.api_secret = secret

    @classmethod
    def start(self):
        print('API connection started')
        self.toggle_updates = True
        time.sleep(5)  # wait a bit

    @classmethod
    def generate_signature(self, verb, url, nonce, data):
        message = verb + url + str(nonce) + data
        sig = hmac.new(
            bytes(self.api_secret, 'utf8'),
            bytes(message,'utf8'),
            digestmod=hashlib.sha256
        )
        return sig.hexdigest()

    @classmethod
    def auth_req(self, method, endpoint, query='', payload=None):
        url = BASE_URL + endpoint
        e_path = '/api/v1' + endpoint
        if query != '':
            e_path += f'?{query}'
            url += f'?{query}'
        expires = int(round(time.time()) + 100)
        headers = {
            'api-expires': str(expires),
            'api-key': self.api_key,
        }
        if payload is not None:
            _payload = str(payload.replace(' ', '')) # remove extra spaces
            signature = self.generate_signature(method, e_path, expires, _payload)
            headers['Content-type'] = 'application/json'
        else:
            signature = self.generate_signature(method, e_path, expires, '')
            
        headers['api-signature'] = signature
        
        while True:
            try:
                if payload is not None:
                    req = requests.request(method, url, headers=headers, data=_payload)
                else:
                    req = requests.request(method, url, headers=headers)
                resp = json.loads(req.content)
                rate = int(req.headers['x-ratelimit-remaining'])
                if rate < 30:  # watch rate limit
                    print(f'REMAINING RATE LIMIT LOW - {rate}\nShuttinng down...')
                    os._exit(1)
                if 'error' in resp:
                    stop_bot(resp)
                else:
                    break
            except Exception as e:
                if isinstance(e,ConnectionError):
                    time.sleep(0.2)  # try to connect again
                else:
                    print(f'An error has occurred.\n{e}')
                    stop_bot(e)
        return resp

    @classmethod
    def account_updates(self):
        if self.toggle_updates:
            # load margin
            _balances = self.auth_req('GET', '/user/margin', query='symbol=XBTUSD&binSize=1m&partial=false&count=100&reverse=false')
            _values = {
                'wallet': _balances['walletBalance'],
                'margin': _balances['marginBalance'],
                'available_margin': _balances['availableMargin']
            }
            self.balances = _values

            _positions = self.auth_req('GET', '/position')

            # load positions
            for pos in _positions:
                sym = pos['symbol']
                qty = pos['currentQty']
                self.positions[sym] = {
                    'leverage': pos['leverage'],
                    'qty': qty,
                    'open': pos['isOpen'],
                    'entry_price': pos['avgEntryPrice'],
                    'liquidation_price': pos['liquidationPrice'],
                }


