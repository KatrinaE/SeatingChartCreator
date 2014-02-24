from collections import Counter

def cf_same_spot(tables):
    """ Cost of people sitting in same place multiple times """
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
    cost = 0
    for freq, tally in frequencies_counter.iteritems():
        if freq > 1:
            cost += (freq**4 * tally)
        #    print "Cost of ppl sitting in same spot: " + str(cost)
    return cost
