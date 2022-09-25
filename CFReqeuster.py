import json
from typing import List
from unicodedata import name
import requests
import random
from hashlib import sha512, md5
from urllib.parse import urlencode
import pathlib
from time import time

API_SECRET = '623fadbb6a08ab8cfe22ccea4349e7ed0637de64'
API_KEY = '4bf7a4f9bec136c41b9b63834c1aa9fee7ea0355'
API_PREFIX = 'https://codeforces.com/api/'

header = { 'apiKey' : API_KEY,
         'Content-Type' : 'application/json' }
def conv_params(params):
    return  '&'.join([entry[0]+'='+entry[1] for entry in sorted(params)])

def gen_secret(params):
    return sha512(str.encode(params)).hexdigest()

def cf_request(url, params: List[List[str]]):
    try:
        params = conv_params(params +  [['apiKey', API_KEY], ['time', str(int(time()))]])
        apiSig = random.randint(100000, 999999)
        url = API_PREFIX + url + params + f'&apiSig={apiSig}' + gen_secret(f'{apiSig}/{url}{params}#{API_SECRET}')
        return requests.get(url=url,headers=header).json()['result']
    except Exception as e:
        print('eeee: ', e, url, params)

if __name__ == '__main__':
    print(cf_request('contest.hacks?', [['contestId', '566']]))
