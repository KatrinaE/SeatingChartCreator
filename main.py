import sys
from all_io import import_all, export_tables
from people_utils import make_person_objects
from table_utils import make_table_and_grouping_objects


def seating(people_csv, tables_csv):
    people_list, \
    categories_list, \
    tables_list, \
    days_list, \
    fieldnames = import_all(people_csv, tables_csv)

    people_master = make_person_objects(people_list, days_list)

    tables_master, \
    groupings_master = make_table_and_grouping_objects(tables_list)
    import pdb; pdb.set_trace()

    #export_tables( , fieldnames)
if __name__ == '__main__':
    seating(sys.argv[1], sys.argv[2])