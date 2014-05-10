import collections
import heapq
import random

import config
from solution import Solution

def get_previous_seatmates(person, tables):
    ids_of_previous_seatmates = []
    for table in tables:
        if person in table.people:
            ids_of_previous_seatmates.extend([p.id for p in table.people if p.id != person.id])
    return ids_of_previous_seatmates

def ordered_by_num_seatmates(tables, ids_of_previous_seatmates):
    h = []
    for table in tables:
        ids_at_table = [person.id for person in table.people]
        intersection = set(ids_at_table) & set(ids_of_previous_seatmates)
        num_prev_seatmates = len(intersection)
        h.append((num_prev_seatmates, table))
    h.sort()
    tables_out = [tup[1] for tup in h]
    return tables_out

def room_for_cat(tables, category):
    open_tables = [t for t in tables if not t.is_full_for_cat(category)]
    if open_tables != []:
        return open_tables
    else:
        return tables

def small_tables(tables, open_tables, day):        
    average = sum([len(t.people) for t in tables if t.day == day and t.name != 'Head'])/len([t for t in tables if t.day == day and t.name != 'Head'])
    open_tables2 = [t for t in open_tables if len(t.people) < average-2]
    if open_tables2 != []:
        return open_tables2
    return open_tables

def not_sat_at_twice(open_tables, person):
    counts = collections.Counter(person.tables.values())
    if counts != {}:
        bad_names = [table_name for (table_name, count) in counts.items() if count > 1
                     and table_name != 'Head' and table_name != '']
        good_tables = [t for t in open_tables if t.name not in bad_names]
        if good_tables != []:
            return good_tables
    return open_tables

def best_table(person, tables, day):
    if config.build_smart == False:
        return random.choice([t for t in tables if t.day == day and t.name != 'Head' and not t.is_full()])

    open_tables = [t for t in tables 
                   if t.day == day 
                   and t.name != 'Head' 
                   and not t.is_full()]
    open_tables = small_tables(tables, open_tables, day)
    open_tables = room_for_cat(open_tables, person.category)
    open_tables = not_sat_at_twice(open_tables, person)
    ids_of_previous_seatmates = get_previous_seatmates(person, tables)
    open_tables = ordered_by_num_seatmates(open_tables, ids_of_previous_seatmates)
    best_table = open_tables[0]
    return best_table

def assign_table(person, tables, day):
    table = best_table(person, tables, day)
    person.tables[day] = table.name
    table.people.append(person)

def seat_people(people, tables, day):
    for person in people:
        table_name = person.tables[day]
        if table_name == '':
            assign_table(person, tables, day)
    return tables

def populate_preassigned_tables(people, tables, days):
    for person in people:
        for day in days:
            table_name = person.tables[day]
            if table_name != '':
                try: 
                    preassigned_table = [t for t in tables \
                                         if t.name == table_name 
                                         and t.day == day][0]
                except IndexError:
                    print '%s %s was pre-assigned to table ' % (person.first_name, person.last_name) + \
                    '%s, which is not in the tables input file.' % table_name
                    raise
                preassigned_table.people.append(person)
    return tables

def build_guess(people, tables, days):
    tables = populate_preassigned_tables(people, tables, days)
    for d in days:
        random.shuffle(people)
        tables = seat_people(people, tables, d)
    guess = Solution(tables)
    return guess
