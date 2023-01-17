"""Module providing function for database connection"""
import sqlite3

class DBCM():
    "Content manager for database connection"
    def __init__(self,dbname):
        self.dbname = dbname

    def __enter__(self):
        self.conn = sqlite3.connect(self.dbname)
        #print("Database opened successfully")
        self.cur = self.conn.cursor()

        return self.cur

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
