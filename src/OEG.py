import time
import click
from callsigns import checkCallsignChanges
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import sys
from api import getMapUsers, getCredentials, sendMsg, getPlayerCount
from chat import processChatMessages
from playerCount import savePlayerCount
from onlineDetector import updateOnlineUsers

@click.command()
@click.option("--push-to-geofs", "--geofs", is_flag=True, help="Send callsigns changes to GeoFS chat.")
@click.option("--callsignChanges", "--cc", is_flag=True, help="Check for callsign changes.")
@click.option("--chatMessages", "--cm", is_flag=True, help="Log chat messages.")
@click.option("--playerCount", "--pc", is_flag=True, help="Log player count.")
@click.option("--logon-logoff", "--ll", is_flag=True, help="Log logon and logoff event tracking.")
def main(push_to_geofs, callsignchanges, chatmessages, playercount, logon_logoff):
    if (push_to_geofs):
        print("WARNING: Pushing messages to GeoFS chat.")

    # Load envs
    load_dotenv()
    geofs_account_id = os.environ.get("GEOFS_ACCOUNT_ID")
    geofs_session_id = os.environ.get("GEOFS_SESSION_ID")
    CHAT_FILE_SAVE_LOCATION = "chat.txt"

    # Do handshake
    id, lastMsgID = getCredentials(geofs_session_id, geofs_account_id)
    time.sleep(1)

    nextPlayerCountLog = datetime.now() + timedelta(hours=1)

    # Announce online
    id, lastMsgID = sendMsg(geofs_account_id, geofs_session_id, id, lastMsgID, "OspreyEyes Gamma Online")

    if (callsignchanges):
        print("Callsign Tracking Enabled.")
    if (chatmessages):
        print("Chat Message Logging Enabled.")
    if (playercount):
        print("Player Count Logging Enabled.")
    if (logon_logoff):
        print("Logon/Logoff Tracking Enabled.")
    print("Starting Tracking...")

    while True:
        try:
            rawData = getMapUsers()
            data = []
            for user in rawData:
                if user != None:
                    if user["acid"] != None:
                        data.append(user)

        except Exception as e:
            print("No data received, retrying...")
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            time.sleep(5)
            continue
        if (callsignchanges):
            callsignchanges = checkCallsignChanges(data) # Get callsign changes
            for msg in callsignchanges: # Send callsign changes
                while True:
                    try:
                        if (push_to_geofs):
                            print(msg)
                            id, lastMsgID = sendMsg(geofs_account_id, geofs_session_id, id, lastMsgID, msg)
                            time.sleep(1)
                        else:
                            print(msg)
                        break
                    except Exception as e:
                        print("Failed to send message, retrying...")
                        print(e)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        time.sleep(5)
                        continue
        if (chatmessages):
            id, lastMsgID = processChatMessages(geofs_account_id, geofs_session_id, id, lastMsgID) # Save chat messages
        if (playercount):
            if (datetime.now() > nextPlayerCountLog):
                try:
                    playercount = getPlayerCount()
                except Exception as e:
                    print("No data received, retrying...")
                    print(e)
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    time.sleep(5)
                    continue
                savePlayerCount(playercount)
                nextPlayerCountLog = datetime.now() + timedelta(hours=1)
        if (logon_logoff):
            activityAlerts = updateOnlineUsers(data)
            if activityAlerts != []:
                for alert in activityAlerts:
                    # print(activityAlerts)
                    pass


if __name__ == "__main__":
    main()