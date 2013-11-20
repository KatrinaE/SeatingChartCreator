import unittest
import pdb
import random

from fixtures import big_people_list, days_fixture
from ..people_utils import Person, make_person_objects

class PeopleTestCase(unittest.TestCase):
    #noinspection PyPep8Naming
    def setUp(self):
        pass

    #noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_make_person_objects(self):
        people_master = make_person_objects(big_people_list, days_fixture)
        self.assertEqual(type(people_master[1]), Person)
        self.assertEqual(len(people_master),len(big_people_list))
        self.assertEqual(people_master[1].id, 1)

    def test_not_head(self):
        pass

    def test_head(self):
        pass