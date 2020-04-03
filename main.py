import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import AxesImage
import pygmo as pg
from pygmo.core import algorithm
import math

from world import world
from field import field

# some initial setup for the plot and the world
figure, ax = plt.subplots()
ax.set_xlim(field.leftx - 1, field.rightx + 1)
ax.set_ylim(field.boty - 1, field.topy + 1)
world = world()
world.create_their_bots(11)
world.create_our_bots(11)
world.plot_bots(ax)

# some constants for the field
N = 100
x = np.linspace(field.leftx, field.rightx, N, endpoint=False)
y = np.linspace(field.boty, field.topy, N, endpoint=False)
main_field = field()


# when the robots are dragged, the cost function needs to be recalculated
def redraw_cost_function():
    z = np.array([[cost_function(xpoint, ypoint) for xpoint in x] for ypoint in y])

    # remove the current imshow object, otherwise it stacks them on each other and your program will run slower
    for child in ax.get_children():
        if type(child) is AxesImage:
            child.remove()

    p = plt.imshow(z, extent=[field.leftx, field.rightx, field.topy, field.boty], cmap="Blues")
    figure.canvas.draw()

# when the canvas is pressed and released, we redraw the cost function (since it may have been a robot drag)
def on_release(event):
    redraw_cost_function()


# This is the cost function for the current scenario
# high score = better point
def cost_function(xpoint, ypoint):
    score = 0
    if main_field.in_defense_area(xpoint, ypoint):
        score += -300

    bot, dist = world.their_closest_robot_to_point(xpoint, ypoint)
    score += 100 * dist

    ourbot, ourdist = world.our_closest_robot_to_point(xpoint, ypoint)
    score += -100 * ourdist

    shoot_succes_reward = bot.shoot_from_pos(xpoint, ypoint)
    score += shoot_succes_reward
    # score += field.distance_to_enemy_goal(field, xpoint, ypoint)

    score += angle_to_goal(xpoint, ypoint) * -500

    return score


def angle_to_goal(x, y):
    angle = math.atan((field.theirgoal[1] - y) / (field.theirgoal[0] - x))
    return abs(angle)


figure.canvas.mpl_connect('button_release_event', on_release)
z = np.array([[cost_function(xpoint, ypoint) for xpoint in x] for ypoint in y])


algo = pg.algorithm(pg.pso(gen = 100))
p = plt.imshow(z, extent=[field.leftx, field.rightx, field.topy, field.boty], cmap="Blues")
plt.colorbar(p)
plt.show()
