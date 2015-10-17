# coding=UTF-8

import numpy
import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

new_frame = False

def fingerPos(hand, handType):
	fingers = hand.fingers
	num_finger = 0
	# Comprueba si la mano tiene algún dedo
	if not fingers.is_empty:
		# Calcula la posición media de los dedos de la mano

		for finger in fingers:
			matrix1[handType][num_finger] = finger.tip_position
			num_finger += 1
			print "num_finger", num_finger

		avg_pos = num_finger
		print "Hand has %d fingers" %(len(fingers))
		print "finger tip position1 is: ", matrix1[handType][0]
		print "finger tip position2 is: ", matrix1[handType][1]
		print "finger tip position3 is: ", matrix1[handType][2]
		print "finger tip position4 is: ", matrix1[handType][3]
		print "finger tip position5 is: ", matrix1[handType][4]

		num_finger = 0
	global matrix1

class SampleListener(Leap.Listener):
	def on_init(self, controller):
		matrix1 = [[Leap.Vector() for i in xrange(5)] for i in xrange(2)]
		global matrix1
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
		new_frame = False

		num_finger = 0

		print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
		frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

		if not frame.hands.is_empty:
			# Primera mano (izquierda)
			if frame.hands[0].is_left:
				lHand = frame.hands[0]
				rHand = frame.hands[1]
			else:
				lHand = frame.hands[1]
				rHand = frame.hands[0]

		#Calculamos las posiciones de los dedos de ambas manos
		fingerPos(lHand, 0)
		fingerPos(rHand, 1)
		new_frame = True
		global new_frame
		global matrix1

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
	global matrix1
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # limpia la ventana
	glLoadIdentity()                                   # reinicia la posición
	refresh2d(width, height)
	#print "coordinatezz: ", a
	# "Deal with itzz:",b

	for num in xrange(5):
		print "finger:", num

		try:
			lx = matrix1[0][num][0]+width/2
			ly = matrix1[0][num][1]-10
			lz = matrix1[0][num][2]+50
		except:
			lx=0
			ly=0
			lz=0

		try:
			rx = matrix1[1][num][0]+width/2
			ry = matrix1[1][num][1]-10
			rz = matrix1[1][num][2]+50
		except:
			rx=0
			ry=0
			rz=0

		glColor3f(1.0, 0.0, 1.0)                           # set color to pink
		circleSections=100
		glBegin(GL_LINE_LOOP)
		for i in xrange(circleSections):
			angle = 2 * numpy.pi * i / circleSections
			glVertex2f(lx+numpy.cos(angle)*(lz/float(10)), ly+numpy.sin(angle)*(lz/float(10)))
		glEnd()

		glColor3f(1.0, 1.0, 0.0)                           # set color to blue
		glBegin(GL_LINE_LOOP)
		for i in xrange(circleSections):
			angle = 2 * numpy.pi * i / circleSections
			glVertex2f(rx+numpy.cos(angle)*(rz/float(10)), ry+numpy.sin(angle)*(rz/float(10)))
		glEnd()


	# ToDo draw rectangle
	glutSwapBuffers()                                  # important fordouble buffering

def getHands():
	return new_frame, matrix1

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

	#dibujado.InicializarDibujado(sys.argv)

	# Mantiene el proceso en ejecución hasta que pulsamos Enter
	print "Press Enter to quit..."

	sys.stdin.readline()

	# Elimina el sample listener cuando se acaba
	controller.remove_listener(listener)

if __name__ == "__main__":
        main()
