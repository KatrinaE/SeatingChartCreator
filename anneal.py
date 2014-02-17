from cost import cost_of

def anneal(init_solution):
	x = cost_of(init_solution)
	return init_solution[0]
