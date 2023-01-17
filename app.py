import os
import requests
import sqlite3
import json
from datetime import datetime
from dbcm import DBCM

#from gasprediction import gasprediction

#os.system('scrapy runspider gasprediction/gasprediction/spiders/gas_prediction.py -o gasprediction.json')

""" url = 'https://maker.ifttt.com/trigger/gas/json/with/key/dPZf92Ytr6YEzriMnQl1Gc'
contents = open('gasprediction.json', 'rb').read()
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=contents, headers=headers)
r.status_code """

price = {}
dataList = []
file = open("gasprediction.json", 'r')
raw = json.load(file)[0]

class App():

    def initialize(self):
        """
        Initialize the database.
        """

        with DBCM("test.sqlite") as cur:
            cur.execute("""create table if not exists data
            (id integer primary key autoincrement not null,
            timestamp text not null,
            location text not null,
            regular real not null,
            premium real not null,
            diesel real not null);""")
            #print("Table created successfully.")
        print("Initialize Completed!")

    def UpdateInfo(self):
        for index, city in enumerate(raw["cityname"]):
            data = {}
            price = {}

            price["regular"] = raw["gasprice"][index*3]
            price["premium"] = raw["gasprice"][index*3+1]
            price["diesel"] = raw["gasprice"][index*3+2]

            data["timestamp"] = datetime.timestamp(datetime.now())
            data["location"] = city
            data["price"] = price

            dataList.append(data)

    def UpdateDB(self):
        with DBCM("test.sqlite") as cur:
            for item in dataList:
                sql = """insert into data (timestamp, location, regular, premium, diesel) values (?,?,?,?,?)"""
                value = (item["timestamp"], item["location"],item["price"]["regular"], item["price"]["premium"], item["price"]["diesel"])
                cur.execute(sql, value)

        print("Database Updated!")

app = App()
app.initialize()
app.UpdateInfo()
app.UpdateDB()



# os.system('python gasprediction/gui.py')