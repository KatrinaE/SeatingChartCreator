from collections import Counter

def imbalance(table):
    """ Calculates how far a seating arrangement deviates from optimal
    Returns a list of the form [1, 2, 3] where each number indicates the
    distance of the # of people in each category from the optimal number.
    """
    # Hack Alert! More hard-coded data
    optimal_sizes = {'Nursing' : 3 , 'Medicine': 4,'Health Administration' : 2 }
    num_by_category = Counter([ person['Category'] for person in table.people ])
    distance_list = []
    for category, optimal_size in optimal_sizes.iteritems():
        actual_size = num_by_category[category]
        distance_from_opt = abs(actual_size - optimal_size)
        distance_list.append(distance_from_opt)
    return distance_list

def cf_category_balance(tables):
    """Distance of each table from an optimum balance of professions"""
    cost = 0
    worst_imbalance = 0
    for table in tables:
        if table.name != 'Head':
            imbalances = imbalance(table)
            for category_imbalance in imbalances:
                cost += category_imbalance**4
    return cost
