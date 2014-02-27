from copy import deepcopy

import config
from seating_io import people_objects, table_objects, write_to_csv, days_list
from build import build_guess
from anneal import anneal
from cost import cost_of
from display_messages import display_settings, display_init_cost, display_cost_after_iteration

def main(people_csv, tables_csv):

    print "*************************************"
    display_settings()
    people = people_objects(people_csv)
    tables = table_objects(tables_csv)
    days = days_list(tables_csv)
    i = 0
    best_cost = float('inf')
    while i < config.num_tries:
        people_copy = deepcopy(people)
        tables_copy = deepcopy(tables)
        init_guess = build_guess(people_copy, tables_copy, days)
        cost = cost_of(init_guess)
        display_init_cost(cost)

        if config.anneal:
            solution = anneal(init_guess)
        else:
            solution = init_guess

        best_cost = cost_of(solution)
        display_cost_after_iteration(i, best_cost)

        filename = "output" + str(i) + ".csv"
        write_to_csv(solution, filename)

        i += 1
        print "************************************"

main('people.csv', 'tables.csv')
