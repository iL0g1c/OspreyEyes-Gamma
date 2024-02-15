from datetime import datetime
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import json
from operator import itemgetter

# MongoDB connection
load_dotenv()
password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb://mongo_db_admin:{password}@45.76.164.130:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+1.5.0"
client = MongoClient(connection_string)
OspreyEyes = client["OspreyEyes"]
callsigns = OspreyEyes["callsigns"]

def removeDuplicateAccounts(users):
    uniqueAccountIDs = set()
    uniqueUsers = []
    for d in users:
        if d != None:
            id = d["acid"]
        if id not in uniqueAccountIDs:
            uniqueAccountIDs.add(id)
            uniqueUsers.append(d)
    return uniqueUsers

def checkCallsignChanges(users):
    users = removeDuplicateAccounts(users) # Remove duplicate accounts patch for multi tab exploit

    # gets all users from database that are currently online
    accountIds = list(map(itemgetter("acid"), users))
    alerts = []
    usersInDatabase = list(callsigns.find({"acid": {"$in": accountIds}})) # get users from database that are online

    # checks if callsign has changed for users in the database
    for accountData in usersInDatabase:
        user = next(item for item in users if item["acid"] == accountData["acid"])
        if accountData["cur_callsign"] != user["cs"]:
            # Update account with new callsign
            old_callsign = accountData["cur_callsign"]
            accountData["cur_callsign"] = user["cs"]
            now = datetime.now()
            if user["cs"] not in accountData["callsigns"]:
                accountData["callsigns"][user["cs"]] = [now]
            else:
                accountData["callsigns"][user["cs"]].append(now)
            callsigns.update_one({"acid": user["acid"]}, {"$set": accountData})
            alerts.append(f"{user['acid']}({old_callsign}) changed their callsign to {user['cs']}\n")
    
    newAccounts = []
    accountIdsInDatabase = list(map(itemgetter("acid"), usersInDatabase))
    for user in users:
        if user["acid"] not in accountIdsInDatabase and user["acid"] != None and isinstance(user["acid"], int) and user["cs"] != "":
            # Create new account entries for users not in the database
            now = datetime.now()
            newAccounts.append({
                "acid": int(user["acid"]),
                "cur_callsign": user["cs"],
                "callsigns": {user["cs"]: [now]}
            })
            alerts.append(f"{user['acid']} created their first callsign: {user['cs']}\n")
    if len(newAccounts) > 0:
        callsigns.insert_many(newAccounts)
    return alerts