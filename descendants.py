"""
Audrey Kan
CPSC 3400 - Languages and Computation
May 2, 2019

ORIGINALITY OF CODE:
I assert that the submitted code was written by myself alone.

"Since this is a course that requires a significant amount of
programming and it is easy to find code for many programming
problems on the Internet, I want to be explicit about my
expectations regarding the code you submit for assignments.
I believe that you can learn a lot from looking at code written
by other people but that you learn very little by simply copying
code.  The learning objectives of this course include you learning
to write and debug programs in Python and F#.  All of the code you
turn in must have been written by you without immediate reference
to another solution to the problem you are solving.  That means
that you can look at other programs to see how someone solved a
similar problem, but you shouldn't have any code written by
someone else visible when you write yours (and you shouldn't have
looked at a solution just a few seconds before you type!).  You
should compose the code you write based on your understanding of
how the features of the language you are using can be used to
implement the algorithm you have chosen to solve the problem you
are addressing.  Doing it this way is "real programming" - in
contrast to just trying to get something to work by cutting and
pasting stuff you don't actually understand.  It is the only way
to achieve the learning objectives of the course."

GEDCOM parser design

Create empty dictionaries of individuals and families
Ask user for a file name and open the gedcom file
Read a line
Skip lines until a FAM or INDI tag is found
    Call functions to process those two types
Print descendant chart when all lines are processed

Processing an Individual
Get pointer string
Make dictionary entry for pointer with ref to Person object
Find name tag and identify parts (surname, given names, suffix)
Find FAMS and FAMC tags; store FAM references for later linkage
Skip other lines

Processing a family
Get pointer string
Make dictionary entry for pointer with ref to Family object
Find HUSB WIFE and CHIL tags
    Add included pointer to Family object
    [Not implemented ] Check for matching references in referenced Person object
        Note conflicting info if found.
Skip other lines

Print info from the collect of Person objects
Read in a person number
Print pedigree chart
"""


#-------------------------------------------------------------------------------

class Person():
    # Stores info about a single person
    # Created when an Individual (INDI) GEDCOM record is processed.
    #---------------------------------------------------------------------------

    def __init__(self,ref):
        # Initializes a new Person object, storing the string (ref) by
        # which it can be referenced.
        self._id = ref
        self._asSpouse = []  # use a list to handle multiple families
        self._asChild = None
        self._born = Event()
        self._died = Event()
                
    def addName(self, nameString):
        # Extracts name parts from nameString and stores them
        names = line[6:].split('/')  # Surname is surrounded by slashes
        self._given = names[0].strip()
        self._surname = names[1]
        self._suffix = names[2].strip()

    def addIsSpouse(self, famRef):
        # Adds the string (famRef) indicating family in which this person
        # is a spouse, to list of any other such families
        self._asSpouse += [famRef]
        
    def addIsChild(self, famRef):
        # Stores the string (famRef) indicating family in which this person
        # is a child
        self._asChild = famRef
    
    def addBirth(self, dateStr='', placeStr=''):
        self._born.addDate(dateStr)
        self._born.addPlace(placeStr)

    def addDeath(self, dateStr='', placeStr=''):
        self._died.addDate(dateStr)
        self._died.addPlace(placeStr)
        
    def printDescendants(self, prefix=''):
        # Print info for this person and then call method in Family
        print(prefix + self.__str__())
        # Recursion stops when self is not a spouse
        for fam in self._asSpouse:
            families[fam].printFamily(self._id,prefix)

    def isDescendant(self, personID):
        # Takes string (personID) and indicates if identified person is a
        # descendant of self
        if self._id == personID: return True
        # Recursion stops when self is not a spouse or if match is found
        for fam in self._asSpouse:
            if families[fam].isFamily(personID):
                return True
        return False

    def printAncestors(self, prefix=''):
        # Print info for this person and then call method in Family
        print(prefix + self.__str__())
        # Recursion stops when self is not a child in a family
        for fam in families:
            if self._id in families[fam]._children:
                families[fam].printParents(self._id, prefix)

    def printCousins(self, n = 1):
        # Print info for this person and then call method in Family
        level = n
        if level == 1: level = 'First'
        elif level == 2: level = 'Second'
        elif level == 3: level = 'Third'
        else: level = str(level)+'th'
        print(level+' cousins for '+self.name())
        
        cousinList = []
        for fam in families:
            if self._id in families[fam]._children:
                families[fam].findCousins(n, cousinList)
                return
        print("None")

    def cousinHelper(self, n, cousinList):
        for cousin in cousinList:
            if self._id in families[fam]._children:
                families[fam].findCousins(n, cousinList)
        
    def name(self):
        return self._given + ' ' + self._surname.upper()\
               + ' ' + self._suffix
    
    def __str__(self):
##        if self._asChild: # Make sure value is not None
##            childString = ' asChild: ' + self._asChild
##        else: childString = ''
##        if self._asSpouse != []: # Make sure _asSpouse list is not empty
##            spouseString = ' asSpouse: ' + str(self._asSpouse)
##        else: spouseString = ''
        return str(self._given + ' ' + self._surname.upper() + ' ' + self._suffix\
               + ' n:' + self._born.__str__() + ', d:' + self._died.__str__())

#-----------------------------------------------------------------------
                    
class Family():
    # Stores info about a family
    # Created when an Family (FAM) GEDCOM record is processed.
    #-------------------------------------------------------------------

    def __init__(self, ref):
        # Initializes a new Family object, storing the string (ref) by
        # which it can be referenced.
        self._id = ref
        self._husband = None
        self._wife = None
        self._children = []
        self._married = Event()

    def addHusband(self, personRef):
        # Stores the string (personRef) indicating the husband in this family
        self._husband = personRef

    def addWife(self, personRef):
        # Stores the string (personRef) indicating the wife in this family
        self._wife = personRef

    def addChild(self, personRef):
        # Adds the string (personRef) indicating a new child to the list
        self._children += [personRef]

    def addMarriage(self, dateStr='', placeStr=''):
        self._married.addDate(dateStr)
        self._married.addPlace(placeStr)
        
    def printFamily(self, firstSpouse, prefix):
        # Used by printDecendants in Person to print spouse
        # and recursively invoke printDescendants on children
        if prefix != '': prefix = prefix[:-2]+'  '
        if self._husband == firstSpouse:
            if self._wife:  # Make sure value is not None
                print(prefix+ '+' +str(persons[self._wife])\
                      + ', m:' + self._married.__str__())
        else:
            if self._husband:  # Make sure value is not None
                print(prefix+ '+' +str(persons[self._husband])\
                      + ', m:' + self._married.__str__())
        for child in self._children:
             persons[child].printDescendants(prefix+'|--')

    def isFamily(self, personID):
        # Used by isDescendant in Person to find spouse
        # and recursively invoke isDescendant on children
        for child in self._children:
            if persons[child].isDescendant(personID):
                return True
        return False

    def printParents(self, person, prefix):
        # Used by printAncestors in Person to print parent
        # and recursively invoke printAncestors on parents
        if prefix != '': prefix = prefix[:-2] + '  '
        if self._wife:   # Make sure value is not None
            persons[self._wife].printAncestors(prefix+'|  ')
        if self._husband:   # Make sure value is not None
            persons[self._husband].printAncestors(prefix+'|  ')
        # NOT IN TREE-STRUCTUED OUTPUT

    def findCousins(self, n, cousinList):
        # DOES NOT HANDLE N > 1
        while n:
            for fam in families:
                if self._husband in families[fam]._children: # If father is a child
                    for child in families[fam]._children: # Father's siblings
                        if child == self._husband: 
                            continue
                        for f in families:
                            if child == families[f]._wife or child == families[f]._husband:
                                cousinList += families[f]._children
                if self._wife in families[fam]._children: # If mother is a child
                    for child in families[fam]._children: # Mother's siblings
                        if child == self._wife: 
                            continue
                        for f in families:
                            if child == families[f]._wife or child == families[f]._husband:
                                cousinList += families[f]._children
            n -= 1
        if cousinList == []: print("None")
        else:
            for cousin in cousinList:
                print('  ' + persons[cousin].__str__())

                
    def __str__(self):
        if self._husband: # Make sure value is not None
            husbString = ' Husband: ' + self._husband
        else: husbString = ''
        if self._wife: # Make sure value is not None
            wifeString = ' Wife: ' + self._wife
        else: wifeString = ''
        if self._children != []: childrenString = ' Children: ' + str(self._children)
        else: childrenString = ''
        return husbString + wifeString + childrenString


#-----------------------------------------------------------------------
class Event():
    # Stores info about an event (i.e. birth, death, or marriage)
    # Created when an Individual (INDI) or Family (FAM) GEDCOM record
    # is processed.

    #-------------------------------------------------------------------

    def __init__(self):
        # Initializes a new Event object, storing the date and location
        # strings
        self._date = ''
        self._place = ''

    def addDate(self, dateStr):
        self._date = dateStr

    def addPlace(self, placeStr):
        self._place = placeStr
        
    def __str__(self):
        return self._date + ' ' + self._place
    
#-----------------------------------------------------------------------
 
def getPointer(line):
    # A helper function used in multiple places in the next two functions
    # Depends on the syntax of pointers in certain GEDCOM elements
    # Returns the string of the pointer without surrounding '@'s or trailing
    return line[8:].split('@')[0]
        
def processPerson(newPerson):
    global line
    line = f.readline()
    while line[0] != '0': # Process all lines until next 0-level
        tag = line[2:6]  # Substring where tags are found in 0-level elements
        if tag == 'NAME':
            newPerson.addName(line[7:])
        elif tag == 'FAMS':
            newPerson.addIsSpouse(getPointer(line))
        elif tag == 'FAMC':
            newPerson.addIsChild(getPointer(line))
        elif tag == 'BIRT':
            dateStr = ''
            placeStr = ''
            line = f.readline()
            while line[0] == '2': # Process all lines at 2-level
                if line[2:6] == 'DATE':
                    dateStr = line[7:].strip('\n')
                elif line[2:6] == 'PLAC':
                    placeStr = line[7:].strip('\n')
                line = f.readline()
            newPerson.addBirth(dateStr, placeStr)
            continue
        elif tag == 'DEAT':
            dateStr = ''
            placeStr = ''
            line = f.readline()
            while line[0] == '2': # Process all lines at 2-level
                if line[2:6] == 'DATE':
                    dateStr = line[7:].strip('\n')
                elif line[2:6] == 'PLAC':
                    placeStr = line[7:].strip('\n')
                line = f.readline()
            newPerson.addDeath(dateStr, placeStr)
            continue
        line = f.readline()

def processFamily(newFamily):
    global line
    line = f.readline()
    while line[0] != '0':  # process all lines until next 0-level
        tag = line[2:6]
        if tag == 'HUSB':
            newFamily.addHusband(getPointer(line))
        elif tag == 'WIFE':
            newFamily.addWife(getPointer(line))
        elif tag == 'CHIL':
            newFamily.addChild(getPointer(line))
        elif tag == 'MARR':
            dateStr = ''
            placeStr = ''
            line = f.readline()
            while line[0] == '2': # Process all lines at 2-level
                if line[2:6] == 'DATE':
                    dateStr = line[7:].strip('\n')
                elif line[2:6] == 'PLAC':
                    placeStr = line[7:].strip('\n')
                line = f.readline()
            newFamily.addMarriage(dateStr, placeStr)
            continue
        line = f.readline()

#-----------------------------------------------------------------------
#                            MAIN PROGRAM
#-----------------------------------------------------------------------

persons = {}  # Holds all references of Person objects
families = {} # Holds all references of Familiy objects

filename = "Kennedy.ged"  # Set a default name for the file to be processed
##filename = input("Type the name of the GEDCOM file:")

f = open (filename)
line = f.readline()
while line != '':  #While file is not empty
    fields = line.strip().split(' ')
    if line[0] == '0' and len(fields) > 2:
        if (fields[2] == "INDI"): 
            ref = fields[1].strip('@')
            persons[ref] = Person(ref)  ## tore ref to new Person
            processPerson(persons[ref])
        elif (fields[2] == "FAM"):
            ref = fields[1].strip('@')
            families[ref] = Family(ref) ## Store ref to new Family
            processFamily(families[ref])      
        else:    # 0-level line, but not of interest -- skip it
            line = f.readline()
    else:    # Skip lines until next candidate 0-level line
        line = f.readline()

import GEDtest
GEDtest.runtests(persons,families)
