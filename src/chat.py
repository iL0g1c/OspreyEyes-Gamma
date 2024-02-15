from dotenv import load_dotenv
import os
import urllib.parse
import time
from datetime import datetime
from pymongo import MongoClient
from api import getChatMessages

# MongoDB connection
load_dotenv()
password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb://mongo_db_admin:{password}@45.76.164.130:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+1.5.0"
client = MongoClient(connection_string)
OspreyEyes = client["OspreyEyes"]
messageCollection = OspreyEyes["messages"]

def parseChat(messages):
    msg = []
    for message in messages:
        parsed_message = {
            "acid": message["acid"],
            "msg": urllib.parse.unquote(message["msg"]),
            "time": datetime.now(),
            "id": message["uid"]
        }
        msg.append(parsed_message)
    return msg

def processChatMessages(geofs_account_id, geofs_session_id, id, lastMsgId):
    while True:
        try:
            id, lastMsgID, messages = getChatMessages(geofs_account_id, geofs_session_id, id, lastMsgId)
            break
        except Exception as e:
            print("Failed to get chat messages, retrying...")
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            time.sleep(5)
            continue
    parsed_messages = parseChat(messages)
    if len(parsed_messages) > 0:
        messageCollection.insert_many(parsed_messages)
    
    return id, lastMsgID