#!/usr/bin/env python
# coding=UTF-8

#origin : https://github.com/analca3/TriedroFrenet_Evoluta

from __future__ import print_functioni

import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys, time

import math

import pygame

from OpenGL.constants import GLfloat
from OpenGL.GL.ARB.multisample import GL_MULTISAMPLE_ARB

import LeapDriver

import colors

class GUI:
    # Camera angle
    x_angle_camera = 50.0
    y_angle_camera = 0.0

    # Window attributes
    x_window_pos  = 50
    y_window_pos  = 50
    x_window_size = 1024
    y_window_size = 800

    # Frustum attributes
    frustum_dis_del = 0.1
    frustum_dis_tra = 10.0
    frustum_width = 0.5 * self.frustum_dis_del
    frustum_scalar_factor = .005

    leap_listener

    # Auxiliar variable to mouse management
    _origin = [-1,-1]

    def __init__(leap_listener,objects):
        self.leap_listener = leap_listener
        self.objects = objects
        initGUI(sys.argv)

    def addObject(item):
        self.objects.append(item)

    # Fix the projection
    def fixProjection():
        ratioYX = float(self.y_window_size) / float(self.x_window_size)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glFrustum(-self.frustum_width, +self.frustum_width, -self.frustum_width*ratioYX, +self.frustum_width*ratioYX, +self.frustum_dis_del, +self.frustum_dis_tra)

        glTranslatef( 0.0,0.0,-0.5*(self.frustum_dis_del+self.frustum_dis_tra))

        glScalef( self.frustum_scalar_factor, self.frustum_scalar_factor, self.frustum_scalar_factor )

    def fixViewportProjection():
        glViewport( 0, 0, self.x_window_size, self.y_window_size )
        fixProjection()

    def fixCamera():
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glRotatef(self.x_angle_camera,1,0,0)
        glRotatef(self.y_angle_camera,0,1,0)

    # Draw axes
    def drawAxes():
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
    def drawGrid():
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
        glColor3f(grid_gray[0], grid_gray[1], grid_gray[2])

        # Draw all the lines
        for i in xrange(num_lines):
            if i != num_lines/2:
                glVertex3f( -long_grid, 0.0, gap*(i-num_lines/2) )
                glVertex3f( +long_grid, 0.0, gap*(i-num_lines/2) )

                glVertex3f( gap*(i-num_lines/2), 0.0, -long_grid )
                glVertex3f( gap*(i-num_lines/2), 0.0, +long_grid )

        glEnd()

    # Distance
    def distance(pos1,pos2):
        return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

    # Draw function
    def draw():
        glClearColor(*colors.steel_blue, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        fixViewportProjection()
        fixCamera()

        #drawAxes()
        drawGrid()

        # Draw all scene elements
        for element in self.objects:
            element.draw()

        glutSwapBuffers()

    # Normal keys: for change scala and speed
    def normalKey(k, x, y):
        self.frustum_scalar_factor, currentVertex, speed, self.x_angle_camera, self.y_angle_camera

        if k == '+':
            self.frustum_scalar_factor *= 1.05
        elif k == '-':
            self.frustum_scalar_factor /= 1.05
        elif k == b'r':
            self.x_angle_camera = self.y_angle_camera = 0.0
        elif k == b'q' or k == b'Q' or ord(k) == 27: # Escape
            sys.exit(0)
        else:
            return
        glutPostRedisplay()

    # Specials keys: for change the camera
    def specialKey(k, x, y):
        self.x_angle_camera, self.y_angle_camera

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
    def sizeChange(width, height):
        self.x_window_size,self.y_window_size

        self.x_window_size = width
        self.y_window_size = height

        fixViewportProjection()
        glutPostRedisplay()

    # Mouse click event handler
    def mouseClick(button,state,x,y):
        da = 5.0
        redisp = False
        self.frustum_scalar_factor,self._origin,self.x_angle_camera,self.y_angle_camera

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
    def moveMouse(x,y):
        self.x_angle_camera,self.y_angle_camera, self._origin

        if self._origin[0] >= 0 and self._origin[1] >= 0:
            self.x_angle_camera += (y - self._origin[1])*0.25;
            self.y_angle_camera += (x - self._origin[0])*0.25;

            self._origin[0] = x;
            self._origin[1] = y;

            # Redisplay
            glutPostRedisplay();

    def initGUI(arguments):
        glutInit(arguments)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_MULTISAMPLE | GLUT_ALPHA)

        glutInitWindowPosition(0, 0)
        glutInitWindowSize(self.x_window_size, self.y_window_size)
        glutCreateWindow("Leap Motion project")

        glEnable(GL_NORMALIZE)
        glEnable(GL_MULTISAMPLE_ARB);
        glEnable(GL_DEPTH_TEST);
        glClearColor( 1.0, 1.0, 1.0, 1.0 ) ;
        glColor3f(0.0,0.0,0.0)

        glutDisplayFunc(draw)
        glutIdleFunc(draw)
        glutReshapeFunc(sizeChange)
        glutKeyboardFunc(normalKey)
        glutSpecialFunc(specialKey)
        glutMouseFunc(mouseClick)
        glutMotionFunc(moveMouse)
        glutMainLoop()
