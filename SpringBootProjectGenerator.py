from popos.Table import *
from popos.Project import *
from utilities.Utilities import *
from utilities.FileMaker import *
from utilities.JavaFileMaker import *
from utilities.TestFileMaker import *
from utilities.SqlParser import *
from utilities.Constants import *
from utilities.JsonUtility import *
from configuration.Configuration import *
import os
import sys
import shutil

"""
    created by Dylan I. Kessler
    03/29/2020
    
    This program will take an sql file that consists of "create table..." statements
    for each one of these that it finds, it will create a simple Spring Boot CRUD project that
    has a REST controller and uses JPA for persistance to this underlying table. The program will also
    add sonarQube analysis and Jaccoco code coverage dependencies to each project.
    
    The main configuration for this program is specified in Configuration.py, which has more details about
    how to configure it
"""
class SpringBootProjectGenerator:




    def init(self):
        # template Spring Boot project that this program uses to clone into new projects
        """
        initialize
        :return:
        """
        self.sourceprojectfolder = Configuration.sourceprojectfolder
        # location of the SQL file to parse
        self.sourcesqlfile = Configuration.sourcesqlfile
        # root detination folder where the new Spring Boot project(s) will go
        self.destinationroot = Configuration.destinationroot
        self.artifactid = ""
        self.projectsnames = []
        self.projectdata = {}
        self.tablenames = []
        self.tabledata = {}
        self.sqlparser = SqlParser(self.tablenames,self.tabledata)
        self.filemaker = FileMaker()
        self.javafilemaker = JavaFileMaker()
        self.testfilemaker = TestFileMaker()
        self.jsonutility = JsonUtility()

    def create_base_project_folders(self, project):
        """
        this method will create the basic folder structure of a SB project
        :param project:
        :return:
        """
        self.filemaker.create_base_project_folders(project, self.sourceprojectfolder, self.destinationroot, self.artifactid, Configuration.groupid)

    def parse_pom(self):
        """
        this method will parse through the source pom.xml to retrieve the artifactId
        :return:
        """
        utilities = Utilities()
        self.artifactid = utilities.parse_source_pom(self.sourceprojectfolder)

    def parsesqlfile(self):
        """
        this method parses the main SQL file
        :return:
        """
        self.tablenames,self.tabledata = self.sqlparser.parseSqlFileToExtractTableData(self.sourcesqlfile)

    def parsesqlfileToGroupProjects(self):
        """
        this method checks the Configuration.
        :return:
        """
        setting = Configuration.generation_type
        portnum = int(Configuration.beginning_port_num)
        if(setting == 1):
            # one project per table
            print("ONE PROJECT PER TABLE SPECIFIED")
            for name in self.tablenames:
                currenttable = Table(name, self.tabledata[name])
                self.projectsnames.append(currenttable.pomname)
                project = Project(currenttable.pomname,portnum)
                portnum +=1
                project.tablenames.append(name)
                project.tabledata[name] = currenttable
                self.projectdata[currenttable.pomname] = project
        elif(setting == 2):
            self.projectsnames.append(Configuration.project_name)
            project = Project(Configuration.project_name,portnum)
            for name in self.tablenames:
                currenttable = Table(name, self.tabledata[name])
                project.tablenames.append(name)
                project.tabledata[name] = currenttable
            self.projectdata[Configuration.project_name] = project
        elif(setting == 3):
            utilities = Utilities()
            projectnames,projectttables = utilities.parseGroupingsTextFile()
            for name in projectnames:
                self.projectsnames.append(name)
                project = Project(name,portnum)
                portnum +=1
                for table in projectttables[name]:
                    if self.tabledata[table] is None:
                        raise Exception("table name " + table + " not found in SQL file!")
                    else:
                        project.tablenames.append(table)
                        currenttable = Table(table, self.tabledata[table])
                        project.tabledata[table] = currenttable
                self.projectdata[name] = project
        else:
            None


    def create_application_resources_file(self, project):
        """
        this method creates the application.properties file for the project
        :param project:
        :return:
        """
        self.filemaker.create_application_resources_file(project)

    def create_main_method_file(self, project):
        """
        this method creates the main Java file in the project
        :param project:
        :return:
        """
        self.javafilemaker.create_main_method_class(project)

    def create_main_test_file(self, project):
        """
        this method creates the main test Java file in the project
        :param project:
        :return:
        """
        self.testfilemaker.create_main_test_class(project)

    def create_swagger_file(self, project):
        """
        this method creates the swagger Java file in the project
        :param project:
        :return:
        """
        self.javafilemaker.create_swagger_class(project)

    def create_randomizer_class(self, project):
        """
        this method creates the swagger Java file in the project
        :param project:
        :return:
        """
        self.javafilemaker.create_randomizer_class(project)

    def create_exceptions_file(self, project):
        """
        this method creates the base Exceptions Java file in the project
        :param project:
        :return:
        """
        self.javafilemaker.make_base_exc_class(project)

    def make_rnf_exc_class(self, project):
        """
        this method creates the ResourceNotFoundException Java file in the project
        :param project:
        :return:
        """
        self.javafilemaker.make_rnf_exc_class(project)

    def make_spec_eh_class(self, project):
        """
        this method creates the SpecializedExceptionHandler Java file in the project
        :param project:
        :return:
        """
        self.javafilemaker.make_spec_eh_class(project)

    def create_repository_file(self, table):
        """
        this method creates the Repository Java file in the project
        :param table:
        :return:
        """
        self.javafilemaker.create_repository_class(table)

    def create_pojo_class(self, table):
        """
        this method creates the POJO Java file in the project
        :param table:
        :return:
        """
        self.javafilemaker.create_pojo_and_dto_classes(table,"pojo")

    def create_dto_class(self, table):
        """
        this method creates the DTO Java file in the project
        :param table:
        :return:
        """
        self.javafilemaker.create_pojo_and_dto_classes(table,"dto")

    def create_controller_class(self, table):
        """
        this method creates the POJO Java file in the project
        :param table:
        :return:
        """
        self.javafilemaker.new_create_controller_class(table)

    def create_pojo_test_file(self, table):
        """
        this method creates the POJO test Java file
        :param table:
        :return:
        """
        self.testfilemaker.create_pojo_test_class(table,"pojo")

    def create_dto_test_file(self, table):
        """
        this method creates the DTO test Java file
        :param table:
        :return:
        """
        self.testfilemaker.create_pojo_test_class(table,"dto")

    def create__exceptions_test_class(self, table):
        """
        this method creates the exceptions test Java file
        :param table:
        :return:
        """
        self.testfilemaker.create__exceptions_test_class(table)

    def create_randomizer_test_class(self, table):
        """
        this method creates the randomizer test Java file
        :param table:
        :return:
        """
        self.testfilemaker.create_randomizer_test_class(table)

    def create_controller_test_file(self, table):
        """
        this method creates the main test Java file in the project
        :param table:
        :return:
        """
        self.testfilemaker.create_controller_test_class(table)

    def create_table_properties(self,currenttable):
        """
        this method will set a table's properties
        :param currenttable:
        :return:
        """
        self.sqlparser.create_table_properties(currenttable)

    def create_postman_collection(self, project):
        """
        this method calls the JsonUtility class to generate a postman test collection for the project
        :param project:
        :return:
        """
        self.jsonutility.createPostmanCollection(project)

    def run(self):
        """
        main method of this program
        :return:
        """
        print("Begin execution")
        self.parse_pom()
        self.parsesqlfile()
        self.parsesqlfileToGroupProjects()
        for project in self.projectsnames:
            currentproject = self.projectdata[project]
            self.create_base_project_folders(currentproject)
            self.create_application_resources_file(currentproject)
            self.create_main_method_file(currentproject)
            self.create_main_test_file(currentproject)
            self.create_randomizer_class(currentproject)
            self.create_swagger_file(currentproject)
            self.create_exceptions_file(currentproject)
            self.make_rnf_exc_class(currentproject)
            self.make_spec_eh_class(currentproject)
            self.create__exceptions_test_class(currentproject)
            self.create_randomizer_test_class(currentproject)
            # for each table found for this project, do:
            for name in currentproject.tablenames:
                currenttable = currentproject.tabledata[name]
                currenttable.rootpackage = currentproject.rootpackage
                currenttable.topmainpackage = currentproject.topmainpackage
                currenttable.toptestpackage = currentproject.toptestpackage
                self.create_table_properties(currenttable)
                #currenttable.properties()
                self.create_repository_file(currenttable)
                self.create_pojo_class(currenttable)
                self.create_dto_class(currenttable)
                self.create_controller_class(currenttable)
                self.create_pojo_test_file(currenttable)
                self.create_dto_test_file(currenttable)
                self.create_controller_test_file(currenttable)
            self.create_postman_collection(currentproject)


"""
    main executable of this program
"""
if __name__ == '__main__':
    executable = SpringBootProjectGenerator()
    executable.init()
    executable.run()


