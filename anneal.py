#from math import *
#import math

from matplotlib.pylab import *
from collections import Counter

from cost import cost_of
from seating_io import tables_to_people
import warnings
import random
from scipy.stats import norm

import config
import copy

def norm_pdf(z):
    """
    Standard normal pdf (Probability Density Function)
    
    pdf is a point value: how dense is the probability at a 
    given point z? See
    http://docs.scipy.org/doc/scipy/reference/generated/
    scipy.stats.norm.html
    """
    prob = norm.pdf(z, scale=1500)
    return prob
    
def acceptance_probability(old_cost, new_cost, T):
    """ Metropolis-Hastings probability function for deciding 
    whether or not to accept a new solution. Based on code from: 
    http://code.activestate.com/recipes/
    414200-metropolis-hastings-sampler/
    """
    try:
        warnings.simplefilter("error")
        acceptance_probability = min([1.,math.exp((old_cost-new_cost)/T)])
    except RuntimeWarning:
        # neither new nor old cost is probable --> 0/0 situation, just return 0
        acceptance_probability = 0.0
    except OverflowError:
        acceptance_probability = 1
    return acceptance_probability
        
def persons_tables(person):
    # Hack Alert! Hard-coded
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    tables = [table for (day, table) in \
              person.__dict__.iteritems() if day in days \
              ]
    return tables

def saddest_person(people):
    fewest_tables_sat_at = float('inf')
    for person in people:
        tables = persons_tables(person)
        num_tables_sat_at = len(set(tables))
        num_times_at_head_table = len([t for t in tables if t == '1'])
        if num_times_at_head_table < 5:
            revised_num_sat_at = num_tables_sat_at + \
                             num_times_at_head_table -1
            if revised_num_sat_at < fewest_tables_sat_at:
                saddest_person = person
                fewest_tables_sat_at = num_tables_sat_at
    return saddest_person

def most_freq_table(person):
    tables = persons_tables(person)
    excluding_head = [t for t in tables if t is not '1']
    c = Counter(excluding_head)
    reoccuring_table_tuple = c.most_common(1)[0]
    return reoccuring_table_tuple
    
def table_switch(person_to_switch, random_person, table_to_switch_from, table_to_switch_to):
    table_to_switch_from.people.remove(person_to_switch)
    table_to_switch_from.people.append(random_person)
    table_to_switch_to.people.remove(random_person)
    table_to_switch_to.people.append(person_to_switch)
    setattr(person_to_switch, table_to_switch_from.day, table_to_switch_to.name)
    setattr(random_person, table_to_switch_from.day, table_to_switch_from.name)

def neighbor(tables):
    tables_out = copy.deepcopy(tables)
    people = tables_to_people(tables_out, output_format = 'objects')

    if config.random_anneal:
        person_to_switch = random.choice([p for p in people 
                                          if '1' not in p.__dict__.values()])
        tables_out_to_switch = [x for x in tables_out if (x.day, x.name) 
                            in person_to_switch.__dict__.items()]
        table_to_switch_from = random.choice(tables_out_to_switch)

    else: 
        person_to_switch = saddest_person(people)
        bad_table_tuple = most_freq_table(person_to_switch)
        bad_table_all_days = [t for t in tables_out
                             if t.name == bad_table_tuple[0]
                              and t.name != '1'
                             and person_to_switch in t.people]
        try:
            table_to_switch_from = random.choice(bad_table_all_days)
        except:
            import ipdb; ipdb.set_trace()

    # there is a bug here somewhere. 
    tables_out_to_switch_to = [t for t in tables_out
                           if t is not table_to_switch_from
                           and t.name is not 'Head'
                           and t.day == table_to_switch_from.day]
    table_to_switch_to = random.choice(tables_out_to_switch_to)
    random_person = random.choice(table_to_switch_to.people)
    table_switch(person_to_switch, random_person, table_to_switch_from, table_to_switch_to)
    return tables_out

def temp(iteration, max_iterations):
    return max_iterations/(iteration+1)**4

def anneal(init_guess, verbose=False):
    """
    Applies a simulated annealing algorithm to improve the generated
    seating chart solution. Similar to vanilla hill climbing, but
    accepts moves to worse states, especially early on, to avoid
    getting trapped at a local maxima.
    
    This is an implementation of pseudocode at: 
    https://en.wikipedia.org/wiki/Simulated_annealing#Pseudocode
    """
    print "The cost @ start of annealing is " + str(cost_of(init_guess))
    max_acceptable = 0
    curr_state = init_guess
    curr_cost = cost_of(init_guess)
    best_state = init_guess
    best_cost = curr_cost
    T = 1
    alpha = 0.95
    T_min = .001
    while T > T_min and best_cost > max_acceptable:
        if verbose:
            print "T is: " + str(T)
        i = 1
        while i < 100:
            new_state = neighbor(curr_state)
            new_cost = cost_of(new_state)

            ap = acceptance_probability(curr_cost, new_cost, T)
            r = random.random()


            if ap > r:
                if verbose==True:
                    print ''
                    print "ACCEPT: " + str(ap) + " > RANDOM: " + str(r)
                    print "new state's cost: " + str(new_cost)
                curr_state = new_state
                curr_cost = new_cost
                if curr_cost < best_cost:
                    best_state = curr_state
                    best_cost = curr_cost
                    if verbose==True:
                        print "changed best cost to " + str(best_cost)

            else:
                if verbose==True:
                    print ''
                    print "REJECT: " + str(ap) + " < RANDOM: " + str(r)
                    print "new state's cost: " + str(new_cost)
            i = i + 1
        T = T*alpha

    print "The best cost found is: " + str(best_cost)
    return best_state
