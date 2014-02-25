def cf_table_size(tables, verbose=False):
    """Distance of each table from its capacity"""
    maximum = 0
    cost = 0
    for table in tables:
        if table.name != 'Head':
            distance_from_capacity = len(table.people) - int(table.capacity)
            cost += abs(distance_from_capacity)**4
            maximum = max(maximum, abs(distance_from_capacity))
            if verbose == True:
                print str(table.name) + " on " + str(table.day) + " is " + str(distance_from_capacity) + " away from optimal capacity "
    return cost
