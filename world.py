from robot import robot
import numpy as np
from matplotlib.patches import Circle
from field import field

# representation of the world.
class world:

    # plot the robots at their current location
    def plot_bots(self, ax):
        for robot in self.robots:
            ax.add_artist(robot.circle)
            robot.connect()

    # create n bots at uniform random positions around the field
    def create_bots(self, n):
        robot_vector = []
        for i in range(n):
            x = np.random.uniform(field.leftx, field.rightx)
            y = np.random.uniform(field.boty, field.topy)
            vel = np.random.uniform(0, 10)
            circle = Circle([x, y], 0.5)
            robot_vector.append(robot(x, y, vel, circle))
        self.robots = robot_vector
