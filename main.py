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
        if c < best_cost: 
            best_cost = c
            best_init_sol = solution = init_guess
        i += 1
        
    if config.anneal:
        print "best init cost " + str(best_cost)
        print "Annealing"
        solution = anneal(best_init_sol)
        best_cost = cost_of(solution)

       # f = open('totally_greedy_anneal_cost_out.txt', 'a')
       # f.write('\n')
       # f.write(str(c))

    print "Final best cost is: " + str(best_cost)
    write_to_csv(solution, "output.csv")
    print "************************************"

main('people.csv', 'tables.csv')
