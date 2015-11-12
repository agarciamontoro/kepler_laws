import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

from constants import *

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

class Ball:
    Slices = SLICES
    Stacks = STACKS

    def __init__(self, color, radius, coord):
        self.color = color
        self.radius = radius
        self.coord = [coord[i] for i in range(3)]

    def draw(self):
        # Initialize the MODELVIEW Matrix
        glMatrixMode(GL_MODELVIEW)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glPushMatrix()

        # Draw the sphere
        glColor3f(*self.color)
        glTranslatef(*self.coord)

        glutSolidSphere(self.radius,self.Slices,self.Stacks)

        # Revert the matrix stack to its previous state
        glPopMatrix()

        # Draw the sphere shadow
        shadow_radius = self.radius*(1+self.coord[1]/380)
        glColor3f(*steel_gray)

        glBegin(GL_POLYGON)
        for i in range(self.Slices):
            angle = i*2*math.pi/self.Slices
            x = shadow_radius * math.cos(angle) + self.coord[0]
            z = shadow_radius * math.sin(angle) + self.coord[2]

            glVertex3f(x,0.0,z)
        glEnd()

        glutPostRedisplay()
