from datetime import datetime
from math import log10

class SeismicEvent:

    def __init__(self, name, coord, p_time, s_time, max_amplitude):

        self.name  = name
        self.coord = coord
        self.p_time, self.s_time = self.parse_arrival_times(p_time, s_time)
        self.max_amplitude = max_amplitude

        self.delta_time = (self.s_time - self.p_time).seconds   #Get Delta time in seconds for epicenter calculation
        self.distance_to_ep = self.calculate_distance()
        self.magnitude = self.calculate_magnitude()


    def calculate_distance(self, Vp=6.4, Vs=3.84):
        
        '''
            Calculates earthquake distance from this specific station using approximated P and S waves velocity on Greece's Region
            where P-wave velocity is ~6.4km/sec. S-wave velocity is around 60% of p-wave's so ~3.84km/sec 

            Distance = velocity * time
            For p-wave d = Vp * Tp
            For s-wave d = Vs * Ts
            Solve the system with 2 unknown vars.
        '''

        wave_velocity = (Vs*Vp)/(Vp-Vs)
        distance = self.delta_time * wave_velocity
        return distance



    def calculate_magnitude(self):

        '''
            Calculates earthquake magnitude (On Richter scale) based on http://www.ux1.eiu.edu/~cfjps/1300/magnitude.html
            Magnitude = log10(Amplitude(mm)) + Distance_correction_factor
            Where Distance_correction_factor = 3*log10(8*delta) - 2.92
        '''

        distance_correction_factor = 3*log10(8*self.delta_time) - 2.92
        magnitude = log10(self.max_amplitude) + distance_correction_factor
        
        return magnitude



    def parse_arrival_times(self, p_time, s_time):

        #parse station time from str
        
        ptime = datetime.strptime(p_time, "%H:%M:%S")
        stime = datetime.strptime(s_time, "%H:%M:%S")

        return ptime, stime

    def report(self):

        print("Wave travelled %s km" % self.distance_to_ep)
        print("Earthquake has a magnitude of %s in Richter scale" % self.magnitude)
        