from datetime import datetime
from math import log10, radians, cos, sin, degrees, asin, atan2
import numpy as np

earthRadius = 6371  # km


class SeismicEvent:

    def __init__(self, name, coord, p_time, s_time, max_amplitude):
        self.name = name
        self.coord = coord
        self.p_time, self.s_time = self.parse_arrival_times(p_time, s_time)
        self.max_amplitude = max_amplitude

        self.delta_time = (self.s_time - self.p_time).seconds  # Get Delta time in seconds for epicenter calculation
        self.distance_to_ep = self.calculate_distance()
        self.magnitude = self.calculate_magnitude()

    def calculate_distance(self, Vp=6.4, Vs=3.84):
        """
            Calculates earthquake distance from this specific station using approximated P and S waves velocity on Greece's Region
            where P-wave velocity is ~6.4km/sec. S-wave velocity is around 60% of p-wave's so ~3.84km/sec

            Distance = velocity * time
            For p-wave d = Vp * Tp
            For s-wave d = Vs * Ts
            Solve the system with 2 unknown vars.
        """
        #Vs = 3.67
        #Vp = 6.34

        wave_velocity = (Vs * Vp) / (Vp - Vs)
        distance = self.delta_time * wave_velocity
        return distance

    def calculate_magnitude(self):
        """
            Calculates earthquake magnitude (On Richter scale) based on http://www.ux1.eiu.edu/~cfjps/1300/magnitude.html
            Magnitude = log10(Amplitude(mm)) + Distance_correction_factor
            Where Distance_correction_factor = 3*log10(8*delta) - 2.92
        """

        distance_correction_factor = 3 * log10(8 * self.delta_time) - 2.92
        magnitude = log10(self.max_amplitude) + distance_correction_factor

        return magnitude

    def parse_arrival_times(self, p_time, s_time):
        # parse station time from str

        ptime = datetime.strptime(p_time, "%H:%M:%S")
        stime = datetime.strptime(s_time, "%H:%M:%S")

        return ptime, stime

    def report(self):
        print("Wave travelled %s km" % self.distance_to_ep)
        print("Earthquake has a magnitude of %s in Richter scale" % self.magnitude)


class Earthquake:
    """
        Gets 3 Seismic Events data and finds
        the  epicenter using triangulation
    """

    def __init__(self, eventsList):
        self.seismicEvents = []

        for event in eventsList:
            self.seismicEvents.append(event)

        self.lat0 = self.seismicEvents[0].coord[0]
        self.lon0 = self.seismicEvents[0].coord[1]
        self.radius0 = self.seismicEvents[0].distance_to_ep
        self.magnitude0 = self.seismicEvents[0].magnitude

        self.lat1 = self.seismicEvents[1].coord[0]
        self.lon1 = self.seismicEvents[1].coord[1]
        self.radius1 = self.seismicEvents[1].distance_to_ep
        self.magnitude1 = self.seismicEvents[1].magnitude


        self.lat2 = self.seismicEvents[2].coord[0]
        self.lon2 = self.seismicEvents[2].coord[1]
        self.radius2 = self.seismicEvents[2].distance_to_ep
        self.magnitude2 = self.seismicEvents[2].magnitude


        # for event in self.seismicEvents:
        #     print(event)

    def calculate_epicenter(self):
        """
        Calculates the epicenter of earthquake in following steps:
        1. Converts latitude and longitude of each station to ECEF coordinates
        """

        x0 = earthRadius * (cos(radians(self.lat0)) * cos(radians(self.lon0)))
        y0 = earthRadius * (cos(radians(self.lat0)) * sin(radians(self.lon0)))
        z0 = earthRadius * sin(radians(self.lat0))

        x1 = earthRadius * (cos(radians(self.lat1)) * cos(radians(self.lon1)))
        y1 = earthRadius * (cos(radians(self.lat1)) * sin(radians(self.lon1)))
        z1 = earthRadius * sin(radians(self.lat1))

        x2 = earthRadius * (cos(radians(self.lat2)) * cos(radians(self.lon2)))
        y2 = earthRadius * (cos(radians(self.lat2)) * sin(radians(self.lon2)))
        z2 = earthRadius * sin(radians(self.lat2))

        """
        Create an array for each set of coord so we can easily transform points so p0 is on origin,
        then rotate so p1 is on x axis and p2 on x-y plane
        For translation substract p0 from p1 and p2
        """

        P0 = np.array([x0, y0, z0])
        P1 = np.array([x1, y1, z1])
        P2 = np.array([x2, y2, z2])

        ex = (P1 - P0) / (np.linalg.norm(P1 - P0))  # Normalized vector of p1-p0 -> x coefficient
        i = np.dot(ex, P2 - P0)

        ey = (P2 - P0 - (i * ex)) / np.linalg.norm(P2 - P0 - (i * ex))  # y coefficient
        ez = np.cross(ex, ey)  # z coefficient

        d = float(np.linalg.norm(P1 - P0))
        j = np.dot(ey, P2 - P0)

        x = (pow(self.radius0, 2) - pow(self.radius1, 2) + pow(d, 2)) / (2 * d)
        y = ((pow(self.radius0, 2) - pow(self.radius2, 2) + pow(i, 2) + pow(j, 2)) / (2 * j)) - ((i / j) * x)
        z = np.sqrt(abs(pow(self.radius0, 2) - pow(x, 2) - pow(y, 2)))

        triPt = P1 + x * ex + y * ey + z * ez

        """
        Convert back to lat/lon
        """

        lat = f"{(degrees(asin(triPt[2] / earthRadius))):.4f}"
        lon = f"{(degrees(atan2(triPt[1], triPt[0]))):.4f}"


        #Lastly average magnitudes of earthquake
        avg_magnitude = (self.magnitude0 + self.magnitude1 + self.magnitude2) / 3

        return (lat, lon), avg_magnitude
