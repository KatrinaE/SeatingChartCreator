def cf_table_size(tables):
    """Distance of each table from its capacity"""
    maximum = 0
    cost = 0
    for table in tables:
        if table.name != 'Head':
            distance_from_capacity = len(table.people) - int(table.capacity)
            cost += abs(distance_from_capacity)**4
            maximum = max(maximum, abs(distance_from_capacity))

    print "Max diff btwn table size and optimum size: " + str(maximum)
    return cost
