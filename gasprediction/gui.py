#----------------------------------------------------------------------------
# Name: Chun Yin Adrian Lee
# Date: 2022-09-15
# ---------------------------------------------------------------------------
import json
from guizero import App, Text, Combo, ListBox

data = json.load(open('gasprediction.json'))[0]

print(data)

def SetCity(value):
    cityIndex.value = (data["cityname"].index(value)*3)
    Calculate()

def SetGrade(value):
    options = ["Regular","Premium","Diesel"]
    gradeIndex.value = options.index(value)
    Calculate()

def Calculate():
    price.value = data["gasprice"][int(cityIndex.value) + int(gradeIndex.value)]

app = App(title="Gas Prediction", width = 800, height= 400)
title = Text(app, text=data["title"], size=20, font="Calibri", color="black", align="top")
cityLabel = Text(app, text="City", font="Calibri", color="black")
city = ListBox(app, items=data["cityname"],command=SetCity)
gasLabel = Text(app, text="Grade", font="Calibri", color="black")
grade = Combo(app, options=["Regular", "Premium","Diesel"],command=SetGrade)
priceLabel = Text(app, text="Predicted Price", font="Calibri", color="black")
price = Text(app, text="N/A", font="Calibri", color="red")
cityIndex = Text(app, text="0", visible=False)
gradeIndex = Text(app, text="0", visible=False)

app.display()