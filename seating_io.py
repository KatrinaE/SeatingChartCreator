import csv
import math
from collections import Counter

def parse_input(people_file, tables_file):
    people = people_objects(people_file)
    categories = Counter([p.category for p in people])
    category_proportions = {name : (count / float(len(people)))
                            for (name, count) in categories.items()}
    tables = table_objects(tables_file, category_proportions)
    days = days_from_tables(tables)
    return people, tables, days


class InputData(object):
    def __init__(self, people_filename, tables_filename):
        self.people, self.tables, self.days = parse_input(people_filename, tables_filename)

class Person(object):
    def __init__(self, id, person_dict):
        self.id = id
        self.first_name = person_dict.pop('First Name')
        self.last_name = person_dict.pop('Last Name')
        self.category = person_dict.pop('Category')
        self.tables = {}
        for (day, preassigned_table) in person_dict.iteritems():
            self.tables[day] = preassigned_table

def people_objects(filename):
    reader = csv.DictReader(open(filename,"rwU"))
    people = [row for row in reader]
    people_list = []
    current_id = 1
    for p in people: 
        person = Person(current_id, p)
        people_list.append(person)
        current_id += 1
    return people_list

class Table(object):
    def __init__(self, name, day, capacity, cat_proportions):
        self.name = name
        self.day = day
        self.people = []
        
        self.capacities = {"overall" : capacity }
        cat_capacities = { name: math.ceil(proportion * float(capacity))
                                for (name, proportion) in cat_proportions.items() }
        self.capacities.update(cat_capacities)

    def is_full(self):
        if len(self.people) > self.capacities['overall']:
            raise RuntimeError("Table %s is over capacity" % self.name)
        else:
            return len(self.people) == self.capacities['overall']

    def is_full_for_cat(self, category):
        people_in_cat = [p for p in self.people if p.category == category]
        if len(people_in_cat) > self.capacities[category]:
            raise RuntimeError("Table %s is over capacity" % self.name)
        else:
            return len(people_in_cat) == self.capacities[category]


def table_objects(filename, category_proportions):
    """
    Creates a list of objects, 1 for each table
    """
    reader = csv.DictReader(open(filename,"rwU"))
    temp_tables = [row for row in reader]
    days = days_list(filename)
    tables = []
    for table in temp_tables:
        name = table['Table Name']
        for day in days:
            capacity = table[day]
            table_object = Table(name, day, capacity, category_proportions)
            tables.append(table_object)
    return tables

def days_list(filename):
    reader = csv.reader(open(filename, "rwU"))
    header = reader.next()
    days_list = [day for day in header if day not in 
                 ['Table Name', 'Category', 'First Name', 'Last Name']]
    return days_list

def days_from_tables(tables):
    days = list(set(t.day for t in tables))
    return days

def tables_to_people(tables_list):
    all_people = []
    people_out = []
    for table in tables_list:
        all_people.extend(table.people)
    for p in set(all_people):
        p_dict = {'First Name' : p.first_name, 'Last Name': p.last_name, 'Category': p.category}
        p_dict.update(p.tables)
        people_out.append(p_dict)
    return people_out

def write_people_to_csv(solution, filename):
    people = tables_to_people(solution.solution)
    fields = ['First Name', 'Last Name', 'Category'] + solution.days
    with open(filename,'wb') as f:
        csvwriter = csv.DictWriter(f, delimiter=',', fieldnames=fields, extrasaction='ignore')
        csvwriter.writerow(dict((fn,fn) for fn in fields))
        for p in people:
            csvwriter.writerow(p)

def write_tables_to_csv(solution, filename):
    all_tables = {}
    for table in solution.solution:
        all_tables[table.name] = { 'Name' : table.name}
        for day in solution.days:
            all_tables[table.name][day] = None
    for table in solution.solution:
            people_list = [' '.join((p.first_name, p.last_name)) for p in table.people]
            all_tables[table.name][table.day] = ', '.join([p for p in people_list])
    fieldnames = ['Name'] + solution.days
    with open(filename,'wb') as file:
        csvwriter = csv.DictWriter(file, dialect='excel', delimiter=',', quoting=csv.QUOTE_ALL, fieldnames=fieldnames)
        csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
        for table in all_tables.itervalues():
            csvwriter.writerow(table)
