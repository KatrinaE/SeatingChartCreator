from itertools import chain, combinations
from cost_funcs.cf_category_balance import cf_category_balance
#from cost.cf_new_connections import cf_newconnections
from cost_funcs.cf_overlaps import cf_overlaps
from cost_funcs.cf_same_spot import cf_same_spot
from cost_funcs.cf_table_size import cf_table_size

def cost_of(solution):
    people_out = solution[0]
    tables_out = solution[1]
    weights = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    total_cost = weights[0] * cf_same_spot(tables_out) + \
                 weights[4] * cf_table_size(tables_out) + \
                 weights[5] * cf_category_balance(tables_out) +\
                 weights[1] * cf_overlaps(tables_out)
    return total_cost
