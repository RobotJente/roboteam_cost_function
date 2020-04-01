from Robot import Robot
import numpy as np
from matplotlib.patches import Circle
from Field import Field

# representation of the world.
class World:
    def __init__(self):
        pass

    # plot the robots at their current location
    def plot_bots(self, ax):
        for robot in self.robots:
            ax.add_artist(robot.circle)
            robot.connect()

    # create n bots at uniform random positions around the field
    def create_bots(self, n):
        robot_vector = []
        for i in range(n):
            x = np.random.uniform(Field.leftx, Field.rightx)
            y = np.random.uniform(Field.boty, Field.topy)
            vel = np.random.uniform(0, 10)
            circle = Circle([x, y], 0.5)
            robot_vector.append(Robot(x, y, vel, circle))
        self.robots = robot_vector
