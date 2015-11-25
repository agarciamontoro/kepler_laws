import primitives
from billiardBall import BilliardBall, BilliardTable
from constants import *

import Leap, time

import LeapDriver
import hand
import gestures
from forceLine import ForceLine

import itertools

draw_hand = [hand.Hand(), hand.Hand()]
last_data_time = [0,0]
time_margin = 0.07

# Distance
def distance(pos1,pos2):
    return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

def initGame(listener):
    global leap, last_data_time, tutorial, b_table, b_whitey, b_balls, loader, force_line, shoot_mode

    leap = listener
    last_data_time = [time.time(), time.time()]
    tutorial = primitives.Image("./Screenshots/01.png")

    b_table = BilliardTable()

    striped_1 = BilliardBall([0,0],[0.0,0.0], BBallType.striped, steel_red)
    striped_2 = BilliardBall([-150,-150],[0.0,0.0], BBallType.striped, steel_yellow)
    # striped_3 = BilliardBall([150,-150],[0.0,0.0], BBallType.striped, steel_orange)
    # striped_4 = BilliardBall([150,-150],[0.0,0.0], BBallType.striped, steel_red)
    # striped_5 = BilliardBall([0,0],[0.0,0.0], BBallType.striped, steel_red)
    # striped_6 = BilliardBall([0,0],[0.0,0.0], BBallType.striped, steel_red)
    # striped_7 = BilliardBall([0,0],[0.0,0.0], BBallType.striped, steel_red)

    solid_1   = BilliardBall([75,-75],[0.0,0.0], BBallType.solid, steel_orange)
    solid_2   = BilliardBall([-75,-75],[0.0,0.0], BBallType.solid, steel_green)
    # solid_3   = BilliardBall([0,-150],[0.0,0.0], BBallType.solid, black)
    # solid_4   = BilliardBall([0,0],[0.0,0.0], BBallType.solid, steel_yellow)
    # solid_5   = BilliardBall([0,0],[0.0,0.0], BBallType.solid, steel_yellow)
    # solid_6   = BilliardBall([0,0],[0.0,0.0], BBallType.solid, steel_yellow)
    # solid_7   = BilliardBall([0,0],[0.0,0.0], BBallType.solid, steel_yellow)

    b_whitey    = BilliardBall([0,90],[0.0,0.0], BBallType.whitey)
    b_black     = BilliardBall([0,-150],[0.0,0.0], BBallType.black)

    # b_balls = [striped_1, striped_2, striped_3, striped_4, striped_5, striped_6, striped_7, solid_1, solid_2, solid_3, solid_4, solid_5, solid_6, solid_7, whitey, black]
    b_balls = [striped_1, striped_2, solid_1, solid_2, b_whitey, b_black]

    loader = primitives.Loader([200.0,200.0])
    loader.activate()
    force_line = ForceLine(b_whitey)

    shoot_mode = False

def isAnyCollision(b_list):
    for ball, other_ball in itertools.combinations(b_list,2):
        if ball.collide(other_ball):
            return True
    return False

def processFrame():
    new_frame, hands = leap.getHands()

    # # Test the image object: shows the tutorial image for the first five seconds
    # if time.time() - last_data_time[0] < 5:
    #     objects.append(tutorial)

    for ball, other_ball in itertools.combinations(b_balls,2):
        if ball.collide(other_ball):
            ball.ellasticCollisionUpdate(other_ball)

    for ball in b_balls:
       ball.updatePos()

    # Test highlight. This should be done only when the ball is touched
    #b_whitey.activateHighlight()
    #b_whitey.highlight()

    objects = [b_table] + b_balls
    '''
    if loader.load():
        loader.deactivate()
    else:
        objects = objects + [loader, tutorial] #The order is important: always puts loader first
    '''
    global shoot_mode, force

    for i in range(2):
        if new_frame[i]:
            if gestures.isGestureOK(hands[i]):
                shoot_mode = True
                hand_pos = [hands[i].palm_position[j] for j in range(3)]

                force_line.setBall(b_whitey)
                force_line.setOrigin(hand_pos)

                force = force_line.getForce()
                print(shoot_mode)
                objects.append(force_line)
            elif shoot_mode:
                shoot_mode = False
                b_whitey.vel = force

            draw_hand[i].setHand(hands[i])
            objects.append(draw_hand[i])
            last_data_time[i] = time.time()
        elif time.time() - last_data_time[i] < time_margin:
            objects.append(draw_hand[i])

    return objects
