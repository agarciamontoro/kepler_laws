#!/usr/bin/env python
# coding=UTF-8

from __future__ import print_function

import sys

import universe
import GUI
from constants import *

def main(arguments):
    # Construct and initialise GUI object
    scene = GUI.GUI([])

    # Initialise the game
    universe.bigBang()

    # Start GUI and Universe :)
    scene.initGUI()


if __name__ == '__main__':
    main(sys.argv)
