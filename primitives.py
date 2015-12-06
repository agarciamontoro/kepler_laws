import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

from constants import *

class Ball:
    Slices = SLICES
    Stacks = STACKS

    def __init__(self, color, radius, coord):
        self.color = color
        self.radius = radius
        self.GUIcoord = [coord[i] for i in range(3)]

    def draw(self):
        # Initialize the MODELVIEW Matrix
        glMatrixMode(GL_MODELVIEW)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glPushMatrix()

        # Draw the sphere
        glColor3f(*self.color)
        glTranslatef(*self.GUIcoord)

        glutSolidSphere(self.radius,self.Slices,self.Stacks)

        # Revert the matrix stack to its previous state
        glPopMatrix()

        glutPostRedisplay()
