import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from constants import *
import primitives

class Finger:
    def __init__(self, finger, color):
        self.color = color
        self.phalanxes = []
        self.knuckles = []

        for i in range(1,3):
            bone_tip = finger.bone(i).next_joint
            bone_base= finger.bone(i+1).next_joint

            line = primitives.Line([bone_tip, bone_base], self.color)
            ball_ = primitives.Ball(self.color,finger.bone(i).width/4,bone_tip)

            self.phalanxes.append(line)
            self.knuckles.append(ball_)

        ball_ = primitives.Ball(self.color,finger.bone(3).width/4,finger.bone(3).next_joint)
        self.knuckles.append(ball_)

    def draw(self):
        for knuckle in self.knuckles:
            knuckle.draw()
        for phalanx in self.phalanxes:
            phalanx.draw()


class Hand:
    def __init__(self, hand, color):
        self.color = color
        self.setHand(hand)

    def __init__(self):
        self.hand = None
        self.color = steel_red
        self.fingers = []

    def setHand(self,hand):
        self.fingers = []

        for finger in hand.fingers:
            draw_finger = Finger(finger,self.color)
            self.fingers.append(draw_finger)

    def draw(self):
        for finger in self.fingers:
            finger.draw()
