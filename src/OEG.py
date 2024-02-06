import time
import click
from callsigns import checkCallsignChanges
from api import getMapUsers, getCredentials, sendMsg
from chat import saveChatMessages

@click.command()
@click.option("--push-to-geofs", "--geofs", is_flag=True, help="Send callsigns changes to GeoFS chat.")
def main(push_to_geofs):
    ACCOUNTID = 897690
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
                    print(msg)
                    if (push_to_geofs):
                        id, lastMsgID = getCredentials(ACCOUNTID)
                        id = sendMsg(msg, id, ACCOUNTID)
                        time.sleep(1)
                    break
                except Exception as e:
                    print("Failed to send message, retrying...")
                    print(e)
                    time.sleep(5)
                    continue
        id = saveChatMessages(ACCOUNTID)

if __name__ == "__main__":
    main()