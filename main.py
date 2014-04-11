from copy import deepcopy

import config
from seating_io import people_objects, table_objects, write_to_csv_2, days_list
from build import build_guess
from anneal import anneal
from display_messages import display_settings, display_init_cost, \
    display_result, display_progress_bar
from solution import Solution

def main(people_csv, tables_csv):
    print 'mom'
    if config.verbose:
        print "*************************************"
        display_settings()
    print 'bar'
    people = people_objects(people_csv)
    tables = table_objects(tables_csv)
    days = days_list(tables_csv)
    print 'baz'
    people_copy = deepcopy(people)
    tables_copy = deepcopy(tables)
    init_solution = build_guess(people_copy, tables_copy, days)
    
    print 'foo'
    best_solution = all_time_greatest = init_solution
    for i in range(0, config.num_tries):
        people_copy = deepcopy(people)
        tables_copy = deepcopy(tables)
        init_solution = build_guess(people_copy, tables_copy, days)

        if config.verbose:
            display_init_cost(init_solution.cost)

        if (config.anneal and config.GUI):
            gen = anneal(init_solution)
            for (best_solution, T) in gen:
                yield best_solution, T
                if config.progress_bar:
                    display_progress_bar(best_solution.cost, T)
        
        if (config.anneal and config.GUI == False):
            gen = anneal(init_solution)
            for (best_solution, T) in gen:
                display_progress_bar(best_solution.cost, T)
                #print "Number of pairs who sit together multiple times: " + \
                #    str(best_solution.overlaps2_freqs)
                #print "Number of people who sit in the same spot multiple times: " + \
                #    str(best_solution.same_spot_freqs)

        else:
                best_solution = init_solution
        """
        print "The best cost found is: " + str(best_solution.cost)
        print "The state info is: "
        print "Pairs overlapping: " + str(best_solution.overlaps2_freqs)
        print "Trios overlapping: " + str(best_solution.overlaps3_freqs)
        print "Same spots: " + str(best_solution.same_spot_freqs)
        print "Category balance: " + str(best_solution.cost_of_category_balance)
        print "Table size: " + str(best_solution.cost_of_table_size)
        """
        if best_solution.cost < all_time_greatest.cost:
            all_time_greatest = best_solution
    print "ALL TIME GREATEST"
    print "The best cost found is: " + str(all_time_greatest.cost)
    print "The state info is: "
    print "Pairs overlapping: " + str(all_time_greatest.overlaps2_freqs)
    print "Trios overlapping: " + str(all_time_greatest.overlaps3_freqs)
    print "Same spots: " + str(all_time_greatest.same_spot_freqs)
    print "Category balance: " + str(all_time_greatest.cost_of_category_balance)
    print "Table size: " + str(all_time_greatest.cost_of_table_size)

    # Write to file
    filename = "output.csv"
    write_to_csv_2(all_time_greatest.solution, days, filename)

    if config.verbose:
        display_result(best_solution.cost)
        print "************************************"

if __name__ == '__main__':
    print 'foo'
    import pdb; pdb.set_trace()
    main('people.csv', 'tables.csv')
    print 'hi'
