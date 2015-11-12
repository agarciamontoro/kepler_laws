#!/usr/bin/env python
# coding=UTF-8

from __future__ import print_function

import Leap, sys

import LeapDriver
import NewGui as GUI
from constants import *
import ball
import game

import threading

def main(arguments):
    # Create sample listener and controller
    listener = LeapDriver.SampleListener()
    controller = Leap.Controller()

    # Let the sample listener receive events from the controller
    controller.add_listener(listener)

    if not controller.is_connected:
        print("Please, connect the Leap Motion device and start its daemon.")

    while not controller.is_connected:
        pass

    print("Thank you, enjoy!")

    scene = GUI.GUI([])

    GUIthread = threading.Thread(target=scene.initGUI, args=(), kwargs={})
    GUIthread.start()

    game.initGame(scene)

    GUIthread.join()


if __name__ == '__main__':
    main(sys.argv)
