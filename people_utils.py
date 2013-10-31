import random
import pdb
from copy import copy, deepcopy
from collections import Counter
from itertools import chain, combinations



# Determining if a person is at the head table
# Example call is isHead(nursing,"Mon")
# Used below in AssignPersons

class Person(object):
    """Person"""
    already_sat_with = []
    already_sat_at = []

    def __init__(self, raw_person, id_number):
        self.id = id_number
        self.first_name = raw_person['First Name']
        self.last_name = raw_person['Last Name']
        self.category = raw_person['Category']

    def __str__(self):
        return str(self.id) + " " + str(self.last_name) + ", " + str(self.first_name)
        

def make_person_objects(raw_person_list, days):
    persons_master = {}
    new_id = 1
    for person in raw_person_list:
        p_object = Person(person, new_id)
        
        for day in days:
            if person[day] != '':
                attribute_name = "p_object." + str(day) + " = " + str(person[day])
                exec attribute_name
        
        persons_master[new_id] = p_object
        new_id += 1
    return persons_master

       
def not_head(group,day):
    studentlist=[]
    for person in group:
        if person[day] != '1':
            studentlist.append(person)
    return studentlist

def head(group,day):
    headlist=[]
    for h in group:
        if h[day] == '1':
            headlist.append(h)
    return headlist

"""
def alreadySatWithPerson(person):
    allTablesTilNow = compute_all_tables_all_days()
    allOverlaps = Counter(chain.from_iterable(combinations(table, 2) for table in allTablesTilNow))

    alreadySatWith=[]
    i=0
    for key in allOverlaps.keys():
        if person["id"] in key:
            pairs=list(key)
            pairs.remove(person['id'])
            alreadySatWith.append(pairs[0])
    return alreadySatWith
"""