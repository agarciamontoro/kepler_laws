from primitives import Ball
from constants import *

import math
from operator import add

# Distance
def distance(pos1,pos2):
    return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

def toPolar(pos):
    module = math.sqrt(sum([pos[i]**2 for i in range(2)]))
    angle = math.atan2(pos[1], pos[0])
    return [module,angle]

class Planet(Ball):
    def __init__(self, semi_major_axis, eccentricity, u, radius, period, name):
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.u = u
        self.radius = radius
        self.name = name
        self.t0 = 0.
        self.period = period
        self.setPos(self.t0)

        Ball.__init__(self, steel_red, self.radius, self.coord)

    def setPos(self, t):
        current_xi = self.xi(t)
        phi = self.build_phi(self.eccentricity, current_xi)

        u = self.NR(phi)

        x_coord = self.semi_major_axis*math.cos(u)-self.eccentricity
        y_coord = self.semi_major_axis*math.sqrt(1-self.eccentricity**2)*math.sin(u)

        self.coord = [x_coord, 0.0, y_coord]

        print(t,u,self.coord)

    def xi(self,t):
        xi = (2*math.pi/self.period)*(t-self.t0)
        return xi

    def build_phi(self,epsilon,xi):
        def phi(u):
            return (epsilon*(math.sin(u)-u*math.cos(u))+xi)/(1-epsilon*math.cos(u))

        return phi

    def NR(self,phi,u_0=math.pi,tol=0.00001):
        prev = u_0
        curr = phi(prev)

        while abs(prev - curr) >= tol:
            prev = curr
            curr = phi(prev)

        return curr
