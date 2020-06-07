# Kennedy Genealogy
👨‍👩‍👧🌲

This project processes genealogy information found in GEDCOM files, a standard interchange format used by genealogists and genealogy software.

The program reads in a **Kennedy.ged** and builds a structure of objects that represent some of the information in the file (i.e. basic info about individuals and families) using the Person and Family classes. The functions processPerson() and processFamily() parse the GEDCOM file to create the Person and Family objects.

The Person.printDescendants() method initiates a traversal of the stored objects in a way that prints out a tree of descendants from the referenced instance of Person. This method uses the corresponding Family.printFamily() method to produce its output. Family.printFamily() calls Person.printDescendants() on each of the children of the family. 


**GEDtest.py** is used to to test the program and it assumes that the **Kennedy.ged** file has been loaded by the program. All of the printing and tests included in the test module are conditional, depending on input prompts that should be answered with a `Y` or `N`.
