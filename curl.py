#!/usr/bin/env python

import json
import requests
from fastnumbers import fast_forceint

##fastnumbers force_int will handle the int conversion of data:wq

#Curl API
r = requests.get('https://koinex.in/api/ticker')


print(r)

#pythonJsonObject with 'u'
json_string = r.json()

#Make O/P Data
d = {
    'vol_24Hrs':{
    'ETH': fast_forceint(json_string['stats']['ETH']['vol_24hrs']),
    'BTC': fast_forceint(json_string['stats']['BTC']['vol_24hrs']),
    'LTC': fast_forceint(json_string['stats']['LTC']['vol_24hrs']),
    'XRP': fast_forceint(json_string['stats']['XRP']['vol_24hrs']),
    'BCH': fast_forceint(json_string['stats']['BCH']['vol_24hrs'])}
}

#PythonObjectToJsonData
parsed_json = json.dumps(d)

print parsed_json

