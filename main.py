
import random
import csv
from copy import copy, deepcopy
from collections import Counter
from itertools import chain, combinations

from c_io import people_dicts, table_dicts, write_to_csv
from c_build import build_solution
from c_anneal import anneal

def main(people_csv, tables_csv):
    people = people_dicts(people_csv)
    tables = table_dicts(tables_csv)
    init_solution = build_solution(people, tables)
    final_solution = anneal(init_solution)
    write_to_csv(final_solution, "output.csv")

main('people.csv', 'tables.csv')