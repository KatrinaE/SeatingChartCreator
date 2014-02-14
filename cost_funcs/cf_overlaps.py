from collections import Counter
from itertools import chain, combinations

def display_output(freq_counter):
    for (k,v) in freq_counter.iteritems():
        if k != 1:
            print str(k) + ": " + str(v)

def get_id_lists(tables):
    """ Returns list of ids of people sitting at a set of tables, e.g. 
    [[1,2,3], [4,5,6]] """
    ids_by_table = []
    for table in tables:
        ids_by_table.append([person['id'] for person in table.people])
    return ids_by_table

def times_each_group_sat_together(tables, group_size):
    """
    times_each_group_sat_together has the form [((id1, id2), count), ]
    """
    ids_by_table = get_id_lists(tables)
    times_each_group_sat_together = (
        Counter(chain.from_iterable(combinations(table, group_size) 
                                    for table in ids_by_table)))
    return times_each_group_sat_together

def create_tally(freq_by_group):
    """ Creates an overall tally of the number of groups that have sat 
    together 1x, 2x, etc. """
    tally = []
    for freq in freq_by_group.values():
        tally.append(freq)
    return tally
    
def cost_of_times_together(tables, group_size):
    freq_of_each_grouping = times_each_group_sat_together(tables, group_size)
    tally = create_tally(freq_of_each_grouping)
    summed_tally = Counter(tally)

    cost = 0
    for freq, tally in summed_tally.iteritems():
        if freq != 1:
            cost += (freq**4 * tally)
    return cost

    if cost > 0:
        print "Number of times a group of " + str(group_size) + " sits together X times: "
        display_output(summed_tally)

    return cost

def cf_pairs(tables):
    '''cost of pairs sitting together 1, 2, 3, 4, 5 times'''
    return cost_of_times_together(tables, 2)

def cf_trios(tables):
    """ Cost of 3 people sitting together 1, 2, 3, 4, 5 times """
    return cost_of_times_together(tables, 3)

def cf_quads(tables):
    '''cost of 4 people sitting together 1, 2, 3, 4, 5 times'''
    return cost_of_times_together(tables, 4)
