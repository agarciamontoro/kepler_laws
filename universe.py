import primitives
from planet import Planet
from constants import *

import itertools
import math
import time

def function_u(t):
    # TODO
    return t*0.001*math.pi

def bigBang():
    global planets, big_bang_time

    #T_0 is measured in days from January 1st, 1900
    #Planets attributes:        Semi-major axis Eccentricity    Radius          Period  T_0     Name
    planetMercury   = Planet(   0.387,          0.206,          MERCURY_RAD,    87.97,  61,     "Mercury")
    planetVenus     = Planet(   0.723,          0.007,          VENUS_RAD,      224.7,  90,     "Venus")
    planetEarth     = Planet(   1.,             0.017,          EARTH_RAD,      365.26, 0,      "Earth")
    planetMars      = Planet(   1.524,          0.093,          MARS_RAD,       686.98, 76,     "Mars")
    planetJupiter   = Planet(   5.203,          0.048,          JUPITER_RAD,    4332.6, 1612,   "Jupiter")
    planetSaturn    = Planet(   9.546,          0.056,          SATURN_RAD,     10759,  5528,   "Saturn")
    planetUranus    = Planet(   19.2,           0.047,          URANUS_RAD,     30687,  24245,  "Uranus")
    planetNeptune   = Planet(   30.09,          0.009,          NEPTUNE_RAD,    60784,  52122,  "Neptune")

    planets = [planetMercury, planetVenus, planetEarth, planetMars, planetJupiter, planetSaturn, planetUranus, planetNeptune]

    big_bang_time = time.time()

def processFrame():
    global big_bang_time
    instant = time.time() - big_bang_time

    objects = []

    for planet in planets:
        planet.setPos(instant)
        objects.append(planet)

    return objects
