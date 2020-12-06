import json
from earthquake import SeismicEvent 




def run():

    event = getEvent(printMenu())
    seismic_Event = SeismicEvent(event['name'], event['coord'], event['ptime'], event['stime'], event['max_amp'])
    seismic_Event.report()


def printMenu():

    print("1. Load Eureka Event")
    print("2. Load Elko Event")
    print("3. Load Las Vegas Event")
    print(">", end=' ')
    return int(input())


def getEvent(selection):

    f = open("test.json")
    x = json.load(f)
    f.close()
    return x['Event'][selection-1]

if __name__ == "__main__":
    run()