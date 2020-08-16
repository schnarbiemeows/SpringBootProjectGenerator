from utilities.Utilities import *
from re import *
from configuration.Configuration import *

"""
    this class represent a project
"""
class Project:
    """
            initialization
        """

    def __init__(self, pomname, port):
        self.root = Configuration.destinationroot+"/" + pomname + "/" + pomname
        self.portnum = port
        self.pomname = pomname
        self.lowercasename = ''
        self.camelcasejavaname = ''
        self.projectresourcesfolder = ''
        self.topmainpackage = ''
        self.toptestpackage = ''
        self.rootpackage = ''
        self.tablenames = []
        self.tabledata = {}
        self.configure_names()
        self.is_mid_level = False
        self.service_config = []

    def configure_names(self):
        """
        configure names for this project
        :return:
        """
        utilities = Utilities()
        # assume that the table name may have underscores, but no dashes
        self.lowercasename = sub('[^A-Za-z]+', '', self.pomname).lower()
        print("converting pomname : " + self.pomname + " to lowercase name = " + self.lowercasename)
        if(self.pomname.find("-")>-1):
            index = 0
            convertedjavaname = ''
            toUpper = False
            x = range(len(self.pomname))
            for n in x:
                if(toUpper == True):
                    convertedjavaname += self.pomname[n].upper()
                    toUpper = False
                elif(self.pomname[n] == "-"):
                    toUpper = True
                else:
                    convertedjavaname += self.pomname[n]
            self.camelcasejavaname = utilities.capitalize(convertedjavaname)
        else:
            self.camelcasejavaname = utilities.capitalize(self.pomname)
        print("converting pomname : " + self.pomname + " to java name = " + self.camelcasejavaname)
        print("converting pomname : " + self.pomname + " to lower name = " + self.lowercasename)