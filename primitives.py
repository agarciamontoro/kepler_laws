import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from constants import *

OpenGL.ERROR_ON_COPY = True


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

        glutSolidSphere(self.radius, self.Slices, self.Stacks)

        # Revert the matrix stack to its previous state
        glPopMatrix()

        glutPostRedisplay()


class Text:
    def __init__(self, text, vertical_pos=25):
        self.text = text
        self.height = vertical_pos

    def draw(self):
        window_width = glutGet(GLUT_WINDOW_WIDTH)
        window_height = glutGet(GLUT_WINDOW_HEIGHT)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0.0, window_width, 0.0, window_height)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glColor3f(*steel_blue)

        num_lines = 0
        for s in self.text:
            glWindowPos2i(10, window_height - (self.height + 15*num_lines))
            for c in s:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))
            num_lines += 1

        # glWindowPos2i(15, window_height - self.height)
        # glRasterPos2f(15, window_height - self.height)
        # for c in self.text:
        #     glutBitmapCharacter( GLUT_BITMAP_HELVETICA_12 , ord(c))
        # glutBitmapString( GLUT_BITMAP_9_BY_15 , self.text)

        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
