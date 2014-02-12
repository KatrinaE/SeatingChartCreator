import heapq
import random
from copy import deepcopy

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
            if len(table.people) < table.capacity:
                open_tables.append(table)
    if open_tables == []:
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
        people = [p for p in table.people if p['Category'] == category]
        if len(people) < max_allowed:
            open_tables.append(table)
    if open_tables == []:
        return tables
    else:
        return open_tables

def get_previous_seatmates(person, tables):
    seatmates = []
    for table in tables:
        if person in table.people:
            seatmates.extend(table.people)
    return seatmates

def table_with_fewest_previous_seatmates(tables, previous_seatmates):
    h = []
    for table in tables:
        ids_at_table = [person['id'] for person in table.people]
        ids_of_previous = [person['id'] for person in previous_seatmates]
        intersection = set(ids_at_table) & set(ids_of_previous)
        num_prev_seatmates = len(intersection)
        h.append((num_prev_seatmates, table))
    best_table = min(h)[1]
    return best_table

def best_table(person, tables, day):
    open_tables = today_only(tables, day)
    open_tables = not_head(open_tables)
    open_tables = not_full(open_tables)
    open_tables = cat_not_full(open_tables, person['Category'])
    previous_seatmates = get_previous_seatmates(person, tables)
    table_name = table_with_fewest_previous_seatmates(open_tables, previous_seatmates)
    return table_name

def assign_table(person, tables, day):
    table = best_table(person, tables, day)
    person[day] = table.name
    seat_person_at_table(table, person)

def seat_campers(people, tables, day):
    for person in people:
        if person[day] is '':
            assign_table(person, tables, day)
    return people, tables

def seat_person_at_table(table, person):
    table.people.append(person)
    return table

def populate_head_table(tables, people):
    all_head_tables = (t for t in tables if t.name == "Head")
    for head_table in all_head_tables:
        day = head_table.day
        for person in people:
            # Hack Alert! Hard-coded
            if person[day] == '1':
                head_table = seat_person_at_table(head_table, person)
    return tables

def build_solution(people, tables, all_days):
    tables_out = populate_head_table(tables, people)
    for d in all_days:
        random.shuffle(people)
        people, tables_out = seat_campers(people, tables_out, d)

    return people, tables_out







