
---------- renderer.py ----------

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from time import strftime
from datetime import datetime
from functions import planTri, isPointInTri


class Renderer:
    def __init__(self, type="2d", is_anim=True):
        """type = "2d" (défaut) ou "3d" """

        if is_anim:
            plt.ion()

        self.type = type
        self.aircrafts_points = []

        self.fig = plt.figure()

        if type == "3d":
            self.ax3d = self.fig.add_subplot(111, projection='3d')
            self.ax3d.scatter(4000, 2200, 130, alpha=0)  # on ajoute des points invisibles pour palier à l'abscence d'option premettant de changer l'échelle en Z
            self.ax3d.scatter(-3500, -2200, 70, alpha=0)

        else:
            self.ax2d = self.fig.add_subplot(111)
            self.date_plot = plt.text(3100, 1700, "")

        plt.axis('equal')


    def show(self):
        plt.show()


    def show3DTerrain(self, Points3D, Lignes, Pistes):
        if self.type == "3d":
            X, Y, Z = [], [], []

            for P in Points3D.values():
                X.append(float(P[0]))
                Y.append(float(P[1]))
                Z.append(float(P[2]))

            self.ax3d.plot_trisurf(X, Y, Z, linewidth=1, cmap=cm.gray, antialiased=True)


    def drawAirportPlan(self, Lignes, Pistes, Triangles=[]):
        def getXY(Points):
            X, Y = [], []
            for pt in Points:
                X.append(pt[0])
                Y.append(pt[1])
            return X, Y

        if self.type == "3d":
            def getZ(X, Y):
                Z = []
                for i in range(len(X)):
                    for T in Triangles.values():
                        if isPointInTri([X[i], Y[i]], T):
                            Plan = planTri(T)
                            Z.append(Plan[0] * X[i] + Plan[1] * Y[i] + Plan[2])
                            break
                return Z

            L3d, R3d = [], []
            for L in Lignes:
                X, Y = getXY(L.pts)
                Z = getZ(X, Y)
                L3d.append([X, Y, Z])

            for R in Pistes:
                X, Y = getXY(R[-2:])
                Z = getZ(X, Y)
                R3d.append([X, Y, Z])

            for L in L3d:
                self.ax3d.plot(L[0], L[1], L[2], linewidth=1, color="black")
            for R in R3d:
                self.ax3d.plot(R[0], R[1], R[2], linewidth=1, color="blue")

        else:  # 2D
            for L in Lignes:
                X, Y = getXY(L.pts)
                self.ax2d.plot(X, Y, linewidth=.5, color="black")

            for R in Pistes:
                X, Y = getXY(R[-2:])
                self.ax2d.plot(X, Y, linewidth=.5, color="blue")


    def drawAircrafts(self, Aircrafts, current_time):
        for point in self.aircrafts_points:  # on libère la mémoire des précédents points
            point.remove()
            del point
        self.aircrafts_points.clear()

        time_str = strftime('%H:%M:%S', datetime.utcfromtimestamp(current_time).timetuple())  # on converti time en string
        self.date_plot.set_text("Heure :" + time_str)

        for a in Aircrafts:
            if a.is_on_map:
                self.aircrafts_points.append(plt.scatter(a.pos[0], a.pos[1], s=25, color='green' if a.type == 'egts' else 'red'))

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
