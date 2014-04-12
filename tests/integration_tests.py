import unittest
import nose
import os
from collections import Counter

from seating_io import days_list, people_objects, table_objects
from build import build_guess
from anneal import anneal

class IOTestCase(unittest.TestCase):

    def test_people_objects(self):
        # test going from input file to people objects
        pass

    def test_table_objects(self):
        # test going from input file to tables objects
        pass

    def test_days_list(self):
        # test going from input tables file to days
        pass

    def test_tables_to_people(self):
        # test going from list of tables objects to list of people objects
        pass


class CostFuncTestCase(unittest.TestCase):
    def setUp(self):
        ppl_file = 'tests/tiny-people-already-seated.csv'
        tables_file = 'tests/tiny-tables-with-head.csv'
        self.tiny_people = people_objects(ppl_file)
        self.tiny_tables = table_objects(tables_file)
        self.days = days_list(tables_file)
    
    def test_cf_overlaps(self):
        input_data = (self.tiny_people,
                      self.tiny_tables,
                      self.days)
        solution = build_guess(*input_data)
        expected_freqs2 = Counter({ 3:1, 2:2, 1:2 })
        expected_freqs3 = Counter()
        nose.tools.assert_equal(solution.overlaps2_freqs, expected_freqs2)
        nose.tools.assert_equal(solution.overlaps3_freqs, expected_freqs3)
    
    def test_cf_same_spot(self):
        input_data = (self.tiny_people,
                      self.tiny_tables,
                      self.days)
        solution = build_guess(*input_data)

        expected_same_spot = Counter({ 3:2, 2:4, 1:4})
        nose.tools.assert_equal(solution.same_spot_freqs, expected_same_spot)

    def test_cf_category_balance(self):
        pass

    def test_cf_table_size(self):
        pass

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        ppl_file = 'tests/tiny-people.csv'
        tables_file = 'tests/tiny-tables.csv'
        self.tiny_people = people_objects(ppl_file)
        self.tiny_tables = table_objects(tables_file)
        self.days = days_list(tables_file)

        h_ppl_file = 'tests/tiny-people-with-head.csv'
        h_tables_file = 'tests/tiny-tables-with-head.csv'
        self.tiny_people_with_head = people_objects(h_ppl_file)
        self.tiny_tables_with_head = table_objects(h_tables_file)
        self.days_with_head = days_list(h_tables_file)

    def tearDown(self):
        pass

    @classmethod
    def _validate_solution(cls, input_data, solution):
        """
        Test that the solution has the correct number of people/tables
        that no person is in two tables on the same day
        """
        people = input_data[0]
        tables_in = input_data[1]
        days_in = input_data[2]
        tables_out = solution.solution
        # make sure the overall number of tables is correct
        nose.tools.assert_equal(len(tables_out), len(tables_in))
        # make sure each table has the correct number of people
        for t in [table.people for table in tables_out]:
            nose.tools.assert_equal(len(t), 2)

        # make sure everyone is placed exactly once each day
        for day in days_in:
            tables_that_day = [t for t in tables_out if t.day == day]
            # make sure each day has the correct number of tables
            nose.tools.assert_equal(len(tables_that_day), len(tables_in)/len(days_in))
            # this list comprehension is gross, but all is does is make a list of
            # the first names of everyone who's seated -somewhere- that day.
            all_people_that_day = [p.first_name for table in tables_that_day for p in table.people]
            # make sure there's the same number of people as we started with
            nose.tools.assert_equal(len(all_people_that_day), len(people))
            # make sure the people are the same ones we started with
            nose.tools.assert_equal(set(all_people_that_day), set([p.first_name for p in people]))

    @classmethod
    def _validate_head_table(cls, expected_people_at_head, solution):
        """
        Make sure the correct people are sitting at the head table
        """
        head_tables  = [t for t in solution.solution if t.name == 'Head']
        normal_tables = [p.first_name for p in t.people 
                         for t in solution.solution if t.name != 'Head']
        # head people @ head
        for h in head_tables:
            people_at_head = set(p.first_name for p in h.people)
            nose.tools.assert_equal(people_at_head, expected_people_at_head)
        # head people not @ normal
        for p in expected_people_at_head:
            nose.tools.assert_not_in(p, normal_tables)

    def test_build_guess(self):
        """
        Test that there are the correct number of people at each table each day
        """
        input_data = (self.tiny_people,
                      self.tiny_tables,
                      self.days)
        solution = build_guess(*input_data)
        self._validate_solution(input_data, solution)

    def test_build_guess_with_head(self):
        """
        Test that head table has correct people each day
        """
        # check the basics
        input_data = (self.tiny_people_with_head,
                      self.tiny_tables_with_head,
                      self.days_with_head)
        solution = build_guess(*input_data)
        expected_people_at_head = set(['Rosemary', 'Francine'])
        self._validate_solution(input_data, solution)
        self._validate_head_table(expected_people_at_head, solution)
        
    def test_anneal(self):
        """
        Test that the solution has the correct number of people/tables
        """
        # TODO: figure out how to change settings in config.py for testing purposes
        input_data = (self.tiny_people,
                      self.tiny_tables,
                      self.days)
        init_solution = build_guess(*input_data)
        gen = anneal(init_solution)
        for (solution, T) in gen:
            best_solution = solution
            print best_solution.cost
        self._validate_solution(input_data, best_solution)
        # final cost should be zero, because it's possible to create perfect
        # seating charts from these input files
        nose.tools.assert_equal(best_solution.cost, 0)

    def test_anneal_with_head(self):
        """
        Test that the correct people are still at the head table every day
        (on top of test_anneal)
        """
        input_data = (self.tiny_people_with_head,
                      self.tiny_tables_with_head,
                      self.days_with_head)
        init_solution = build_guess(*input_data)
        expected_people_at_head = set(['Rosemary', 'Frances'])
        gen = anneal(init_solution)
        for (solution, T) in gen:
            best_solution = solution
        self._validate_soluTion(input_data, best_solution)
        self._validate_head_table(best_solution)
        nose.tools.assert_equal(best_solution.cost, 0)
