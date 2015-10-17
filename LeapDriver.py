# coding=UTF-8

import numpy
import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

new_frame = [False, False] #Guarda si hay un nuevo frame para la mano izqda. y la dcha.

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

	def fingerPos(self, hand, handType):
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

	def getHands(self):


	def on_frame(self, controller):
		# Obtiene el frame mas reciente y proporciona información básica
		frame = controller.frame()
		new_frame = [False, False]

		num_finger = 0

		print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
		frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

		if not frame.hands.is_empty:
			for i in xrange(2):
				if frame.hands[i].is_valid:
					new_frame[i] = True
					self.fingerPos(frame.hands[i], i)

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
'''
def getHands():
	return new_frame, matrix1
'''
