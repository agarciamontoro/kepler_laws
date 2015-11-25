from primitives import Line
from billiardBall import *

import math

# Distance
def distance(pos1,pos2):
    return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

class ForceLine(Line):
    def __init__(self, ball, pos = [0.0, 0.0, 0.0]):
        self.points = [ball.coord, pos]
        self.setIntensity()
        self.color = [self.intensity, 1.0, 1.0]

        Line.__init__(self.points, self.color)

    def setIntensity(self):
        dist = distance(*self.points)/50.0
        self.intensity = 1.0 if dist > 1.0 else dist
        self.color[0] = self.intensity

    def setBall(self, ball):
        self.points[0] = ball.coord
        self.setIntensity()

    def setOrigin(self, pos):
        self.points[1] = pos
        self.setIntensity()

    def getForce(self):
        dir_vector = self.getDirVector()
        return [self.intensity * dir_vector[i] for i in range(3)]
