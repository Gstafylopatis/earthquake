from datetime import datetime

class SeismicEvent:

    def __init__(self, name, coord, p_time, s_time, max_amplitude):

        self.name  = name
        self.coord = coord
        self.p_time, self.s_time = self.parse_arrival_times(p_time, s_time)
        self.max_amplitude = max_amplitude

    def parse_arrival_times(self, p_time, s_time):

        #parse station time from str
        
        ptime = datetime.strptime(p_time, "%H:%M:%S")
        stime = datetime.strptime(s_time, "%H:%M:%S")

        return ptime, stime

    def printTimes(self):
        print("Ptime :", self.p_time)
        print("Stime :", self.s_time)
        