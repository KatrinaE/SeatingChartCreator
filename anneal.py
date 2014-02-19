from math import *
from matplotlib.pylab import *
from collections import Counter

from cost import cost_of
from seating_io import tables_to_people

import random
from scipy.stats import norm

def norm_pdf(z):
    """
    Standard normal pdf (Probability Density Function)
    
    pdf is a point value: how dense is the probability at a 
    given point z? See
    http://docs.scipy.org/doc/scipy/reference/generated/
    scipy.stats.norm.html
    """
    return norm.pdf(z, scale=1500)

def acceptance_probability(old_guess, old_cost, new_guess, new_cost, 
                           temp):
    """ Metropolis-Hastings probability function for deciding 
    whether or not to accept a new solution. Based on code from: 
    http://code.activestate.com/recipes/
    414200-metropolis-hastings-sampler/
    """
    acceptance_probability = min\
                             ([1.,norm_pdf(new_cost)/norm_pdf(old_cost)])
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
        revised_num_sat_at = num_tables_sat_at + \
                             num_times_at_head_table -1
        if revised_num_sat_at < fewest_tables_sat_at:
            saddest_person = person
            fewest_tables_sat_at = num_tables_sat_at
    return saddest_person

def most_freq_table(person):
    tables = persons_tables(person)
    c = Counter(tables)
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

    """
    Need to find good way to reduce diameter of search graph!!
    Also need to understand what barrier avoidance is.
    """
    people = tables_to_people(tables, output_format = 'objects')
    person_to_switch = saddest_person(people)

    # this is the bad part!
    bad_table_tuple = most_freq_table(person_to_switch)
    bad_table_all_days = [t for t in tables
                             if t.name == bad_table_tuple[0]
                             and person_to_switch in t.people]
    table_to_switch_from = random.choice(bad_table_all_days)
    tables_to_switch_to = [t for t in tables
                           if t is not table_to_switch_from
                           and t.name is not 'Head'
                           and t.day == table_to_switch_from.day]
    table_to_switch_to = random.choice(tables_to_switch_to)
    random_person = random.choice(table_to_switch_to.people)
    table_switch(person_to_switch, random_person, table_to_switch_from, table_to_switch_to)
    return tables

def temp(iteration, max_iterations):
    return max_iterations/(iteration+1)**4

def anneal(init_guess):
    """
    Applies a simulated annealing algorithm to improve the generated
    seating chart solution. Similar to vanilla hill climbing, but
    accepts moves to worse states, especially early on, to avoid
    getting trapped at a local maxima.
    
    This is an implementation of pseudocode at: 
    https://en.wikipedia.org/wiki/Simulated_annealing#Pseudocode
    """

    max_acceptable_cost = 2000
    current_state = best_state = init_guess
    current_cost = best_cost = cost_of(init_guess)
    i = 0
    imax = 100
    while i < imax and best_cost > max_acceptable_cost:
        pass
        T = temp(i, imax)
        new_state = neighbor(current_state)
        new_cost = cost_of(new_state)
        ap = acceptance_probability(current_state, current_cost, new_state, new_cost, T)
        r = random.random()
        if ap > r:
            print "ACCEPT: " + str(ap) + " > RANDOM: " + str(r)
            current_state = new_state
            current_cost = new_cost
            if current_cost < best_cost:
                best_state = current_state
                best_cost = current_cost
                print "changed best cost to " + str(best_cost)
                print ''
        else:
            print "FAILED TO ACCEPT"
        i += 1
    print "The best cost found is: " + str(best_cost)
    return best_state
