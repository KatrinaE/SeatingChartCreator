import csv
import random
from copy import copy, deepcopy
from collections import Counter
from itertools import chain, combinations


# Create dictionary of campers (titled "campers")r
# Entry representing each camper has format {["Discipline"]:[discipline],["First Name"]:[name],["Last Name"]:[name],["Mon"]:[Monday table],["Tues"]:[Tuesday table],["Wed"]: Wednesday table, "Thurs" : Thursday table, "Fri" : Friday table}
reader = csv.DictReader(open("campers.csv","rwU"))
campers = [row for row in reader]
import pdb; pdb.set_trace()

# add a unique ID for each camper
def addIDs(people):
    i=1
    for person in people:
        person["id"] = i
        i +=1
    return people
campers = addIDs(campers)

# Determining if a person is at the head table
# Example call is isHead(nursing,"Mon")
# Used below in AssignCampers
def notHead(group,day):
    studentlist=[]
    for camper in group:
        if camper[day] != '1':
            studentlist.append(camper)
    return studentlist

def Head(group,day):
    headlist=[]
    for head in group:
        if head[day] == '1':
            headlist.append(head)
    return headlist

# Create array of tables in the format [table#,has,meds,nurses,total,capacity]
# Weds tables have different capacities bc more ppl sit @ head table
global tables
tables = [[2,0,0,0,0,7],
          [3,0,0,0,0,7],
          [4,0,0,0,0,7],
          [5,0,0,0,0,8],
          [6,0,0,0,0,8],
          [7,0,0,0,0,8],
          [8,0,0,0,0,8],
          [9,0,0,0,0,8],
          [10,0,0,0,0,8]]

wedTables = [[2,0,0,0,0,7],
          [3,0,0,0,0,7],
          [4,0,0,0,0,7],
          [5,0,0,0,0,7],
          [6,0,0,0,0,7],
          [7,0,0,0,0,8],
          [8,0,0,0,0,8],
          [9,0,0,0,0,8],
          [10,0,0,0,0,8]]

# Also create a table class
class Table:
    "Tables"
    def __init__(self, tableNumber,capacity,wedsCapacity):
        self.number=tableNumber
        self.capacity=capacity
        self.wedsCapacity=wedsCapacity
        self.Mon=[]
        self.Tues=[]
        self.Wed=[]
        self.Thurs=[]
        self.Fri=[]

    def __str__(self):
        return "table" + str(self.number)

    def addCamper(self,camperID,day):
        eval("self." + day).append(camperID)
        return

    def getTodaysTable(self,day):
        return eval("self." + day)

table2=Table(2,7,7)
table3=Table(3,7,7)
table4=Table(4,7,7)
table5=Table(5,8,7)
table6=Table(6,8,7)
table7=Table(7,8,8)
table8=Table(8,8,8)
table9=Table(9,8,8)
table10=Table(10,8,8)
    
def getTable(number):
    theTable= "table" + str(number)
    return eval(theTable)


def compute_all_tables_all_days():
    all_tables_all_days = []
    for i in range (2,10):
        for day in ["Mon","Tues","Wed","Thurs","Fri"]:
            todaysTable = eval(str(getTable(i)) + "." + str(day))
            all_tables_all_days.append(todaysTable)
    return all_tables_all_days

def alreadySatWithCamper(camper):
    allTablesTilNow = compute_all_tables_all_days()
    allOverlaps = Counter(chain.from_iterable(combinations(table, 2) for table in allTablesTilNow))

    alreadySatWith=[]
    i=0
    for key in allOverlaps.keys():
        if camper["id"] in key:
            pairs=list(key)
            pairs.remove(camper['id'])
            alreadySatWith.append(pairs[0])
    return alreadySatWith

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


def openGroupTables(tables,groupNumber,round):
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
        if table[groupNumber] >= round:
            openTables.remove(table)
        # remove tables that are full overall
        elif table[4] >= table[5]:
            openTables.remove(table)
    return openTables


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

    return (outGroup,groupTables)


def assignAllCampers(allCampers,day,dayTables):
    # Put all campers into lists by category
    ha = []
    medicine = []
    nursing = []

    for camper in allCampers:
        if camper['Discipline'] == 'Health Administration ':
            ha.append(camper)
        elif camper['Discipline'] == 'Medicine':
            medicine.append(camper)
        elif camper['Discipline'] == 'Nursing':
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

campersThruMon = assignAllCampers(campers,"Mon",tables)
campersThruTues = assignAllCampers(campersThruMon,"Tues",tables)
campersThruWed = assignAllCampers(campersThruTues,"Wed",wedTables)
campersThruThurs = assignAllCampers(campersThruWed,"Thurs",tables)
campersThruFri = assignAllCampers(campersThruThurs,"Fri",tables)

# Check how many people sit at the same table multiple times
satTwice = 0
satThrice = 0
satQuad = 0
satFive = 0

camperArray=[]
for camper in campersThruFri:
    camperTables=[camper['Mon'],camper['Tues'],camper['Wed'],camper['Thurs'],camper['Fri']]
    camperArray.append(camperTables)

for camper in camperArray:
    icount = {}
    for i in camper:
        icount[i] = icount.get(i, 0) + 1

    for key,value in icount.iteritems():
        if value == 2:
            satTwice += 1
        if value == 3:
            satThrice += 1
        if value == 4:
            satQuad += 1
        if value == 5:
            satFive += 1

print "# sitting @ same physical table twice"
print satTwice
print "# sitting @ same physical table 3 times"
print satThrice
print "# sitting @ same physical table 4 times"
print satQuad
print "# sitting @ same physical table 5 times"
print satFive

all_tables_all_days = compute_all_tables_all_days()
# Groups that sit together multiple times
groupOverlaps = Counter(chain.from_iterable(combinations(table, 3) for table in all_tables_all_days))

print "groups of 3 that sit together 2x:"
twice = 0
for x in groupOverlaps.itervalues():
    if x == 2:
        twice += 1
print twice

# Determine how many people sit together multiple times


overlaps = Counter(chain.from_iterable(combinations(table, 2) for table in all_tables_all_days))
print " "

print "pairs that sit together 2x:"
threetimes = 0
for x in overlaps.itervalues():
    if x == 2:
        threetimes += 1
print threetimes

print "pairs that sit together 3x:"
fourtimes = 0
for x in overlaps.itervalues():
    if x == 3:
        fourtimes += 1
print fourtimes

print "pairs that sit together 4x"
fivetimes = 0
for x in overlaps.itervalues():
    if x == 4:
        fivetimes += 1
print fivetimes

print "people who sit together 5x:"
twotimes = 0
for x in overlaps.itervalues():
    if x == 5:
        twotimes += 1
print twotimes


print "total overlaps are"
print sum(overlaps.values())

# Create the output file
fieldnames = ['id','Discipline', 'Last Name', 'First Name', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri']
test_file = open('test2.csv','wb')
csvwriter = csv.DictWriter(test_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in campersThruFri:
     csvwriter.writerow(row)
test_file.close()
