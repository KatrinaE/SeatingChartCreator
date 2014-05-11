import time
from ..seating_io import people_objects, table_objects, days_list
from ..build import build_guess
from cf_category_balance import cost
from cf_same_spot import cf_same_spot
# turning this off for now because there's no more function with this name
#from cf_overlaps import cf_overlaps, alt_times_each_group_sat_together

def get_random_solution():
    people = people_objects('seating/people.csv')
    tables = table_objects('seating/tables.csv')
    days = days_list('seating/tables.csv')
    solution = build_guess(people, tables, days)
    return solution

def timing(func):
    sol = get_random_solution()
    print func.__name__
    t0 = time.time()
    func(sol)
    print time.time() - t0

#timing(alt_times_each_group_sat_together)
timing(cf_category_balance)
timing(cf_same_spot)
#timing(cf_overlaps)
