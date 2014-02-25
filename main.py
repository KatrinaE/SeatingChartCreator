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
    best_cost = float('inf')
    while i < 10:
        people_copy = deepcopy(people)
        tables_copy = deepcopy(tables)
        init_guess = build_guess(people_copy, tables_copy, days)
        c = cost_of(init_guess)
        #if c < best_cost: 
            #best_cost = c
            #best_init_sol = solution = init_guess
        
        if config.anneal:
            print "best init cost " + str(c)
            print "Annealing best init solution"
            solution = anneal(init_guess)
            best_cost = cost_of(solution)

        print "Final best cost on iteration " + str(i) + ": " + str(cost_of(solution, verbose=True))
        filename = "output" + str(i) + ".csv"
        write_to_csv(solution, filename)

        i += 1

        # f = open('totally_greedy_anneal_cost_out.txt', 'a')
        # f.write('\n')
        # f.write(str(c))
        print "************************************"

#main('people.csv', 'tables.csv')
