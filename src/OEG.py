import time
import click
from callsigns import checkCallsignChanges
from dotenv import load_dotenv
import os
from api import getMapUsers, getCredentials, sendMsg
from chat import saveChatMessages

@click.command()
@click.option("--push-to-geofs", "--geofs", is_flag=True, help="Send callsigns changes to GeoFS chat.")
def main(push_to_geofs):
    if (push_to_geofs):
        print("WARNING: Pushing messages to GeoFS chat.")   
    load_dotenv()
    geofs_account_id = os.environ.get("GEOFS_ACCOUNT_ID")
    geofs_session_id = os.environ.get("GEOFS_SESSION_ID")
    CHAT_FILE_SAVE_LOCATION = "chat.txt"
    id, lastMsgID = getCredentials(geofs_session_id, geofs_account_id)
    time.sleep(1)
    id, lastMsgID = sendMsg(geofs_account_id, geofs_session_id, id, lastMsgID, "OspreyEyes Gamma Online")
    print("Starting Tracking...")

    while True:
        try:
            data = getMapUsers()
        except Exception as e:
            print("No data received, retrying...")
            print(e)
            time.sleep(5)
            continue
        messages = checkCallsignChanges(data)
        for msg in messages:
            while True:
                try:
                    if (push_to_geofs):
                        id, lastMsgID = sendMsg(geofs_account_id, geofs_session_id, id, lastMsgID, msg)
                        time.sleep(1)
                    else:
                        print(msg)
                    break
                except Exception as e:
                    print("Failed to send message, retrying...")
                    print(e)
                    time.sleep(5)
                    continue
        id, lastMsgID = saveChatMessages(geofs_account_id, geofs_session_id, id, lastMsgID, CHAT_FILE_SAVE_LOCATION)

if __name__ == "__main__":
    main()