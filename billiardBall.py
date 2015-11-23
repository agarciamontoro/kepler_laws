import primitives
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

class BilliardBall(primitives.Ball):
    def __init__(self, coord=[0.0,0.0], vel=[0.0,0.0], b_type=BBallType.whitey, color=steel_red):
        self.coord = [coord[0], BALL_RADIUS, coord[1]]
        self.vel = [vel[0], 0.0, vel[1]]
        self.type = b_type

        self.radius = BALL_RADIUS
        if self.type == BBallType.whitey:
            self.radius = BALL_RADIUS*0.9
            color=steel_white
        if self.type == BBallType.black:
            color = black

        primitives.Ball.__init__(self, color, self.radius, self.coord)

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

        self.vel        = [new_vel_1_x, 0.0, new_vel_1_y]
        other_ball.vel  = [new_vel_2_x, 0.0, new_vel_2_y]

    def ellasticCollisionUpdate_rest(self, other_ball):
        vel_1 = self.velToPolar()
        # other_ball is at rest

        collision_angle = self.collisionAngle(other_ball)

        angle_1 = math.atan(math.tan(collision_angle)/2)
        angle_2 = (math.pi - collision_angle)/2

        module_1 = vel_1[0] * math.sqrt(2+2*math.cos(collision_angle)) / 2
        module_2 = vel_1[0] * math.sin(collision_angle/2)

        self.vel        = [module_1*math.cos(angle_1), 0.0, module_1*math.sin(angle_1)]
        other_ball.vel  = [module_2*math.cos(angle_2), 0.0, module_2*math.sin(angle_2)]
