from dotenv import load_dotenv
import os
import urllib.parse
import time
from datetime import datetime
from api import getChatMessages

load_dotenv()
geofs_session_id = os.environ.get("GEOFS_SESSION_ID")
ACCOUNTID = 897690

def parseChat(messages):
    msg = ""
    for message in messages:
        message["msg"] = urllib.parse.unquote(message["msg"])
        msg += f"({message['acid']}){message['cs']}> {message['msg']} | {datetime.now()}\n"
    return msg

def saveChatMessages(geofs_account_id, geofs_session_id, id, lastMsgId, saveLocation):
    while True:
        try:
            id, lastMsgID, messages = getChatMessages(geofs_account_id, geofs_session_id, id, lastMsgId)
            break
        except Exception as e:
            print("Failed to get chat messages, retrying...")
            print(e)
            time.sleep(5)
            continue
    parsed_messages = parseChat(messages)
    with open(saveLocation, "a") as file:
        file.write(parsed_messages)
    return id, lastMsgID