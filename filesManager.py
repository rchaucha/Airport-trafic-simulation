
---------- filesManager.py ----------

 numpy as np
import pickle
import os
import airport

CWD = os.getcwd().replace('\\', '/') + '/'


def saveData(Flights, Aircrafts, airport, Graph):
    with open(CWD + "data/Flights.pkl", 'wb') as output:
        pickle.dump(Flights, output, pickle.HIGHEST_PROTOCOL)

    with open(CWD + "data/Aircrafts.pkl", 'wb') as output:
        pickle.dump(Aircrafts, output, pickle.HIGHEST_PROTOCOL)

    with open(CWD + "data/Airport.pkl", 'wb') as output:
        pickle.dump(airport, output, pickle.HIGHEST_PROTOCOL)

    with open(CWD + "data/Graph.pkl", 'wb') as output:
        pickle.dump(Graph, output, pickle.HIGHEST_PROTOCOL)


def loadData():
    """Return : [Flights, Aircrafts, airport, Graph]"""

    with open(CWD + "data/Flights.pkl", 'rb') as input:
        Flights = pickle.load(input)

    with open(CWD + "data/Aircrafts.pkl", 'rb') as input:
        Aircrafts = pickle.load(input)

    with open(CWD + "data/airport.pkl", 'rb') as input:
        airport = pickle.load(input)

    with open(CWD + "data/Graph.pkl", 'rb') as input:
        Graph = pickle.load(input)

    return [Flights, Aircrafts, airport, Graph]


def getFlightsData():
    Flights = []
    with open(CWD + "data/flights.txt", "r") as flights:
        for line in flights:
            Line = line.split()
            Line[5] = int(Line[5])
            Line[6] = int(Line[6])
            for i in range(8, len(Line)):
                Coos = Line[i].split(',')
                Line[i] = (int(Coos[0]), int(Coos[1]))

            Flights.append(Line)

    return np.array(Flights)


def getAirportData():
    """ Retourne : [Points, Lignes, Pistes, Altitudes, Noms_Triangles, Coos_Triangles] """

    Points, Lignes, Pistes, Altitudes, Noms_Triangles, Coos_Triangles = [], [], [], {}, [], {}

    with open(CWD + "data/map.txt", "r") as map:
        for line in map:
            Line = line.split()

            if Line[0] == 'P':
                Points += [Line[1:]]

            elif Line[0] == 'L':
                Pts_on_line = []
                for P in Line[5:]:
                    Coos = P.split(',')
                    Pts_on_line.append((int(Coos[0]), int(Coos[1])))

                Lignes.append(airport.Taxiway(Line[1] + " " + Line[2], Line[3], Line[4], Pts_on_line))

            elif Line[0] == 'R':
                Pts_on_line = []
                for P in Line[5:]:
                    Coos = P.split(',')
                    Pts_on_line.append((int(Coos[0]), int(Coos[1])))
                Pistes += [Line[1:4] + Line[4].split(',') + Pts_on_line]

        Points = np.array(Points)
        Lignes = np.array(Lignes)
        Pistes = np.array(Pistes)

    with open(CWD + "data/alt.txt", "r") as alt:
        for line in alt:
            Line = line.split()
            if Line[0] == 'Point':
                Altitudes[Line[1]] = Line[2:]

            elif Line[0] == 'Triangles':
                Noms_Triangles += [' '.join(Line[1:])]

        Noms_Triangles = np.array(Noms_Triangles)

        for T in Noms_Triangles:
            Coos_Triangles[T] = [Altitudes[P] for P in T.split(' ')]

    return Points, Lignes, Pistes, Altitudes, Noms_Triangles, Coos_Triangles


def logResults(Aircrafts, EGTS_RATE, PUISSANCE_EGTS):
    from datetime import datetime

    def getTerminal(parking):
        for i, c in enumerate(parking):
            if c.isdigit(): break
        return parking[:i]

    with open(CWD + "Results/" + datetime.now().strftime("%m-%d_%Hh%M") + " EGTS" + str(EGTS_RATE) + " POWER" + str(PUISSANCE_EGTS) + ".txt", 'w') as output:
        output.write("ID,Callsign,Type,Terminal,Parking,Temps de trajet\n")
        for a in Aircrafts:
            if a.h_end != 0:
                output.write(str(a.id) + ',' + a.callsign + ',' + a.type + ',' + getTerminal(a.parking) + ',' + a.parking + ',' + str(a.h_end - a.h_start) + '\n')
