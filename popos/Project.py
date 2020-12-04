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

    def __init__(self, projectname, port):
        self.pomname = ''
        self.referencename = ''
        self.configure_reference_name(projectname)
        self.root = Configuration.destinationroot+"/" + self.pomname + "/" + self.pomname
        self.portnum = port
        self.lowercasename = ''
        self.camelcasejavaname = ''
        self.projectresourcesfolder = ''
        self.topmainpackage = ''
        self.toptestpackage = ''
        self.rootpackage = ''
        self.tablenames = []
        self.tabledata = {}
        self.lowerprojectnames = []
        self.lowerprojectdata = {}
        self.configure_names()
        self.is_mid_level = False
        self.service_config = []
        self.urls = {}
        self.rest_call_names = {}
        self.rest_call_types = {}
        self.rest_call_parameters = {}
        self.components = []

    def configure_reference_name(self, projectname):
        """

        :param projectname:
        :return:
        """
        if Configuration.generation_type == 1:
            self.referencename = projectname.replace("`","").replace("~|*", "-")
            self.pomname = self.referencename.lower()
        else:
            self.referencename = projectname
            self.pomname = projectname

    def configure_names(self):
        """
        configure names for this project
        :return:
        """
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
            self.camelcasejavaname = Utilities.capitalize(convertedjavaname)
        else:
            self.camelcasejavaname = Utilities.capitalize(self.pomname)
        print("converting pomname : " + self.pomname + " to java name = " + self.camelcasejavaname)
        print("converting pomname : " + self.pomname + " to lower name = " + self.lowercasename)