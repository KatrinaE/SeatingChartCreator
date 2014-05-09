import config

def print_settings():
    if config.verbose:
        print "config.anneal = " + str(config.anneal)
        print "config.greedy_start = " + str(config.greedy)

def print_init_cost(cost):
    if config.verbose:
        print "Best init cost " + str(cost)

def print_acceptance(ap, r, new_cost, status):
    if config.super_verbose:
        if status == "ACCEPT" : 
            sym = ">"
        else: 
            sym = "<"
        print ''
        print str(status) + ": " + str(ap) + " " + sym + " > RANDOM: " + str(r)
        print "new state's cost: " + str(new_cost)

def print_cost_update(bcost):
    if config.super_verbose:
        print "changed best cost to " + str(bcost)

def print_progress(solution, T):
    if config.display_progress:
        print "T is: " + str(T) + "   Best cost is: " + str(solution.cost)

def print_final_metrics(best_solution):
    print "FINAL SOLUTION"
    print "The best cost found is: " + str(best_solution.cost)
    print "Pairs overlapping: " + str(best_solution.overlaps2_freqs)
    print "Trios overlapping: " + str(best_solution.overlaps3_freqs)
    print "Same spot twice: " + str(best_solution.same_spot_freqs[2])
    print "Same spot three times: " + str(best_solution.same_spot_freqs[3])
    print "Category balance: " + str(best_solution.cost_of_category_balance)
    print "Table size: " + str(best_solution.cost_of_table_size)
