from popos.Table import *
from utilities.Utilities import *
from utilities.Constants import *
from configuration.Configuration import *
import os
import sys
import xml.etree.ElementTree as ET
import shutil


class FileMaker:

    """
        this method will create the basic folder structure of a SB project
    """
    def create_base_project_folders(self, table, sourceprojectfolder, destinationroot, artifactid, groupid):
        utilities = Utilities()
        utilities.mkdir(destinationroot + "/" + table.pomname)
        utilities.mkdir(destinationroot + "/" + table.pomname + "/" + table.pomname)
        utilities.mkdir(destinationroot + "/" + table.pomname + "/" + table.pomname + "/.mvn")
        utilities.mkdir(destinationroot + "/" + table.pomname + "/" + table.pomname + "/.mvn/wrapper")

        utilities.cpy(sourceprojectfolder + "/" + artifactid + "/.mvn/wrapper/maven-wrapper.jar",
                      destinationroot + "/" + table.pomname + "/" + table.pomname + "/.mvn/wrapper/maven-wrapper.jar")
        utilities.cpy(sourceprojectfolder + "/" + artifactid + "/.mvn/wrapper/maven-wrapper.properties",
                      destinationroot + "/" + table.pomname + "/" + table.pomname + "/.mvn/wrapper/maven-wrapper.properties")
        utilities.cpy(sourceprojectfolder + "/" + artifactid + "/.mvn/wrapper/MavenWrapperDownloader.java",
                      destinationroot + "/" + table.pomname + "/" + table.pomname + "/.mvn/wrapper/MavenWrapperDownloader.java")

        utilities.mkdir(destinationroot + "/" + table.pomname + "/" + table.pomname + "/src")
        utilities.cpy(sourceprojectfolder + "/" + artifactid + "/.gitIgnore",
                      destinationroot + "/" + table.pomname + "/" + table.pomname + "/.gitIgnore")
        utilities.cpy(sourceprojectfolder + "/" + artifactid + "/HELP.md",
                      destinationroot + "/" + table.pomname + "/" + table.pomname + "/HELP.md")
        utilities.cpy(sourceprojectfolder + "/" + artifactid + "/mvnw",
                      destinationroot + "/" + table.pomname + "/" + table.pomname + "/mvnw")
        utilities.cpy(sourceprojectfolder + "/" + artifactid + "/mvnw.cmd",
                      destinationroot + "/" + table.pomname + "/" + table.pomname + "/mvnw.cmd")
        projectrootpackage = destinationroot + "/" + table.pomname + "/" + table.pomname + "/src/"
        utilities.mkdir(projectrootpackage + "main")
        utilities.mkdir(projectrootpackage + "test")
        utilities.mkdir(projectrootpackage + "main/java")
        utilities.mkdir(projectrootpackage + "main/resources")
        utilities.mkdir(projectrootpackage + "test/java")
        projectmainfolder = projectrootpackage + "main/java/"
        table.projectresourcesfolder = projectrootpackage + "main/resources/"
        projecttestfolder = projectrootpackage + "test/java/"
        # how far we have to go into the source folder depends on if the groupId has any periods in it, which each
        # represent its own sub-folder
        packages = groupid.split(".")
        packageslength = len(packages)
        topmainpackage = packages[0]
        toptestpackage = packages[0]
        utilities.mkdir(projectmainfolder + topmainpackage)
        utilities.mkdir(projecttestfolder + toptestpackage)
        if packageslength > 1:
            x = range(1, packageslength)
            for n in x:
                topmainpackage += "/" + packages[n]
                toptestpackage += "/" + packages[n]
                utilities.mkdir(projectmainfolder + topmainpackage)
                utilities.mkdir(projecttestfolder + toptestpackage)
        # now have to add the artifactID folder to these roots
        topmainpackage += "/" + table.lowercasename
        toptestpackage += "/" + table.lowercasename
        utilities.mkdir(projectmainfolder + topmainpackage)
        # make subpackages
        utilities.mkdir(projectmainfolder + topmainpackage + "/config")
        utilities.mkdir(projectmainfolder + topmainpackage + "/controllers")
        utilities.mkdir(projectmainfolder + topmainpackage + "/exceptions")
        utilities.mkdir(projectmainfolder + topmainpackage + "/dtos")
        utilities.mkdir(projectmainfolder + topmainpackage + "/pojos")
        utilities.mkdir(projectmainfolder + topmainpackage + "/services")
        utilities.mkdir(projectmainfolder + topmainpackage + "/utilities")

        utilities.mkdir(projecttestfolder + toptestpackage)
        # make subpackages
        utilities.mkdir(projecttestfolder + toptestpackage + "/config")
        utilities.mkdir(projecttestfolder + toptestpackage + "/controllers")
        utilities.mkdir(projecttestfolder + toptestpackage + "/exceptions")
        utilities.mkdir(projecttestfolder + toptestpackage + "/dtos")
        utilities.mkdir(projecttestfolder + toptestpackage + "/pojos")
        utilities.mkdir(projecttestfolder + toptestpackage + "/services")
        utilities.mkdir(projecttestfolder + toptestpackage + "/utilities")

        # set the Table object's main java and test package roots
        table.topmainpackage = projectmainfolder + topmainpackage
        table.toptestpackage = projecttestfolder + toptestpackage
        # rootpackage is for the individual Java files' "package ..." statement
        table.rootpackage = topmainpackage.replace("/", ".")
        self.create_pom_file(table,sourceprojectfolder,artifactid,destinationroot)

    """
        this method creates the application.properties file for the project
    """
    def create_application_resources_file(self, table):
        resources_file = open(table.projectresourcesfolder + "/application.properties", "w")
        resources_file.write(Configuration.app_log + "\n")
        resources_file.write(Configuration.app_jpa + "\n")
        resources_file.write(Configuration.app_jpa_show + "\n")
        resources_file.write(Configuration.app_hib_seq + "\n")
        resources_file.write(Configuration.app_mysql_conn + "\n")
        resources_file.write(Configuration.app_mysql_usr + "\n")
        resources_file.write(Configuration.app_mysql_pwd + "\n")
        resources_file.write(Configuration.app_actu_conf + "\n")
        resources_file.write(Configuration.app_sec_usr + "\n")
        resources_file.write(Configuration.app_sec_pwd + "\n")
        resources_file.close()

    """
        this method will copy the pom.xml while changing some things
        - it needs to change the groupId, artifactId, description, and name fields
        - it needs to add in the swagger2 dependencies(from dependencies.xml file)
        - it needs to add in the com.fasterxml.jackson.dataformat dependency(from dependencies.xml file)
        - it needs to add in the sonarqube and jacoco stuff(from jacoco_props.xml file and sonar_jacoco.xml file)  
    """
    def create_pom_file(self,table,sourceroot,artifactId,destinationroot):
        oldpom = open(sourceroot + "/" + artifactId + "/pom.xml","r")
        newpom = open(destinationroot + "/" + table.pomname + "/" + table.pomname + "/pom.xml","w")
        parentpassed = False
        groupIdadded = False
        artifactIdadded = False
        nameadded = False
        desc_added = False
        for item in oldpom:
            itemstr = str(item)
            if(parentpassed == False):
                newpom.write(itemstr)
                if(itemstr.find("</parent>")>-1):
                    parentpassed = True
            else:
                if(itemstr.find("</groupId>") > -1):
                    if(groupIdadded == False):
                        newpom.write(Constants.xml_grp.replace("*", Configuration.groupid)+"\n")
                        groupIdadded = True
                    else:
                        newpom.write(itemstr)
                elif (itemstr.find("</artifactId>") > -1):
                    if (artifactIdadded == False):
                        newpom.write(Constants.xml_art.replace("*",table.lowercasename)+"\n")
                        artifactIdadded = True
                    else:
                        newpom.write(itemstr)
                elif (itemstr.find("</name>") > -1):
                    if (nameadded == False):
                        newpom.write(Constants.xml_name.replace("*",table.pomname)+"\n")
                        nameadded = True
                    else:
                        newpom.write(itemstr)
                elif (itemstr.find("</description>") > -1):
                    if (desc_added == False):
                        newpom.write(Constants.xml_desc.replace("*",table.tablename))
                        desc_added = True
                    else:
                        newpom.write(itemstr)
                elif (itemstr.find("</properties>") > -1):
                    jacocoprops = open("files/jacoco_props.xml","r")
                    for prop in jacocoprops:
                        propstr = str(prop)
                        newpom.write(propstr)
                    jacocoprops.close()
                    newpom.write("\n")
                    newpom.write(itemstr)
                elif (itemstr.find("</dependencies>") > -1):
                    dependencies = open("files/dependencies.xml","r")
                    for dep in dependencies:
                        depstr = str(dep)
                        newpom.write(depstr)
                    dependencies.close()
                    newpom.write("\n")
                    newpom.write(itemstr)
                elif (itemstr.find("</plugins>") > -1):
                    sonarjacoco = open("files/sonar_jacoco.xml","r")
                    for line in sonarjacoco:
                        linestr = str(line)
                        newpom.write(linestr)
                    sonarjacoco.close()
                    newpom.write("\n")
                    newpom.write(itemstr)
                else:
                    newpom.write(itemstr)
        newpom.close()

