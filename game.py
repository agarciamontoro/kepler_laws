import primitives
from constants import *

import Leap, time

import LeapDriver
import hand

draw_hand = [hand.Hand(), hand.Hand()]
last_data_time = [0,0]
time_margin = 0.07

# Distance
def distance(pos1,pos2):
    return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

def initGame(listener):
    global leap
    leap = listener
    last_data_time = [time.time(), time.time()]

def processFrame():
    new_frame, hands = leap.getHands()

    ball_1 = primitives.Ball(steel_yellow, 75, [0.0,125.0,-50.0])
    ball_2 = primitives.Ball(steel_red, 50, [0.0,125.0,-100.0])
    ball_3 = primitives.Ball(steel_white, 25, [0.0,125.0,-137.5])

    objects = []

    objects.append(ball_1)
    objects.append(ball_2)
    objects.append(ball_3)

    for i in range(2):
        if new_frame[i]:
            draw_hand[i].setHand(hands[i])
            objects.append(draw_hand[i])
            last_data_time[i] = time.time()
            print("New frame: ",i)
        elif time.time() - last_data_time[i] < time_margin:
            objects.append(draw_hand[i])
            print("Not new frame: ",i)


    return objects
