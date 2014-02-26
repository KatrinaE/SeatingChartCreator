from collections import Counter
from itertools import chain, combinations

def display_output(freq_counter):
    for (k,v) in freq_counter.iteritems():
        if k != 1:
            print str(k) + ": " + str(v)


#Thanks, stack overflow!
from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction

def nCk(n,k): 
  return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1) )

def remove_dups(c):
    # it's choose!! n choose k = (n!)/((k!)(n-k)!)
    # if they sit together twice --> counter will say once
    # if they sit together three times --> counter will say 3
    # if they sit together four times --> counter will say 6
    # it's __blank__ choose 2 because each time you compare tables, you choose 2 of them.
    c_out = {}
    for (grouping, freq) in c.iteritems():
        if freq > 1:
            print grouping, freq
            c_out[grouping] = nCk(freq, 2)
        #else:
            #c_out[grouping] = 1
    return c_out
        
def alt_times_each_group_sat_together(tables):
    """
    # 1: get list of seatmates by day (maybe use get-previous-seatmates?)
    for t in tables: loop through and populate dictionary with people they sat at
    { person-1 : { mon : [4, 2, 9, 8], tue : [1, 2, 3] }
      this is (N/n * days * n)
      where n = ppl at table
      N = total n of ppl
      N/n = # of tables per day
      days = # of days
      as opposed to (N * days * 1)
      to loop through each person and get the table.people list associated with each day
    """
    tables_sat_at = {}
    for table in tables:
        for person in table.people:
            try:
                tables_sat_at[person.id].append([p.id for p in table.people])
            except KeyError:
                tables_sat_at[person.id] = [[p.id for p in table.people]]

    # 2: for each person, perform set intersections on each of those pairs of lists
    ppl_already_visited = []
    big_counter = {}
    for (p, tables_list) in tables_sat_at.iteritems(): 
        personal_tracker = []
        num_tables = len(tables_list)
        i = 0
        while i < num_tables:
            the_table = tables_list[i]
            for j in range(i+1,num_tables):
                table = tables_list[j]
                overlapping_ppl = set.intersection(set(the_table), set(table))
                if set.intersection(overlapping_ppl, ppl_already_visited) == set() and len(overlapping_ppl) != 1:
                    personal_tracker.append(tuple(overlapping_ppl))
                j+=1
            i+=1
        c = Counter(personal_tracker)
        # Bug in here somewhere!
        ppl_already_visited.append(p)
        big_counter.update(remove_dups(c))
    pairs = [x for x in big_counter.items() if len(x[0]) == 2]
    trios = [x for x in big_counter.items() if len(x[0]) == 3]
    cost_of_pairs = sum([x[1] for x in pairs])
    cost_of_trios = sum([x[1] for x in trios])
    print cost_of_pairs
    print cost_of_trios
    return



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
