#!/usr/bin/env python
# coding=UTF-8

#origin : https://github.com/analca3/TriedroFrenet_Evoluta

from __future__ import print_function

import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.constants import GLfloat
from OpenGL.GL.ARB.multisample import GL_MULTISAMPLE_ARB

import sys, time, math, threading

import universe

from constants import *

class GUI:
    # Camera angle
    x_angle_camera = 90.0
    y_angle_camera = 90.0

    # Window attributes
    x_window_pos  = 50
    y_window_pos  = 50
    x_window_size = 1024
    y_window_size = 800

    # Frustum attributes
    frustum_dis_del = 0.1
    frustum_dis_tra = 0.5
    frustum_width = 0.5 * frustum_dis_del
    frustum_scalar_factor = .005

    # Auxiliar variable to mouse management
    _origin = [-1,-1]

    objects = []

    def __init__(self, objects):
        self.objects = objects

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_MULTISAMPLE | GLUT_ALPHA)

        glutInitWindowPosition(0, 0)
        glutInitWindowSize(self.x_window_size, self.y_window_size)
        glutCreateWindow("Mecánica Celeste")

        glEnable(GL_NORMALIZE)
        glEnable(GL_MULTISAMPLE_ARB);
        glEnable(GL_DEPTH_TEST);
        glClearColor( 1.0, 1.0, 1.0, 1.0 ) ;
        glColor3f(0.0,0.0,0.0)

        glutDisplayFunc(self.draw)
        glutIdleFunc(self.draw)
        glutReshapeFunc(self.sizeChange)
        glutKeyboardFunc(self.normalKey)
        glutSpecialFunc(self.specialKey)
        glutMouseFunc(self.mouseClick)
        glutMotionFunc(self.moveMouse)

        # Let the loop finish when glutLeaveMainLoop() is called
        glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS)


    # Fix the projection
    def fixProjection(self):
        ratioYX = float(self.y_window_size) / float(self.x_window_size)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glFrustum(-self.frustum_width, +self.frustum_width, -self.frustum_width*ratioYX, +self.frustum_width*ratioYX, +self.frustum_dis_del, +self.frustum_dis_tra)

        glTranslatef( 0.0,0.0,-0.5*(self.frustum_dis_del+self.frustum_dis_tra))

        glScalef( self.frustum_scalar_factor, self.frustum_scalar_factor, self.frustum_scalar_factor )

    def fixViewportProjection(self):
        glViewport( 0, 0, self.x_window_size, self.y_window_size )
        self.fixProjection()

    def fixCamera(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glRotatef(self.x_angle_camera,1,0,0)
        glRotatef(self.y_angle_camera,0,1,0)

    # Draw axes
    def drawAxes(self):
        axisLong = 1000.0

        # Establish draw mode to line
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );

        # Line width
        glLineWidth( 1.5 );
        # Draw three segment
        glBegin(GL_LINES)

        # Axis X, color red
        glColor3f( 1.0, 0.0, 0.0 )
        glVertex3f( -axisLong, 0.0, 0.0 )
        glVertex3f( +axisLong, 0.0, 0.0 )
        # Axis Y, color green
        glColor3f( 0.0, 1.0, 0.0 )
        glVertex3f( 0.0, -axisLong, 0.0 )
        glVertex3f( 0.0, +axisLong, 0.0 )
        # Axis Z, color blue
        glColor3f( 0.0, 0.0, 1.0 )
        glVertex3f( 0.0, 0.0, -axisLong )
        glVertex3f( 0.0, 0.0, +axisLong )

        glEnd()

    # Draw grid
    def drawGrid(self):
        # Grid long
        long_grid = 1000.0
        gap = 15.0
        num_lines = int( (long_grid*2)/gap )

        # Establish draw mode to lines
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
        # Line width
        glLineWidth( 0.2 );

        # Draw lines
        glBegin(GL_LINES)
        glColor3f(*grid_gray)

        # Draw all the lines
        for i in xrange(num_lines):
            if i != num_lines/2:
                glVertex3f( -long_grid, 0.0, gap*(i-num_lines/2) )
                glVertex3f( +long_grid, 0.0, gap*(i-num_lines/2) )

                glVertex3f( gap*(i-num_lines/2), 0.0, -long_grid )
                glVertex3f( gap*(i-num_lines/2), 0.0, +long_grid )

        glEnd()

    # Distance
    def distance(self,pos1,pos2):
        return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

    # Draw function
    def draw(self):
        glClearColor(steel_blue[0],steel_blue[1],steel_blue[2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.fixViewportProjection()
        self.fixCamera()

        #drawAxes()
        #self.drawGrid()

        self.objects = universe.processFrame()

        # Draw all scene elements
        for element in self.objects:
            element.draw()

        glutSwapBuffers()

    # Normal keys: for change scala and speed
    def normalKey(self,k, x, y):
        if k == '+':
            self.frustum_scalar_factor *= 1.05
        elif k == '-':
            self.frustum_scalar_factor /= 1.05
        elif k == b'r':
            self.x_angle_camera = self.y_angle_camera = 0.0
        elif k == b'q' or k == b'Q' or ord(k) == 27: # Escape
            glutLeaveMainLoop()
        else:
            return
        glutPostRedisplay()

    # Specials keys: for change the camera
    def specialKey(self,k, x, y):
        if k == GLUT_KEY_UP:
            self.x_angle_camera += 5.0
        elif k == GLUT_KEY_DOWN:
            self.x_angle_camera -= 5.0
        elif k == GLUT_KEY_LEFT:
            self.y_angle_camera += 5.0
        elif k == GLUT_KEY_RIGHT:
            self.y_angle_camera -= 5.0
        else:
            return
        glutPostRedisplay()

    # New size of window
    def sizeChange(self,width, height):
        self.x_window_size = width
        self.y_window_size = height

        self.fixViewportProjection()
        glutPostRedisplay()

    # Mouse click event handler
    def mouseClick(self,button,state,x,y):
        da = 5.0
        redisp = False

        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_UP:
                self._origin = [-1,-1]
            else:
                self._origin = [x,y]
        elif button == 3: # Wheel up increases zoom
            self.frustum_scalar_factor *= 1.05;
            redisp = True
        elif button == 4: # Wheel down decreases zoom
            self.frustum_scalar_factor /= 1.05;
            redisp = True
        elif button == 5: # Move the wheel to the left to turn the camera to the left
            self.y_angle_camera -= da
            redisp = True
        elif button == 6: # Move the wheel to the right to turn the camera to the right
            self.y_angle_camera += da
            redisp = True

        if redisp:
            glutPostRedisplay();

    # Move mouse event handler
    def moveMouse(self,x,y):
        if self._origin[0] >= 0 and self._origin[1] >= 0:
            self.x_angle_camera += (y - self._origin[1])*0.25;
            self.y_angle_camera += (x - self._origin[0])*0.25;

            self._origin[0] = x;
            self._origin[1] = y;

            # Redisplay
            glutPostRedisplay();

    def initGUI(self):
        glutMainLoop()
