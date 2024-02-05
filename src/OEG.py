import time
from callsigns import checkCallsignChanges
from api import getMapUsers, getCredentials, sendMsg

def main():
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

                    id, lastMsgID = getCredentials(ACCOUNTID)
                    id = sendMsg(msg, id, ACCOUNTID)
                    break
                except Exception as e:
                    print("Failed to send message, retrying...")
                    print(e)
                    time.sleep(5)
                    continue
            time.sleep(1)

if __name__ == "__main__":
    main()