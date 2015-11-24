from enum import Enum

COF = 0.99

BALL_RADIUS = 40

SLICES = 50
STACKS = 50

steel_blue   = [0.27,0.5,0.7]
steel_red    = [1.0,0.32,0.32]
steel_yellow = [1.0, 0.75, 0.03]
steel_orange = [1.0, 0.34, 0.14]
steel_white  = [1.0, 1.0, 1.0]
steel_gray   = [0.25, 0.25, 0.25]
steel_green  = [0.0, 0.47, 0.41]
black        = [0.0, 0.0, 0.0]
grid_gray    = [0.2, 0.2, 0.2]
billiard_green=[0.04,0.42,0.01]

class BBallType(Enum):
    whitey = 1
    striped = 2
    solid = 3
    black = 4
