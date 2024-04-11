# -*- coding: utf-8 -*-

# import required libraries
import time
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Here, the objective function is simply defined as an equation but
# more generally, it could represent natural phenomena, physical laws, or mathematical models
#   X: a 2-dimensional floating-point vector consisting of an x-value and a y-value
#   returns: a scalar floating-point value representing the output of the objective function
def objective_function(X):
    x = X[0]
    y = X[1]
    value = 3 * (1 - x) ** 2 * math.exp(-x ** 2 - (y + 1) ** 2) - 10 * (x / 5 - x ** 3 - y ** 5) * math.exp(
        -x ** 2 - y ** 2) - (1 / 3) * math.exp(-(x + 1) ** 2 - y ** 2)
    return value

# to limit the search space for this problem, we will only consider solutions
# where x ranges from -4 to 4 and y ranges from -4 to 4
lower_bounds = [-4, -4]
upper_bounds = [4, 4]

"""A 3D plot of the objective function can be viewed [here](https://c3d.libretexts.org/CalcPlot3D/index.html?type=z;z=3(1-x)%5E2*exp(-x%5E2-(y+1)%5E2)-10(x/5-x%5E3-y%5E5)*exp(-x%5E2-y%5E2)-(1/3)*exp(-(x+1)%5E2-y%5E2);visible=true;umin=-4;umax=4;vmin=-4;vmax=4;grid=30;format=normal;alpha=-1;hidemyedges=true;constcol=rgb(255,0,0);view=0;contourcolor=red;fixdomain=false;contourplot=true;showcontourplot=false;firstvalue=-1;stepsize=0.2;numlevels=11;list=;uselist=false;xnum=46;ynum=46;show2d=false;hidesurface=false;hidelabels=true;showprojections=false;surfacecontours=true;projectioncolor=rgba(255,0,0,1);showxygrid=false;showxygridonbox=false;showconstraint=false&type=window;hsrmode=3;nomidpts=true;anaglyph=-1;center=-5.2487653277286155,6.815843602039553,5.098503557610455,1;focus=0,0,0,1;up=0.39284920127083023,-0.3373981166615778,0.8554718089651412,1;transparent=false;alpha=140;twoviews=false;unlinkviews=false;axisextension=0.7;xaxislabel=x;yaxislabel=y;zaxislabel=z;edgeson=true;faceson=true;showbox=true;showaxes=true;showticks=true;perspective=true;centerxpercent=0.5;centerypercent=0.5;rotationsteps=30;autospin=true;xygrid=false;yzgrid=false;xzgrid=false;gridsonbox=true;gridplanes=false;gridcolor=rgb(128,128,128);xmin=-4;xmax=4;ymin=-4;ymax=4;zmin=-4;zmax=4;xscale=2;yscale=2;zscale=2;zcmin=-8;zcmax=8;xscalefactor=1;yscalefactor=1;zscalefactor=1;tracemode=0;keep2d=false;zoom=0.89)"""

# Let's try to randomly generate several random inputs to the objective function
# and manually observe how the outputs change with different inputs

X = np.random.uniform(lower_bounds, upper_bounds)
value = objective_function(X)
print('objective_function(%.3f, %.3f) = %.3f' % (X[0], X[1], value))

"""# Hill-climbing"""

# Hill-climbing search algorithm: a loop that continually moves in the direction of increasing value.
# It terminates when it reaches a “peak” where no neighbor has a higher value.
#   objective function: function to be maximized
#   initial_state: initial (x, y) vector
#   step_size: numerical interval by which to change the current (x,y) state to generate a new neighboring state
#   print_iters: set to True to print out the current value at each iteration
#   returns: best [x, y] solution found
def hill_climbing(objective_function, initial_state = np.array([0, 0]), step_size = 0.01, print_iters=True):
    # set the starting point of the search algorithm
    current_state = initial_state

    # loop until a peak is found
    i = 0
    while True:
        # Step 1: create a list of neighboring states to the current state
        neighbors = []
        for delta in np.identity(len(initial_state)):
            neighbors.append(current_state + step_size * delta)
            neighbors.append(current_state - step_size * delta)
        
        # Step 2: calculate the objective function at each of the neighboring states
        neighbor_values = [objective_function(neighbor) for neighbor in neighbors]

        # Step 3: determine the highest-valued neighboring state
        best_neighbor_idx = np.argmax(neighbor_values)
        best_neighbor_value = neighbor_values[best_neighbor_idx]
        best_neighbor = neighbors[best_neighbor_idx]

        # Step 4: compare the highest value among neighboring states to the current value
        #         if the latter is higher, we have found a peak -> return the current state
        #         if the former is higher, assign current state to be the best neighbor state
        current_value = objective_function(current_state)
        if best_neighbor_value <= current_value:
            if print_iters:
                print('iteration: {}, current_state: {}, current_value: {}'.format(i, current_state, current_value))
            return current_state
        else:
            current_state = best_neighbor
            if print_iters:
                print('iteration: {}, current_state: {}, current_value: {}'.format(i, current_state, best_neighbor_value))
        i += 1

hill_climbing_solution = hill_climbing(objective_function)
print('Hill climbing solution is:', hill_climbing_solution)

"""# Random Restart"""

#   Improvement to the Hill-climbing search algorithm using random restarts
#   objective function: function to be maximized
#   lower_bounds: minimum allowable values for the input vector to the objective function 
#   upper_bounds: maximum allowable values for the input vector to the objective function
#   step_size: numerical interval by which to change the current (x,y) state to generate a new neighboring state
#   num_restarts: how many times to restart hill-climbing
#   returns: best [x, y] solution found
def random_restart_hill_climbing(objective_function, lower_bounds, upper_bounds, step_size = 0.01, num_restarts=10):
    best_solution = None
    best_value = float('-inf')
    
    for i in range(num_restarts):
        # generate a random initial state within the bounds
        initial_state = np.random.uniform(lower_bounds, upper_bounds)
        
        # run the hill-climbing algorithm with the random initial state
        solution = hill_climbing(objective_function, initial_state, step_size, False)
        value = objective_function(solution)
        
        # update the best solution if necessary
        if value > best_value:
            best_solution = solution
            best_value = value
        
    return best_solution, best_value

random_restart_solution = random_restart_hill_climbing(objective_function, lower_bounds, upper_bounds)
print('Random restart hill climbing solution is:', random_restart_solution)

"""# Simulated Annealing"""

#   Simulated annealing algorithm
#   objective function: function to be maximized
#   lower_bounds: minimum allowable values for the input vector to the objective function 
#   upper_bounds: maximum allowable values for the input vector to the objective function
#   returns: best [x, y] solution found

def simulated_annealing(objective_function, lower_bounds, upper_bounds):
    # Set initial temperature
    temperature = 1.0

    # Set the cooling rate
    cooling_rate = 0.01

    # Set the current state
    current_state = np.random.uniform(lower_bounds, upper_bounds)

    # Set the best state to the current state
    best_state = current_state

    # Set the best objective value to the current objective value
    best_value = objective_function(current_state)

    # Loop until the temperature is very low
    while temperature > 1e-5:
        # Generate a new state by perturbing the current state
        new_state = current_state + np.random.normal(0, 1, size=current_state.shape) * 0.1

        # Clip the new state so that it falls within the bounds
        new_state = np.clip(new_state, lower_bounds, upper_bounds)

        # Calculate the objective value for the new state
        new_value = objective_function(new_state)

        # Calculate the energy difference between the new state and the current state
        delta = new_value - best_value

        # If the new state is better, accept it as the new current state
        if delta > 0:
            current_state = new_state
            best_value = new_value

        # If the new state is worse, accept it with some probability
        else:
            probability = np.exp(delta / temperature)
            if np.random.random() < probability:
                current_state = new_state

        # If the current state is better than the best state, update the best state
        if best_value < objective_function(best_state):
            best_state = current_state

        # Cool the system
        temperature *= 1 - cooling_rate

    # Return the best state
    return best_state, best_value

simulated_annealing_solution = simulated_annealing(objective_function, lower_bounds, upper_bounds)
print('Simulated annealing solution is:', simulated_annealing_solution)

# First-choice Hill Climbing Algorithm

def first_choice_hill_climbing(objective_function, initial_state = np.array([0, 0]), step_size = 0.01, print_iters=True):
    # set the starting point of the search algorithm
    current_state = initial_state
    current_value = objective_function(current_state)
    
    # loop until a peak is found
    i = 0
    while True:
        # Step 1: generate a random neighboring state to the current state
        next_state = current_state + np.random.uniform(-step_size, step_size, size=current_state.shape)
        
        # Step 2: evaluate the objective function at the neighboring state
        next_value = objective_function(next_state)
        
        # Step 3: if the neighboring state is better, accept it as the new current state
        if next_value > current_value:
            current_state = next_state
            current_value = next_value
        # Step 4: if the neighboring state is not better, generate another random neighboring state and try again
        else:
            continue
        
        if print_iters:
            print('iteration: {}, current_state: {}, current_value: {}'.format(i, current_state, current_value))
        i += 1
        
        # check if we have found a peak (i.e., there are no neighboring states that are better)
        num_improvements = 0
        for j in range(10):
            next_state = current_state + np.random.uniform(-step_size, step_size, size=current_state.shape)
            next_value = objective_function(next_state)
            if next_value > current_value:
                num_improvements += 1
                break
        if num_improvements == 0:
            return current_state, current_value

first_choice_solution = first_choice_hill_climbing(objective_function)
print('First-choice hill climbing solution is:', first_choice_solution)
