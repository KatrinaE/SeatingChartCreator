from itertools import chain, combinations
from cost_funcs.cf_category_balance import cf_category_balance
from cost_funcs.cf_new_connections import cf_avg_connections, cf_diff_in_connections
from cost_funcs.cf_overlaps import cf_overlaps
from cost_funcs.cf_same_spot import cf_same_spot
from cost_funcs.cf_table_size import cf_table_size

def cost_of(solution):
    tables_out = solution
    weights = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    #print "Cost of same spot: " + str(cf_same_spot(tables_out))
    #print "Cost of table size: " + str(cf_table_size(tables_out))
    #print "Cost of cat balance: " + str(cf_category_balance(tables_out))
    #print "Cost of overlaps: " + str(cf_overlaps(tables_out))
    #print "Cost of diff in connections: " + str(cf_diff_in_connections(tables_out))
    total_cost = weights[1] * cf_same_spot(tables_out) + \
                 weights[1] * cf_table_size(tables_out) + \
                 weights[1] * cf_category_balance(tables_out) +\
                 weights[1] * cf_overlaps(tables_out) #+ \
                 #weights[1] * cf_diff_in_connections(tables_out)
    #print "Total cost: " + str(total_cost)
    return total_cost
