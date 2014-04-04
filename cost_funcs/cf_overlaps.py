from collections import Counter
from itertools import chain, combinations

import config

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

def freqs(tables, group_size):
    freq_of_each_grouping = times_each_group_sat_together(tables, group_size)
    tally_of_freqs = []
    for grouping, freq in freq_of_each_grouping.iteritems():
        tally_of_freqs.append(freq)
    freq_of_freqs = Counter(tally_of_freqs)
    return freq_of_freqs

def cost(freqs, group_size):
    cost = 0
    for freq, num_occurrences in freqs.iteritems():
        if freq != 1:
            cost += (freq**4 * num_occurrences)

    if cost > 0 and config.verbose:
        print ''
        print "Number of times a group of " + str(group_size) + " sits together X times: "
        display_output(freqs)
        print "Cost of these overlaps: " + str(cost)
        print ''
    return cost
