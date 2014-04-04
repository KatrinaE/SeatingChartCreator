from collections import Counter

import config

def freqs(tables):
    all_people_ever_at_tables = {}
    for table in [table for table in tables if table.name != 'Head']:
        ids = [person.id for person in table.people]
        try:
            all_people_ever_at_tables[table.name].extend(ids)
        except KeyError: # table not yet in dict
            all_people_ever_at_tables[table.name] = ids

    frequencies = []
    for table_name, ids in all_people_ever_at_tables.iteritems():
        c = Counter(ids)
        frequencies.extend(c.values())
    frequencies_counter = Counter(frequencies)
    return frequencies_counter

def cost(frequencies_counter):
    cost = 0
    for freq, tally in frequencies_counter.iteritems():
        if freq > 1:
            cost += (freq**4 * tally)
            if config.verbose:
                print str(tally) + " people sit in the same spot " + str(freq) + " times."
    return cost


def cf_same_spot(tables):
    """ Cost of people sitting in same place multiple times """
    frequencies_counter = freqs(tables)
    return cost(frequencies_counter)
