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

def ordered_by_same_spot(tables, person):
    persons_tables = collections.Counter([t for t in person.tables.values()])
    l = []
    for table in tables:
        frequency_tuple = (persons_tables[table.name], table)
        l.append(frequency_tuple)
    l.sort()
    tables_out = [tup[1] for tup in l]
    return tables_out

def best_table(person, tables, day):
    if config.build_smart == False:
        return random.choice([t for t in tables if t.day == day and t.name != 'Head' and not t.is_full()])

    open_tables = [t for t in tables 
                   if t.day == day 
                   and t.name != 'Head' 
                   and not t.is_full()
                   and not t.is_full_for_cat(person.category)]
    ids_of_previous_seatmates = get_previous_seatmates(person, tables)
    open_tables = ordered_by_num_seatmates(open_tables, ids_of_previous_seatmates)
    #open_tables = ordered_by_same_spot(open_tables, person)
    best_table = open_tables[0]
    return best_table

def assign_table(person, tables, day):
    table = best_table(person, tables, day)
    person.tables[day] = table.name
    table.people.append(person)
    # TODO: remove this part!!!
    table_from_person = person.tables[day]
    table_from_table = [table.name for table in tables if table.day == day and person in table.people][0]
    if table_from_person != table_from_table:
        raise RuntimeError("Table list from person and table list from table do not match")

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
