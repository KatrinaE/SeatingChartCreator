import heapq
import random
from copy import deepcopy

from c_io import days_list

def table_not_full(table, day):
    return len(table[day]['ppl']) < (int(table[day]['opt']));

def not_full(tables, d):
    open_tables = []
    for t in tables:
        if t['Table Name'] != 'Head':
            if table_not_full(t, d):
                open_tables.append(t)              
    random.shuffle(open_tables)
    return open_tables

def max_for_cat(cat):
    if cat == 'Health Administration':
        max_num = 2
    elif cat == 'Nursing':
        max_num = 3
    elif cat == 'Medicine' or cat == 'Other':
        max_num = 4
    return max_num

def cat_not_full(tables, d, cat):
    max_num = max_for_cat(cat)        
    open_tables = []
    for t in tables:
        ppl = [x for x in t[d]['ppl'] if x[1] == cat]
        if len(ppl) < max_num:
            open_tables.append(t)
    if open_tables == []:
        open_tables = not_full(tables, d)
    random.shuffle(open_tables)
    return open_tables

def get_ids_at_table(t):
    return [ x[0] for x in t['ppl'] ]

def get_previous_seatmates(person, tables, days):
    seatmates = []
    for t in tables:
        for d in days:
            ids_at_table = get_ids_at_table(t[d])
            if person['id'] in ids_at_table:
                seatmates.extend(ids_at_table)
    return seatmates

def table_with_fewest_previous_seatmates(open_tables, previous_seatmates, d):
    h = []
    for t in open_tables:
        ppl_at_t = [x[0] for x in t[d]['ppl']]
        intersection = list(set(ppl_at_t) & set(previous_seatmates))
        num_prev_seatmates = len(intersection)
        h.append((num_prev_seatmates, t))
    best_table = min(h)[1]
    return best_table

def best_table(person, tables, day):
    cat = person['Category']
    open_tables = not_full(tables, day)
    open_tables = cat_not_full(open_tables, day, cat)
    all_days = days_list('tables.csv')
    previous_seatmates = get_previous_seatmates(person, tables, all_days)
    the_table = table_with_fewest_previous_seatmates(open_tables, previous_seatmates, day)

    return the_table

def assign_table(person, tables, day):
    the_table = best_table(person, tables, day)
    person[day] = the_table['Table Name']
    the_table[day]['ppl'].append((person['id'], person['Category']))

def seat_campers(people, tables, d):
    for p in people:
        if p[d] is '':
                assign_table(p, tables, d)
    return people, tables

def get_head_table(tables):
    return [x for x in tables if x['Table Name'] == 'Head'][0]

def populate_head_table(tables, people, days):
    head_table = get_head_table(tables)
    for p in people:
        for d in days:
            if p[d] == '1':
                head_table[d]['ppl'].append((p['id'], p['Category']))
    # How come I have to explicitly return tables here?
    return tables

def build_solution(people, tables):
    people_out = deepcopy(people)
    tables_out = deepcopy(tables)

    days = days_list('tables.csv')
    tables_out = populate_head_table(tables_out, people_out, days)
    for d in days:
        random.shuffle(people_out)
        random.shuffle(tables_out)
        people_out, tables_out = seat_campers(people_out, tables_out, d)

    return people_out, tables_out







