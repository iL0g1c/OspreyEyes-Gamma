from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

# MongoDB connection
load_dotenv()
password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb://mongo_db_admin:{password}@45.76.164.130:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+1.5.0"
client = MongoClient(connection_string)
OspreyEyes = client["OspreyEyes"]
playerCounts = OspreyEyes["playercounts"]

def savePlayerCount(playerCount):
    data = {
        "time": datetime.now(),
        "playerCount": playerCount
    }

    playerCounts.insert_one(data)