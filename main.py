#!/usr/bin/env python
# coding=UTF-8

from __future__ import print_function

import sys

import threading

import universe
import GUI
from constants import *

from wxGUI import MyApp

def main(arguments):
    # Construct and initialise GUI objects
    scene = GUI.GUI([])

    # Initialise the program
    universe.bigBang()

    # Create the animation thread and start it
    animation_thread = threading.Thread(target=scene.initGUI, args=(), kwargs={})
    animation_thread.start()

    # Create the wx app, its thread and start it
    app = MyApp(0)
    GUI_thread = threading.Thread(target=app.MainLoop, args=(), kwargs={})
    GUI_thread.start()

    # When the animation thread finishes, terminate wx main loop and quit.
    animation_thread.join()
    app.ExitMainLoop()

if __name__ == '__main__':
    """An incredibly simplified simulation of the Solar System

    Usage:
        python main.py

    Use your mouse (clicking and dragging) to move the angle of view. You can
    also zoom in or zoom out the scene using the mouse wheel.

    In the upper left corner there's a text showing the date in which the
    planets positions are being calculated. By default, for each second of your
    clock, the animation will run a whole day. You can change the animation
    speed using the following keys :
        Z: Decelerate the simulation time
        X: Accelerate the simulation time

    For quitting the program, just hit the key 'Q'.
    """
    main(sys.argv)
