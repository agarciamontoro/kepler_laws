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
    frustum_width = 0.5 * frustum_dis_del
    frustum_scalar_factor = .005



    # Objects to draw
    Objects = []

    # To the color desired, the radius of the sphere and his position
    def drawSphere(color, radio, coords):
        # Initialize the MODELVIEW Matrix
        glMatrixMode(GL_MODELVIEW)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glPushMatrix()

        # Draw the sphere
        glColor3f(color[0], color[1], color[2])
        glTranslatef(coords[0], coords[1], coords[2])

        glutSolidSphere(radio,Slices,Stacks)

        glPopMatrix()
        glPushMatrix()

        # Draw the sphere shadow
        glColor3f(steel_gray[0], steel_gray[1], steel_gray[2])
        glTranslatef(coords[0], 0, coords[2])
        glRotatef(90, 1.0, 0.0, 0.0)

        gluDisk(quadric, 0.0, radio*(1+coords[1]/380), Slices, 1)

        glPopMatrix()
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

# Draw fingers
def drawFingerBones(color, finger):
    # First check if the fingers data are valid
    if finger.is_valid:
        # For each finger junctions and bones
        for i in range(1,3):
            bone_tip = finger.bone(i).next_joint
            bone_base= finger.bone(i+1).next_joint

            # Phalanx
            glColor3f(color[0], color[1], color[2])
            glBegin(GL_LINES)
            glVertex3f(bone_tip[0],bone_tip[1],bone_tip[2])
            glVertex3f(bone_base[0],bone_base[1],bone_base[2])
            glEnd()

            # Phalanx shadow
            glColor3f(steel_gray[0], steel_gray[1], steel_gray[2])
            glBegin(GL_LINES)
            glVertex3f(bone_tip[0],0,bone_tip[2])
            glVertex3f(bone_base[0],0,bone_base[2])
            glEnd()

            # Draw distal, intermediate phalanges
            drawSphere(color,finger.bone(i).width/4,bone_tip)
        # Draw knuckles
        drawSphere(color,finger.bone(3).width/4,finger.bone(3).next_joint)

def drawHand(color, hands):
    for i,hand in enumerate(hands):
        if redraw[i]:
            #drawSphere(colors[i], 30, hand.palm_position)
            # For each finger draw all its elements
            for finger in hand.fingers:
                if distance(finger.tip_position, sphere_pos) < sphere_radius*1.5:
                    touch[i] = True
                    color = colors[i]

                drawFingerBones(colors[i],finger)

# Fix the projection
def fixProjection():
    ratioYX = float(y_window_size) / float(x_window_size)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glFrustum(-frustum_width, +frustum_width, -frustum_width*ratioYX, +frustum_width*ratioYX, +frustum_dis_del, +frustum_dis_tra)

    glTranslatef( 0.0,0.0,-0.5*(frustum_dis_del+frustum_dis_tra))

    glScalef( frustum_scalar_factor, frustum_scalar_factor, frustum_scalar_factor )

def fixViewportProjection():
    glViewport( 0, 0, x_window_size, y_window_size )
    fixProjection()

def fixCamera():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glRotatef(x_angle_camera,1,0,0)
    glRotatef(y_angle_camera,0,1,0)

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

# Draw all the objects of the scene
def drawObjects():
    redraw, hands = LeapListener.getHands()

    # Sphere attributes
    sphere_pos = [0.0,100.0,-50.0]
    sphere_radius = 50

    if redraw[0] or redraw[1]:
        colors = [steel_red, steel_yellow]
        touch = [False,False]

        # For each hand, draw all its elements
        for i,hand in enumerate(hands):
            if redraw[i]:
                #drawSphere(colors[i], 30, hand.palm_position)
                # For each finger draw all its elements
                for finger in hand.fingers:
                    if distance(finger.tip_position, sphere_pos) < sphere_radius*1.5:
                        touch[i] = True
                        color = colors[i]

                    drawFingerBones(colors[i],finger)

        # Control logic for the interaction with the sphere
        if touch[0] and touch[1]:
            color = [(colors[0][j] + colors[1][j])/2 for j in range(3)]
        elif not touch[0] and not touch[1]:
            color = steel_white
        elif touch[0] and not touch[1]:
            color = colors[1]
        elif not touch[0] and touch[1]:
            color = colors[0]

        drawSphere(color, sphere_radius, sphere_pos)
    else:
        drawSphere(steel_white, sphere_radius, sphere_pos)

def load_image(filename, scale = 1):
    try: image = pygame.image.load(filename)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert()

    image = pygame.transform.scale(image, (WIDTH / scale, HEIGHT / scale))
    image = image.convert()
    return image

def showTutorialImage(num_image):
    actual_image = load_image(tutorial_images[num_image])
    screen.blit(actual_image, (0,0))
    pygame.display.flip()

# Draw function
def draw():
    global tutorial_images, screen
    glClearColor(steel_blue[0], steel_blue[1], steel_blue[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    fixViewportProjection()
    fixCamera()

    #drawAxes()
    drawGrid()

    if not LeapListener.tutorialFinished():
        num_image = LeapListener.tutorialState()
        showTutorialImage(num_image)
    else:
        pygame.display.quit()
        drawObjects()

    glutSwapBuffers()

# Normal keys: for change scala and speed
def normalKey(k, x, y):
    global frustum_scalar_factor, currentVertex, speed, x_angle_camera, y_angle_camera

    if k == '+':
        frustum_scalar_factor *= 1.05
    elif k == '-':
        frustum_scalar_factor /= 1.05
    elif k == b'r':
        x_angle_camera = y_angle_camera = 0.0
    elif k == b'q' or k == b'Q' or ord(k) == 27: # Escape
        sys.exit(0)
    else:
        return
    glutPostRedisplay()

# Specials keys: for change the camera
def specialKey(k, x, y):
    global x_angle_camera, y_angle_camera

    if k == GLUT_KEY_UP:
        x_angle_camera += 5.0
    elif k == GLUT_KEY_DOWN:
        x_angle_camera -= 5.0
    elif k == GLUT_KEY_LEFT:
        y_angle_camera += 5.0
    elif k == GLUT_KEY_RIGHT:
        y_angle_camera -= 5.0
    else:
        return
    glutPostRedisplay()

# New size of window
def sizeChange(width, height):
    global x_window_size,y_window_size

    x_window_size = width
    y_window_size = height

    fixViewportProjection()
    glutPostRedisplay()

origin = [-1,-1]
# Mouse click event handler
def mouseClick(button,state,x,y):
    da = 5.0
    redisp = False
    global frustum_scalar_factor,origin,x_angle_camera,y_angle_camera

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_UP:
            origin = [-1,-1]
        else:
            origin = [x,y]
    elif button == 3: # Wheel up increases zoom
        frustum_scalar_factor *= 1.05;
        redisp = True
    elif button == 4: # Wheel down decreases zoom
        frustum_scalar_factor /= 1.05;
        redisp = True
    elif button == 5: # Move the wheel to the left to turn the camera to the left
        y_angle_camera -= da
        redisp = True
    elif button == 6: # Move the wheel to the right to turn the camera to the right
        y_angle_camera += da
        redisp = True

    if redisp:
        glutPostRedisplay();

# Move mouse event handler
def moveMouse(x,y):
    global x_angle_camera,y_angle_camera, origin

    if origin[0] >= 0 and origin[1] >= 0:
        x_angle_camera += (y - origin[1])*0.25;
        y_angle_camera += (x - origin[0])*0.25;

        origin[0] = x;
        origin[1] = y;

        # Redisplay
        glutPostRedisplay();

def initGUI(argumentos, listener):
    global LeapListener, quadric, screen
    LeapListener = listener

    glutInit(argumentos)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_MULTISAMPLE | GLUT_ALPHA)

    glutInitWindowPosition(0, 0)
    glutInitWindowSize(x_window_size, y_window_size)
    glutCreateWindow("Leap Motion project")

    glEnable(GL_NORMALIZE)
    glEnable(GL_MULTISAMPLE_ARB);
    glEnable(GL_DEPTH_TEST);
    glClearColor( 1.0, 1.0, 1.0, 1.0 ) ;
    glColor3f(0.0,0.0,0.0)

    pygame.display.set_caption("Leap Motion tutorial")

    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutReshapeFunc(sizeChange)
    glutKeyboardFunc(normalKey)
    glutSpecialFunc(specialKey)
    glutMouseFunc(mouseClick)
    glutMotionFunc(moveMouse)
    quadric = gluNewQuadric()
    glutMainLoop()
