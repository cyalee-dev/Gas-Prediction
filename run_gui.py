import os
import sys

os.system('scrapy runspider gasprediction/gasprediction/spiders/gas_prediction.py -o gasprediction.json')
os.system('python gasprediction/gui.py')
sys.exit(os.remove("gasprediction.json"))