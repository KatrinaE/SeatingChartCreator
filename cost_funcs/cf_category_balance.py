from collections import Counter

def imbalance(table, verbose):
    """ Calculates how far a seating arrangement deviates from optimal
    Returns a list of the form [1, 2, 3] where each number indicates the
    distance of the # of people in each category from the optimal number.
    """
    # Hack Alert! More hard-coded data
    optimal_sizes = {'Nursing' : 3 , 'Medicine': 4,'Health Administration' : 2 }
    num_by_category = Counter([ person.category for person in table.people ])
    distance_list = []
    for category, optimal_size in optimal_sizes.iteritems():
        actual_size = num_by_category[category]
        distance_from_opt = abs(actual_size - optimal_size)
        distance_list.append(distance_from_opt)

    return distance_list

def cf_category_balance(tables, verbose=False):
    """Distance of each table from an optimum balance of professions"""
    cost = 0
    worst_imbalance = 0
    for table in tables:
        if table.name != 'Head':
            table_cost = 0
            imbalances = imbalance(table, verbose)
            for category_imbalance in imbalances:
                table_cost += category_imbalance**4
            cost += table_cost
            
            if verbose == True and table_cost > 0:
                print "On " + str(table.day) + ", " + str(table.name) + " has a category imbalance cost of " + str(table_cost)
                num_by_category = Counter([ person.category for person in table.people ]) 
                list_of_tups = [(k,v) for (k,v) in num_by_category.iteritems()]
                list_of_colons =  [(str(t[0]) + ': ' + str(t[1])) for t in list_of_tups]
                for category in list_of_colons:
                    print category
                print ''
    return cost
