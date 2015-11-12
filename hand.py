import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from constants import *
import ball

class Line:
    def __init__(self, points, color):
        self.points = [[points[i][j] for j in range(3)] for i in range(2)]
        self.color = color

    def draw(self):
        # Phalanx
        glColor3f(*self.color)
        glBegin(GL_LINES)
        glVertex3f(*self.points[0])
        glVertex3f(*self.points[1])
        glEnd()

        # Phalanx shadow
        shadows = self.points
        shadows[0][1] = shadows[1][1] = 0
        glColor3f(*steel_gray)
        glBegin(GL_LINES)
        glVertex3f(*shadows[0])
        glVertex3f(*shadows[1])
        glEnd()


class Finger:
    phalanxes = []
    knuckles = []

    def __init__(self, finger, color):
        self.color = color

        for i in range(1,3):
            bone_tip = finger.bone(i).next_joint
            bone_base= finger.bone(i+1).next_joint

            line = Line([bone_tip, bone_base], self.color)
            ball_ = ball.Ball(self.color,finger.bone(i).width/4,bone_tip)

            self.phalanxes.append(line)
            self.knuckles.append(ball_)

        ball_ = ball.Ball(self.color,finger.bone(3).width/4,finger.bone(3).next_joint)
        self.knuckles.append(ball_)

    def draw(self):
        for knuckle in self.knuckles:
            knuckle.draw()
        for phalanx in self.phalanxes:
            phalanx.draw()


class Hand:

    def __init__(self, hand, color):
        self.hand = hand
        self.color = color

        '''
        for finger in hand.fingers:
            draw_finger = Finger(finger,self.color)
            self.fingers.append(draw_finger)
        '''

    def __init__(self):
        self.color = steel_red

    def setHand(self,hand):
        self.hand = hand
        self.fingers = []
        for finger in hand.fingers:
            draw_finger = Finger(finger,self.color)
            self.fingers.append(draw_finger)

    def draw(self):
        for finger in self.fingers:
            finger.draw()
