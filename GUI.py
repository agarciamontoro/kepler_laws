#!/usr/bin/env python
# coding=UTF-8

#Origen : https://github.com/analca3/TriedroFrenet_Evoluta

from __future__ import print_function

import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys, time

import math

from OpenGL.constants import GLfloat
from OpenGL.GL.ARB.multisample import GL_MULTISAMPLE_ARB

import LeapDriver

camara_angulo_x = 25.0
camara_angulo_y = 25.0

ventana_pos_x  = 50
ventana_pos_y  = 50
ventana_tam_x  = 1024
ventana_tam_y  = 800

frustum_dis_del = 0.1
frustum_dis_tra = 10.0
frustum_ancho = 0.5 * frustum_dis_del

frustum_factor_escala = .005
Slices = 10
Stacks = 10

quadric = None

# Obtiene el angulo que tiene pos respecto los diferentes ejes
def obtainAngle(pos):
    r = 1
    tita = 360*math.atan(pos[0]/pos[2])/(2.0*math.pi)
    phi = 360*math.acos(pos[1]/r)/(2.0*math.pi)
    print(tita,phi)

    return [tita, phi]

# A partir del color deseado, el radio de la esfera y su posición

def dibujarEsfera(color, radio, coords):
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()

    glColor3f(color[0], color[1], color[2])
    glTranslatef(coords[0],coords[1],coords[2])

    glutSolidSphere(radio,Slices,Stacks)

    glPopMatrix()


def dibujarFalanges(color, finger):
    if finger.is_valid:
        glColor3f(color[0], color[1], color[2])
        for i in range(1,3):
            bone_tip = finger.bone(i).next_joint
            bone_base= finger.bone(i+1).next_joint

            glBegin(GL_LINES)
            glVertex3f(bone_tip[0],bone_tip[1],bone_tip[2])
            glVertex3f(bone_base[0],bone_base[1],bone_base[2])
            glEnd()

            dibujarEsfera(color,finger.bone(i).width/4,bone_tip)

        dibujarEsfera(color,finger.bone(3).width/4,finger.bone(3).next_joint)

def fijarProyeccion():
    ratioYX = float(ventana_tam_y) / float(ventana_tam_x)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glFrustum(-frustum_ancho, +frustum_ancho, -frustum_ancho*ratioYX, +frustum_ancho*ratioYX, +frustum_dis_del, +frustum_dis_tra)

    glTranslatef( 0.0,0.0,-0.5*(frustum_dis_del+frustum_dis_tra))

    glScalef( frustum_factor_escala, frustum_factor_escala,  frustum_factor_escala )


def fijarViewportProyeccion():
    glViewport( 0, 0, ventana_tam_x, ventana_tam_y )
    fijarProyeccion()

def fijarCamara():

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glRotatef(camara_angulo_x,1,0,0)
    glRotatef(camara_angulo_y,0,1,0)

def dibujarEjes():

    long_ejes = 1000.0

    # establecer modo de dibujo a lineas (podría estar en puntos)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );

    # Ancho de línea
    glLineWidth( 1.5 );
    # dibujar tres segmentos
    glBegin(GL_LINES)

    # eje X, color rojo
    glColor3f( 1.0, 0.0, 0.0 )
    glVertex3f( -long_ejes, 0.0, 0.0 )
    glVertex3f( +long_ejes, 0.0, 0.0 )
    # eje Y, color verde
    glColor3f( 0.0, 1.0, 0.0 )
    glVertex3f( 0.0, -long_ejes, 0.0 )
    glVertex3f( 0.0, +long_ejes, 0.0 )
    # eje Z, color azul
    glColor3f( 0.0, 0.0, 1.0 )
    glVertex3f( 0.0, 0.0, -long_ejes )
    glVertex3f( 0.0, 0.0, +long_ejes )

    glEnd()

def dibujarRejilla():
    long_grid = 1000.0
    gap = 50.0

    num_lines = int( (long_grid*2)/gap )

    # establecer modo de dibujo a lineas (podría estar en puntos)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
    # Ancho de línea
    glLineWidth( 0.2 );

    # dibujar las líneas
    glBegin(GL_LINES)
    # Color negro
    glColor3f( 0.2, 0.2, 0.2 )

    for i in xrange(num_lines):
        if i != num_lines/2:
            glVertex3f( -long_grid, 0.0, gap*(i-num_lines/2) )
            glVertex3f( +long_grid, 0.0, gap*(i-num_lines/2) )

            glVertex3f( gap*(i-num_lines/2), 0.0, -long_grid )
            glVertex3f( gap*(i-num_lines/2), 0.0, +long_grid )

    glEnd()

def dibujarObjetos():
    redraw, hands = LeapListener.getHands()
    colors = [ [1.0,0.0,1.0], [1.0,1.0,0.0] ]

    for i,hand in enumerate(hands):
        if redraw[i]:
            #dibujarEsfera(colors[i], 30, hand.palm_position)
            for finger in hand.fingers:
                dibujarFalanges(colors[i],finger)

# Función de dibujado
def dibujar():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    fijarViewportProyeccion()
    fijarCamara()

    dibujarEjes()
    dibujarRejilla()
    dibujarObjetos()

    glutSwapBuffers()

# Teclas normales: para cambiar escala y velocidad
def teclaNormal(k, x, y):
    global frustum_factor_escala, vertice_actual, velocidad, camara_angulo_x, camara_angulo_y, dibujoEvoluta

    if k == '+':
        frustum_factor_escala *= 1.05
    elif k == '-':
        frustum_factor_escala /= 1.05
    elif k == b'r':
        camara_angulo_x = camara_angulo_y = 0.0
    elif k == b'q' or k == b'Q' or ord(k) == 27: # Escape
        sys.exit(0)
    else:
        return
    glutPostRedisplay()


# Teclas especiales: para cambiar la cámara
def teclaEspecial(k, x, y):
    global camara_angulo_x, camara_angulo_y

    if k == GLUT_KEY_UP:
        camara_angulo_x += 5.0
    elif k == GLUT_KEY_DOWN:
        camara_angulo_x -= 5.0
    elif k == GLUT_KEY_LEFT:
        camara_angulo_y += 5.0
    elif k == GLUT_KEY_RIGHT:
        camara_angulo_y -= 5.0
    else:
        return
    glutPostRedisplay()


# Nuevo tamaño de ventana
def cambioTamanio(width, height):
    global ventana_tam_x,ventana_tam_y

    ventana_tam_x = width
    ventana_tam_y = height

    fijarViewportProyeccion()
    glutPostRedisplay()

origen = [-1,-1]
def pulsarRaton(boton,estado,x,y):
    da = 5.0
    redisp = False
    global frustum_factor_escala,origen,camara_angulo_x,camara_angulo_y

    if boton == GLUT_LEFT_BUTTON:
        if estado == GLUT_UP:
            origen = [-1,-1]
        else:
            origen = [x,y]
    elif boton == 3: # Rueda arriba aumenta el zoom
        frustum_factor_escala *= 1.05;
        redisp = True
    elif boton == 4: # Rueda abajo disminuye el zoom
        frustum_factor_escala /= 1.05;
        redisp = True
    elif boton == 5: # Llevar la rueda a la izquierda gira la cámara a la izquierda
        camara_angulo_y -= da
        redisp = True
    elif boton == 6: # Llevar la rueda a la derecha gira la cámara a la derecha
        camara_angulo_y += da
        redisp = True

    if redisp:
        glutPostRedisplay();

def moverRaton(x,y):
    global camara_angulo_x,camara_angulo_y, origen

    if origen[0] >= 0 and origen[1] >= 0:
        camara_angulo_x += (y - origen[1])*0.25;
        camara_angulo_y += (x - origen[0])*0.25;

        origen[0] = x;
        origen[1] = y;

        # Redibujar
        glutPostRedisplay();

def initGUI(argumentos, listener):
    global LeapListener, quadric
    LeapListener = listener

    glutInit(argumentos)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_MULTISAMPLE | GLUT_ALPHA)

    glutInitWindowPosition(0, 0)
    glutInitWindowSize(ventana_tam_x, ventana_tam_y)
    glutCreateWindow("Leap Motion project")

    glEnable(GL_NORMALIZE)
    glEnable(GL_MULTISAMPLE_ARB);
    glClearColor( 1.0, 1.0, 1.0, 1.0 ) ;
    glColor3f(0.0,0.0,0.0)

    glutDisplayFunc(dibujar)
    glutIdleFunc(dibujar)
    glutReshapeFunc(cambioTamanio)
    glutKeyboardFunc(teclaNormal)
    glutSpecialFunc(teclaEspecial)
    glutMouseFunc(pulsarRaton)
    glutMotionFunc(moverRaton)

    quadric = gluNewQuadric()

    glutMainLoop()
