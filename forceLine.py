from primitives import Line
from billiardBall import *

import math

# Distance
def distance(pos1,pos2):
    return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

class ForceLine(Line):
    def __init__(ball, finger):
        self.points = [ball.coord, finger.tip_position]
        self.setIntensity()

        Line.__init__(points, [self.intensity, 0.0, 0.0])

    def setIntensity(self):
        dist = distance(*self.points)/50.0
        self.intensity = 1.0 if dist > 1.0 else dist

    def setBall(self, ball):
        self.points[0] = ball.coord

    def setFinger(self, finger):
        self.points[1] = finger.tip_position
