#!/usr/bin/env python
# coding=UTF-8

from __future__ import print_function
import threading

import Leap, sys

import LeapDriver, game
import GUI
from constants import *

def main(arguments):
    # Create sample listener and controller
    listener = LeapDriver.SampleListener()
    controller = Leap.Controller()

    # Let the sample listener receive events from the controller
    controller.add_listener(listener)

    if not controller.is_connected:
        print("Please, connect the Leap Motion device and start its daemon.")

    # Wait until Leap Device is connected
    while not controller.is_connected:
        pass

    print("Thank you, enjoy!")

    # Construct GUI object
    scene = GUI.GUI([])

    # Start OpenGL main loop in a different thread
    GUIthread = threading.Thread(target=scene.initGUI, args=(), kwargs={})
    GUIthread.start()

    # Start the game
    game.initGame(listener)

    # Wait to the GUI object to be finished
    GUIthread.join()


if __name__ == '__main__':
    main(sys.argv)
