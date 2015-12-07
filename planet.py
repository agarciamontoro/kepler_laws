import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from primitives import Ball
from constants import *

import math
from operator import add

from datetime import date

def squaredModule(vec):
    return sum([v**2 for v in vec])

def module(vec):
    return math.sqrt(squaredModule(vec))

def vectProduct(u,v):
    w1 = u[1]*v[2] - u[2]*v[1]
    w2 = u[2]*v[0] - u[0]*v[2]
    w3 = u[0]*v[1] - u[1]*v[0]
    return [w1,w2,w3]

class Planet(Ball):
    def __init__(self, semi_major_axis, ecc, radius, period, t_0, name):
        self.semi_major_axis = semi_major_axis
        self.eccentricity = ecc
        self.radius = radius
        self.period = period
        self.t0 = t_0
        self.name = name

        self.setPos(self.t0)

        Ball.__init__(self, steel_red, self.radius, self.GUIcoord)

    def setPos(self, t):
        self.date = t
        delta = (t - self.t0).days

        self.pos, self.ecc_anomaly = self.getPos(delta)

        self.GUIcoord = self.getGUICoords(self.pos)

    # Delta : number of days (can be float) from the 1st perihelion
    # after December 31st, 1899
    def getPos(self,delta):
        current_xi = self.xi(delta)
        phi = self.build_phi(self.eccentricity, current_xi)

        u = self.NR(phi)#math.fmod(self.NR(phi),2*math.pi)

        sin_u = math.sin(u)
        cos_u = math.cos(u)

        x_coord = self.semi_major_axis*(cos_u-self.eccentricity)
        y_coord = self.semi_major_axis*math.sqrt(1-self.eccentricity**2)*sin_u

        return [x_coord, y_coord], u

    # Translates XY coordinates to XZ plane in XYZ (with Z decreasing from the
    # monitor towards you) coordinates
    def getGUICoords(self,pos):
        #Invert Z coordinate to preserve anticlockwise rotation
        return [pos[0], 0.0, -pos[1]]

    # Delta : number of days (can be float) from the 1st perihelion
    # after December 31st, 1899
    def xi(self,delta):
        xi = delta*2*math.pi/self.period
        return xi#math.fmod(xi,2*math.pi)

    def build_phi(self,epsilon,xi):
        def phi(u):
            sin_u = math.sin(u)
            cos_u = math.cos(u)
            return (epsilon * (sin_u-u*cos_u) + xi) / (1 - epsilon*cos_u)

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
            pos, _ = self.getPos(time)
            coords = self.getGUICoords(pos)
            glVertex3f(*coords)
            time += self.period / 50

        glEnd()

        # Draw the planet
        Ball.draw(self)

    def getInfo(self):
        string  = '{name}\t - Position\t: {pos}\n'.format(
                  name=self.name, pos=self.pos)
        string += '\t - Energy\t\t: {energy}\n'.format(
                  energy=self.getEnergy())
        string += '\t - Momentum\t: {momentum}\n'.format(
                  momentum=self.getMomentum())
        string += '\t - Ecc. anomaly\t: {ecc}\n'.format(
                  ecc=self.ecc_anomaly)
        string += '\t - Date\t\t: {date}\n'.format(
                  date=self.date.strftime("%A, %d %B, %Y"))

        return string.expandtabs(10)

    def getVel(self):
        a = self.semi_major_axis
        e = self.eccentricity
        u = self.ecc_anomaly
        p = self.period

        sqrt_mu = 2*math.pi * math.sqrt(a)**3 / p

        du = sqrt_mu / (math.sqrt(a)**3 * (1-e*math.cos(u)))
        dx = [-a*du*math.sin(u), a*du*math.sqrt(1-e**2)*math.cos(u)]

        return dx

    def getEnergy(self):
        x = self.pos
        dx = self.getVel()

        a = self.semi_major_axis
        p = self.period

        mu = 4*math.pi**2 * a**3 / p**2

        return squaredModule(dx)/2 - mu/module(x)

    def getMomentum(self):
        x = self.pos
        dx = self.getVel()

        x.append(0)
        dx.append(0)

        return vectProduct(x,dx)
