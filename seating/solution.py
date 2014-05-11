import random

from .cost_funcs import cf_same_spot as same_spot
from .cost_funcs import cf_overlaps as overlaps
from .cost_funcs import cf_category_balance as category_balance
from .cost_funcs import cf_table_size as table_size

class Solution(object):
    """
    Holds seat assignments and associated cost metrics
    """
    def __init__(self, solution):
        self.solution = solution
        self.days = list(set(t.day for t in self.solution))

        self.overlaps2_freqs = None
        self.overlaps3_freqs = None
        self.same_spot_freqs = None

        self.cost_of_overlaps = None
        self.cost_of_same_spot = None
        self.cost_of_category_balance = None
        self.cost_of_table_size = None
        self.cost = None

        self.switch_args = None
        self.switchback_args = None

        self.update_solution_metrics()

    def update_solution_metrics(self):
        """
        Updates all metrics (# of people cost
        """

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
        """
        Moves from a solution to a 'neighboring' solution by switching
        two random people on a random day.
        """
        day_to_switch = random.choice(self.days)
        tables_that_day = [t for t in self.solution \
                           if t.day == day_to_switch and t.name != 'Head']


        sub_capacity_tables = [t for t in tables_that_day
                               if not t.is_full()]
        num_ppl = float(len(set([p for t in tables_that_day
                                 for p in t.people])))
        num_seats = float(sum([t.capacities['overall-max']
                               for t in tables_that_day]))
        single_switch_probability = num_ppl/num_seats
        single_switch = sub_capacity_tables != [] \
                        and (random.random() > single_switch_probability)
        if single_switch:
            table0 = random.choice([t for t in tables_that_day
                                         if t not in sub_capacity_tables])
            table1 = random.choice(sub_capacity_tables)
            person0 = random.choice(table0.people)
            person1 = None
        else:
            tables_to_switch = random.sample(tables_that_day, 2)
            table0 = tables_to_switch[0]
            table1 = tables_to_switch[1]
            person0 = random.choice(table0.people)
            person1 = random.choice(table1.people)

        # pass switchback_args along in case the new solution is not
        # accepted and we need to revert 'tables' to its old state. The
        # alternative to mutating the solution like this is to make a
        # deep copy the solution (and therefore of 'tables') so that
        # old_solution.tables and new_solution.tables point at completely
        # different things, but this was causing unacceptable performance
        # degradation.
        self.switch_args = [table0, person0,
                            table1, person1]
        self.switchback_args = [table1, person0,
                                table0, person1]
        table_switch(*self.switch_args)
        self.update_solution_metrics()

    def move_back_from_neighbor(self):
        """
        Reverses changes made to solution in move_to_neighbor()
        """
        table_switch(*self.switchback_args)
        self.update_solution_metrics()


def table_switch(table0, person0, table1, person1):
    """
    Switches two people on a particular day. If one of the people is
    'None', _table_switch just moves someone to a table with an open
    seat.
    """
    if person0 != None and person1 != None:
        table0.people.remove(person0)
        table0.people.append(person1)
        table1.people.remove(person1)
        table1.people.append(person0)
        person0.tables[table0.day] = table1.name
        person1.tables[table0.day] = table0.name

    elif person0 != None and person1 == None:
        table0.people.remove(person0)
        table1.people.append(person0)
        person0.tables[table0.day] = table1.name

    elif person0 == None and person1 != None:
        table0.people.remove(person1)
        table1.people.append(person1)
        person1.tables[table0.day] = table1.name
