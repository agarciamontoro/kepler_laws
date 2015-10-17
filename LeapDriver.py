# coding=UTF-8

import numpy
import Leap, sys

class SampleListener(Leap.Listener):
	def on_init(self, controller):
		self.new_frame = [False, False]
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

	def getHands(self):
		return self.new_frame, self.hands

	def on_frame(self, controller):
		# Obtiene el frame mas reciente y proporciona información básica
		frame = controller.frame()
		self.new_frame = [False, False]

		if not frame.hands.is_empty:
			self.hands = frame.hands
			self.new_frame = [frame.hands[0].is_valid, frame.hands[1].is_valid]

	def state_string(self, state):
		if state == Leap.Gesture.STATE_START:
			return "STATE_START"

		if state == Leap.Gesture.STATE_UPDATE:
			return "STATE_UPDATE"

		if state == Leap.Gesture.STATE_STOP:
			return "STATE_STOP"

		if state == Leap.Gesture.STATE_INVALID:
			return "STATE_INVALID"
