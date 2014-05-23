## Seating Chart Creator
Seating Chart Creator is a Python desktop application that finds an 
optimal set of seating charts for a multi-day event, subject
to multiple constraints. It can be run either from the command line
or from a GUI. 

### Usage
#### Command Line
Run Seating Chart Creator from the command line via `main.py`. SCC requires
two inputs: a 'people' file and a 'tables' file, both in CSV format
(see below for examples).

    cd /your/path/to/SCC
    python main.py <input people file> <input tables file>

SCC outputs two CSV files - one organized by person, the other
by table. By default, these files are called `output-people.csv`
and `output-tables.csv` and are saved to the current directory.
You can use the optional `-p` and `-t` command-line arguments to 
save them somewhere else:

    python main.py input-ppl.csv input-tables.csv -p ~/file1.csv -t ~/file2.csv

#### GUI
Run the Seating Chart Creator GUI via `SeatingChartCreator.py`.
SCC requires two inputs: a 'people' file and a 'tables' file, both 
in CSV format (see below for examples). You will be able to select these
files from the GUI.


### Expected File Formats
Seating Chart Creator takes in two separate CSV files: one
containing the people attending the event,
and another containing the tables they may sit at.

#### People file
The first file must have columns for individuals' first names and last names,
for which category they are in, and for each day of the event.
The cells in these columns are empty unless an individual is sitting
at the head table that day, in which case the cell contains the word 'Head'.
This prevents SCC from moving the person out of the head table by mistake.

    # sample people csv.
    Category,Last Name,First Name,Mon,Tue,Wed,Thu,Fri
    Engineering,Johnson,Barbara,,,,,
    Sales,James,Diana,,,,,Head
    Management,Smith,Rose,,,,,


#### Tables file
The second must have columns for each table's name and for each day
of the event. The day columns contain the capacity
of each table on that day.

    # sample tables csv
    Table Name,Mon,Tue,Wed,Thu,Fri
    Head,5,5,7,5,5
    Table 1,10,10,10,10,10
    Table 2,7,7,7,7,7

The name 'Head' is reserved; no one will ever be switched into or out of this table.
This allows you to choose the specific individuals who will sit at the head table.

#### Output files
Seating Chart Creator outputs two CSV files: one sorted by person name, and one
sorted by table number. These look similar to the input files, but contain 
seating assignments.


### Constraints
Seating Chart Creator attempts to create a seating chart that satisfies the following
constraints:

1.  No two people may sit together more than once.
2.  No person may sit at the same table more than once.
3.  If there are multiple categories of attendees, people from each category
    must be evenly distributed across the tables.
4.  Each table must be a specified size, which varies from table
    to table and from day to day.

Simulated annealing is used to search for a solution that best satisfies these constraints.

If you have a head table (or other special table), people may pulled from the group
and seated there; they will not be switched to another table during the optimization process. 
The people sitting at the head table can vary from 
day to day. These arrangements are set in your `people` CSV file and not included in the 
optimization process.

### Configuration Options
Warning! Depending on the input, SCC can take a significant amount
of time (minutes to hours) to run.

The annealing parameters in `seating/config.py` can be modified to decrease the amount of time
SCC takes (at the expense of settling for a less-optimal solution).
    
    T = 1        # Do not change.
    alpha = 0.99        # Decrease to speed running time. Must be between 0 and 1.
    T_min = 0.001        # Increase to speed running time. Must be between 0 and 1.
    max_acceptable_cost = 0        # Increase to speed running time.
    iterations_per_temp = 500        # Decrease to speed running time.

The ideal settings vary depending on the input; for best results, you may want to spend some time
playing around with them.