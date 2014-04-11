import random

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
        people = tables_to_people(self.solution, output_format = 'objects')
        p_to_switch, t_to_switch_from = self._pick_switcher(people, self.solution)
        # there is a bug here somewhere. 
        t_to_switch_to = self._switcher_destination(self.solution, t_to_switch_from)
        random_person = random.choice(t_to_switch_to.people)
        
        # performance optimization - pass switchback_args along in case the new solution is not
        # accepted and we need to revert 'tables' to its old state. The alternative
        # is to make a deep copy of 'tables' so that old_solution.tables and
        # new_solution.tables point at completely different things, but this was 
        # causing unacceptable performance degradation.
        self.switch_args = [p_to_switch, random_person, t_to_switch_from, t_to_switch_to]
        self.switchback_args = [random_person, p_to_switch, t_to_switch_from, t_to_switch_to]
        self._table_switch(*self.switch_args)
        self.update_solution_metrics()

    def move_back_from_neighbor(self):
        self._table_switch(*self.switchback_args)
        self.update_solution_metrics()


    def _pick_switcher(self, people, tables):
        if config.random_anneal:
            person_to_switch = random.choice([p for p in people 
                                              if '1' not in p.__dict__.values()])
            tables_out_to_switch = [x for x in tables if (x.day, x.name) 
                                    in person_to_switch.__dict__.items()]
            table_to_switch_from = random.choice(tables_out_to_switch)

        else: 
            person_to_switch = self._saddest_person(people)
            bad_table_tuple = self._most_freq_table(person_to_switch)
            bad_table_all_days = [t for t in tables_out
                                 if t.name == bad_table_tuple[0]
                                  and t.name != '1'
                                 and person_to_switch in t.people]
            try:
                table_to_switch_from = random.choice(bad_table_all_days)
            except:
                import ipdb; ipdb.set_trace()
        return person_to_switch, table_to_switch_from

    def _switcher_destination(self, tables, table_to_switch_from):
        tables_to_switch_to = [t for t in tables
                               if t is not table_to_switch_from
                               and t.name != 'Head'
                               and t.name != '1'
                               and t.day == table_to_switch_from.day]
        destination = random.choice(tables_to_switch_to)
        return destination

    def _table_switch(self, person_to_switch, random_person, table_to_switch_from, table_to_switch_to):
        #print "before switching " + person_to_switch.first_name + " and " + \
        #    random_person.first_name
        #print [p.first_name for p in table_to_switch_from.people]
        #print [p.first_name for p in table_to_switch_to.people]
        table_to_switch_from.people.remove(person_to_switch)
        table_to_switch_from.people.append(random_person)
        table_to_switch_to.people.remove(random_person)
        table_to_switch_to.people.append(person_to_switch)
        setattr(person_to_switch, table_to_switch_from.day, table_to_switch_to.name)
        setattr(random_person, table_to_switch_from.day, table_to_switch_from.name)
        #print "after switch: "
        #print [p.first_name for p in table_to_switch_from.people]
        #print [p.first_name for p in table_to_switch_to.people]

    def persons_tables(self, person):
        # Hack Alert! Hard-coded
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        tables = [table for (day, table) in \
                  person.__dict__.iteritems() if day in days \
                  ]
        return tables

    def _saddest_person(self, people):
        fewest_tables_sat_at = float('inf')
        for person in people:
            tables = self.persons_tables(person)
            num_tables_sat_at = len(set(tables))
            num_times_at_head_table = len([t for t in tables if t == '1'])
            if num_times_at_head_table < 5:
                revised_num_sat_at = num_tables_sat_at + \
                                 num_times_at_head_table -1
                if revised_num_sat_at < fewest_tables_sat_at:
                    _saddest_person = person
                    fewest_tables_sat_at = num_tables_sat_at
        return _saddest_person

    def _most_freq_table(self, person):
        tables = self.persons_tables(person)
        excluding_head = [t for t in tables if t is not '1']
        c = Counter(excluding_head)
        reoccuring_table_tuple = c.most_common(1)[0]
        return reoccuring_table_tuple
