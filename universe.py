import primitives
from planet import Planet
from constants import *

import itertools
import math
from datetime import *

def function_u(t):
    # TODO
    return t*0.001*math.pi

def bigBang():
    global planets, big_bang_time

    #T_0 is the 1st perihelion after December 31st, 1899
    #Planets attributes:        Semi-major axis Eccentricity    Radius          Period  T_0                 Name
    planetMercury   = Planet(   0.387,          0.206,          MERCURY_RAD,    87.97,  date(1900,3,3),     "Mercury"   )
    planetVenus     = Planet(   0.723,          0.007,          VENUS_RAD,      224.7,  date(1900,4,1),     "Venus"     )
    planetEarth     = Planet(   1.,             0.017,          EARTH_RAD,      365.26, date(1900,1,1),     "Earth"     )
    planetMars      = Planet(   1.524,          0.093,          MARS_RAD,       686.98, date(1900,3,18),    "Mars"      )
    planetJupiter   = Planet(   5.203,          0.048,          JUPITER_RAD,    4332.6, date(1904,6,1),     "Jupiter"   )
    planetSaturn    = Planet(   9.546,          0.056,          SATURN_RAD,     10759,  date(1915,2,20),    "Saturn"    )
    planetUranus    = Planet(   19.2,           0.047,          URANUS_RAD,     30687,  date(1966,5,20),    "Uranus"    )
    planetNeptune   = Planet(   30.09,          0.009,          NEPTUNE_RAD,    60784,  date(2042,9,15),    "Neptune"   )

    planets = [planetMercury, planetVenus, planetEarth, planetMars, planetJupiter, planetSaturn, planetUranus, planetNeptune]

def processFrame():
    objects = []
    now = datetime.today().date()

    for planet in planets:
        planet.setPos(now)
        objects.append(planet)

    return objects
