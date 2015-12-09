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
    """Squared module

    Args:
        vec: An iterable object whose elements can be exponentiated
    Returns:
        The squared module of vec.
    """
    return sum([v**2 for v in vec])

def module(vec):
    """Module

    Args:
        vec: An iterable object whose elements can be exponentiated
    Returns:
        The module of vec.
    """
    return math.sqrt(squaredModule(vec))

def vectProduct(u,v):
    """Vectorial product

    Args:
        u: A 3D vector; i.e., a list with three numbers
        v: A 3D vector; i.e., a list with three numbers
    Returns:
        The vector u^v; i.e., the vectorial product of u and v
    """
    w1 = u[1]*v[2] - u[2]*v[1]
    w2 = u[2]*v[0] - u[0]*v[2]
    w3 = u[0]*v[1] - u[1]*v[0]
    return [w1,w2,w3]

class Planet(Ball):
    """
    Particle whose motion follows the Kepler laws.
    """

    def __init__(self, semi_major_axis, ecc, radius, period, t_0, name):
        """Constructor

        The constructor receives the planet attributes and set its position
        at the perihelium (whose date is given by t_0 and should be the first
        perihelium after 31st December, 1899).

        Args:
            semi_major_axis: Longitude of the semi-major axis of the planet
                orbit.
            ecc: Eccentricity of the elliptical planet orbit; a float in ]0,1[
            radius: Radius of the planet, for visual purposes only.
            period: Period of the planet, measured in days.
            t_0: Date in which the first perihelium after 31st December, 1899
                was reached.
            name: Name of the planet, for visual purposes only.
        """
        self.semi_major_axis = semi_major_axis
        self.eccentricity = ecc
        self.radius = radius
        self.period = period
        self.t0 = t_0
        self.name = name

        self.setPos(self.t0)

        # Ball constructor, for visual purposes only
        Ball.__init__(self, steel_red, self.radius, self.GUIcoord)

    def _getFloatDays(self,delta):
        """Translates a timedelta object to exact days

        Args:
            delta: A timedelta object
        Returns:
            The exact number of days, including hours, minutes and
            seconds as decimals.
        """
        days, seconds = delta.days, delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return days + hours/24. + minutes/(60.*24.) + seconds/(60.*60.*24.)

    def setPos(self, t):
        """Updates the date and position of the planet.

        Sets the planet position given a date. Its eccentric anomaly -and its
        date- are also stored.

        Args:
            t: Date in which the planet shall be set. It has to be a datetime
                object
        """
        self.date = t
        delta = self._getFloatDays(t-self.t0)
        #print(delta)

        self.pos, self.ecc_anomaly = self.getPos(delta)

        self.GUIcoord = self.getGUICoords(self.pos)

    def getPos(self,delta):
        """Retrieves the position and eccentric anomaly values.

        Retrieves the planet position at the day `delta` after the self.t_0
        date. Along with the plane coordinates -returned as a list- the
        eccentric anomaly is returned.

        Args:
            delta: Number of days after self.t_0 date; i.e., the number of days
                after the first perihelium of the planet after 31st December,
                1899. Integer or float.
        Returns:
            A two-positions list [x,y] giving the XY plane coordinates and the
            eccentric anomaly measured in radians in the interval [0,2*pi[
        """
        current_xi = self.xi(delta)
        phi = self.build_phi(self.eccentricity, current_xi)

        u = self.NR(phi)

        sin_u = math.sin(u)
        cos_u = math.cos(u)

        x_coord = self.semi_major_axis*(cos_u-self.eccentricity)
        y_coord = self.semi_major_axis*math.sqrt(1-self.eccentricity**2)*sin_u

        return [x_coord, y_coord], math.fmod(u,2*math.pi)

    def getGUICoords(self,pos):
        """Coordinates translation. For visual purposes only.

        Translates 2D coordinates in a XY plane to 3D coordinates in a
        XYZ OpenGL space -i.e., X horizontal axis; Y vertical axis; Z 'depth'
        axis, with Z decreasing from the monitor towards you-.

        Args:
            pos: 2D coordinates in a [x,y] form

        Returns:
            The pos coordinates translated to the OpenGL world; i.e., [x,0,-y]
        """

        return [pos[0], 0.0, -pos[1]]

    def xi(self,delta):
        """Calculates mean anomaly in Kepler's equation

        Given a time delta from the self.t_0 date, obtains the rhs of the
        Kepler's equation
                u - e*sin(u) = xi
        i.e., the mean anomaly. See https://en.wikipedia.org/wiki/Mean_anomaly

        Args:
            delta: Number of days after the first perihelium of the planet after 31st December, 1899. Integer or float.

        Returns:
            The mean anomaly of the planet at the given day.
        """

        xi = delta*2*math.pi/self.period
        return xi

    def build_phi(self,epsilon,xi):
        """Returns the phi function given its attributes.

        Builds a phi function depending only on u, given its attributes epsilon
        and xi. The fixed point of this function is the eccentric anomaly we
        need to obtain the planet position.

        Args:
            epsilon: Planet orbit eccentricity
            xi: Planet mean anomaly

        Returns:
            A real function of real variable whose fixed point is interesting.
        """
        def phi(u):
            sin_u = math.sin(u)
            cos_u = math.cos(u)
            return (epsilon * (sin_u-u*cos_u) + xi) / (1 - epsilon*cos_u)

        return phi

    def NR(self,phi,u_0=math.pi,tol=0.00001):
        """Finds the fixed point of phi.

        Algorithm to find the fixed point of the phi function, provided it has
        at least one. Please, be sure that the algorithm converges with the
        given function and first iteration, as this algorithm does not care
        about convergence and can enter an endless loop.

        Args:
            phi: Function whose fixed point we want to obtain.
            u_0: First iteration; defaults to pi, as the convergence
            tol: Accepted error in the approximation; defaults to 0.00001

        Returns:
            Fixed point of phi with a tolerance of tol.
        """
        prev = u_0
        curr = phi(prev)

        while abs(prev - curr) >= tol:
            prev = curr
            curr = phi(prev)

        return curr

    def draw(self):
        """Draws the planet and its orbit

        OpenGL-only function. Override the Ball draw function, as the orbit
        also has to be drawn.
        """
        # Draws orbit
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

        # Draws the planet
        Ball.draw(self)

    def getInfo(self):
        """Retrieves important information of the planet

        Returns a string containing important information of the planet, for
        visual purposes only.

        Returns:
            A pretty-formatted string containing the planet's name, position,
            energy, momentum, eccentric anomaly and date.
        """
        string  = '{name}\t - Position\t: {pos}\n'.format(
                  name=self.name, pos=self.pos)
        string += '\t - Energy\t\t: {energy}\n'.format(
                  energy=self.getEnergy())
        string += '\t - Momentum\t: {momentum}\n'.format(
                  momentum=self.getMomentum())
        string += '\t - Ecc. anomaly\t: {ecc}\n'.format(
                  ecc=self.ecc_anomaly)
        string += '\t - Date\t\t: {date}\n'.format(
                  date=self.date.strftime("%d %B, %Y - %A"))

        return string.expandtabs(10)

    def getVel(self):
        """Retrieves the velocity of the planet.

        Retrieves the current velocity of the planet, using its stored eccentric anomaly.

        Returns:
            A two-positions list [x,y] showing the x- and y- components of the planet velocity.
        """
        a = self.semi_major_axis
        e = self.eccentricity
        u = self.ecc_anomaly
        p = self.period

        sqrt_mu = 2*math.pi * math.sqrt(a)**3 / p

        du = sqrt_mu / (math.sqrt(a)**3 * (1-e*math.cos(u)))
        dx = [-a*du*math.sin(u), a*du*math.sqrt(1-e**2)*math.cos(u)]

        return dx

    def getEnergy(self):
        """Retrieves the energy of the planet.

        Retrieves the current energy of the planet, using its current position
        and velocity.

        Returns:
            The energy value, that should be constant
        """
        x = self.pos
        dx = self.getVel()

        a = self.semi_major_axis
        p = self.period

        mu = 4*math.pi**2 * a**3 / p**2

        return squaredModule(dx)/2 - mu/module(x)

    def getMomentum(self):
        """Retrieves the angular momentum of the planet.

        Retrieves the angular momentum of the planet, using its current
        position and velocity.

        Returns:
            The angular momentum, that should be constant.
        """
        x = self.pos
        dx = self.getVel()

        x.append(0)
        dx.append(0)

        return vectProduct(x,dx)
