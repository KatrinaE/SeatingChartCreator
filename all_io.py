import csv
import pdb
import itertools

from table_utils import Table, Grouping
# PEOPLE INPUT
# =============
#
# Also creates a list of days, e.g. ["Monday", "Tuesday"]
# and a list of categories, e.g. ["Managers", "Engineers"]
def import_people(csv_file_name):
    """
    INPUT
    =====
    import_people expects a csv of the following format:

    Category,Last Name,First Name,Mon,Tues,Wed,Thurs,Fri
    Manager,Smith,John,,2,2,,
    Manager,Jones,Diane,,,,,1
    Engineer,Anderson,George,3,,,,

    The column order is unimportant.

    One or more of the following fields (columns) are required:
    "id", "Name", "First Name", "Last Name".
    These are used to identify the person. Note that we do not use the
    "id" field internally - we create our own.

    "Category" is optional. If included, the algorithm will attempt to
    evenly distribute people in each category between all of the tables.
    This is useful e.g. if you are planning a meeting and want to ensure
    people from different departments interact.

    All of the remaining fieldnames are presumed to be days we need to
    make seating arrangements for.

    If you already know where a person is sitting on a particular day,
    pre-populate that field with the table's name (e.g. "5" or
    "head table").

    If you know a person will not be present on a particular day, pre-
    populate that field with "XXX".

    An error will be raised if any cells in the days columns' contain
    anything other than "XXX" or the names of tables imported in
    import_tables below.


    OUTPUT
    ======
    import_people creates 3 things: a list of people, a list of days,
    and a list of all fieldnames.

    In the list of people, the entry for each person is a dict of
    the format:
    {
    "Category" : "category name",
    "First Name": "name",
    "Last Name" : "name",
    "Mon" : Monday table number,
    "Tues" : Tuesday table number,
    "Wed": Wednesday table number,
    "Thurs" : Thursday table number,
    "Fri" : Friday table number
    }

    The tables numbers are typically empty.

    """
    # TODO: what if there are duplicate people?
    reader = csv.DictReader(open(csv_file_name,"rwU"))
    people = [row for row in reader]
    fieldnames = reader.fieldnames

    if "iid" in fieldnames:
        raise Exception("The name iid is reserved for internal use."
                        "Please choose a different name for this field.")

    if len(set(fieldnames)) != len(fieldnames):
        raise Exception("One or more fields have the same name. Please"
                        "choose a unique name for each field.")

    days = fieldnames[:]
    days.remove('First Name')
    days.remove('Last Name')
    days.remove('Category')
    return people, days, fieldnames

def add_person_ids(people):
    i = 0
    for person in people:
        person['iid'] = i
        i += 1
    return people

def make_categories_list(people):
    all_categories=[]
    for person in people:
        if person['Category'] not in all_categories:
            all_categories.append(person['Category'])
    return all_categories


# IMPORT TABLES
# =============

def import_tables(csv_file_name):
    """
    We expect that the csv file has the format:
    Table Name,Mon,Tue,Wed,Thu,Fri
    Head,5,5,7,5,5
    Table 2,7,7,7,7,7

    If it does, import_tables creates 2 things: a list of tables and a
    list of days.

    In the list of tables, each table is an entry like:
    {
    'Wed': '7',
    'Fri': '5',
    'Thu': '5',
    'Mon': '5',
    'Table Name': 'Head',
    'Tue': '5'
    }
    The dicts come from the fact that we used csv.DictReader.

    The list of days is like ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri']
    """

    reader = csv.DictReader(open(csv_file_name,"rwU"))
    tables = [row for row in reader]
    fieldnames = reader.fieldnames
    days = fieldnames[:]
    days.remove('Table Name')
    return tables, days


# IMPORT EVERYTHING
# =================

def import_all(people_csv_name, tables_csv_name):
    raw_people_list, people_days_list, fieldnames = \
        import_people(people_csv_name)
    people_list = add_person_ids(raw_people_list)
    categories_list = make_categories_list(people_list)


    tables_list, table_days_list = import_tables(tables_csv_name)

    if set(people_days_list) != set(table_days_list):
        raise Exception("The days in the tables csv file: " +
                         str(people_days_list) +
                         " are different from the ones in the people "
                         "csv file: " + str(table_days_list))

    return (people_list, categories_list, tables_list, table_days_list,
            fieldnames)


# EXPORT EVERYTHING
# ==========
# Create the output file

def export_people(people_output, fieldnames):
    """
    export_people writes a csv file in which each person has his/her
    own row. The file's fieldnames are the same as the ones
    imported during import_people, but with 'iid' added.
    e.g. [iid, Category, Last Name, First Name, Mon, Tues, Wed, Thurs, Fri]

    A table name is written in the field for each person/day combination.


    """

def export_tables(table_output, fieldnames):
    """
    export_tables writes a csv file in which each table has its own row.

    A list of people (e.g. '"Martin Wallace", "Lucy Smith"') is written
    in the field for each table/day combination.
    """

    output_file = open('people-output.csv','wb')
    csvwriter = csv.DictWriter(output_file, delimiter=',',
                               fieldnames=fieldnames)
    csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
    for row in table_output:
        csvwriter.writerow(row)
    output_file.close()