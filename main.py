# external imports
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import AxesImage
import pygmo as pg
import geometer as geo

# user-defined imports
from world import world
from field import field


# Problem definition class for INTERMEDIATE_PASS. It is in main.py because the fitness function requires data from here
# Its purpose is to define the optimization problem for pygmo
#################################################################################################
class intermediate_pass_problem:
    def __init__(self, name, desired_point):
        self.name = name
        self.dim = 2
        self.desired_point = desired_point
        self.start_point = geo.Point(world.ball.x, world.ball.y)

    def fitness(self, x):
        return self.cost_function(xpoint=x[0], ypoint=x[1])

    def get_bounds(self):
        return [field.leftx, field.boty], [field.rightx, field.topy]

    def get_name(self):
        return self.name

    # higher is worse
    def cost_function(self, xpoint, ypoint):
        score = 0

        candidate_point = geo.Point(xpoint, ypoint)
        intermediate_can_reach_desired = world.can_reach(candidate_point, self.desired_point)
        start_can_reach_intermediate = world.can_reach(self.start_point, candidate_point)
        if main_field.in_defense_area(xpoint, ypoint) or not start_can_reach_intermediate or not intermediate_can_reach_desired:
            score = 300
            return [score]

        bot, dist = world.their_closest_robot_to_point(xpoint, ypoint)
        score += -100 * dist

        ourbot, ourdist = world.our_closest_robot_to_point(xpoint, ypoint)
        score += 100 * ourdist

        shoot_succes_reward = bot.shoot_from_pos(xpoint, ypoint)
        score += -shoot_succes_reward * 2
        score += field.distance_to_enemy_goal(field, xpoint, ypoint)
        return [score]


#################################################################################################
# Problem definition class for BEST_LOCATION. It is in main.py because the fitness function requires data from here
# Its purpose is to define the optimization problem for pygmo
#################################################################################################
class best_location_problem:
    def __init__(self, name):
        self.name = name
        self.dim = 2

    def fitness(self, x):
        return self.cost_function(xpoint=x[0], ypoint=x[1])

    def get_bounds(self):
        return ([field.leftx, field.boty], [field.rightx, field.topy])

    def get_name(self):
        return self.name

    # higher is worse
    def cost_function(self, xpoint, ypoint):
        score = 0
        if main_field.in_defense_area(xpoint, ypoint) or not world.can_reach(geo.Point(xpoint, ypoint),
                                                                             geo.Point(field.rightx, 0)):
            score = 300
            return [score]

        bot, dist = world.their_closest_robot_to_point(xpoint, ypoint)
        score += -100 * dist

        ourbot, ourdist = world.our_closest_robot_to_point(xpoint, ypoint)
        score += 100 * ourdist

        shoot_succes_reward = bot.shoot_from_pos(xpoint, ypoint)
        score += -shoot_succes_reward * 2
        score += field.distance_to_enemy_goal(field, xpoint, ypoint)
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
N = 30
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


def find_best():
    print("Finding the best point for this cost function. Please wait...")
    a = best_location_problem("best_location")

    algo = pg.algorithm(pg.pso(gen=10))
    prob = pg.problem(best_location_problem("name is cool"))
    pop = pg.population(prob, 10)
    pop = algo.evolve(pop)

    print(pop)
    print("Done plotting the best point")

    return [pop.champion_x[0], pop.champion_x[1]]


def find_intermediate(desired_point):
    # pro = intermediate_pass_problem("intermediate_pass", desired_point)

    algo = pg.algorithm(pg.pso(gen=10))
    prob = pg.problem(intermediate_pass_problem("intermediate_pass", desired_point))
    pop = pg.population(prob, 10)
    pop = algo.evolve(pop)

    print(pop)
    print("Done plotting the best point")
    return [pop.champion_x[0], pop.champion_x[1]]


# when the canvas is pressed and released, we redraw the cost function (since it may have been a robot drag)
def on_press(event):
    if (event.dblclick):
        print("Double click registered")
        best = find_best()
        inter = find_intermediate(geo.Point(best[0], best[1]))
        plt.plot(best[0], best[1], '*')
        plt.plot(inter[0], inter[1], '*')


def on_release(event):
    for robot in world.robots:
        if robot.press == True:
            print("Released mouse. Redrawing cost function. Please wait...")
            redraw_cost_function()




figure.canvas.mpl_connect('button_press_event', on_press)
figure.canvas.mpl_connect('button_release_event', on_release)

a = best_location_problem("supermeow")
z = np.array([[a.cost_function(xpoint=xpoint, ypoint=ypoint)[0] for xpoint in x] for ypoint in y])
p = plt.imshow(z, extent=[field.leftx, field.rightx, field.topy, field.boty], cmap="Blues")
plt.colorbar(p)
plt.show()

print("Double click to find best point for the cost function")
print("Drag and drop robots. The cost function will redraw automatically")
