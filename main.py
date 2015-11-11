#!/usr/bin/env python
# coding=UTF-8

from __future__ import print_function

import Leap, sys

import LeapDriver
#import GUI
import NewGui as GUI
import colors

def main(argumentos):
    # Create sample listener and controller
    listener = LeapDriver.SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    if not controller.is_connected:
        print("Please, connect the Leap Motion device and start its daemon.")

    while not controller.is_connected:
        pass

    print("Thank you!")

    # Initialize program
    # GUI.initGUI(argumentos, listener)

    bola = Ball(colors.steel_red, 50, [0.0,100.0,-200.0])
    GUIscene = GUI(listener, [bola])


if __name__ == '__main__':
    main(sys.argv)
