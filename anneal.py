import math
import warnings
import random
import copy
from collections import Counter

import config
from cost import cost_of
from seating_io import tables_to_people


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
    

def pick_switcher(people, tables):
    if config.random_anneal:
        person_to_switch = random.choice([p for p in people 
                                          if '1' not in p.__dict__.values()])
        tables_out_to_switch = [x for x in tables if (x.day, x.name) 
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
    return person_to_switch, table_to_switch_from

def switcher_destination(tables, table_to_switch_from):
    tables_to_switch_to = [t for t in tables
                           if t is not table_to_switch_from
                           and t.name is not 'Head'
                           and t.day == table_to_switch_from.day]
    return random.choice(tables_to_switch_to)

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
    p_to_switch, t_to_switch_from = pick_switcher(people, tables_out)
    # there is a bug here somewhere. 
    t_to_switch_to = switcher_destination(tables_out, t_to_switch_from)
    random_person = random.choice(t_to_switch_to.people)
    table_switch(p_to_switch, random_person, t_to_switch_from, t_to_switch_to)
    return tables_out

def display_acceptance(ap, r, new_cost, status):
    if status == "ACCEPT" : 
        sym = ">"
    else: 
        sym = "<"
    print ''
    print str(status) + ": " + str(ap) + " " + sym + " > RANDOM: " + str(r)
    print "new state's cost: " + str(new_cost)

def anneal_at_temp(bstate, bcost, cstate, ccost, T):
    i = 1
    while i < config.iterations_per_temp:
        new_state = neighbor(cstate)
        new_cost = cost_of(new_state)

        ap = acceptance_probability(ccost, new_cost, T)
        r = random.random()

        if ap > r:
            if config.verbose==True:
                display_acceptance(ap, r, new_cost, "ACCEPT")
            cstate = new_state
            ccost = new_cost
            if ccost < bcost:
                bstate = cstate
                bcost = ccost
                if config.verbose==True:
                        print "changed best cost to " + str(bcost)
        else:
            if config.verbose==True:
                display_acceptance(ap, r, new_cost, "REJECT")
        i = i + 1
    return bstate, bcost, cstate, ccost

def progress_bar(bcost, T):
    if config.progress_bar:
        print "T is: " + str(T) + "   Best cost is: " + str(bcost)

def anneal(init_guess):
    """
    Applies a simulated annealing algorithm to improve the generated
    seating chart solution. Similar to vanilla hill climbing, but
    accepts moves to worse states, especially early on, to avoid
    getting trapped at a local maxima.
    """
    cstate = bstate = init_guess
    ccost = bcost = cost_of(init_guess)
    T = config.T
    while T > config.T_min and bcost > config.max_acceptable_cost:
        progress_bar(bcost, T)
        bstate, bcost, cstate, ccost \
            = anneal_at_temp(bstate, bcost, cstate, ccost, T)
        T = T*config.alpha

    print "The best cost found is: " + str(bcost)
    return bstate
