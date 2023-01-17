import os
import requests

from gasprediction import gasprediction

os.system('scrapy runspider gasprediction/gasprediction/spiders/gas_prediction.py -o gasprediction.json')

url = 'https://maker.ifttt.com/trigger/gas/json/with/key/dPZf92Ytr6YEzriMnQl1Gc'
contents = open('gasprediction.json', 'rb').read()
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=contents, headers=headers)
r.status_code