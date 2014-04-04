import config

def display_settings():
    print "config.anneal = " + str(config.anneal)
    print "config.random_start = " + str(config.random_start)
    print "config.random_anneal = " + str(config.random_anneal)

def display_init_cost(cost):
            print "Best init cost " + str(cost)

def display_acceptance(ap, r, new_cost, status):
    if config.verbose == True:
        if status == "ACCEPT" : 
            sym = ">"
        else: 
            sym = "<"
        print ''
        print str(status) + ": " + str(ap) + " " + sym + " > RANDOM: " + str(r)
        print "new state's cost: " + str(new_cost)

def display_cost_update(bcost):
    if config.verbose==True:
        print "changed best cost to " + str(bcost)

def progress_bar(bcost, T):
    if config.progress_bar:
        print "T is: " + str(T) + "   Best cost is: " + str(bcost)


def display_result_of_try(i, cost):
    if config.verbose == True:
        print "Final best cost for try #" + str(i) + ": " + str(cost)
