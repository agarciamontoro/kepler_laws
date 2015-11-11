#!/usr/bin/env python
# coding=UTF-8

#origin : https://github.com/analca3/TriedroFrenet_Evoluta

import math

steel_gray   = [0.25, 0.25, 0.25]

class Ball:
    color = [1.0, 1.0, 1.0]
    radius = 50
    coord = [0.0,100.0,-50.0]
    Slices = 10
    Stacks = 10

    def __init__(self, color, radius, coord):
        self.color = color
        self.radius = radius
        self.coord = coord

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

        # Draw the sphere shadow
        shadow_radius = radius*(1+coords[1]/380)
        glColor3f(steel_gray[0], steel_gray[1], steel_gray[2])

        glBegin(GL_POLYGON)
        for i in range(Slices):
            angle = i*2*math.pi/Slices
            x = shadow_radius * math.cos(angle) + coords[0]
            z = shadow_radius * math.sin(angle) + coords[2]

            glVertex3f(x,0.0,z)
        glEnd()

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
