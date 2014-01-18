import random
import pdb

import camper_utils
import table_utils
from all_io import make_categories_list, import_campers, import_tables

# Define the basic data structures:
# camper_objects,
# camper_categories,
# table_objects,
# grouping_objects,        (grouping = collection of people @ a table on a specific day)
# and days_list.

(raw_camper_list, days) = import_campers('campers.csv')
camper_objects = camper_utils.create_camper_objects(raw_camper_list, days)
camper_categories = make_categories_list(raw_camper_list)
(table_objects, grouping_objects) = import_tables('tables.csv')                                 # area of trouble - import_tables does not create grouping objects
days_list = make_days_list(tables)

def compute_all_tables_all_days():
    all_tables_all_days = []
    for i in range (2,10):
        for day in ["Mon","Tues","Wed","Thurs","Fri"]:
            todaysTable = eval(str(getTable(i)) + "." + str(day))
            all_tables_all_days.append(todaysTable)
    return all_tables_all_days

def getTablesForCamper(openTables,camper,day):
    alreadySat = [camper['Mon'],camper['Tues'],camper['Wed'],camper['Thurs'],camper['Fri']]
    openTablesForCamper = deepcopy(openTables)

    # Remove tables from the list if the camper has already sat there twice
    for table in openTablesForCamper:
        if alreadySat.count(table[0]) >= 2:
            openTablesForCamper.remove(table)
    if openTablesForCamper == []:
        openTablesForCamper = deepcopy(openTables)
        for table in openTablesForCamper:
            if alreadySat.count(table[0]) >= 3:
                openTablesForCamper.remove(table)
        

    # Remove tables from the list if the camper has already sat there
    openTablesForCamperCopy = deepcopy(openTablesForCamper)
    for table in openTablesForCamperCopy:
        if table[0] in alreadySat:
            openTablesForCamperCopy.remove(table)
    if openTablesForCamperCopy != []:
        theTable = returnMinAlreadySatWith(camper,openTablesForCamperCopy,day)
        if theTable != "No table available":
            return theTable
    else:
        theTable = returnMinAlreadySatWith(camper,openTablesForCamper,day)
        return theTable

    
    # Only allow camper to sit at tables they've never sat at (unless that's not possible)
    if openTablesForCamper != []:
        return openTablesForCamper
    else:
        return openTables
    
def returnMinAlreadySatWith(camper,openTablesForCamper,day):
    # Remove tables from the list if the camper has already sat with a bunch of people
    alreadySatWith=alreadySatWithCamper(camper)
    openTablesForCamperObjects = []
    # Get the actual table objects
    for tableNumber in openTablesForCamper:
        if tableNumber[0] != '' and tableNumber != '1':
            table = getTable(tableNumber[0])
            openTablesForCamperObjects.append(table)
    #Compute the intersections of ppl already seated @ this table today w/ ppl this camper has already sat with
    alreadySatWithByTable = {}
    for table in openTablesForCamperObjects:
        todaysTable = table.getTodaysTable(day)
        peopleAlreadySatWith = [person for person in alreadySatWith if person in todaysTable]
        numAlreadySatWith = sum(1 for _ in peopleAlreadySatWith)
        alreadySatWithByTable[table.number] = numAlreadySatWith

    random.shuffle(openTablesForCamper)
    for tableNum,overlaps in alreadySatWithByTable.items():
        if overlaps == 0:
            for x in openTablesForCamper:
                if x[0] == tableNum:
                    return [x]
    for tableNum,overlaps in alreadySatWithByTable.items():
        if overlaps == 1:
            for x in openTablesForCamper:
                if x[0] == tableNum:
                    return [x]
    for tableNum,overlaps in alreadySatWithByTable.items():
        if overlaps == 2:
            for x in openTablesForCamper:
                if x[0] == tableNum:
                    return [x]
    #for tableNum,overlaps in alreadySatWithByTable.items():
    #    if overlaps == 3:
    #        for x in openTablesForCamper:
    #            if x[0] == tableNum:
    #                return [x]
    return "No table available"


def openGroupTables(tables,groupNumber,this_round):
    openTables = deepcopy(tables)
    openTablesCopy = deepcopy(openTables)

    # Hack - don't impose max #s of people for ha's, who are added to tables last
    if groupNumber == 2:
        for table in openTablesCopy:
            if table[4] >= table[5]:
                openTables.remove(table)
        return openTables

    for table in openTablesCopy:
        # remove tables that are full of this type of person for this round
        if table[groupNumber] >= this_round:
            openTables.remove(table)
        # remove tables that are full overall
        elif table[4] >= table[5]:
            openTables.remove(table)
    return openTables
    
    # This is where the meat of the work happens
def assignCampers(inGroup,day,dayTables,groupNumber,maxAtTable):
    groupTables = deepcopy(dayTables)
    inGroupCopy = deepcopy(inGroup)

    # Counters for how we are placing people at tables
    round = 1
    roundCounter = 0
    outTables = []

    # Figure out who needs to be assigned seats today
    # outGroup is where we will put the output, seed it w/ ppl @ head table
    studentGroup=notHead(inGroupCopy,day)
    outGroup=Head(inGroupCopy,day)

    while studentGroup != []:
        # Get a camper
        current_camper=random.choice(studentGroup)
        # Get a table
        openTables = openGroupTables(groupTables,groupNumber,round)
        openTablesForCamper = getTablesForCamper(openTables,current_camper,day)
        # Assign current camper to the table.
        camper_table = random.choice(openTablesForCamper)
        current_camper[day] = camper_table[0]
        tableObject = getTable(camper_table[0])
        tableObject.addCamper(current_camper["id"],day)
        studentGroup.remove(current_camper)
        outGroup.append(current_camper)

        # Increment the number of people at the table by 1
        camper_table[groupNumber] += 1
        camper_table[4] += 1

        # Put the table back into groupTables
        for n,i in enumerate(groupTables):
            if i[0] == camper_table[0]:
                groupTables[n] = camper_table

        # Increment counters
        roundCounter += 1
        if roundCounter == 9:
            round += 1        
            roundCounter = 0

    return outGroup,groupTables

def assignAllCampers(allCampers,day,dayTables):
    # Put all campers into lists by category
    ha = []
    medicine = []
    nursing = []

    for camper in allCampers:
        if camper['Category'] == 'Health Administration ':
            ha.append(camper)
        elif camper['Category'] == 'Medicine':
            medicine.append(camper)
        elif camper['Category'] == 'Nursing':
            nursing.append(camper)

    (docs, outTables) = assignCampers(medicine,day,dayTables,1,4)
    (has, outTables2) = assignCampers(ha,day,outTables,3,2)
    (nurses, outTablesFinal) = assignCampers(nursing,day,outTables2,2,3)

    # Add campers back together into 1 list
    allAssignedCampers = []
    allAssignedCampers[0:0] = docs
    allAssignedCampers[0:0] = has
    allAssignedCampers[0:0] = nurses
    return allAssignedCampers

#campersThruMon = assignAllCampers(campers,"Mon",tables)
#campersThruTues = assignAllCampers(campersThruMon,"Tues",tables)
#campersThruWed = assignAllCampers(campersThruTues,"Wed",wedTables)
#campersThruThurs = assignAllCampers(campersThruWed,"Thurs",tables)
#campersThruFri = assignAllCampers(campersThruThurs,"Fri",tables)


# Diagnostics go here
# (see diagnostics)

# Create the output file
#(see io)