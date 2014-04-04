from itertools import chain, combinations

import config

from cost_funcs.cf_category_balance import cost as cf_category_balance
from cost_funcs.cf_new_connections import cf_avg_connections, cf_diff_in_connections
from cost_funcs.cf_overlaps import cf_overlaps
from cost_funcs.cf_same_spot import cf_same_spot
from cost_funcs.cf_table_size import cost as cf_table_size

def cost_of(solution):
    weights = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    c1 = cf_same_spot(solution)
    c2 = cf_table_size(solution)
    c3 = cf_category_balance(solution)
    c4 = cf_overlaps(solution)
    total_cost = weights[1] * c1 + \
                 weights[2] * c2 + \
                 weights[3] * c3 + \
                 weights[4] * c4
    if config.verbose == True:
        print "Cost of same spot: " + str(c1)
        print "Cost of table size: " + str(c2)
        print "Cost of cat balance: " + str(c3)
        print "Cost of overlaps: " + str(c4)
        print "Total cost: " + str(total_cost)
    return total_cost
