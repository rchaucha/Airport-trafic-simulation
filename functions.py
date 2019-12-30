
---------- functions.py ----------

import numpy as np
import networkx as nx
from math import sqrt


def distance(A, B):
    return sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)
    


def planTri(Triangle):
    """Calule le plan déterminé par le triangle [P1, P2, P3] de forme ax + by + c = z
    
    On résout le système suivant:
    (x1 y1 1) (a) (z1)
    (x2 y2 1)x(b)=(z2)
    (x3 y3 1) (c) (z3)
        T          Z
    """
    
    T = np.array([point[:2] + [1] for point in Triangle]).astype(float) 
    Z = np.array([point[2] for point in Triangle]).astype(float)
    
    return np.linalg.solve(T, Z)
    
    
    
def aire(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)
    
    
    
def isPointInTri(P, Triangle):
    """P=[x,y], Triangle = [[x1,y1],[x2,y2],[x3,y3]]"""
    
    A = np.array(Triangle[0]).astype(float)
    B = np.array(Triangle[1]).astype(float)
    C = np.array(Triangle[2]).astype(float)
    
    [Ax, Ay, Az] = A
    [Bx, By, Bz] = B
    [Cx, Cy, Cz] = C
    [x, y] = P
    
    A = aire(Ax, Ay, Bx, By, Cx, Cy)
    A1 = aire(x, y, Bx, By, Cx, Cy) 
    A2 = aire(Ax, Ay, x, y, Cx, Cy) 
    A3 = aire(Ax, Ay, Bx, By, x, y) 
      
    return A == A1 + A2 + A3
