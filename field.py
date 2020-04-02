# used to store the field dimensions
import numpy as np
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

    def in_defense_area(self, x, y):
        if x < self.rightx and x > self.rightx - self.def_area_width:
            if abs(y) < self.def_area_height:
                return True
        return False
    def distance_to_enemy_goal(self, x, y):
        length = (x - self.theirgoal[0]) ** 2 + (y - self.theirgoal[1]) ** 2
        return np.sqrt(length)