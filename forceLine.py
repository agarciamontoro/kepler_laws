from primitives import Line
from billiardBall import *

import math

# Distance
def distance(pos1,pos2):
    return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

class ForceLine(Line):
    def __init__(self, ball, pos = [0.0, 0.0, 0.0]):
        self.points = [ball.coord, pos]
        self.intensity = self.getIntensity()
        self.color = [self.intensity, 1.0, 0.0]

        Line.__init__(self, self.points, self.color)

    def getIntensity(self):
        dist = distance(*self.points)/200.0
        intensity = 1.0 if dist > 1.0 else dist
        return intensity

    def setColor(self):
        self.intensity = self.getIntensity()
        self.color[0] = self.intensity

    def setBall(self, ball):
        self.points[0] = ball.coord
        self.setColor()

    def setOrigin(self, pos):
        self.points[1] = pos
        self.setColor()

    def getForce(self):
        dir_vector = self.getDirVector()
        force = [FORCE_CONSTANT * self.intensity * dir_vector[i] for i in range(3)]
        force[1] = 0.0
        return force
