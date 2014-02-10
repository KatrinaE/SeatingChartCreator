from collections import Counter
from itertools import chain, combinations


def most_days_at_one_table(person):
    days = [k for k in person.keys() if k not in ('First Name', 'Last Name', 'id', 'Category')]
    sits_at = [v for (k, v) in person.iteritems() if k in days]
    excluding_head_table = [x for x in sits_at if x != 'Head']
    sits_at_freq = Counter(excluding_head_table)
    max_freq = max(sits_at_freq.values())
    return max_freq

def calc_cost(counter, weights):
    cost = 0
    for (freq, count) in counter.items():
        cost += count * weights[freq]
    return cost

def display_output(freq_counter):
    for (k,v) in freq_counter.iteritems():
        if k != 1:
            print str(k) + ": " + str(v)

def cf_location(people):
    """ Cost of people sitting in same place multiple times """
    max_freq_tally = []
    for p in people:
        max_freq = most_days_at_one_table(p)
        max_freq_tally.append(max_freq)
    max_freq_counter = Counter(max_freq_tally)
    weights = { 1:0, 2:1, 3:10, 4:100, 5:1000 }
    cost = calc_cost(max_freq_counter, weights)

    print "Number of times a person sits at each of his/her tables: "
    display_output(max_freq_counter)

    return cost

def get_id_lists(tables):
    """ Returns list of ids of ppl sitting at a set of tables, e.g. 
    [[1,2,3], [4,5,6]] """
    ids_by_table = []
    for t in tables:
        t_by_day = [ day_info for (day, day_info) in t.iteritems() \
                     if day != 'Table Name']
        for day in t_by_day:
            ids_at_t = [ x[0] for x in day['ppl'] ]
            ids_by_table.append(ids_at_t)
    return ids_by_table

def times_each_group_sat_together(tables, group_size):
    ids_by_table = get_id_lists(tables)
    times_each_group_sat_together = Counter(chain.from_iterable(combinations(\
                            table, group_size) for table in ids_by_table))
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
    weights = { 1:0, 2:1, 3:10, 4:100, 5:1000 }    
    cost = calc_cost(summed_tally, weights)

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

def diff_from_opt_size(table):
    return len(table['ppl']) - int(table['opt'])

def update_max(maximum, new_item):
    if new_item  > maximum:
        maximum = new_item
    return maximum

def cf_table_size(tables):
    """Distance of each table from its optimum size"""
    maximum = 0
    cost = 0
    for t in tables:
        if t['Table Name'] != 'Head':
            for (day, table) in t.iteritems():
                if day != 'Table Name':
                    distance_from_opt = diff_from_opt_size(table)
                    cost += abs(distance_from_opt)
                    maximum = update_max(maximum, abs(distance_from_opt))

    print "Max diff btwn table size and optimum size: " + str(maximum)
    return cost

def imbalance_by_category(table, optimal_sizes):
    """ Calculates how far a seating arrangement deviates from the optimal
    balance of people in each category. Expects a list (optimal_sizes)
    of sets. Each set contains a category (e.g. 'Nursing') and the number of
    desired people in that category (e.g. 3). Returns a list of integers
    relating the distance from optimal for each category, e.g. [1, 2, 3]
    """
    tally_num_ppl_in_each_cat = [ x[1] for x in table['ppl'] ]
    summed_tally = Counter(tally_num_ppl_in_each_cat)
        
    distance_list = []
    for category in optimal_sizes:
        cat_distance = abs(summed_tally[category[0]] - category[1])
        if cat_distance >= 3:
            print category
            print cat_distance
            print summed_tally
        distance_list.append(cat_distance)
    return distance_list

def calc_max_cat_imbalance(table):
    """ Calculates how far a seating arrangement deviates from optimal,
    specifically how far the number of people in the least-optimal
    category deviates from that category's optimal number.
    """
    optimal_sizes = [('Nursing', 3), ('Medicine', 4), ('Health Administration', 2)]
    imbalance_of_each_cat = imbalance_by_category(table, optimal_sizes)
    return max(imbalance_of_each_cat)

def calc_overall_imbalance(table):
    """ Calculates how far a seating arrangement deviates from optimal
    by summing the distances between the optimal number in each category
    and the actual number in that category."""
    optimal_sizes = [('Nursing', 3), ('Medicine', 4), ('Health Administration', 2)]
    cost = imbalance_by_category(table, optimal_sizes)
    return sum(cost)

def cf_balance(tables):
    """Distance of each table from an optimum balance of professions"""
    cost = 0
    maximum = 0
    for t in tables:
        print t['Table Name']
        if t['Table Name'] != 'Head':
            for (day, table) in t.iteritems():
                if day != 'Table Name':
                    max_imbalance_at_table = calc_max_cat_imbalance(table)
                    maximum = update_max(maximum, max_imbalance_at_table)
                    cost_of_table_imbalance = calc_overall_imbalance(table)
                    cost += cost_of_table_imbalance
    print "Max distance from optimal # in cat: " + str(maximum)
    return cost

def add_to_connections_tally(tally, pair):
    """ Given a pair of people (IDs) who sit together 1+ times, adds one 
    to the overall tally of how many others each person has sat with """
    for person in pair:
        # ids 32 & 33 sit @ head table every day
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

def cost_of(solution):
    people_out = solution[0]
    tables_out = solution[1]
    weights = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    total_cost = weights[0] * cf_location(people_out) + \
                 weights[1] * cf_pairs(tables_out) + \
                 weights[2] * cf_trios(tables_out) + \
                 weights[3] * cf_quads(tables_out) + \
                 weights[4] * cf_table_size(tables_out) + \
                 weights[5] * cf_balance(tables_out) + \
                 weights[6] * cf_diff_in_connections(tables_out) + \
                 weights[7] * cf_avg_connections(tables_out)
    return total_cost
