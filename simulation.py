
---------- simulation.py ----------

from renderer import *
from aircraft import *
from airport import *
from filesManager import *
from math import ceil, floor
from random import random
from winsound import Beep
from donnees import PUISSANCE_EGTS


GENERATE_DATA = 0
IS_PLOT = 1
IS_SLOPE = 1
EGTS_RATE = 0.5

print("Paramètres:")
print("  Pente: " + "Oui" if IS_SLOPE else ("Non"))
print("  Pourcentage d'EGTS: " + str(EGTS_RATE*100))
print("  PUISSANCE_EGTS = " + str(PUISSANCE_EGTS))


#------- ON RECUPERE LES DONNEES -------#
if GENERATE_DATA:
    airport = Airport()
    Graph = airport.createAirportGraph()
    
    Flights = getFlightsData()      #['DEP', 'BCS1748', 'M', 'M17', '27L', 1440, 2115, '_', (-955, -1104), (-946, -1116), ...] = [DEP|ARR, callsign (nom avion), Taille, Parking, QFU (sens de la piste), h_debut, h_piste, h_slot, (x1,y1), (x2,y2), ...] (cf .txt pr + d'info)
    
    Aircrafts = []
    for F in Flights:
        mass = 0
        type = 'classique'

        if F[2] == 'M' and random() < EGTS_RATE:    #on installe des egts sur les M avec un taux EGTS_RATE
            mass = 69 if F[0] == 'DEP' else 62      #et on aura besoin de leur masse (masse d'un A320 en tonnes)
            type = 'egts'

        Aircrafts.append(Aircraft(F[1], F[3], F[5], mass * 1000, type, F[8:]))

    saveData(Flights, Aircrafts, airport, Graph)

else: [Flights, Aircrafts, airport, Graph] = loadData()

#--------------------------------------#


if IS_PLOT:
    renderer = Renderer('2d', is_anim=1)
    renderer.drawAirportPlan(airport.Lignes, airport.Pistes, airport.Coos_Triangles)


TIME_STEP = 15   #nombre de secondes écoulées dans la simulation entre 2 rafraichissements

for current_time in range(24 * 3600):
    for aircraft in Aircrafts[365:]:
        aircraft.update(current_time, airport, IS_SLOPE)

    if IS_PLOT and current_time % TIME_STEP == 0:
        renderer.drawAircrafts(Aircrafts[365:], current_time)
        input("a ")

logResults(Aircrafts, EGTS_RATE, PUISSANCE_EGTS)

print("Done")
Beep(800, 200)
Beep(2000, 200)
Beep(1500, 200)
