import random
import copy

import cost_funcs.cf_same_spot as same_spot
import cost_funcs.cf_overlaps as overlaps
import cost_funcs.cf_category_balance as category_balance
import cost_funcs.cf_table_size as table_size
from seating_io import tables_to_people
import config

class Solution(object):
    def __init__(self, solution):
        self.solution = solution
        self.update_solution_metrics()
        
    def update_solution_metrics(self):
        # FREQUENCIES
        # number refers to the group size
        self.overlaps2_freqs = overlaps.freqs(self.solution, 2)
        self.overlaps3_freqs = overlaps.freqs(self.solution, 3)
        self.same_spot_freqs = same_spot.freqs(self.solution)
        # COSTS
        self.cost_of_overlaps = overlaps.cost(self.overlaps2_freqs, 2) + \
                                overlaps.cost(self.overlaps3_freqs, 3)
        self.cost_of_same_spot = same_spot.cost(self.same_spot_freqs)
        self.cost_of_category_balance = category_balance.cost(self.solution)
        self.cost_of_table_size = table_size.cost(self.solution)
        self.cost = self.calc_cost()

    def calc_cost(self):
        cost = self.cost_of_same_spot + \
               self.cost_of_overlaps + \
               self.cost_of_category_balance + \
               self.cost_of_table_size
        return cost

    def move_to_neighbor(self):
        # Hack alert! Hard-coded
        day_to_switch = random.choice(['Mon','Tue','Wed'])#,'Thu','Fri'])
        tables_that_day = [t for t in self.solution \
                           if t.day == day_to_switch and t.name != 'Head']
        tables_to_switch = random.sample(tables_that_day, 2)
        person0 = random.choice(tables_to_switch[0].people)
        person1 = random.choice(tables_to_switch[1].people)

        # performance optimization - pass switchback_args along in case the new solution is not
        # accepted and we need to revert 'tables' to its old state. The alternative
        # is to make a deep copy of 'tables' so that old_solution.tables and
        # new_solution.tables point at completely different things, but this was 
        # causing unacceptable performance degradation.
        self.switch_args = [tables_to_switch[0], person0, tables_to_switch[1], person1]
        self.switchback_args = [tables_to_switch[1], person0, tables_to_switch[0], person1]
        self._table_switch(*self.switch_args)
        self.update_solution_metrics()

    def move_back_from_neighbor(self):
        self._table_switch(*self.switchback_args)
        self.update_solution_metrics()



    def _table_switch(self, table0, person0, table1, person1):
        table0.people.remove(person0)
        table0.people.append(person1)
        table1.people.remove(person1)
        table1.people.append(person0)
        setattr(person0, table0.day, table1.name)
        setattr(person1, table0.day, table0.name)

