"""Module providing function for database connection"""
import os
import psycopg2
from dotenv import load_dotenv

class DBCM():
    "Content manager for database connection"
    def __init__(self):
        #self.dbname = dbname
        load_dotenv()

    def __enter__(self):
        #self.conn = sqlite3.connect(self.dbname)
        #print("Database opened successfully")
        self.conn = psycopg2.connect(host=os.getenv("HOST"),port=os.getenv("PORT"),database=os.getenv("DATABASE"),user=os.getenv("USER"),password=os.getenv("PASSWORD"))
        print("Database opened successfully")
        self.cur = self.conn.cursor()

        return self.cur

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
