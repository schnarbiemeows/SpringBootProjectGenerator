from utilities.Utilities import *

"""
    this class represent a table in the sql file, and all of its corresponding meta-data
    needed for generating the project associated with that file
"""
class Table:

    """
        initialization
    """
    def __init__(self,name,createtablestring):
        print("initializing table object : " + name)
        self.tablename = name
        self.pomname = ''
        self.camelcasejavaname = ''
        self.lowercasename = ''
        self.dtoname = ''
        self.projectresourcesfolder = ''
        self.topmainpackage = ''
        self.toptestpackage = ''
        self.rootpackage = ''
        self.fieldnames = []
        self.fielddata = {}
        self.hasprimary = False
        self.primary_name = None
        self.hasunique = False
        self.unique_name = None
        self.createtablestring = createtablestring
        self.configure_names()


    """
        configure names for this project
    """
    def configure_names(self):
        utilities = Utilities()
        # assume that the table name may have underscores, but no dashes
        self.pomname = self.tablename.replace("_","-")
        print("converting tablename : " + self.tablename + " to pom name = " + self.pomname)
        if(self.tablename.find("_")>-1):
            index = 0
            convertedjavaname = ''
            toUpper = False
            x = range(len(self.tablename))
            for n in x:
                if(toUpper == True):
                    convertedjavaname += self.tablename[n].upper()
                    self.lowercasename += self.tablename[n].lower()
                    toUpper = False
                elif(self.tablename[n] == "_"):
                    toUpper = True
                else:
                    convertedjavaname += self.tablename[n]
                    self.lowercasename += self.tablename[n].lower()
            self.camelcasejavaname = utilities.capitalize(convertedjavaname)
        else:
            self.camelcasejavaname = utilities.capitalize(self.tablename)
            self.lowercasename = self.tablename.lower()
        self.dtoname = self.camelcasejavaname + "DTO"
        print("converting tablename : " + self.tablename + " to java name = " + self.camelcasejavaname)
        print("converting tablename : " + self.tablename + " to lower name = " + self.lowercasename)

    """
        print out the objects fields and properties
    """
    def properties(self):
        print("Table - tablename = " + self.tablename)
        print("Table - pomname = " + self.pomname)
        print("Table - camelcasejavaname = " + self.camelcasejavaname)
        print("Table - lowercasename = " + self.lowercasename)
        print("Table - projectresourcesfolder = " + self.projectresourcesfolder)
        print("Table - topmainpackage = " + self.topmainpackage)
        print("Table - toptestpackage = " + self.toptestpackage)
        print("Table - rootpackage = " + self.rootpackage)
