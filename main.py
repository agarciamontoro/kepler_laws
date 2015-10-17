#!/usr/bin/env python
# coding=UTF-8

#Origen : https://github.com/analca3/TriedroFrenet_Evoluta

from __future__ import print_function

import Leap, sys

import LeapDriver
import GUI

def main(argumentos):
    # Crea el sample listener y el controller
    listener = LeapDriver.SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    #Inicializa el programa
    GUI.initGUI(argumentos)


if __name__ == '__main__':
    main(sys.argv)
