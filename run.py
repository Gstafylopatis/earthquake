import json
from earthquake import SeismicEvent
from earthquake import Earthquake


def run():
    eventList = []

    while len(eventList) < 3:
        newEvent = getEvent(printMenu())
        seismicEvent = SeismicEvent(newEvent['name'], newEvent['coord'], newEvent['ptime'], newEvent['stime'],
                                    newEvent['max_amp'])
        # seismicEvent.report()
        eventList.append(seismicEvent)

    earthquake = Earthquake(eventList)
    lat, lon = earthquake.calculate_epicenter()

    print("Latitude = %s and longitude = %s" % (lat, lon))


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
