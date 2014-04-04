from copy import deepcopy

import config
from seating_io import people_objects, table_objects, write_to_csv, days_list
from build import build_guess
from anneal import anneal
from cost import cost_of
from display_messages import display_settings, display_init_cost, \
    display_result, display_progress_bar
from solution import Solution

def main(people_csv, tables_csv):

    if config.verbose:
        print "*************************************"
        display_settings()
    people = people_objects(people_csv)
    tables = table_objects(tables_csv)
    days = days_list(tables_csv)

    people_copy = deepcopy(people)
    tables_copy = deepcopy(tables)
    init_solution = build_guess(people_copy, tables_copy, days)

    if config.verbose:
        display_init_cost(init_solution.cost)

    if config.anneal:
        gen = anneal(init_solution)
        for (best_solution, T) in gen:
            yield best_solution, T
            if config.progress_bar:
                display_progress_bar(best_solution.cost, T)
    else:
        best_solution = init_solution

    # Write to file
    filename = "output.csv"
    write_to_csv(best_solution.solution, filename)

    if config.verbose:
        display_result(best_solution.cost)
        print "************************************"

if __name__ == '__main__':
    main('people.csv', 'tables.csv')
