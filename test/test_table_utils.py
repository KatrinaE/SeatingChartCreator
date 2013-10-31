import unittest
import pdb
import random

from fixtures import big_people_fixture, big_tables_fixture, test_table, test_grouping
from ..table_utils import Grouping, Table, make_table_and_grouping_objects, get_table, get_grouping

class SeatingTestCase(unittest.TestCase):
    #noinspection PyPep8Naming
    def setUp(self):
        pass

    #noinspection PyPep8Naming
    def tearDown(self):
        pass
        #self.widget.dispose()
        #self.widget = None
        
        
    def test_make_table_and_grouping_objects(self):
        num_tables = 10
        groupings_per_table = 5
        (tables_master, groupings_master) = make_table_and_grouping_objects(big_tables_fixture.tables)
        self.assertEqual(len(tables_master.items()), num_tables, "The number of tables is " + str(len(tables_master.items())) + ", not " + str(num_tables))
        self.assertEqual(len(groupings_master.items()), num_tables, "The number of tables with groupings is " + str(len(groupings_master.items())) + ", not " + str(num_tables))

        for table in groupings_master.values():
            self.assertEqual(len(table.items()), groupings_per_table, "The number of groupings for this table is " + str(len(table.items())) + " not " + str(groupings_per_table))

        a_table = random.choice(tables_master.values())
        all_groupings_for_table = random.choice(groupings_master.values())
        a_grouping = random.choice(all_groupings_for_table.values())

        self.assertNotEqual(a_table.name, None, "a_table.name is " + str(a_table.name))
        self.assertEqual(len(a_table.groupings), 5, "a_table does not have 5 groupings")
        self.assertEqual(a_table.already_sat_here, [], "a_table.already sat is " + str(a_table.already_sat_here))

        self.assertNotEqual(a_grouping.name, None, "a_grouping.name is " + str(a_grouping.name))
        self.assertNotEqual(a_grouping.day, None, "a_grouping.day is " + str(a_grouping.day))
        self.assertNotEqual(a_grouping.capacity, None, "a_grouping.capacity is " + str(a_grouping.capacity))
        self.assertEqual(a_grouping.people_list, [], "a_grouping.people_list is " + str(a_grouping.people_list))

    def test_table_object(self):
        table_object = test_table
        self.assertEqual(table_object.name, '4', "table_object.name is " + str(table_object.name))
        self.assertEqual(len(table_object.groupings), 1)
        self.assert_(str(table_object) == "4")

    def test_grouping_object(self):
        grouping_object = test_grouping
        self.assert_(grouping_object.day == 'Wed')
        self.assertEqual(str(grouping_object), "4-Wed", "grouping_object string is " + str(grouping_object))

    def test_add_grouping_to_table(self):
        table = test_table
        grouping = test_grouping
        table.add_grouping(grouping)
        self.assertEqual(table.groupings, [grouping])


    # TODO: test_people_who_have_sat_at
    #def test_people_who_have_sat_at(self):
    #    table = test_table

    def test_get_table(self):
        table_object = test_table
        name = table_object.name

        tables_master = {}
        self.assertRaises(KeyError, get_table(name, tables_master))

        tables_master[table_object.name] = table_object
        t = get_table(name, tables_master)
        self.assertEqual(table_object, t)

    def test_get_grouping(self):
        table_object = test_table
        grouping_object = test_grouping
        day = test_grouping.day
        name = test_grouping.name

        groupings_master = {}
        self.assertRaises(KeyError, get_grouping(name, day, groupings_master))
        groupings_master[name] = {}
        self.assertRaises(KeyError, get_grouping(name, day, groupings_master))
        groupings_master[name][day] = grouping_object
        self.assertEqual(grouping_object, get_grouping(name, day, groupings_master))

