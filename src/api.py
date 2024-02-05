import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
geofs_session_id = os.environ.get("GEOFS_SESSION_ID")

def getMapUsers():
    response = requests.post(
        "https://mps.geo-fs.com/map",
        json = {
        }
    )

    response_body = json.loads(response.text)
    userList = response_body["users"]
    return userList
def getCredentials(acid):
    body = {
        "origin": "https://www.geo-fs.com",
        "acid": acid,
        "sid": geofs_session_id,
        "id": "",
        "ac": "1",
        "co": [42.36021568682466,-70.98767598755524,4.589746820023676,-103.04273973572526,-15.919583740307557,-0.376840533503692],
        "ve": [2.7011560632672626e-10,7.436167948071671e-11,0.000004503549489433212,0,0,0],
        "st": {"gr":True,"as":0},
        "ti": 1678751444055,
        "m": "", 
        "ci": 0
    }
    response = requests.post(
        "https://mps.geo-fs.com/update",
        json = body,
        cookies = {"PHPSESSID": geofs_session_id}
    )
    print("Successfully connect to server.")
    response_body = json.loads(response.text)
    id = response_body["myId"]


    body2 = {
        "origin": "https://www.geo-fs.com",
        "acid": acid,
        "sid": geofs_session_id,
        "id": id,
        "ac": "1",
        "co": [42.36021568682466,-70.98767598755524,4.589746820023676,-103.04273973572526,-15.919583740307557,-0.376840533503692],
        "ve": [2.7011560632672626e-10,7.436167948071671e-11,0.000004503549489433212,0,0,0],
        "st": {"gr":True,"as":0},
        "ti": 1678751444055,
        "m": "", 
        "ci": 0
    }
    response = requests.post(
        "https://mps.geo-fs.com/update",
        json = body2,
        cookies = {"PHPSESSID": geofs_session_id}
    )
    response_body = json.loads(response.text)
    id = response_body["myId"]
    lastMsgID = response_body["lastMsgId"]
    return id, lastMsgID

def sendMsg(msg, id, accountID):
    body = {
        "origin": "https://www.geo-fs.com",
        "acid": accountID,
        "sid": geofs_session_id,
        "id": id,
        "ac": "1",
        "co": [42.36021568682466,-70.98767598755524,4.589746820023676,-103.04273973572526,-15.919583740307557,-0.376840533503692],
        "ve": [2.7011560632672626e-10,7.436167948071671e-11,0.000004503549489433212,0,0,0],
        "st": {"gr":True,"as":0},
        "ti": None,
        "m": msg,
        "ci": 0
    }
    response = requests.post(
        "https://mps.geo-fs.com/update",
        json = body,
        cookies = {"PHPSESSID": geofs_session_id}
    )
    response_body = json.loads(response.text)
    id = response_body["myId"]
    return id

def getChatMessages(id, accountID, lastMsgID):
    body = {
        "origin": "https://www.geo-fs.com",
        "acid": accountID,
        "sid": geofs_session_id,
        "id": id,
        "ac": "1",
        "co": [42.36021568682466,-70.98767598755524,4.589746820023676,-103.04273973572526,-15.919583740307557,-0.376840533503692],
        "ve": [2.7011560632672626e-10,7.436167948071671e-11,0.000004503549489433212,0,0,0],
        "st": {"gr":True,"as":0},
        "ti": None,
        "m": "",
        "ci": lastMsgID
    }
    response = requests.post(
        "https://mps.geo-fs.com/update",
        json = body,
        cookies = {"PHPSESSID": geofs_session_id}
    )
    response_body = json.loads(response.text)
    id = response_body["myId"]
    lastMsgID = response_body["lastMsgId"]
    return id, lastMsgID, response_body["chatMessages"]