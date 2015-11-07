# coding=UTF-8

import numpy
import Leap, sys

from Leap import Finger
import math

tutorial_steps = 4
current_step = 0

class SampleListener(Leap.Listener):
	def on_init(self, controller):
		self.new_frame = [False, False]
		self.hands = None
		print "Initialized"

	def on_connect(self, controller):
		print "Connected"

		# Activate gestures
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
		controller.config.set("Gesture.KeyTap.MinDownVelocity", 40.0)
		controller.config.set("Gesture.KeyTap.HistorySeconds", .2)
		controller.config.set("Gesture.KeyTap.MinDistance", 1.0)
		controller.config.save()

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
		# Obtain the most recent frame and provides basic information
		frame = controller.frame()
		self.new_frame = [False, False]

		global current_step

		# If the tutorial is not finished, try to detect key tap gesture
		if current_step < tutorial_steps:
			for gesture in frame.gestures():
				if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
					# Screen tap gesture detected!
					tap = Leap.KeyTapGesture(gesture)
					if tap.state is Leap.Gesture.STATE_STOP:
						# Screen tap gesture finished!
						current_step += 1

		if not frame.hands.is_empty:
			self.hands = frame.hands
			self.new_frame = [frame.hands[0].is_valid, frame.hands[1].is_valid]
			fingerCount(frame.hands[0])

	def state_string(self, state):
		if state == Leap.Gesture.STATE_START:
			return "STATE_START"

		if state == Leap.Gesture.STATE_UPDATE:
			return "STATE_UPDATE"

		if state == Leap.Gesture.STATE_STOP:
			return "STATE_STOP"

		if state == Leap.Gesture.STATE_INVALID:
			return "STATE_INVALID"
