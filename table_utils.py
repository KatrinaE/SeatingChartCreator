import pdb

class Table(object):
    """
    Table, e.g. '4' or 'Head'

    Tables contain a list of groupings (groups sitting there on different days -
    there is a Monday grouping, a Tuesday grouping, etc.) and a list of people
    who have already sat there.
    """
    
    def __init__(self, table_name):
        self.name = table_name
        self.groupings = []
        self.already_sat_here = []

    def __str__(self):
        return str(self.name)

    def add_grouping(self, grouping):
        self.groupings.append(grouping)
    
    
class Grouping(object):
    """
    A grouping stores who is sitting at a table on a specific day.
    Its name is a compound of its table's name and it's day, e.g. '1-Mon'

    In addition to a Table (self.table_name) and a day (self.day),
     a grouping has the following properties:
    - capacity: how many people can fit
    - people_list: who's currently sitting there

    """

    def __init__(self, table_name, day, capacity):
        self.table_name = table_name
        self.day = day
        self.name = str(table_name) + "-" + str(day)
        self.capacity = capacity
        self.people_list = []

    def __str__(self):
        return str(self.name)

    def add_person(self, person_id):
        self.people_list.append(person_id)
        return

    def remove_person(self, person_id):
        self.people_list.remove(person_id)
        return


def make_table_and_grouping_objects(tables):
    """
    Creates all Table objects and all Grouping objects
    from the information imported in Tables.csv

    tables_master is the master list of all table objects.
    groupings_master is the master list of all grouping objects.

    tables_master is a dict. It has the format:
    {'Head': <Table object>, '2': <Table object> }

    groupings_master is a dict of dicts. It has the format:
    {'Head': {'Mon': <Grouping object>, 'Fri': <Grouping object> },
    '2': {'Mon': <Grouping object>, 'Fri': <Grouping object> } }

    """
    # TODO: need to create an error if 'Table Name' key is not in dictionary ('if key not in d: do something')
    tables_master = {}
    groupings_master = {}

    for table_dict in tables:
        table_name = table_dict.pop('Table Name')
        table_object = Table(table_name)
        tables_master[table_object.name] = table_object
        
        for d in table_dict.iteritems():
            day = d[0]
            capacity = d[1]
            grouping_object = Grouping(table_name, day, capacity)
            table_object.add_grouping(grouping_object)
            try:
                groupings_master[table_object.name][day] = grouping_object
            except KeyError:
                groupings_master[table_object.name] = {}
                groupings_master[table_object.name][day] = grouping_object
            
    return tables_master, groupings_master
        

def people_who_have_sat_at(table_name):
    """
    gets all people who are in grouping objects where number = table_number
    """
    return

def get_table(name, tables_master):
    # Important! 'name' must be a string.
    try:
        return tables_master[name]
    except KeyError:
        print "There is no table named " + str(name) + " in the given tables_master dict."

def get_grouping(name, day, groupings_master):
    # Important! 'name' must be a string.
    try:
        table = groupings_master[name]
        try:
            return table[day]
        except KeyError:
            print "There is no grouping for " + str(name) + " on " + str(day)
    except KeyError:
        print "There is no table named " + str(name) + " in the given groupings_master dict."
