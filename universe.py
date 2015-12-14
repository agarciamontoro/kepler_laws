import primitives
from planet import Planet
from constants import *

import itertools
import math
from datetime import *

import time

from wxGUI import draw_planets

def bigBang():
    """Initialises the planet

    Creates all the planets, stores a timestamp to use it as initial time
    and stores the date in which the program is being executed. The list with
    all the planets, the timestamp and the date are declared as global to be
    used throughout all the module.
    It also cretes two drawable object containing strings: one with the date
    and another one with some help strings. These two objects are also made
    global.
    """
    global planets, before, today, date_string, help_string

    #T_0 is the 1st perihelion after December 31st, 1899
    #Planets attributes: Axis    Eccentricity           Radius
    #                    Period  T_0                    Name

    p_Mercury = Planet(  0.387,  0.206,                 MERCURY_RAD,
                         87.97,  datetime(1900,3,3),    "Mercury"   )

    p_Venus   = Planet(  0.723,  0.007,                 VENUS_RAD,
                         224.7,  datetime(1900,4,1),    "Venus"     )

    p_Earth   = Planet(  1.,     0.017,                 EARTH_RAD,
                         365.26, datetime(1900,1,1),    "Earth"     )

    p_Mars    = Planet(  1.524,  0.093,                 MARS_RAD,
                         686.98, datetime(1900,3,18),   "Mars"      )

    p_Jupiter = Planet(  5.203,  0.048,                 JUPITER_RAD,
                         4332.6, datetime(1904,6,1),    "Jupiter"   )

    p_Saturn  = Planet(  9.546,  0.056,                 SATURN_RAD,
                         10759,  datetime(1915,2,20),   "Saturn"    )

    p_Uranus  = Planet(  19.2,   0.047,                 URANUS_RAD,
                         30687,  datetime(1966,5,20),   "Uranus"    )

    p_Neptune = Planet(  30.09,  0.009,                 NEPTUNE_RAD,
                         60784,  datetime(2042,9,15),   "Neptune"   )

    # Global list of planets
    planets = [p_Mercury, p_Venus,  p_Earth,  p_Mars,
               p_Jupiter, p_Saturn, p_Uranus, p_Neptune]

    # Global timestamp and date
    before = time.time()
    today = datetime.today()

    # Global strings
    help_string = primitives.Text(["Z: Decelerate the animation",
                                   "X: Accelerate the animation",
                                   "Q: Quit the program"],50)
    date_string = primitives.Text([today.strftime("%A, %d %B, %Y")])

def processFrame(vel):
    """Updates the planets positions.

    Method called from the endless GUI loop. The time is moved to the future
    vel*(seconds from previous frame) days, where vel is an integer controlling
    the velocity of the animation. The position of each planet is then updated
    depending on this date.

    By default, vel is 1; i.e., a second in the real life is one day in the
    animation. The user can change this velocity using Z and X keys.
    """
    global before, today

    # Timestamps to control the animation velocity and simulation date
    now = time.time()
    duration = now - before
    before = now

    today = today + timedelta(days=vel*duration)

    # String update with the current simulation date
    date_string.text = [today.strftime("%d %B, %Y - %A")]

    objects =  [help_string, date_string]

    for planet in planets:
        if draw_planets[planet.name]:
            planet.setPos(today)
            print(planet.getInfo())
            objects.append(planet)

    return objects
