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
        init_guess = build_guess(people_copy, tables_copy, days)
        import pdb; pdb.set_trace()
        init_cost = init_guess.calc_cost()
        display_init_cost(init_cost)
        """
        GUI = False
        if config.anneal and GUI == True:
            gen = anneal(init_guess)
            x = []
            y = []
            for (bstate, bcost, T) in gen:
                yield bstate, bcost, T
                progress_bar(bcost, T)
                solution = bstate
        else:
            solution = init_guess

        best_cost = min(best_cost, cost_of(solution))
        display_result_of_try(i, best_cost)

        # Write each try to its own file
        filename = "output" + str(i) + ".csv"
        write_to_csv(solution, filename)
        """
        i += 1
        print "************************************"

if __name__ == '__main__':
    main('people.csv', 'tables.csv')
