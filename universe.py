import primitives
from planet import Planet
from constants import *

import itertools, math

def function_u(t):
    # TODO
    return t*0.001*math.pi

def bigBang():
    global planets, time

    p_planetMercury = Planet(0.387, 0.206, function_u, BALL_RADIUS, 87.97, "Mercury")
    p_planetVenus = Planet(0.723, 0.007, function_u, BALL_RADIUS, 224.7, "Venus")
    p_planetEarth = Planet(1., 0.017, function_u, BALL_RADIUS, 365.26, "Earth")
    p_planetMars = Planet(1.524, 0.093, function_u, BALL_RADIUS, 686.98, "Mars")
    p_planetJupiter = Planet(5.203, 0.048, function_u, BALL_RADIUS, 4332.6, "Jupiter")
    p_planetSaturn = Planet(9.546, 0.056, function_u, BALL_RADIUS, 10759, "Saturn")
    p_planetUranus = Planet(19.2, 0.047, function_u, BALL_RADIUS, 30687, "Uranus")
    p_planetNeptune = Planet(30.09, 0.009, function_u, BALL_RADIUS, 60784, "Neptune")

    planets = [planetMercury, planetVenus, planetEarth, planetMars, planetJupiter, planetSaturn, planetUranus, planetNeptune]

    time = 0

def processFrame():
    global time
    time = time + 1

    objects = []

    for planet in planets:
        planet.setPos(time)
        objects.append(planet)

    return objects
