from collections import Counter
from itertools import chain, combinations

def add_to_connections_tally(tally, pair):
    """ Given a pair of people (IDs) who sit together 1+ times, adds one 
    to the overall tally of how many others each person has sat with """
    for person in pair:
        # Hack Alert! ids 32 & 33 sit @ head table every day
        if person not in (32, 33):
            try:
                tally[person] += 1
            except KeyError:
                tally[person] = 1        
    return tally

def calc_connections(tables):
    """ Creates a dict of how many new people each person (ID) sat with.
    e.g. { 1 : 35, 2: 30 }
    """
    freq_of_each_pair = times_each_group_sat_together(tables, 2)
    num_sat_with = {}

    for pair in freq_of_each_pair.keys():
        num_sat_with = add_to_connections_tally(num_sat_with, pair)
    return num_sat_with

def cf_diff_in_connections(tables):
    """Connections = number of new people met over the course of the week.
    This is the difference in the number of connections between the person
    who made the most and the person who made the least."""

    num_sat_with = calc_connections(tables)
    person_who_made_fewest_connections = min(num_sat_with, key = num_sat_with.get)
    min_sat_with = num_sat_with[person_who_made_fewest_connections]

    person_who_made_most_connections = max(num_sat_with, key = num_sat_with.get)
    max_sat_with = num_sat_with[person_who_made_most_connections]

    cost = max_sat_with - min_sat_with
    print "Diff btwn  most connections & fewest connections: " + str(cost)
    return cost

def mean(nums):
    if len(nums):
        return float( sum(nums) / len(nums))
    else:
        return 0.0


def cf_avg_connections(tables):
    """ Average number of new people each person sits with all week """
    num_sat_with_dict = calc_connections(tables)
    avg_connections = mean(num_sat_with_dict.values())
    print "Avg num connections: " + str(avg_connections)
    return avg_connections
