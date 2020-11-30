import json



def input_data():

    f = open("test.json")
    x = json.load(f)
    for i in x["Event"]:
        print(i["coord"])

    f.close()