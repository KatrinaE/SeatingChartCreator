import config
from seating_io import people_objects, table_objects, write_to_csv, days_list
from build import build_guess
from anneal import anneal
from cost import cost_of
from copy import deepcopy

def main(people_csv, tables_csv):

    print "*************************************"
    print "config.anneal = " + str(config.anneal)
    print "config.random_start = " + str(config.random_start)
    print "config.random_anneal = " + str(config.random_anneal)
    people = people_objects(people_csv)
    tables = table_objects(tables_csv)
    days = days_list('tables.csv')

    i = 0
    while i < 100:
        people_copy = deepcopy(people)
        tables_copy = deepcopy(tables)
        init_guess = build_guess(people_copy, tables_copy, days)
        if config.anneal:
            final_solution = anneal(init_guess)
        else:
            final_solution = init_guess
        
        f = open('totally_random_anneal_cost_out.txt', 'a')
        f.write('\n')
        f.write(str(cost_of(final_solution)))
        i += 1

    write_to_csv(final_solution, "output.csv")
    print "************************************"

main('people.csv', 'tables.csv')
