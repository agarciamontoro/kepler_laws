import primitives
from planet import Planet
from constants import *

import itertools
import math
from datetime import *

def bigBang():
    global planets, big_bang_time, tick

    #T_0 is the 1st perihelion after December 31st, 1899
    #Planets attributes:    Semi-major axis Eccentricity    Radius
    #                       Period          T_0         Name
    p_Mercury   = Planet(   0.387,          0.206,          MERCURY_RAD,
                            87.97,  date(1900,3,3),     "Mercury"   )

    p_Venus     = Planet(   0.723,          0.007,          VENUS_RAD,
                            224.7,  date(1900,4,1),     "Venus"     )

    p_Earth     = Planet(   1.,             0.017,          EARTH_RAD,
                            365.26, date(1900,1,1),     "Earth"     )

    p_Mars      = Planet(   1.524,          0.093,          MARS_RAD,
                            686.98, date(1900,3,18),    "Mars"      )

    p_Jupiter   = Planet(   5.203,          0.048,          JUPITER_RAD,
                            4332.6, date(1904,6,1),     "Jupiter"   )

    p_Saturn    = Planet(   9.546,          0.056,          SATURN_RAD,
                            10759,  date(1915,2,20),    "Saturn"    )

    p_Uranus    = Planet(   19.2,           0.047,          URANUS_RAD,
                            30687,  date(1966,5,20),    "Uranus"    )

    p_Neptune   = Planet(   30.09,          0.009,          NEPTUNE_RAD,
                            60784,  date(2042,9,15),    "Neptune"   )

    planets = [p_Mercury, p_Venus,  p_Earth,  p_Mars,
               p_Jupiter, p_Saturn, p_Uranus, p_Neptune]
    tick = 0

def processFrame():
    global tick
    tick += 1
    objects = []

    today = datetime.today().date()
    now = today + timedelta(days=tick)

    for planet in planets:
        planet.setPos(now)
        if planet.name == "Venus":
            planet.printInfo()
        objects.append(planet)

    return objects
