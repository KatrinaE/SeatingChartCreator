from copy import deepcopy
import math
import argparse

import config
from seating_io import InputData, write_tables_to_csv, write_people_to_csv
from build import build_guess
from anneal import anneal
from display_messages import print_settings, print_init_cost, print_progress, print_final_metrics
from solution import Solution

def check_negative(value):
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("'%s' is not a positive integer" % value)
    if ivalue < 0:
         raise argparse.ArgumentTypeError("%s is not a positive integer" % value)
    return ivalue

def create_parser():
    parser = argparse.ArgumentParser(description="Run the Seating Chart Creator command-line app")
    parser.add_argument("people_file", action="store")
    parser.add_argument("tables_file", action="store")
    parser.add_argument("-p", "--output_people_filename", default='output-people.csv', action="store")
    parser.add_argument("-t", "--output_tables_filename", default='output-tables.csv', action="store")
    return parser

def main(input_data):
    people = deepcopy(input_data.people)
    tables = deepcopy(input_data.tables)
    init_solution = build_guess(people, tables, input_data.days)
    best_solution = deepcopy(init_solution)
    print_init_cost(init_solution.cost)

    if config.anneal:
        for (solution, T) in anneal(init_solution):
            if solution.cost < best_solution.cost:
                best_solution = deepcopy(solution)
            yield best_solution, T
    else:
        yield best_solution, None

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    input_data = InputData(args.people_file, 
                           args.tables_file)
    for (best_solution, T) in main(input_data):
        print_progress(best_solution, T)

    print_final_metrics(best_solution)
    write_people_to_csv(best_solution, args.output_people_filename)
    write_tables_to_csv(best_solution, args.output_tables_filename)
