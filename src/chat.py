from dotenv import load_dotenv
import os
import urllib.parse
import time
from api import getCredentials, getChatMessages

load_dotenv()
geofs_session_id = os.environ.get("GEOFS_SESSION_ID")
ACCOUNTID = 897690

def parseChat(messages):
    msg = ""
    for message in messages:
        message["msg"] = urllib.parse.unquote(message["msg"])
        msg += f"({message['acid']}){message['cs']}> {message['msg']}\n"
    return msg

def saveChatMessages(geofs_account_id, geofs_session_id, id, lastMsgId):
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
    return id, lastMsgID