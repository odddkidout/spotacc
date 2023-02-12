from ast import Delete
import email
from enum import unique

from logging import exception
import pymongo
from pymongo import MongoClient

class database:
    def __init__(self, USER, PASSWORD, CLUSTER) -> None:
        self.CLUSTER = CLUSTER
        self.USER = USER
        self.PASSWORD = PASSWORD
        """connect to mongo databse and check if table exists if not create it"""
        

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = f"mongodb+srv://{self.USER}:{self.PASSWORD}@{self.CLUSTER}.mongodb.net/?retryWrites=true&w=majority"
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        try:
            self.client = MongoClient(CONNECTION_STRING)
            """check if database exists"""
            self.db = self.client.ACC
        except Exception as e:
            print(e)
            raise Exception("Error connecting to MongoDB")

            
    def LockedAccounts(self):
            return self.db.Accs.find({"status": False})

    def LockedAccount_one(self):
            return self.db.Accs.find_one({"status": False})

    def accounts(self):
            return self.db.accs

    def update(self, email, password):
        self.db.Accs.update_one({"email": email}, {"$set": {"status": True, "password": password}})

    def add(self,acc):
        self.db.accs.create_index('email',unique=True)
        try:
            self.db.accs.insert_one(acc)
        except pymongo.errors.DuplicateKeyError:
            pass

    def getacc(self,quantity = 1):
        accs = []
        for acc in self.db.Accs.find({'status': True}).limit(quantity):
            if acc['token'] != "":
                accs.append(acc['email']+":"+acc['password']+'\n')
        return accs

