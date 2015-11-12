import ball
from constants import *

import Leap

import LeapDriver
import hand

draw_hand = hand.Hand()

# Distance
def distance(pos1,pos2):
    return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

def initGame(listener):
    global leap
    leap = listener

def processFrame():
    new_frame, hands = leap.getHands()

    ball_1 = ball.Ball(steel_yellow, 75, [0.0,125.0,-50.0])
    ball_2 = ball.Ball(steel_red, 50, [0.0,125.0,-100.0])
    ball_3 = ball.Ball(steel_white, 25, [0.0,125.0,-137.5])

    objects = []

    objects.append(ball_1)
    objects.append(ball_2)
    objects.append(ball_3)

    if new_frame[0]:
        draw_hand.setHand(hands[0])
        objects.append(draw_hand)

    return objects
