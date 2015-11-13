# coding=UTF-8

import Leap, sys

from Leap import Finger
import math

class SampleListener(Leap.Listener):
	def on_init(self, controller):
		self.new_frame = [False, False]
		self.hands = None
		print "Initialized"

	def on_connect(self, controller):
		print "Connected"

	def on_disconnect(self, controller):
		# Note: not shown when it starts in a debugger
		print "Disconnected"

	def on_exit(self, controller):
		print "Exited"

	def getHands(self):
		return self.new_frame, self.hands

	def tutorialFinished(self):
		return current_step >= tutorial_steps

	def tutorialState(self):
		return current_step

	def on_frame(self, controller):
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
