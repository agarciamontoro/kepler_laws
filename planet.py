import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from primitives import Ball
from constants import *

import math
from operator import add

class Planet(Ball):
    def __init__(self, semi_major_axis, eccentricity, radius, period, t_0, name):
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.radius = radius
        self.name = name
        self.t0 = t_0
        self.period = period
        self.setPos(self.t0)

        Ball.__init__(self, steel_red, self.radius, self.coord)

    def setPos(self, t):
        self.coord = self.getCoords(t)
        print(t,self.coord)

    def getCoords(self,t):
        current_xi = self.xi(t)
        phi = self.build_phi(self.eccentricity, current_xi)

        u = self.NR(phi)

        x_coord = self.semi_major_axis*math.cos(u)-self.eccentricity
        y_coord = self.semi_major_axis*math.sqrt(1-self.eccentricity**2)*math.sin(u)

        return [x_coord, 0.0, y_coord]


    def xi(self,t):
        return (2*math.pi/self.period)*(t-self.t0)

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

    def draw(self):
        # Draw the orbit
        glColor3f(*steel_blue)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_POLYGON)
        time = 0
        while time <= self.period:
            coords = self.getCoords(time)
            glVertex3f(*coords)
            time += self.period / 50
        glEnd()

        # Draw the planet
        Ball.draw(self)
