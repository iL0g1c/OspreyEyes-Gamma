from pymongo import MongoClient
from datetime import datetime
import os
from bson import json_util
import json
from dotenv import load_dotenv

def datetime_to_string(datetime_obj):
    datetime_str = datetime_obj.strftime("%Y-%m-%d %H-%M-%S")
    return datetime_str

load_dotenv()
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb://mongo_db_admin:{password}@45.76.164.130:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+1.5.0"
client = MongoClient(connection_string)

database = client["OspreyEyes"]
callsigns = database["messages"]
print("Fetching data from MongoDB...")
documents = callsigns.find()
chatData = []

print("Converting to json...")
i = 0
for document in documents:
    document_dict = json_util.loads(json_util.dumps(document))
    print(f"Processing document {i}...")
    chatData.append(
        {
            "acid": document_dict["acid"],
            "msg": document_dict["msg"],
            "time": datetime_to_string(document_dict["time"]),
            "id": document_dict["id"]
        }
    )
    i += 1
print("Saving to file...")

with open("chat.json", mode = 'w') as writer:
    json.dump(chatData, writer)