import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import AxesImage

from world import world
from robot import robot
from field import field

# some initial setup for the plot and the world
figure, ax = plt.subplots()
ax.set_xlim(field.leftx - 1, field.rightx + 1)
ax.set_ylim(field.boty - 1, field.topy + 1)
world = world()
world.create_bots(12)
world.plot_bots(ax)

# some constants for the field
N = 100
x = np.linspace(field.leftx, field.rightx, N, endpoint=False)
y = np.linspace(field.boty, field.topy, N, endpoint=False)


# when the robots are dragged, the cost function needs to be recalculated
def redraw_cost_function():
    z = np.array([[cost_function(xpoint, ypoint) for xpoint in x] for ypoint in y])

    # remove the current imshow object, otherwise it stacks them on each other and your program will run slower
    for child in ax.get_children():
        if type(child) is AxesImage:
            child.remove()

    p = plt.imshow(z, vmin=-10, vmax=10, extent=[field.leftx, field.rightx, field.topy, field.boty])

    figure.canvas.draw()
    print(len(ax.get_children()))


# when the canvas is pressed and released, we redraw the cost function (since it may have been a robot drag)
def on_release(event):
    redraw_cost_function()


# This is the cost function for the current scenario
def cost_function(xpoint, ypoint):
    return world.robots[0].distance([xpoint, ypoint])

figure.canvas.mpl_connect('button_release_event', on_release)
z = np.array([[cost_function(xpoint, ypoint) for xpoint in x] for ypoint in y])

p = plt.imshow(z, vmin=-10, vmax=10, extent=[field.leftx, field.rightx, field.topy, field.boty])
plt.colorbar(p)
plt.show()

