import Leap
from Leap import Finger

import math

# Distance
def distance(pos1,pos2,weight=[1.0,1.0,1.0]):
    return math.sqrt(sum([weight[i]*(pos2[i]-pos1[i])**2 for i in range(3)]))

# Returns whether a hand is doing an OK gesture
def isGestureOK(hand, tolerance = 30):
    gesture = False
    if hand.is_valid:
        index = hand.fingers.finger_type(Finger.TYPE_INDEX)[0]
        thumb = hand.fingers.finger_type(Finger.TYPE_THUMB)[0]

        if distance(index.tip_position,thumb.tip_position) < tolerance:
            gesture = True

    return gesture

# Returns whether a hand is counting
def isGestureCounting(hand):
    thumb = hand.fingers.finger_type(Finger.TYPE_THUMB)[0]
    return distance(thumb.tip_position, hand.palm_position, [1.0,0.0,1.0]) < hand.palm_width/2.0

def isFingerCounting(hand,finger):
    return distance(finger.tip_position, hand.palm_position, [0,0,1.0]) > hand.palm_width/2.0

# Returns the number shown by the fingers when the hand is counting
def fingerCount(hand):
    if hand.is_valid and isGestureCounting(hand):
        count = sum( (1 if isFingerCounting(hand,finger) else 0 for finger in hand.fingers) )
    else:
        count = -1

    return count
