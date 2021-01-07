from flask import Flask, render_template
import json
from earthquake import SeismicEvent


app = Flask(__name__)


def getEvents():
    f = open("testFiles/test.json")
    x = json.load(f)
    f.close()
    return x['Event']

@app.route('/', methods=['POST', 'GET'])
def index():
    events = getEvents()

    eventList = []

    for event in events:
        seismicEvent = SeismicEvent(event['name'], event['coord'], event['ptime'], event['stime'],
                                    event['max_amp'])
        # seismicEvent.report()
        eventList.append(seismicEvent)
        print(f"STATION: %s , MAGNITUDE : {seismicEvent.magnitude:0.2f}" % seismicEvent.name)

    return render_template('index.html', events=eventList)

if __name__ == "__main__":
    app.run(debug=True)