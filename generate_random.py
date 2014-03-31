from seating_io import people_objects, table_objects, write_to_csv
from build import build_guess
from anneal import anneal
from seating_io import days_list

def main(people_csv, tables_csv):

    print "*************************************"
    people = people_objects(people_csv)
    tables = table_objects(tables_csv)
    days = days_list('tables.csv')
    init_guess = build_guess(people, tables, days)
    final_solution = anneal(init_guess)
    write_to_csv(final_solution, "output.csv")
    print "************************************"

main('people.csv', 'tables.csv')
