from pymongo import MongoClient, UpdateOne
import os
from dotenv import load_dotenv
from operator import itemgetter
from datetime import datetime

# MongoDB connection
load_dotenv()
password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb://mongo_db_admin:{password}@45.76.164.130:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+1.5.0"
client = MongoClient(connection_string)
OspreyEyes = client["OspreyEyes"]
activity = OspreyEyes["activity"]

def updateOnlineUsers(users):

    # update users that came online
    currentOnlineUsers = list(map(itemgetter("acid"), users))
    alerts = []
    usersInDatabase = list(activity.find({"acid": {"$in": currentOnlineUsers}}))
    updateOperations = []
    for accountData in usersInDatabase:
        for item in users:
            if item["acid"] == accountData["acid"]:
                user = item
                break
        if (accountData["currentStatus"] == 0):
            accountData["times"].append({
                "status": 1,
                "time": datetime.now()
            })
            updateOperations.append(
                UpdateOne(
                    {"acid": accountData["acid"]},
                    {"$set": {
                        "currentStatus": 1,
                        "times": accountData["times"]
                    
                    }}
                )
            )
            alerts.append(f"{user['acid']} | {user['cs']} came online.\n")
    if updateOperations:
        activity.bulk_write(updateOperations)
    
    # update users that went offline
    currentOfflineUsers = list(activity.find({"currentStatus": 1}))
    updateOperations = []
    for accountData in currentOfflineUsers:
        for item in users:
            if item["acid"] == accountData["acid"]:
                user = item
                break
        if accountData["acid"] not in currentOnlineUsers:
            accountData["times"].append({
                "status": 0,
                "time": datetime.now()
            })
            updateOperations.append(
                UpdateOne(
                    {"acid": accountData["acid"]},
                    {"$set": {
                        "currentStatus": 0,
                        "times": accountData["times"]
                    }}
                )
            )
            alerts.append(f"{user['acid']} | {user['cs']} came offline.\n")
    if updateOperations:
        activity.bulk_write(updateOperations)
    
    # create users that detected online for the first time.
    newAccounts = []
    accountIdsInDatabase = list(map(itemgetter("acid"), usersInDatabase))
    for user in users:
        if user["acid"] not in accountIdsInDatabase and user["acid"] != None and isinstance(user["acid"], int) and user["cs"] != "":
            newAccounts.append({
                "acid": user["acid"],
                "currentStatus": 1,
                "times" : [
                    {
                        "status": 1,
                        "time": datetime.now()
                    }
                ]
            })
            alerts.append(f"{user['acid']} | {user['cs']} detected online for the first time.\n")
    if newAccounts:
        activity.insert_many(newAccounts)
    return alerts