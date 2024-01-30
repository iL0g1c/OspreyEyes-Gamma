from geofs import MapAPI
import time
from callsigns import parseCallsigns

def main():
    print("Starting Tracking...")
    map_api = MapAPI()
    while True:
        data = map_api.getUsers(foos=False)
        if data == None:
            print("No data received, retrying...")
            time.sleep(5)
            continue
        parseCallsigns(data)
        time.sleep(1)

if __name__ == "__main__":
    main()