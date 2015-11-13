import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# NEEDS PYTHON2-PILLOW
import PIL.Image

from collections import namedtuple

import math

from constants import *

class Image:
    def __init__(self, img_file_name):
        image = PIL.Image.open(img_file_name)
        self.raw_data = image.tobytes("raw", "RGBA", 0, -1)
        self.width, self.height = image.size

        glEnable( GL_TEXTURE_2D )

        # Texture identifier assignment and binding
        self.id_text = glGenTextures( 1 )
        glBindTexture( GL_TEXTURE_2D, self.id_text )

        # Texture mipmaps
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_GENERATE_MIPMAP, GL_TRUE)

        # Send texels to GPU
        # Params: flag, mipmap level, intern format, width, height, border size, texels format, texel type, texture
        glTexImage2D(GL_TEXTURE_2D,0,3,self.width,self.height,0,GL_RGBA,GL_UNSIGNED_BYTE,self.raw_data)

        # Unbinding
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable( GL_TEXTURE_2D )

    def draw(self):
        window_size = (glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0.0, window_size[0], 0.0, window_size[1], -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        glLoadIdentity()

        glColor3f(1,1,1)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.id_text)

        # Draw a textured quad
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
        glTexCoord2f(0, 1); glVertex3f(0, window_size[1], 0)
        glTexCoord2f(1, 1); glVertex3f(window_size[0], window_size[1], 0)
        glTexCoord2f(1, 0); glVertex3f(window_size[0], 0, 0)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

        glMatrixMode(GL_MODELVIEW)


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
        shadows = [[self.points[i][j] for j in range(3)] for i in range(2)]
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

        # Draw a filled disk
        glBegin(GL_POLYGON)
        for i in range(self.Slices):
            angle = i*2*math.pi/self.Slices
            x = shadow_radius * math.cos(angle) + self.coord[0]
            z = shadow_radius * math.sin(angle) + self.coord[2]

            glVertex3f(x,0.0,z)
        glEnd()

        glutPostRedisplay()
