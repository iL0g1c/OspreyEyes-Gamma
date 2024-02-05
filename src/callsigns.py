from datetime import datetime
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import json

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
    
    users = removeDuplicateAccounts(users)
    alerts = []
    for user in users:
        if user["acid"] is not None and user["cs"] != "" and user["cs"] != "Foo":
            query = {"acid": user["acid"]}
            accountData = callsigns.find_one(query)
            # Check if user is in database
            if accountData:
                if accountData["cur_callsign"] != user["cs"]:
                    # Update account with new callsign
                    old_callsign = accountData["cur_callsign"]
                    accountData["cur_callsign"] = user["cs"]
                    now = datetime.now()
                    if user["cs"] not in accountData["callsigns"]:
                        accountData["callsigns"][user["cs"]] = [now]
                    else:
                        accountData["callsigns"][user["cs"]].append(now)
                    callsigns.update_one(query, {"$set": accountData})
                    alerts.append(f"{user['acid']}({old_callsign}) changed their callsign to {user['cs']}\n")
            else:
                # Create new account entry
                now = datetime.now()
                newAccountData = {
                    "acid": int(user["acid"]),
                    "cur_callsign": user["cs"],
                    "callsigns": {user["cs"]: [now]}
                }
                callsigns.insert_one(newAccountData)
    return alerts