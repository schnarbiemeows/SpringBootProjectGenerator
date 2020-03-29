from popos.Table import *
from utilities.Utilities import *
import os
import sys
import xml.etree.ElementTree as ET
import shutil

"""
    created by Dylan I. Kessler
    03/29/2020
    
    This program will take an sql file that consists of "create table..." statements
    for each one of these that it finds, it will create a simple Spring Boot CRUD project that
    has a REST controller and uses JPA for persistance to this underlying table
"""
class SpringBootProjectDemo:

    """
        initialize
    """
    def init(self):
        # template Spring Boot project that this program uses to clone into new projects
        self.sourceprojectfolder = "/Users/dylan/PycharmProjects/demo"
        # location of the SQL file to parse
        self.sourcesqlfile = "/Users/dylan/Desktop/PhaseII/Programs/NutritionMicroServiceSuite/SQL/accounts/global_food_tables.sql"
        # root detination folder where the new Spring Boot project(s) will go
        self.destinationroot = "/eclipse_workspaces/nutrition_microservices_workspace"
        self.artifactid = ""
        self.groupid = ""
        self.description = ""


    """
        this method will parse through the pom.xml to retrieve certain data
        we need to get the groupId and artifactId and description from this pom
    """
    def parse_pom(self):
        pomfile = open(self.sourceprojectfolder+"/demo/pom.xml")
        tree = ET.parse(pomfile)
        root = tree.getroot()
        for child in root:
            childitem = str(child.tag)
            if(childitem.find('groupId')>-1):
                print(child.text)
                self.groupid = child.text
            if(childitem.find('artifactId')>-1):
                print(child.text)
                self.artifactid = child.text
            if (childitem.find('description') > -1):
                print(child.text)
                self.description = child.text
        pomfile.close()

    
    """
        this method will create the basic folder structure of a SB project
    """
    def create_base_project_folders(self,table):
        utilities = Utilities()
        utilities.mkdir(self.destinationroot+"/"+table.pomname)
        utilities.mkdir(self.destinationroot+"/"+table.pomname+"/"+table.pomname)
        utilities.mkdir(self.destinationroot + "/" + table.pomname + "/" + table.pomname + "/.mvn")
        utilities.mkdir(self.destinationroot + "/" + table.pomname + "/" + table.pomname + "/src")
        utilities.cpy(self.sourceprojectfolder+"/"+self.artifactid+"/.gitIgnore",self.destinationroot + "/" + table.pomname + "/" + table.pomname + "/.gitIgnore")
        utilities.cpy(self.sourceprojectfolder+"/"+self.artifactid+"/HELP.md",self.destinationroot + "/" + table.pomname + "/" + table.pomname + "/HELP.md")
        utilities.cpy(self.sourceprojectfolder+"/"+self.artifactid+"/mvnw",self.destinationroot + "/" + table.pomname + "/" + table.pomname + "/mvnw")
        utilities.cpy(self.sourceprojectfolder+"/"+self.artifactid+"/mvnw.cmd",self.destinationroot + "/" + table.pomname + "/" + table.pomname + "/mvnw.cmd")
        projectrootpackage = self.destinationroot + "/" + table.pomname + "/" + table.pomname + "/src/"
        utilities.mkdir(projectrootpackage+"main")
        utilities.mkdir(projectrootpackage + "test")
        utilities.mkdir(projectrootpackage + "main/java")
        utilities.mkdir(projectrootpackage + "main/resources")
        utilities.mkdir(projectrootpackage + "test/java")
        projectmainfolder = projectrootpackage+"main/java/"
        table.projectresourcesfolder = projectrootpackage + "main/resources/"
        projecttestfolder = projectrootpackage + "test/java/"
        # how far we have to go into the source folder depends on if the groupId has any periods in it, which each
        # represent its own sub-folder
        packages = self.groupid.split(".")
        packageslength = len(packages)
        topmainpackage = packages[0]
        toptestpackage = packages[0]
        utilities.mkdir(projectmainfolder + topmainpackage)
        utilities.mkdir(projecttestfolder + toptestpackage)
        if packageslength>1:
            x = range(1,packageslength)
            for n in x:
                topmainpackage += "/"+packages[n]
                toptestpackage += "/"+packages[n]
                utilities.mkdir(projectmainfolder + topmainpackage)
                utilities.mkdir(projecttestfolder + toptestpackage)
        # now have to add the artifactID folder to these roots
        topmainpackage += "/"+table.lowercasename
        toptestpackage += "/"+table.lowercasename
        utilities.mkdir(projectmainfolder + topmainpackage)
        utilities.mkdir(projecttestfolder + toptestpackage)
        # set the Table object's main java and test package roots
        table.topmainpackage = projectmainfolder + topmainpackage
        table.toptestpackage = projecttestfolder + toptestpackage
        table.rootpackage = topmainpackage.replace("/",".")
        

    def create_application_resources_file(self,table):
        resources_file = open(table.projectresourcesfolder+"/application.properties","w")
        resources_file.close()

    def create_main_method_file(self,table):
        filename = table.topmainpackage + "/" + table.camelcasejavaname + "Application.java"
        resources_file = open( filename, "w")
        resources_file.write("package " + table.rootpackage +";\n\n")
        resources_file.write("import org.springframework.boot.SpringApplication;\n")
        resources_file.write("import org.springframework.boot.autoconfigure.SpringBootApplication;\n\n")
        resources_file.write("@SpringBootApplication\n")
        resources_file.write("public class " + table.camelcasejavaname + "Application {\n\n")
        resources_file.write("\tpublic static void main(String[] args) {\n")
        resources_file.write("\t\tSpringApplication.run(" + table.camelcasejavaname + "Application.class, args);\n")
        resources_file.write("\t}\n\n")
        resources_file.write("}")
        resources_file.close()
    
    
    def run(self):
        print("Begin execution")
        self.parse_pom()
        currenttable = Table("my_table")
        self.create_base_project_folders(currenttable)
        currenttable.properties()
        self.create_application_resources_file(currenttable)
        self.create_main_method_file(currenttable)

if __name__ == '__main__':
    executable = SpringBootProjectDemo()
    executable.init()
    executable.run()


