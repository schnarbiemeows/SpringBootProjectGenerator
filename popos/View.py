from re import *
from utilities.Utilities import Utilities


class View:
    
    def __init__(self,name,createviewstring):
        """
        initialization
        :param name:
        :param createviewstring:
        """
        print("initializing view object : " + name)
        self.is_mid_level = False
        self.viewname = name
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
        self.createviewstring = createviewstring
        self.configure_names()

    def configure_names(self):
        """
        configure names for this project
        :return:
        """
        # assume that the view name may have underscores, but no dashes
        self.correctedviewname = self.viewname.replace("`","").replace("~|*", "_")
        self.pomname = self.correctedviewname.lower().replace("_","-")
        self.projectname = self.pomname
        self.lowercasename = sub('[^A-Za-z0-9]+', '', self.correctedviewname).lower()
        #print("converting viewname : " + self.viewname + " to pom name = " + self.pomname)
        if(self.correctedviewname.find("_")>-1):
            index = 0
            convertedjavaname = ''
            toUpper = False
            x = range(len(self.correctedviewname))
            for n in x:
                if(toUpper == True):
                    convertedjavaname += self.correctedviewname[n].upper()
                    toUpper = False
                elif(self.correctedviewname[n] == "_"):
                    toUpper = True
                else:
                    convertedjavaname += self.correctedviewname[n]
            self.camelcasejavaname = Utilities.capitalize(convertedjavaname)
        else:
            self.camelcasejavaname = Utilities.capitalize(self.correctedviewname)
        self.dtoname = self.camelcasejavaname + "DTO"
        #print("converting viewname : " + self.correctedviewname + " to java name = " + self.camelcasejavaname)
        #print("converting viewname : " + self.correctedviewname + " to lower name = " + self.lowercasename)

    def properties(self,outputfile=None):
        """
        #print out the objects fields and properties
        :return:
        """
        #print("view - viewname = " + self.viewname)
        #print("view - pomname = " + self.pomname)
        #print("view - camelcasejavaname = " + self.camelcasejavaname)
        #print("view - lowercasename = " + self.lowercasename)
        if(outputfile is not None):
            outputfile.write("view - viewname = " + self.viewname+"\n")
            outputfile.write("view - pomname = " + self.pomname+"\n")
            outputfile.write("view - camelcasejavaname = " + self.camelcasejavaname+"\n")
            outputfile.write("view - lowercasename = " + self.lowercasename+"\n")
        for item in self.fieldnames:
            currentitem = self.fielddata[item]
            currentitem.properties(outputfile)