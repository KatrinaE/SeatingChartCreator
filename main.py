from copy import deepcopy

import config
from seating_io import people_objects, table_objects, write_to_csv, days_list
from build import build_guess
from anneal import anneal
from cost import cost_of
from display_messages import display_settings, display_init_cost, display_result_of_try, progress_bar
from solution import Solution

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
        init_solution = build_guess(people_copy, tables_copy, days)

        if config.verbose:
            display_init_cost(init_solution.cost)

        if config.anneal:
            gen = anneal(init_solution)
            x = []
            y = []
            for (best_state, T) in gen:
                yield best_state, T
                progress_bar(best_state.cost, T)
                solution = best_state
        else:
            solution = init_solution

        best_cost = min(best_cost, best_state.cost)
        display_result_of_try(i, best_state.cost)

        # Write each try to its own file
        filename = "output" + str(i) + ".csv"
        write_to_csv(solution.solution, filename)

        i += 1
        print "************************************"

if __name__ == '__main__':
    main('people.csv', 'tables.csv')
