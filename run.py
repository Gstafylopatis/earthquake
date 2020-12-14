import json
import timeit

from earthquake import SeismicEvent
from earthquake import Earthquake
import time


def run():
    events = getEvents()
    eventList = []

    for event in events:
        seismicEvent = SeismicEvent(event['name'], event['coord'], event['ptime'], event['stime'],
                                    event['max_amp'])
        # seismicEvent.report()
        eventList.append(seismicEvent)

    tic = time.perf_counter()
    earthquake = Earthquake(eventList)
    coord, magnitude = earthquake.calculate_epicenter()
    toc = time.perf_counter()

    magnitude = f"{magnitude:.2f}"

    print("Earthquake magnitude: %s" % magnitude)
    print("Coordinates of epicenter (lat,lon): %s" % (coord,))
    print(f"Trilateration calculation completed in {toc - tic:0.5f} seconds")



def getEvents():
    f = open("test.json")
    x = json.load(f)
    f.close()
    return x['Event']


if __name__ == "__main__":
    tic = time.perf_counter()
    run()
    toc = time.perf_counter()
    print(f"Whole Execution time = {toc-tic:.5f}")
