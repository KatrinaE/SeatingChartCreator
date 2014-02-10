import heapq
import random
from copy import deepcopy

def table_not_full(table, day):
    return len(table[day]['people']) < (int(table[day]['opt']));

def not_full(tables, d):
    open_tables = {}
    for table_name, table in tables.iteritems():
        if table_name != 'Head':
            if table_not_full(table, d):
                open_tables[table_name] = table
    return open_tables

def max_for_cat(cat):
    # Hack Alert! Hard-coded
    maxima = {'Health Administration' : 2,
              'Nursing' : 3,
              'Medicine' : 4,
              'Other' : 4,
             }
    return maxima[cat]

def cat_not_full(tables, d, cat):
    max_num = max_for_cat(cat)        
    open_tables = {}
    for table_name, table in tables.iteritems():
        people = [x for x in table[d]['people'] if x[1] == cat]
        if len(people) < max_num:
            open_tables[table_name] = table
    if open_tables == {}:
        return tables
    else:
        return open_tables

def get_previous_seatmates(person, tables, days):
    seatmates = []
    for table_name, table in tables.iteritems():
        for d in days:
            people_at_table = table[d]['people']
            if person in people_at_table:
                seatmates.extend(people_at_table)
    return seatmates

def table_with_fewest_previous_seatmates(open_tables, previous_seatmates, d):
    h = []
    for table_name, table in open_tables.iteritems():
        people_at_t = table[d]['people']
        intersection = set(people_at_t) & set(previous_seatmates)
        num_prev_seatmates = len(intersection)
        h.append((num_prev_seatmates, table_name))
    best_table = min(h)[1]
    return best_table

def best_table(person, tables, day, all_days):
    cat = person['Category']
    person_tup = (person['id'], cat)
    open_tables = not_full(tables, day)
    open_tables = cat_not_full(open_tables, day, cat)
    previous_seatmates = get_previous_seatmates(person_tup, tables, all_days)
    table_name = table_with_fewest_previous_seatmates(open_tables, previous_seatmates, day)
    return table_name

def add_person_to_seatee_list(table, person, day):
    table[day]['people'].append((person['id'], person['Category']))

def assign_table(person, tables, day, all_days):
    table_name = best_table(person, tables, day, all_days)
    person[day] = table_name
    add_person_to_seatee_list(tables[table_name], person, day)

def seat_campers(people, tables, day, all_days):
    for p in people:
        if p[day] is '':
            assign_table(p, tables, day, all_days)
    return people, tables

def populate_head_table(tables, people, all_days):
    head_table = tables["Head"]
    for p in people:
        for d in all_days:
            # Hack alert! this assumes that the head table is '1'
            # because this is how Jane entered it in her spreadsheet
            if p[d] == '1':
                add_person_to_seatee_list(head_table, p, d)
    # How come I have to explicitly return tables here?
    return tables

def build_solution(people, tables, all_days):
    people_out = deepcopy(people)
    tables_out = deepcopy(tables)
    tables_out = populate_head_table(tables_out, people_out, all_days)
    for d in all_days:
        random.shuffle(people_out)
        people_out, tables_out = seat_campers(people_out, tables_out, d, all_days)

    return people_out, tables_out







