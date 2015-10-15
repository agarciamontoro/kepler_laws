

'''
def DrawGLScene():
	glBegin(GL_LINE_LOOP)
	circleSections=100
        for x in xrange(circleSections):
            angle = 2 * numpy.pi * x / circleSections
            glVertex2f(100+numpy.cos(angle)*100,100+numpy.sin(angle)*100)
        glEnd()
'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy
import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

matrix1 = [[0 for x in xrange(6)] for x in xrange(1)] 
matrix2 = [[0 for x in xrange(5)] for x in xrange(3)] 
matrix1[0][0] = 0
matrix1[0][1] = 0
matrix1[0][2] = 0
matrix1[0][3] = 0
matrix1[0][4] = 0
matrix1[0][5] = 0
num_finger = 0
a=0
b=0
c=0
window = 0                                             # glut window number
width, height = 640, 480                               # window size

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        matrix1 = [[0 for x in xrange(6)] for x in xrange(1)] 
        num_finger = 0

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        if not frame.hands.is_empty:
            # Get the first hand
            hand = frame.hands[0]

            # Check if the hand has any fingers
            fingers = hand.fingers
            if not fingers.is_empty:
                # Calculate the hand's average finger tip position
                matrix1[0][0] = Leap.Vector()
                matrix1[0][1] = Leap.Vector()
                matrix1[0][2] = Leap.Vector()
                matrix1[0][3] = Leap.Vector()
                matrix1[0][4] = Leap.Vector()
                matrix1[0][5] = Leap.Vector()
                for finger in fingers:
                    #print "finger is", finger
                    #print "num_finger bef:", num_finger
                    matrix1[0][num_finger] = finger.tip_position
                    num_finger += 1
                    print "num_finger", num_finger
                avg_pos = num_finger
                print "Hand has %d fingers" %(len(fingers))
                print "finger tip position1 is: ", matrix1[0][0]
                print "finger tip position2 is: ", matrix1[0][1]
                print "finger tip position3 is: ", matrix1[0][2]
                print "finger tip position4 is: ", matrix1[0][3]
                print "finger tip position5 is: ", matrix1[0][4]
                '''
                global a
                global b
                global c
                '''
                global matrix1
                '''
                a = matrix1[0][0][0]+150
                b = matrix1[0][0][1]
                c = matrix1[0][0][2]
                print "x of finger 1 is :", a
                print "y of finger 1 is :", b
                print "z of finger 1 is :", c
               	'''

                num_finger = 0

           

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"





def refresh2d(width, height):

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw():                                            # ondraw is called all the time

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
    glLoadIdentity()                                   # reset position
    refresh2d(width, height) 
    #print "coordinatezz: ", a
    # "Deal with itzz:",b
    
    for num in xrange(4):
    	glColor3f(1.0, 1.0, 1.0)                           # set color to blue 
    	glBegin(GL_LINE_LOOP)
    	circleSections=100
        print "finger:", num
    	print "test: ", matrix1[0][num]
    	try:
    		a = matrix1[0][num][0]+250
    		b = matrix1[0][num][1]
    		c = matrix1[0][num][2]+50
    	except:
    		a=0
    		b=0
    		c=0

    	for x in xrange(circleSections):
    		angle = 2 * numpy.pi * x / circleSections
    		glVertex2f(a+numpy.cos(angle)*(c/float(10)), b+numpy.sin(angle)*(c/float(10)))
    	glEnd()
       
    # ToDo draw rectangle
    glutSwapBuffers()                                  # important fordouble buffering

# initialization
def main():
	# Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()


    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    glutInit()                                             # initialize glut
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)                      # set window size
    glutInitWindowPosition(0, 0)                           # set window position
    window = glutCreateWindow("FingerTracking")              # create window with title
    glutDisplayFunc(draw)                                  # set draw function callback
    glutIdleFunc(draw)                                     # draw all the time
    glutMainLoop()                                         # start everything


    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)

if __name__ == "__main__":
        main() 
