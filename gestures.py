import Leap
from Leap import Finger

# Distance
def distance(pos1,pos2,weight=[1.0,1.0,1.0]):
    return math.sqrt(sum([weight[i]*(pos2[i]-pos1[i])**2 for i in range(3)]))

# Returns wether a hand is doing an OK gesture
def isGestureOK(hand, tolerance = 10):
    gesture = False
    if hand.is_valid:
        index = hand.fingers.finger_type(Finger.TYPE_INDEX)[0]
        thumb = hand.fingers.finger_type(Finger.TYPE_THUMB)[0]

        if distance(index.tip_position,thumb.tip_position) < tolerance:
            gesture = True

    return gesture

def isGestureCounting(hand):
	return distance(thumb.tip_position, hand.palm_position, [1.0,0.0,1.0]) < hand.palm_width/2.0:

# Return the number shown by the fingers
def fingerCount(hand):
	count = 0
	if hand.is_valid:
		thumb = hand.fingers.finger_type(Finger.TYPE_THUMB)[0]
		if isGestureCounting(hand):   

	return count
