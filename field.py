# used to store the field dimensions
import numpy as np
from matplotlib.patches import Circle


class field:
    leftx = -6
    rightx = 6
    topy = 4.5
    boty = -4.5
    width = 12
    height = 9
    theirgoal = [6, 0]

    def_area_width = 1.8
    def_area_height = 1.8

    viable_shot_radius = 2
    viable_shot_position_circle = Circle([theirgoal[0], theirgoal[1], viable_shot_radius])

    def in_defense_area(self, x, y):
        if x < self.rightx and x > self.rightx - self.def_area_width:
            if abs(y) < self.def_area_height:
                return True
        return False

    def distance_to_enemy_goal(self, x, y):
        length = (x - self.theirgoal[0]) ** 2 + (y - self.theirgoal[1]) ** 2
        return np.sqrt(length)

    def distance_between_points(self, x1, y1, x2, y2):
        length = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return np.sqrt(length)

    # return true if (x,y) is in the circle
    def inside_circle(self, x, y, circle):
        if self.distance_between_points(x1=x, y1=y, x2=circle.center[0], y2=circle.center[1]) < circle.get_radius():
            return True
        return False
