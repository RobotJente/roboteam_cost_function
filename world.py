import numpy as np
from matplotlib.patches import Circle
from field import field
import geometer as geo


# representation of the world.
from robot import robot


class world:

    def __init__(self):
        self.robots = []
        self.our_bots = []
        self.their_bots = []

    # plot the robots at their current location
    def plot_bots(self, ax):
        for robot in self.robots:
            ax.add_artist(robot.circle)
            robot.connect()

    # create n bots at uniform random positions around the field
    def create_our_bots(self, n):
        for i in range(n):
            x = np.random.uniform(field.leftx, field.rightx)
            y = np.random.uniform(field.boty, field.topy)
            vel = np.random.uniform(0, 10)
            circle = Circle([x, y], 0.3, fc="purple", alpha=0.7)
            bot = robot(x, y, vel, circle)

            self.robots.append(bot)
            self.our_bots.append(bot)

    # create n bots at uniform random positions around the field
    def create_their_bots(self, n):
        for i in range(n):
            x = np.random.uniform(field.leftx, field.rightx)
            y = np.random.uniform(field.boty, field.topy)
            vel = np.random.uniform(0, 10)
            circle = Circle([x, y], 0.3, fc="aqua", alpha=0.7, label = 'them')
            bot = robot(x, y, vel, circle)

            self.robots.append(bot)
            self.their_bots.append(bot)

    # return our closest robot and the distance to the point
    def our_closest_robot_to_point(self, x, y):
        smallest = field.width
        closestbot = None

        for robot in self.our_bots:
            if robot.distance(x, y) < smallest:
                closestbot = robot
                smallest = robot.distance(x, y)

        return closestbot, smallest

    # return their closest robot and the distance to the point
    def their_closest_robot_to_point(self, x, y):
        smallest = field.width
        closestbot = None
        for robot in self.their_bots:
            if robot.distance(x, y) < smallest:
                closestbot = robot
                smallest = robot.distance(x, y)

        return closestbot, smallest

    # return closest robot and the distance to the point
    def closest_robot_to_point(self, x, y):
        smallest = field.width
        closestbot = None
        for robot in self.robots:
            if robot.distance(x, y) < smallest:
                closestbot = robot
                smallest = robot.distance(x, y)

        return closestbot, smallest

    def can_reach(self, start_point, end_point):
        for robot in self.their_bots:
            line = geo.Line(start_point, end_point)
            intersects = robot.intercept_circle.intersect(line)

            if len(intersects) > 0:
                if not np.iscomplexobj(intersects[0].array[0]):
                    return False
            else: print("TRUE")
        return True
