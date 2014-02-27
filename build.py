import collections
import heapq
import random
from copy import deepcopy
import config

def today_only(tables, day):
    tables_out = []
    for table in tables:
        if table.day == day:
            tables_out.append(table)
    return tables_out

def not_head(tables):
    return [table for table in tables if table.name != 'Head']

def not_full(tables):
    open_tables = []
    for table in tables:
        if len(table.people) < int(table.capacity):
            open_tables.append(table)
    if not open_tables:
        raise Error("More people than tables!")
    else:
        return open_tables

def max_for_category(category):
    # Hack Alert! Hard-coded
    maxima = {'Health Administration' : 2,
              'Nursing' : 3,
              'Medicine' : 4,
              'Other' : 4,
             }
    return maxima[category]

def cat_not_full(tables, category):
    max_allowed = max_for_category(category)
    open_tables = []
    for table in tables:
        people = [p for p in table.people if p.category  == category]
        if len(people) < max_allowed:
            open_tables.append(table)
    if open_tables == []:
        return tables
    else:
        return open_tables

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
    try:
        # try to return the best 3 tables
        return tables_out[:2]
    except:
        return tables_out

def ordered_by_same_spot(tables, person):
    persons_tables = collections.Counter([v for (k,v) in person.__dict__.iteritems() if k in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']])
    l = []
    for table in tables:
        tup = (persons_tables[table.name], table)
        l.append(tup)
    l.sort()
    tables_out = [tup[1] for tup in l]
    return tables_out

def best_table(person, tables, day):
    open_tables = today_only(tables, day)
    open_tables = not_head(open_tables)
    open_tables = not_full(open_tables)
    if not config.random_start:
        open_tables = cat_not_full(open_tables, person.category)
        ids_of_previous_seatmates = get_previous_seatmates(person, tables)
        open_tables = ordered_by_num_seatmates(open_tables, ids_of_previous_seatmates)
        open_tables = ordered_by_same_spot(open_tables, person)
        best_table = open_tables[0]
    else:
        best_table = random.choice(open_tables)
    return best_table

def assign_table(person, tables, day):
    table = best_table(person, tables, day)
    setattr(person, day, table.name)
    seat_person_at_table(table, person)
    table_from_person = getattr(person, day)
    table_from_table = [table.name for table in tables if table.day == day and person in table.people][0]
    if table_from_person != table_from_table:
        raise RuntimeError("Table list from person and table list from table do not match")

def seat_campers(people, tables, day):
    for person in people:
        if getattr(person, day) is '':
            assign_table(person, tables, day)
    return tables

def seat_person_at_table(table, person):
    table.people.append(person)
    return table

def populate_head_table(tables, people):
    all_head_tables = (t for t in tables if t.name == "Head")
    for head_table in all_head_tables:
        day = head_table.day
        for person in people:
            # Hack Alert! Hard-coded
            if getattr(person, day) == '1':
                head_table = seat_person_at_table(head_table, person)
    return tables

def build_guess(people, tables, all_days):
    tables_out = populate_head_table(tables, people)
    for d in all_days:
        random.shuffle(people)
        tables_out = seat_campers(people, tables_out, d)
    return tables_out
