#!/usr/bin/python

from .utils import *
import sqlite3,os,logging

class ZipCode:
    def __init__(self):
        self.location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.store_db_path = os.path.join(self.location,STORE_DB)
        self.conn,self.curr = self.db()
        self.getHaders = self.getDbHaders()
    
    def db(self):
        try:
            if not os.path.isfile(self.store_db_path):
                logging.debug("Requriment File Missing!. ")
                return None,None
            conn = sqlite3.connect(self.store_db_path)
            curr = conn.cursor()
            return conn,curr
        except Exception as e:
            logging.debug(e)
            return None,None

    def get_zipcode_info(self,code):
        try:
            if type(code) == str or type(code) == int:
                data = self.fetch(PINCODE,code)
                return data
        except Exception as e:
            logging.debug(e)

    def fetch(self,field,entry):
        try:
            self.curr.execute(QUERY_FETCH.format(field),(entry,))
            rows = self.curr.fetchall()
            main = list()
            for row in rows:
                inner = dict()
                for head,item in zip(self.getHaders,row):
                    inner[head] = item
                main.append(inner)
            return main
        except Exception as e:
            print(e)
            logging.debug(e)
    
    def getDbHaders(self):
        try:
            headers = None
            self.curr.execute(QUERY_HADER)
            rows = self.curr.fetchall()
            headers = list()
            for row in rows:
                headers.append(row[1])
            return headers
        except Exception as e:
            logging.debug(e)
            return None