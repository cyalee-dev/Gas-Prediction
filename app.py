import os
import json
import re
from datetime import datetime
from dbcm import DBCM

#from gasprediction import gasprediction

#os.system('scrapy runspider gasprediction/gasprediction/spiders/gas_prediction.py -o gasprediction.json')

""" url = 'https://maker.ifttt.com/trigger/gas/json/with/key/dPZf92Ytr6YEzriMnQl1Gc'
contents = open('gasprediction.json', 'rb').read()
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=contents, headers=headers)
r.status_code """


class App():

    dataList = []

    def initialize(self):
        """
        TESTING ONLY - Depercated!!
        Initialize the database.
        """

        with DBCM() as cur:
            cur.execute("""create table if not exists data
            (id integer primary key autoincrement not null,
            timestamp text not null,
            date text not null,
            location text not null,
            regular real not null,
            premium real not null,
            diesel real not null);""")
            #print("Table created successfully.")
        print("Initialize Database Completed!")

    def fetchData(self):
        os.system(
            'scrapy runspider gasprediction/gasprediction/spiders/gas_prediction.py -o gasprediction.json')

    def UpdateInfo(self):
        price = {}
        file = open("gasprediction.json", 'r')
        raw = json.load(file)[0]
        for index, city in enumerate(raw["cityname"]):
            data = {}
            price = {}

            price["regular"] = raw["gasprice"][index*3]
            price["premium"] = raw["gasprice"][index*3+1]
            price["diesel"] = raw["gasprice"][index*3+2]

            data["timestamp"] = datetime.timestamp(datetime.now())
            data["date"] = self.getYMD()
            data["location"] = city
            data["price"] = price

            self.dataList.append(data)

    def monthToNum(self,month):
        mth = {'January': 1,
               'February': 2,
               'March': 3,
               'April': 4,
               'May': 5,
               'June': 6,
               'July': 7,
               'August': 8,
               'Septemper': 9,
               'October': 10,
               'November': 11,
               'December': 12}
        try:
            out = mth[month]
            return out
        except:
            raise ValueError("Not month input")

    def getYMD(self):
        file = open("gasprediction.json", 'r')
        raw = json.load(file)[0]
        ymd = raw["title"].split()
        year = ymd[7]
        month = str(self.monthToNum(ymd[6])).zfill(2)
        day = re.findall(r'\d+', ymd[4])[0]
        out = f"{year}-{month}-{day}"
        return out

    def UpdateDB(self):
        with DBCM() as cur:
            for item in self.dataList:
                sql = """insert into data (timestamp, date, location, regular, premium, diesel) values (%s,%s,%s,%s,%s,%s)"""
                value = (item["timestamp"], item["date"], item["location"], item["price"]
                         ["regular"], item["price"]["premium"], item["price"]["diesel"])
                cur.execute(sql, value)

        print("Database Updated!")

    def removeData(self):
        os.remove("gasprediction.json")


app = App()
#app.initialize()
app.fetchData()
app.getYMD()
app.UpdateInfo()
app.UpdateDB()
app.removeData()

