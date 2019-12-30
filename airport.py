
---------- airport.py ----------

import networkx as nx
from functions import planTri, isPointInTri, distance
from filesManager import getAirportData


class Taxiway:
    def __init__(self, nom, autorisation, sens, points):
        self.nom = nom
        self.aut = autorisation
        self.sens = sens
        self.pts = points

    def __str__(self):
        return str([self.nom, self.aut, self.sens, self.pts])



class Airport:
    def __init__(self):
        Points, Lignes, Pistes, Altitudes, Noms_Triangles, Coos_Triangles = getAirportData()

        self.Points = Points        # ['K05' '0' '2741,-243'] = [Nom point, Type, Coordonées]
        self.Lignes = Lignes
        self.Pistes = Pistes
        self.Altitudes = Altitudes
        self.Noms_Triangles = Noms_Triangles
        self.Coos_Triangles = Coos_Triangles
        
        self.Plans = {}
        for T in self.Noms_Triangles:
            self.Plans[T] = planTri(self.Coos_Triangles[T])
        
        
        
    def triThePointIsIn(self, P):
        for T in self.Noms_Triangles:
            if isPointInTri(P, self.Coos_Triangles[T]): return T
        return -1


    
    def createAirportGraph(self):
        G = nx.DiGraph()
        
        for ligne in self.Lignes:
            Pts = ligne.pts
            G.add_nodes_from(nx.Graph(Pts))
            for i in range(0, len(Pts) - 1):
                P1, P2 = Pts[i], Pts[i+1]
                d = distance(P1, P2)
                
                G.add_edge(P1, P2, distance = d)
                
                if ligne.sens == 'D': G.add_edge(P2, P1, distance = d)
                
        for piste in self.Pistes:
            Pts = piste[-2:]
            G.add_nodes_from(nx.Graph(Pts))
            for i in range(0, len(Pts) - 1):
                P1, P2 = Pts[i], Pts[i+1]
                d = distance(P1, P2)
                G.add_edge(P1, P2, distance = d)
        
        return G
		