Seating Chart Creator is a Python desktop application that finds an 
optimal set of seating charts for a multi-day event, subject
to multiple constraints. It can be run either from the command line
or from a GUI.

###Constraints
1.  No two people may sit together more than once.
2.  No person may sit at the same table more than once.
3.  There are multiple categories of attendees. People from each category
    must be evenly distributed across the tables.
4.  Each table must be a specified size, which varies from table
    to table and from day to day.

****
In addition, several specific people must pulled from the group
and seated at the head table each day. The people sitting at the head table vary from day to day. These arrangements are preset and not
included in the optimization process.
****

###Inputs and Outputs
Seating Chart Creator takes in two separate CSV files: one
containing the people attending the event,
and another containing the tables they may sit at.

The first file must have columns for individuals' first names and last names,
for which category they are in, and for each day of the event.
The cells in these columns are empty unless an individual is sitting
at the head table that day, in which case the cell contains a 1.

The second must have columns for each table's name and for each day
of the conference. The day columns contain the capacity
of each table on that day.

Seating Chart Creator outputs a third CSV file
