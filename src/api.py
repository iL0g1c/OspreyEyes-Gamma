import requests
import json

def getMapUsers():
    response = requests.post(
        "https://mps.geo-fs.com/map",
        json = {}
    )

    response_body = json.loads(response.text)
    userList = response_body["users"]
    return userList
def getCredentials(acid, geofs_session_id):
    body = {
        "acid":acid,
        "sid":geofs_session_id,
        "id":"","ac":"24",
        "co":[51.16707412918196,-0.08848770230371465,69.26255848717521,-56.08184334084648,0,0],
        "ve":[7.105427357601002e-18,1.3877787807814457e-20,1.0154927565508843e-10,0,0,0],
        "st":{"gr":True,"as":0},
        "ti":1707753106276,
        "m":"",
        "ci":0
    }
    response = requests.post(
        "https://mps.geo-fs.com/update",
        json = body,
        cookies = {"PHPSESSID": geofs_session_id}
    )
    response_body = json.loads(response.text)
    id = response_body["myId"]
    lastMsgId = response_body["lastMsgId"]
    return id, lastMsgId

def sendMsg(acid, geofs_session_id, id, lastMsgId, message):
    body = {
        "acid": acid,
        "sid": geofs_session_id,
        "id": id,
        "ac":"24",
        "co":[51.16707792407465,-0.08848356497311004,69.16003342673534,-57.19284101863162,0.028139623668361896,-0.17216500902194584],
        "ve":[1.6153655906236964e-9,1.946535969118979e-9,-0.00007273660338903198,0,0,0],
        "st":{"gr":True,"as":0},
        "ti":1707753107638.99,
        "m": message,
        "ci":lastMsgId
    }
    response = requests.post(
        "https://mps.geo-fs.com/update",
        json = body,
        cookies = {"PHPSESSID": geofs_session_id}
    )
    response_body = json.loads(response.text)
    id = response_body["myId"]
    return id, lastMsgId

def getChatMessages(acid, geofs_session_id, id, lastMsgId):
    body = {
        "acid": acid,
        "sid": geofs_session_id,
        "id": id,
        "ac":"24",
        "co":[51.16707792407465,-0.08848356497311004,69.16003342673534,-57.19284101863162,0.028139623668361896,-0.17216500902194584],
        "ve":[1.6153655906236964e-9,1.946535969118979e-9,-0.00007273660338903198,0,0,0],
        "st":{"gr":True,"as":0},
        "ti":1707753107638.99,
        "m":"",
        "ci":lastMsgId
    }
    response = requests.post(
        "https://mps.geo-fs.com/update",
        json = body,
        cookies = {"PHPSESSID": geofs_session_id}
    )
    response_body = json.loads(response.text)
    id = response_body["myId"]
    lastMsgId = response_body["lastMsgId"]
    chatMessages = response_body["chatMessages"]
    return id, lastMsgId, chatMessages