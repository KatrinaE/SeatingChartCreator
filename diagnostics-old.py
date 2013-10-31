# Check how many people sit at the same table multiple times
satZero = 0
satTwice = 0
satThrice = 0
satQuad = 0
satFive = 0

personArray=[]
for person in peopleThruFri:
    personTables=[person['Mon'],person['Tues'],person['Wed'],person['Thurs'],person['Fri']]
    personArray.append(personTables)

for personTables in personArray:
    icount = {}
    for i in personTables:
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

# Determine how many people sit together multiple times
overlaps = Counter(chain.from_iterable(combinations(table, 2) for table in all_tables_all_days))
print " "

#total number of possible pairings is n choose 2.
# all pairings that happen at least once appear once in 'overlaps'.
# so the total # of pairings that didn't happen is n choose 2 - len(overlaps)

overlapslength=0
for x in overlaps.itervalues():
    overlapslength += 1

def factorial(n):
    """factorial(n): return the factorial of the integer n.
    factorial(0) = 1
    factorial(n) with n<0 is -factorial(abs(n))
    """
    result = 1
    for i in xrange(1, abs(n)+1):
        result *= i
    if n >= 0:
        return result
    else:
        return -result

def binomial(n, k):
    """binomial(n, k): return the binomial coefficient (n k)."""
    assert n>0 and isinstance(n, (int, long)) and isinstance(k, (int,long))
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    return factorial(n) // (factorial(k) * factorial(n-k))

numpossiblepairings = binomial(len(people), 2)
missedpairings = numpossiblepairings - overlapslength

print "number of people"
print len(people)
print "pairings that never happen:"
print missedpairings

print "approximate max number of different pairings that could happen in time alloted"
print "(note: this is a high estimate)"
# each person's max is = number of days * other people who sat at their table each day
# sum across all people, divide by 2 to prevent double-counting
# for simplicity, assume each table seats 8 people each day
maxdiffpairings=(5*7)*len(people)/2
print maxdiffpairings

print "pairings that DID happen in time allotted"
print overlapslength

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

# Groups that sit together multiple times
groupOverlaps = Counter(chain.from_iterable(combinations(table, 3) for table in all_tables_all_days))

print "groups of 3 that sit together 2x:"
twice = 0
for x in groupOverlaps.itervalues():
    if x == 2:
        twice += 1
print twice

print "total overlaps are"
print sum(overlaps.values())

# Make sure everyone meets everyone else
# perhaps 'person who sits with the fewest people' <- maximize the # of people this person has sat with.


# Even distribution of doctors, nurses, and administrators
# (not sure yet how to check this - will depend on other implementations)