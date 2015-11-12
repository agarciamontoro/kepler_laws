import NewGui
import ball
from constants import *

import Leap

import LeapDriver
import hand

draw_hand = hand.Hand()

def initGame(GUI):
    global scene
    scene = GUI

def processFrame(new_frame,hands):
    global scene

    ball_1 = ball.Ball(steel_yellow, 75, [0.0,125.0,-50.0])
    ball_2 = ball.Ball(steel_yellow, 50, [0.0,125.0,-100.0])
    ball_3 = ball.Ball(steel_yellow, 25, [0.0,125.0,-150.0])

    scene.objects = []

    if new_frame[0]:
        draw_hand.setHand(hands[0])
        scene.objects.append(draw_hand)
