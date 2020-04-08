# external imports
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import AxesImage
import pygmo as pg
from pygmo.core import algorithm
from matplotlib.widgets import Button

# user-defined imports
from world import world
from field import field


# Problem definition class. It is in main.py because the fitness function requires data from here
# Its purpose is to define the optimization problem for pygmo
#################################################################################################
class optimprob:
    def __init__(self, name):
        self.name = name
        self.dim = 2

    def fitness(self, x):
        return self.cost_function(xpoint=x[0], ypoint=x[1])

    def get_bounds(self):
        return ([field.leftx, field.boty], [field.rightx, field.topy])

    def get_name(self):
        return self.name

    def cost_function(self, xpoint, ypoint):
        score = 0
        if main_field.in_defense_area(xpoint, ypoint):
            score += 300

        bot, dist = world.their_closest_robot_to_point(xpoint, ypoint)
        score += -100 * dist

        ourbot, ourdist = world.our_closest_robot_to_point(xpoint, ypoint)
        score += 100 * ourdist

        shoot_succes_reward = bot.shoot_from_pos(xpoint, ypoint)
        score += -shoot_succes_reward*2
        # score += field.distance_to_enemy_goal(field, xpoint, ypoint)
        return [score]


#################################################################################################

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
    z = np.array([[a.cost_function(xpoint, ypoint)[0] for xpoint in x] for ypoint in y])

    # remove the current imshow object, otherwise it stacks them on each other and your program will run slower
    for child in ax.get_children():
        if type(child) is AxesImage:
            child.remove()

    p = plt.imshow(z, extent=[field.leftx, field.rightx, field.topy, field.boty], cmap="Blues")
    figure.canvas.draw()
    print("Finished redrawing cost function.")

def plot_best():
    print("Finding the best point for this cost function. Please wait...")
    a = optimprob("hi")

    algo = pg.algorithm(pg.pso(gen=1000))
    prob = pg.problem(optimprob("name is cool"))
    pop = pg.population(prob, 100)
    pop = algo.evolve(pop)

    print(pop)
    print("Done plotting the best point")
    plt.plot(pop.champion_x[0], pop.champion_x[1], '*')


# when the canvas is pressed and released, we redraw the cost function (since it may have been a robot drag)
def on_press(event):
    if (event.dblclick):
        print("Double click registered")
        plot_best()
def on_release(event):
    print("Released mouse. Redrawing cost function. Please wait...")
    redraw_cost_function()

a = optimprob("supermeow")
figure.canvas.mpl_connect('button_press_event', on_press)
figure.canvas.mpl_connect('button_release_event', on_release)

z = np.array([[a.cost_function(xpoint=xpoint, ypoint=ypoint)[0] for xpoint in x] for ypoint in y])
p = plt.imshow(z, extent=[field.leftx, field.rightx, field.topy, field.boty], cmap="Blues")
plt.colorbar(p)
print("Double click to find best point for the cost function")
print("Drag and drop robots. The cost function will redraw automatically")


plt.show()
