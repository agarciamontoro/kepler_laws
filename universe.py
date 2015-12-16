import primitives
from planet import Planet
from constants import *

from datetime import *

import time

import wxGUI

prev_vel = 0


def bigBang():
    """Initialises the planet

    Creates all the planets and stores a timestamp to use it as initial time.
    The list with all the planets and the timestamp are declared as global to
    be used throughout all the module.
    It also cretes two drawable object containing strings: one with the date
    and another one with some help strings. These two objects are also made
    global.
    """
    global planets, before, date_string, help_string

    # T_0 is the 1st perihelion after December 31st, 1899
    # Planets attributes:Axis    Eccentricity           Radius
    #                    Period  T_0                    Name
    #                    Tilt    Node angle             Eccentricity angle

    p_Mercury = Planet(  0.387,  0.206,                 MERCURY_RAD,
                         87.97,  datetime(1900, 3, 3),  "Mercury",
                         7,      47.14,                 75.9)

    p_Venus   = Planet(  0.723,  0.007,                 VENUS_RAD,
                         224.7,  datetime(1900, 4, 1),  "Venus",
                         3.59,   75.78,                 130.15)

    p_Earth   = Planet(  1.,     0.017,                 EARTH_RAD,
                         365.26, datetime(1900, 1, 1),  "Earth",
                         0.,     0.,                    101.22)

    p_Mars    = Planet(  1.524,  0.093,                 MARS_RAD,
                         686.98, datetime(1900, 3, 18), "Mars",
                         1.85,   48.78,                 334.22)

    p_Jupiter = Planet(  5.203,  0.048,                 JUPITER_RAD,
                         4332.6, datetime(1904, 6, 1),  "Jupiter",
                         1.31,   99.44,                 12.72)

    p_Saturn  = Planet(  9.546,  0.056,                 SATURN_RAD,
                         10759,  datetime(1915, 2, 20), "Saturn",
                         2.5,    112.79,                91.09)

    p_Uranus  = Planet(  19.2,   0.047,                 URANUS_RAD,
                         30687,  datetime(1966, 5, 20), "Uranus",
                         0.77,   73.48,                 169.05)

    p_Neptune = Planet(  30.09,  0.009,                 NEPTUNE_RAD,
                         60784,  datetime(2042, 9, 15), "Neptune",
                         1.78,   130.68,                43.83)

    # Global list of planets
    planets = [p_Mercury, p_Venus,  p_Earth,  p_Mars,
               p_Jupiter, p_Saturn, p_Uranus, p_Neptune]

    # Global timestamp
    before = time.time()

    # Global strings
    help_string = primitives.Text(["Z: Decelerate the animation",
                                   "X: Accelerate the animation",
                                   "Q: Quit the program"], 50)
    str_format = "%A, %d %B, %Y"
    date_string = primitives.Text([wxGUI.current_date.strftime(str_format)])


def processFrame(vel=prev_vel):
    """Updates the planets positions.

    Method called from the endless GUI loop. The time is moved to the future
    vel*(seconds from previous frame) days, where vel is an integer controlling
    the velocity of the animation. The position of each planet is then updated
    depending on this date.

    By default, vel is 1; i.e., a second in the real life is one day in the
    animation. The user can change this velocity using Z and X keys.
    """
    global before, prev_vel
    prev_vel = vel

    # Timestamps to control the animation velocity and simulation date
    now = time.time()
    duration = now - before
    before = now

    wxGUI.current_date = wxGUI.current_date + timedelta(days=vel*duration)

    # String update with the current simulation date (be careful with the 1900
    # date restriction)
    if wxGUI.current_date.year < 1900:
        date_string.text = [wxGUI.current_date.isoformat()]
    else:
        date_string.text = [wxGUI.current_date.strftime("%d %B, %Y - %A")]

    objects = [help_string, date_string]

    for planet in planets:
        if wxGUI.draw_planets[planet.name]:
            planet.setPos(wxGUI.current_date)
            objects.append(planet)

    return objects
