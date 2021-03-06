import math
import warnings
import random
import copy

from . import config

def acceptance_probability(old_cost, new_cost, T):
    """ Function for calculating the probability of
    accepting a new solution.

    It says 'the probability density function of the solution
    moving to this new state is exp((old_cost - new_cost) / T).
    If this expression is >1, just return 1 (because you can't have
    a probability > 100%)

    This is based on the Metropolis-Hastings algorithm and based on code from:
    http://code.activestate.com/recipes/
    414200-metropolis-hastings-sampler/
    """
    try:
        warnings.simplefilter("error")
        acceptance_probability = min([1., math.exp((old_cost-new_cost)/T)])
    except RuntimeWarning:
        # neither new nor old cost is probable --> 0/0 situation, just return 0
        acceptance_probability = 0.0
    except OverflowError:
        acceptance_probability = 1
    return acceptance_probability

def anneal_at_temp(best_solution, current_solution, T):
    """
    Executes the annealing process (move to neighbor, compare costs, accept
    neighbor if new cost < old cost or if acceptance probability > random #)
    a bunch of times at the same temperature.
    """
    i = 1
    while i < config.iterations_per_temp:
        old_cost = current_solution.cost
        current_solution.move_to_neighbor()
        new_cost = current_solution.cost

        ap = acceptance_probability(old_cost, new_cost, T)
        r = random.random()

        if ap > r:
            if new_cost < best_solution.cost:
                best_solution = copy.deepcopy(current_solution)
        else:
            current_solution.move_back_from_neighbor()
        i += 1
    return best_solution, current_solution


def anneal(solution):
    """
    Applies a simulated annealing algorithm to improve the generated
    seating chart solution. Similar to hill climbing, but
    accepts moves to worse states, especially early on, to avoid
    getting trapped at a local maxima.
    """
    current_solution = solution
    best_solution = copy.deepcopy(solution)
    T = config.T
    while T > config.T_min and best_solution.cost > config.max_acceptable_cost:
        best_solution, current_solution = anneal_at_temp(best_solution,
                                                         current_solution,
                                                         T)
        T = T*config.alpha
        yield best_solution, T
    yield best_solution, T
