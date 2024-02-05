from dotenv import load_dotenv
import os
import urllib.parse
from geofs import multiplayerAPI

load_dotenv()
password = os.environ.get("MONGODB_PWD")
geofs_session_id = os.environ.get("GEOFS_SESSION_ID")
multiplayerAPI = multiplayerAPI(geofs_session_id, 893868)
multiplayerAPI.handshake()

def parseChat(messages):
    msg = ""
    for message in messages:
        message["msg"] = urllib.parse.unquote(message["msg"])
        msg += f"({message['acid']}){message['cs']}> {message['msg']}\n"
    return msg

def saveChatMessages():
    messages = multiplayerAPI.getMessages()
    print(messages)
    parsed_messages = parseChat(messages)
    print(parsed_messages)