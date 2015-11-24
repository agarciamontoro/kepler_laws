from primitives import Ball, Quad
from constants import *

import math
from operator import add

# Distance
def distance(pos1,pos2):
    return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

def toPolar(pos):
    module = math.sqrt(sum([pos[i]**2 for i in range(2)]))
    angle = math.atan2(pos[1], pos[0])
    return [module,angle]

class BilliardBall(Ball):
    def __init__(self, coord=[0.0,0.0], vel=[0.0,0.0], b_type=BBallType.whitey, color=steel_red):
        self.coord = [coord[0], BALL_RADIUS, coord[1]]
        self.vel = [vel[0], 0.0, vel[1]]
        self.type = b_type

        self.frame_tick = 0
        self.highlighted = False

        self.first_radius = self.radius = BALL_RADIUS
        if self.type == BBallType.whitey:
            self.radius = BALL_RADIUS*0.9
            color=steel_white
        if self.type == BBallType.black:
            color = black

        Ball.__init__(self, color, self.radius, self.coord)

    def updatePos(self):
        self.vel = [self.vel[i]*COF for i in range(3)]
        self.coord = map(add,self.coord,self.vel)

    def velToPolar(self):
        return toPolar([self.vel[0],self.vel[2]])

    def posToPolar(self):
        return toPolar([self.pos[0],self.pos[2]])

    def isMoving(self):
        vel_module = self.velToPolar()[0]
        return vel_module > 0

    def collide(self, other_ball):
        speed_module = self.velToPolar()[0]
        dist = distance(self.coord, other_ball.coord) - (self.radius+other_ball.radius)

        if speed_module != 0 and 0 < dist / speed_module < 1:
            return True

        return distance(self.coord, other_ball.coord) <= self.radius+other_ball.radius

    # def tableCollision(self, table):
    #     if table.collision(self) == VERTICAL:
    #         self.vel[0] = -self.vel[0]
    #     else:
    #         self.vel[2] = -self.vel[1]

    def collisionPoint(self, other_ball):
        return [(self.coord[i]+other_ball.coord[i])/2 for i in range(3)]

    def collisionAngle(self, other_ball):
        collision_pt = self.collisionPoint(other_ball)
        polar_collision_point = toPolar([collision_pt[0], collision_pt[2]])
        return polar_collision_point[1]

    def ellasticCollisionUpdate(self, other_ball):
        polar_vel_1 = self.velToPolar()
        polar_vel_2 = other_ball.velToPolar()

        collision_angle = self.collisionAngle(other_ball)

        new_vel_1_x = polar_vel_2[0] * math.cos(polar_vel_2[1]-collision_angle) * math.cos(collision_angle) + polar_vel_1[0] * math.sin(polar_vel_1[1]-collision_angle) * math.cos(collision_angle + math.pi/2)

        new_vel_1_y = polar_vel_2[0] * math.cos(polar_vel_2[1]-collision_angle) * math.sin(collision_angle) + polar_vel_1[0] * math.sin(polar_vel_1[1]-collision_angle) * math.sin(collision_angle + math.pi/2)

        new_vel_2_x = polar_vel_1[0] * math.cos(polar_vel_1[1]-collision_angle) * math.cos(collision_angle) + polar_vel_2[0] * math.sin(polar_vel_2[1]-collision_angle) * math.cos(collision_angle + math.pi/2)

        new_vel_2_y = polar_vel_1[0] * math.cos(polar_vel_1[1]-collision_angle) * math.sin(collision_angle) + polar_vel_2[0] * math.sin(polar_vel_2[1]-collision_angle) * math.sin(collision_angle + math.pi/2)

        self.vel        = [COF*new_vel_1_x, 0.0, COF*new_vel_1_y]
        other_ball.vel  = [COF*new_vel_2_x, 0.0, COF*new_vel_2_y]

    def activateHighlight(self):
        self.highlighted = True

    def deactivateHighlight(self):
        self.radius = self.first_radius

    def highlight(self):
        if self.highlighted:
            self.frame_tick = (self.frame_tick + 5)%360
            radian_tick = self.frame_tick / 360.0  * 2 * math.pi
            self.radius = self.radius + 0.3*math.sin(radian_tick)

class BilliardTable:
    def __init__(self, width=1000, length=1500, height=2*BALL_RADIUS, center = [0.0, 0.0, 0.0]):
        self.width = width
        self.length = length
        self.height = height

        half_width = self.width/2.
        half_length = self.length/2.

        top_left_corner     = [center[0] - half_width, -0.01, center[0] + half_length]
        top_right_corner    = [center[0] + half_width, -0.01, center[0] + half_length]
        bottom_right_corner = [center[0] + half_width, -0.01, center[0] - half_length]
        bottom_left_corner  = [center[0] - half_width, -0.01, center[0] - half_length]

        corners = [top_left_corner, bottom_left_corner, bottom_right_corner, top_right_corner]

        self.table = Quad(corners, billiard_green)

    def draw(self):
        self.table.draw()
