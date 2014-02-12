from io import people_dicts, table_objects, write_to_csv
from build import build_solution
from anneal import anneal
from io import days_list

def main(people_csv, tables_csv):
    people = people_dicts(people_csv)
    tables = table_objects(tables_csv)
    days = days_list('tables.csv')
    init_solution = build_solution(people, tables, days)
    final_solution = anneal(init_solution)
    write_to_csv(final_solution, "output.csv")

main('people.csv', 'tables.csv')
