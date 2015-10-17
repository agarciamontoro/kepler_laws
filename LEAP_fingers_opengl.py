# coding=UTF-8

'''
def DrawGLScene():
	glBegin(GL_LINE_LOOP)
	circleSections=100
        for x in xrange(circleSections):
            angle = 2 * numpy.pi * x / circleSections
            glVertex2f(100+numpy.cos(angle)*100,100+numpy.sin(angle)*100)
        glEnd()
'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy
import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

matrix1 = [[0 for i in xrange(5)] for i in xrange(1)]
# matrix2 = [[0 for i in xrange(5)] for i in xrange(3)] no se usa en todo el código

matrix1[0][0] = 0
matrix1[0][1] = 0
matrix1[0][2] = 0
matrix1[0][3] = 0
matrix1[0][4] = 0
#matrix1[0][5] = 0

num_finger = 0
x=0
y=0
z=0
window = 0                                             # Numero de ventana glut
width, height = 800, 600                               # Tamaño de ventana

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Activar gestos
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Nota: no se mostrará cuando se arranque en un debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Obtiene el frame mas reciente y proporciona información básica
        frame = controller.frame()
        matrix1 = [[0 for i in xrange(5)] for i in xrange(1)]
        num_finger = 0

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        if not frame.hands.is_empty:
        	# Primera mano
            hand = frame.hands[0]

            # Comprueba si la mano tiene algún dedo
            fingers = hand.fingers
            if not fingers.is_empty:
                # Calcula la posición media de los dedos de la mano
                matrix1[0][0] = Leap.Vector()
                matrix1[0][1] = Leap.Vector()
                matrix1[0][2] = Leap.Vector()
                matrix1[0][3] = Leap.Vector()
                matrix1[0][4] = Leap.Vector()
                #matrix1[0][5] = Leap.Vector()

                for finger in fingers:
                    #print "finger is", finger
                    #print "num_finger bef:", num_finger
                    matrix1[0][num_finger] = finger.tip_position
                    num_finger += 1
                    print "num_finger", num_finger

                avg_pos = num_finger
                print "Hand has %d fingers" %(len(fingers))
                print "finger tip position1 is: ", matrix1[0][0]
                print "finger tip position2 is: ", matrix1[0][1]
                print "finger tip position3 is: ", matrix1[0][2]
                print "finger tip position4 is: ", matrix1[0][3]
                print "finger tip position5 is: ", matrix1[0][4]
                '''
                global x
                global y
                global z
                '''
                global matrix1
                '''
                x = matrix1[0][0][0]+150
                y = matrix1[0][0][1]
                z = matrix1[0][0][2]
                print "x of finger 1 is :", x
                print "y of finger 1 is :", y
                print "z of finger 1 is :", z
               	'''
                num_finger = 0

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw():                                            # ondraw es llamado todo el tiempo

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # limpia la ventana
    glLoadIdentity()                                   # reinicia la posición
    refresh2d(width, height)
    #print "coordinatezz: ", a
    # "Deal with itzz:",b

    for num in xrange(5):
    	glColor3f(1.0, 0.0, 1.0)                           # set color to blue
    	glBegin(GL_LINE_LOOP)
    	circleSections=100
        print "finger:", num
    	print "test: ", matrix1[0][num]
    	try:
    		x = matrix1[0][num][0]+400
    		y = matrix1[0][num][1]-10
    		z = matrix1[0][num][2]+50
    	except:
    		x=0
    		y=0
    		z=0

    	for i in xrange(circleSections):
    		angle = 2 * numpy.pi * i / circleSections
    		glVertex2f(x+numpy.cos(angle)*(z/float(10)), y+numpy.sin(angle)*(z/float(10)))
    	glEnd()

    # ToDo draw rectangle
    glutSwapBuffers()                                  # important fordouble buffering

# inicialización
def main():
	# Crea el sample listener y el controller
    listener = SampleListener()
    controller = Leap.Controller()


    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    glutInit()                                             # inicializar glut
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)                      # define el tamaño de la ventana
    glutInitWindowPosition(0, 0)                           # define la posición de la ventana
    window = glutCreateWindow("FingerTracking")            # crea la ventana con su título
    glutDisplayFunc(draw)                                  # set draw function callback
    glutIdleFunc(draw)                                     # dibuja todo el rato
    glutMainLoop()                                         # activa todo


    # Mantiene el proceso en ejecución hasta que pulsamos Enter
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Elimina el sample listener cuando se acaba
    controller.remove_listener(listener)

if __name__ == "__main__":
        main()
