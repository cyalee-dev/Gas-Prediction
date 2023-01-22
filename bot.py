import requests
import os
import telebot
from dbcm import DBCM
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
city = ("Toronto", "Montreal", "Vancouver", "Calgary", "Barrie", "Brampton", "Charlottetown", "Cornwall", "Edmonton", "Fredericton", "GTA", "Halifax", "Hamilton", "Kamloops", "Kelowna", "Kingston", "London", "Markham", "Mississauga", "Moncton", "Niagara", "Oakville", "Oshawa", "Ottawa", "Peterborough", "Prince George", "Quebec City", "Regina", "Saskatoon", "St Catharines", "St John (NB)", "St. John's", "Sudbury", "Thunder Bay", "Victoria", "Waterloo", "Windsor", "Winnipeg")

@bot.message_handler(commands=['start'])
def send_welcome(message):
   bot.reply_to(message, "Welcome to Gas Prediction Bot! \n /help for how to use this bot")

@bot.message_handler(commands=['help'])
def send_welcome(message):
   bot.reply_to(message, f"Enter the cityname to get the latest predicted gas price. \nSupport city: {city}")

@bot.message_handler(func=lambda message: True)
def checkmsg(message):
   queryLoc = f"{message.text}".capitalize()
   if queryLoc in city:
      with DBCM() as cur:
         sql = f"SELECT * FROM data WHERE location = '{queryLoc}' ORDER BY timestamp DESC limit 1"
         cur.execute(sql)
         result = cur.fetchone()
         bot.reply_to(message, f"Prediction for: {result[0]}\n\n\U0001F3D9City: {result[1]} \n\U000026FDRegular: {result[2]}\U000000A2 \n\U000026FDPremium: {result[3]}\U000000A2 \n\U000026FDDiesel: {result[4]}\U000000A2 \n\nLast update: {datetime.fromtimestamp(int(float(result[6])))}")
   else:
      bot.reply_to(message, "The city you entered is not currently support by this bot.")

bot.infinity_polling()
