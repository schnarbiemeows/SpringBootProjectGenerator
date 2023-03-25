from utilities.Utilities import *
from re import *
"""
    this class represent a table in the sql file, and all of its corresponding meta-data
    needed for generating the project associated with that file
"""
class Table:

    def __init__(self,name,createtablestring):
        """
        initialization
        :param name:
        :param createtablestring:
        """
        print("initializing table object : " + name)
        self.is_mid_level = False
        self.tablename = name
        self.projectname = ''
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
        self.fksymbolnames = []
        self.fksymboldata = {}
        self.fknames = []
        self.parentkeysymbolnames = []
        self.parentkeysymboldata = {}
        self.primarykeys = []
        self.uniquekeys = []
        self.droppk = False
        self.createtablestring = createtablestring
        self.configure_names()

    def configure_names(self):
        """
        configure names for this project
        :return:
        """
        # assume that the table name may have underscores, but no dashes
        self.correctedtablename = self.tablename.replace("`","").replace("~|*", "_")
        self.pomname = self.correctedtablename.lower().replace("_","-")
        self.projectname = self.pomname
        self.lowercasename = sub('[^A-Za-z0-9]+', '', self.correctedtablename).lower()
        #print("converting tablename : " + self.tablename + " to pom name = " + self.pomname)
        if(self.correctedtablename.find("_")>-1):
            index = 0
            convertedjavaname = ''
            toUpper = False
            x = range(len(self.correctedtablename))
            for n in x:
                if(toUpper == True):
                    convertedjavaname += self.correctedtablename[n].upper()
                    toUpper = False
                elif(self.correctedtablename[n] == "_"):
                    toUpper = True
                else:
                    convertedjavaname += self.correctedtablename[n]
            self.camelcasejavaname = Utilities.capitalize(convertedjavaname)
        else:
            self.camelcasejavaname = Utilities.capitalize(self.correctedtablename)
        self.dtoname = self.camelcasejavaname + "DTO"
        #print("converting tablename : " + self.correctedtablename + " to java name = " + self.camelcasejavaname)
        #print("converting tablename : " + self.correctedtablename + " to lower name = " + self.lowercasename)

    def properties(self,outputfile=None):
        """
        #print out the objects fields and properties
        :return:
        """
        #print("Table - tablename = " + self.tablename)
        #print("Table - pomname = " + self.pomname)
        #print("Table - camelcasejavaname = " + self.camelcasejavaname)
        #print("Table - lowercasename = " + self.lowercasename)
        if(outputfile is not None):
            outputfile.write("Table - tablename = " + self.tablename+"\n")
            outputfile.write("Table - pomname = " + self.pomname+"\n")
            outputfile.write("Table - camelcasejavaname = " + self.camelcasejavaname+"\n")
            outputfile.write("Table - lowercasename = " + self.lowercasename+"\n")
        for item in self.fieldnames:
            currentitem = self.fielddata[item]
            currentitem.properties(outputfile)
