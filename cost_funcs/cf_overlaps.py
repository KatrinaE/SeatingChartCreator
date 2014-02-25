from collections import Counter
from itertools import chain, combinations

def display_output(freq_counter):
    for (k,v) in freq_counter.iteritems():
        if k != 1:
            print str(k) + ": " + str(v)


def times_each_group_sat_together(tables, group_size):
    """
    times_each_group_sat_together has the form [((id1, id2), count), ]
    """
    ids_by_table = []
    for table in tables:
        ids_by_table.append([person.id for person in table.people])
    times_each_group_sat_together = (
        Counter(chain.from_iterable(combinations(table, group_size) 
                                    for table in ids_by_table)))
    return times_each_group_sat_together


def cost_of_overlaps(tables, group_size, verbose=False):
    freq_of_each_grouping = times_each_group_sat_together(tables, group_size)
    tally_of_freqs = []
    for grouping, freq in freq_of_each_grouping.iteritems():
        tally_of_freqs.append(freq)
    freq_of_freqs = Counter(tally_of_freqs)
    cost = 0
    for freq, num_occurrences in freq_of_freqs.iteritems():
        if freq != 1:
            cost += (freq**4 * num_occurrences)

    if cost > 0 and verbose == True:
        print ''
        print "Number of times a group of " + str(group_size) + " sits together X times: "
        display_output(freq_of_freqs)
        print "Cost of these overlaps: " + str(cost)
        print ''
    return cost

def cf_pairs(tables, verbose):
    '''cost of pairs sitting together 1, 2, 3, 4, 5 times'''
    return cost_of_overlaps(tables, 2, verbose)

def cf_trios(tables, verbose):
    """ Cost of 3 people sitting together 1, 2, 3, 4, 5 times """
    return cost_of_overlaps(tables, 3, verbose)

def cf_quads(tables, verbose):
    '''cost of 4 people sitting together 1, 2, 3, 4, 5 times'''
    return cost_of_overlaps(tables, 4, verbose)

def cf_overlaps(tables, verbose=False):
    return cf_pairs(tables, verbose) + cf_trios(tables, verbose)**3 + cf_quads(tables, verbose)**4
