
---------- aircraft.py ----------

import numpy as np
from donnees import *
from functions import distance
from math import sin, atan, floor


class Aircraft:
    aircrafts_nbr = 0

    def __init__(self, callsign, parking, h_debut, masse, type_moteur, path_to_visit):
        """Un avion est caratérisé par son nom, son parking, l'heure de départ, son poids, son moteur ('egts' ou 'classique'), et le chemin qu'il doit parcourir"""
        self.id = Aircraft.aircrafts_nbr
        Aircraft.aircrafts_nbr += 1
        self.callsign = callsign
        self.parking = parking
        self.h_start = h_debut
        self.pos = path_to_visit[0]
        self.is_on_map = False
        self.is_arrived = False
        self.type = type_moteur
        self.max_speed = distance(path_to_visit[0], path_to_visit[1]) / PAS
        self.speed = self.max_speed
        self.mass = masse
        self.stop_counter = 0   #compteur de secondes passées à l'arrêt (PAS secondes entre chaque point)
        self.h_end = 0

        self.path_to_visit = path_to_visit   #liste des points à visiter (on retire les points au fur et à mesure)
        self.current_aim = self.path_to_visit.pop(0)
        self.dir = np.array(self.current_aim) - np.array(self.pos)  #on calcule le vecteur directeur


    def update(self, current_time, airport, is_slope):
        if self.is_on_map:
            if self.speed < self.max_speed:
                pente = 0
                if is_slope and self.type == 'egts':
                    Triangle = airport.triThePointIsIn(self.pos)

                    if Triangle != -1:  # si l'avion est dans la zone de relevés altimétriques
                        plan = airport.Plans[Triangle]
                        pente = 100 * (plan[0] * self.dir[0] + plan[1] * self.dir[1])  # a*Xdir+b*Ydir+c => Zdir+c = Δz+c car Δz = (Zdir+Zpos)-Zpos => pente = Δz/Δ(xy) car Δ(xy) = ||dir|| = 1

                self.accelerate(pente)

            if self.speed >= self.max_speed:
                self.speed = self.max_speed

            self.move()

            if self.is_arrived:
                self.h_end = current_time

        elif (not self.is_arrived) and (current_time >= self.h_start):
            self.is_on_map = True


    def accelerate(self, pente = 0):
        if self.type == 'egts':
            couple_pente = -self.mass * 9.81 * sin(atan(pente / 100)) * RAYON_ROUE
            couple_resistant = -self.mass * 10 * RAYON_ROUE * (BREAKAWAY_RESISTANCE if self.speed < 1 else ROLLING_RESISTANCE)
            couple_egts = (COUPLE_MAX_EGTS) if (self.speed < 1) else (min(COUPLE_MAX_EGTS, PUISSANCE_EGTS / (self.speed/RAYON_ROUE)))
            couple_aero = COEF_AERO * self.speed**2
            
            couple = couple_pente + couple_resistant + couple_egts + couple_aero

            acc = max(0, couple / (RAYON_ROUE * self.mass))

            self.speed += PAS_MODELE*acc
        
        else:
            self.speed += 0.9
        
    
    def move(self):
        if self.speed == 0:                 #si l'avion est à l'arrêt (2x le même point)
            if self.type == 'egts':             #si c'est un egts, l'avion redémarre immédiatement après le pushback
                self.stop_counter = PAS
                while self.path_to_visit[1] == self.current_aim:
                    self.path_to_visit.pop(0)
            else:                               #sinon, on attend PAS tours (ie PAS sec) avant de supprimer le point
                self.stop_counter += 1

        distance_to_aim = distance(self.current_aim, self.pos)
        
        if distance_to_aim < self.speed or self.stop_counter >= PAS:   #si on arrive au point suivant (on compare à la vitesse car la position évolue avec speed * dir et ||dir|| = 1 )
            if len(self.path_to_visit) == 1:    #si on est arrivé au bout du chemin, on supprime l'avion
                self.is_on_map = False
                self.is_arrived = True
                return 0

            self.stop_counter = 0
            self.max_speed = distance(self.path_to_visit[0], self.path_to_visit[1]) / PAS
            self.path_to_visit.pop(0)
            self.current_aim = self.path_to_visit[0]
            self.dir = np.array(self.current_aim) - np.array(self.pos)  #on calcule le vecteur directeur            
            self.dir = self.dir / np.linalg.norm(self.dir)              #que l'on rend unitaire

        self.pos = self.pos + self.speed * self.dir
            