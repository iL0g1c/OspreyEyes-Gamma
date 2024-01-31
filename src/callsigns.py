from datetime import datetime
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from geofs import multiplayerAPI

# MongoDB connection
load_dotenv()
password = os.environ.get("MONGODB_PWD")
geofs_session_id = os.environ.get("GEOFS_SESSION_ID")

connection_string = f"mongodb://mongo_db_admin:{password}@45.76.164.130:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+1.5.0"
client = MongoClient(connection_string)
OspreyEyes = client["OspreyEyes"]
callsigns = OspreyEyes["callsigns"]

def checkCallsignChanges(users):
    for user in users:
        if user.userInfo["id"] is not None and user.userInfo["callsign"] != "" and user.userInfo["callsign"] != "Foo":
            query = {"acid": user.userInfo["id"]}
            accountData = callsigns.find_one(query)
            # Check if user is in database
            if accountData:
                if accountData["cur_callsign"] != user.userInfo["callsign"]:
                    # Update account with new callsign
                    old_callsign = accountData["cur_callsign"]
                    accountData["cur_callsign"] = user.userInfo["callsign"]
                    now = datetime.now()
                    if user.userInfo["callsign"] not in accountData["callsigns"]:
                        accountData["callsigns"][user.userInfo["callsign"]] = [now]
                    else:
                        accountData["callsigns"][user.userInfo["callsign"]].append(now)
                    callsigns.update_one(query, {"$set": accountData})
                    alert = f"{user.userInfo['id']}({old_callsign}) changed their callsign to {user.userInfo['callsign']}\n"
                    print(alert)
                    # api = multiplayerAPI(geofs_session_id, 893200)
                    # api.handshake()
                    # api.sendMsg(alert)
                    return f"{user.userInfo['id']}({old_callsign}) changed their callsign to {user.userInfo['callsign']}\n"
            else:
                # Create new account entry
                now = datetime.now()
                newAccountData = {
                    "acid": int(user.userInfo["id"]),
                    "cur_callsign": user.userInfo["callsign"],
                    "callsigns": {user.userInfo["callsign"]: [now]}
                }
                callsigns.insert_one(newAccountData)
                return ""