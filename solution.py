import random
import copy
from collections import Counter
from itertools import chain, combinations

import cost_funcs.cf_same_spot as same_spot
import cost_funcs.cf_overlaps as overlaps
import cost_funcs.cf_category_balance as category_balance
import cost_funcs.cf_table_size as table_size
from seating_io import tables_to_people, days_from_tables
import config

class Solution(object):
    def __init__(self, solution):
        self.solution = solution
        self.days = days_from_tables(self.solution)

        # FREQUENCIES
        # number refers to the group size
        # do this here because it's different the first time
        # the solution is created. Later, we'll pass the 'changes_counter' argument.
        self.overlaps2_pairings = overlaps.times_each_group_sat_together(self.solution, 2)
        self.overlaps3_pairings = overlaps.times_each_group_sat_together(self.solution, 3)
        self.overlaps2_freqs = overlaps.freqs(self.overlaps2_pairings)
        self.overlaps3_freqs = overlaps.freqs(self.overlaps3_pairings)

        self.table0 = None
        self.table1 = None
        self.person0 = None
        self.person1 = None

        self.update_solution_metrics()


    def update_solution_metrics(self, switchback = False):
        # if table0, table1, person0, and person1 exist, it's because
        # this solution state was created by switching 2 people.
        # Rather than re-create the overlaps counter, we'll just modify
        # the existing one (because that's cheaper). We'll create a new
        # counter here and sum the two of them later.
        # person1 is now sitting at table0, person0 is now sitting at table1.
        if self.table0 != None \
            and self.table1 != None \
            and self.person0 != None \
            and self.person1 != None:
            if switchback == False:
                self.changes_counter2 = self._create_changes_counter(2)
                self.changes_counter3 = self._create_changes_counter(3)
            else:
                # if switching back, changes are the reverse of the previous
                # changes applied
                for (k,v) in self.changes_counter2.iteritems(): 
                    self.changes_counter2[k] = -v
                for (k,v) in self.changes_counter3.iteritems(): 
                    self.changes_counter3[k] = -v

            #self.overlaps2_pairings = self.overlaps2_pairings + self.changes_counter2
            #self.overlaps3_pairings = self.overlaps3_pairings + self.changes_counter3

        #self.overlaps2_pairings = overlaps.times_each_group_sat_together(self.solution, 2)
        #self.overlaps3_pairings = overlaps.times_each_group_sat_together(self.solution, 3)

        self.overlaps2_freqs = overlaps.freqs(self.overlaps2_pairings)
        self.overlaps3_freqs = overlaps.freqs(self.overlaps3_pairings)

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
        day_to_switch = random.choice(self.days)
        tables_that_day = [t for t in self.solution \
                           if t.day == day_to_switch and t.name != 'Head']
        tables_to_switch = random.sample(tables_that_day, 2)
        self.table0 = tables_to_switch[0]
        self.table1 = tables_to_switch[1]
        self.person0 = random.choice(self.table0.people)
        self.person1 = random.choice(self.table1.people)

        # performance optimization - pass switchback_args along in case the new solution is not
        # accepted and we need to revert 'tables' to its old state. The alternative
        # is to make a deep copy of 'tables' so that old_solution.tables and
        # new_solution.tables point at completely different things, but this was 
        # causing unacceptable performance degradation.
        self.switch_args = [self.table0, self.person0, self.table1, self.person1]
        self.switchback_args = [self.table1, self.person0, self.table0, self.person1]
        self._table_switch(*self.switch_args)
        self.update_solution_metrics()

    def move_back_from_neighbor(self):
        self._table_switch(*self.switchback_args)
        self.update_solution_metrics(switchback=True)



    def _table_switch(self, table0, person0, table1, person1):
        table0.people.remove(person0)
        table0.people.append(person1)
        table1.people.remove(person1)
        table1.people.append(person0)
        setattr(person0, table0.day, table1.name)
        setattr(person1, table0.day, table0.name)



    def _create_changes_counter(self, group_size):
        # momentarily switch back tables to previous state
        # to figure out which groupings no longer exist now that
        # people have switched
        self._table_switch(*self.switchback_args)
        ids_by_table = []

        for table in [self.table0, self.table1]:
            ids = [person.id for person in table.people]
            ids.sort()
            ids_by_table.append(ids)
        groupings_to_remove = Counter(chain.from_iterable(
            combinations(i,group_size) for i in ids_by_table))

        # switch back to current tables to figure out
        # which new groupings exist now that people have switched
        self._table_switch(*self.switch_args)
        ids_by_table = []
        for table in [self.table0, self.table1]:
            ids = [person.id for person in table.people]
            ids.sort()
            ids_by_table.append(ids)
        groupings_to_add = Counter(chain.from_iterable(
            combinations(i,group_size) for i in ids_by_table))

        # Combine the two counters. You can't just add them together
        # because the final counter will have negative values,
        # and adding the counters will cause those values to be lost.
        for (k,v) in groupings_to_remove.iteritems(): 
            groupings_to_add[k] = groupings_to_add[k] - v
            if groupings_to_add[k] == 0:
                del groupings_to_add[k]

        return groupings_to_add
