def cost(tables, verbose=False):
    """Distance of each table from its capacity"""
    maximum = 0
    cost = 0
    for table in tables:
        if table.name != 'Head':
            num_ppl = len(table.people)
            too_big = max(num_ppl - table.capacities['overall-max'], 0)
            too_small = max(table.capacities['overall-min'] - num_ppl, 0)
            distance = max(too_big, too_small)
            cost += distance**100000
    return cost
