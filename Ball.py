#!/usr/bin/env python
# coding=UTF-8

#origin : https://github.com/analca3/TriedroFrenet_Evoluta

steel_gray   = [0.25, 0.25, 0.25]

class Ball:
    color = [1.0, 1.0, 1.0]
    radius = 50
    coord = [0.0,100.0,-50.0]
    Slices = 10
    Stacks = 10
    quadric = None

    def __init__(self, color, radius, coord):
        self.color = color
        self.radius = radius
        self.coord = coord
        self.quadric = gluNewQuadric()

    def draw(self):
        # Initialize the MODELVIEW Matrix
        glMatrixMode(GL_MODELVIEW)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glPushMatrix()

        # Draw the sphere
        glColor3f(*self.color)
        glTranslatef(*self.coords)

        glutSolidSphere(self.radius,self.Slices,self.Stacks)

        glPopMatrix()
        glPushMatrix()

        # Draw the sphere shadow
        glColor3f(*steel_gray)
        glTranslatef(self.coords[0], 0, self.coords[2])
        glRotatef(90, 1.0, 0.0, 0.0)

        gluDisk(self.quadric, 0.0, self.radius*(1+self.coords[1]/380), self.Slices, 1)

        glPopMatrix()
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
