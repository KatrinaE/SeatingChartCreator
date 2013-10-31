import unittest
import pdb
import random

from fixtures import big_people_fixture, big_tables_fixture
from ..all_io import import_people, add_person_ids, make_categories_list, import_tables


class CampersTestCase(unittest.TestCase):
    #noinspection PyPep8Naming
    def setUp(self):
        pass

    #noinspection PyPep8Naming
    def tearDown(self):
        pass
        #self.widget.dispose()
        #self.widget = None

    def person_import(self, filename, num_people, days_list, fields_list, categories_list):
        """ Helper method. Tests import_people and extract_categories."""
        (people, days, fieldnames) = import_people(filename)
        test_person = people[0]
        self.assert_(len(people) == num_people, "The number of people imported was " + str(people))
        self.assertItemsEqual(days_list, days, "The days imported were " + str(days))
        self.assertItemsEqual(fields_list, fieldnames, "The fieldnames imported were " + str(fieldnames) + ", not " + str(fields_list))

    def test_simple_person_import(self):
        filename = "csv/people_small_basic.csv"
        num_people = 9
        days_list = ['Mon', 'Tues', 'Wed']
        fields_list = ['Mon', 'Tues', 'Wed', 'First Name', 'Last Name', 'Category']
        categories_list = ['']
        self.person_import(filename, num_people, days_list, fields_list, categories_list)

    def test_full_person_import(self):
        filename = "csv/people.csv"
        num_people = len(big_people_fixture.people)
        days_list = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri']
        fields_list = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'First Name', 'Last Name', 'Category']
        categories_list = big_people_fixture.categories
        self.person_import(filename, num_people, days_list, fields_list, categories_list)

    def test_person_ids(self):
        people = big_people_fixture.people
        self.assert_(len(people) == 74)
        i = random.randint(0, 73)
        self.assertFalse(people[i].has_key('id'),
                         "Random person already has id key before assign_person_ids was called")
        add_person_ids(people)
        self.assertTrue(people[i].has_key('id'),
                        "Random person does not have an id key after assign_person_ids was called")
        self.assert_(people[i]['id'] != '',
                     "Random person does not have an id value after assign_person_ids was called")

    def test_make_categories_list(self):
        people = big_people_fixture.people
        categories_list = big_people_fixture.categories
        categories = make_categories_list(people)
        self.assertItemsEqual(categories, categories_list, "The categories list is " + str(categories) + ", not " + str(
            categories_list) + " as expected.")


class TablesTestCase(unittest.TestCase):
    #noinspection PyPep8Naming
    def setUp(self):
        pass

    #noinspection PyPep8Naming
    def tearDown(self):
        pass

    @staticmethod
    def tables_import(filename):
        table_dicts = import_tables(filename)
        return table_dicts

    def test_full_tables_import(self):
        filename = "csv/tables.csv"
        num_tables = 10
        num_groupings = 50
        table_dicts, days = self.tables_import(filename)
        self.assertEqual(len(table_dicts), num_tables)
        imported_groupings = 0
        for t in table_dicts:
            imported_groupings = imported_groupings + len(t.values()) - 1 # 1 of the t.values() is the table name
        self.assertEqual(imported_groupings, num_groupings)
