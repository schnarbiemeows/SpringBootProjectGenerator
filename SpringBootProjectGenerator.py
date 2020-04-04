from popos.Table import *
from utilities.Utilities import *
from utilities.FileMaker import *
from utilities.JavaFileMaker import *
from utilities.TestFileMaker import *
from utilities.SqlParser import *
from utilities.Constants import *
from configuration.Configuration import *
import os
import sys
import shutil

"""
    created by Dylan I. Kessler
    03/29/2020
    
    This program will take an sql file that consists of "create table..." statements
    for each one of these that it finds, it will create a simple Spring Boot CRUD project that
    has a REST controller and uses JPA for persistance to this underlying table
"""
class SpringBootProjectGenerator:




    """
        initialize
    """
    def init(self):
        # template Spring Boot project that this program uses to clone into new projects
        self.sourceprojectfolder = "/Users/dylan/PycharmProjects/demo"
        # location of the SQL file to parse
        self.sourcesqlfile = "/Users/dylan/Desktop/PhaseII/Programs/NutritionMicroServiceSuite/SQL/accounts/temp.sql"
        # root detination folder where the new Spring Boot project(s) will go
        self.destinationroot = "/eclipse_workspaces/nutrition_microservices_workspace"
        self.artifactid = ""
        self.tablenames = []
        self.tabledata = {}
        self.sqlparser = SqlParser(self.tablenames,self.tabledata)
        self.filemaker = FileMaker()
        self.javafilemaker = JavaFileMaker()
        self.testfilemaker = TestFileMaker()


    """
        this method will create the basic folder structure of a SB project
    """
    def create_base_project_folders(self, table):
        self.filemaker.create_base_project_folders(table, self.sourceprojectfolder, self.destinationroot, self.artifactid, Configuration.groupid)

    """
        this method will parse through the source pom.xml to retrieve the artifactId
    """
    def parse_pom(self):
        utilities = Utilities()
        self.artifactid = utilities.parse_source_pom(self.sourceprojectfolder)



    """
        this method parses the main SQL file
    """
    def parsesqlfile(self):
        self.tablenames,self.tabledata = self.sqlparser.parseSqlFile(self.sourcesqlfile)

    """
        this method creates the application.properties file for the project
    """
    def create_application_resources_file(self,table):
        self.filemaker.create_application_resources_file(table)

    """
        this method creates the main Java file in the project
    """
    def create_main_method_file(self,table):
        self.javafilemaker.create_main_method_class(table)

    """
        this method creates the main test Java file in the project
    """
    def create_main_test_file(self, table):
        self.testfilemaker.create_main_test_class(table)

    """
        this method creates the swagger Java file in the project
    """
    def create_swagger_file(self, table):
        self.javafilemaker.create_swagger_class(table)

    """
        this method creates the base Exceptions Java file in the project
    """
    def create_exceptions_file(self, table):
        self.javafilemaker.make_base_exc_class(table)

    """
        this method creates the Repository Java file in the project
    """
    def create_repository_file(self, table):
        self.javafilemaker.create_repository_class(table)

    """
        this method creates the POJO Java file in the project
    """
    def create_pojo_class(self, table):
        self.javafilemaker.create_pojo_class(table)

    """
        this method creates the POJO Java file in the project
    """
    def create_controller_class(self, table):
        self.javafilemaker.create_controller_class(table)

    """
        this method creates the main test Java file in the project
    """
    def create_pojo_test_file(self, table):
        self.testfilemaker.create_pojo_test_class(table)

    """
        this method creates the main test Java file in the project
    """
    def create_controller_test_file(self, table):
        self.testfilemaker.create_controller_test_class(table)

    """
        this method will set a table's properties
    """
    def create_table_properties(self,currenttable):
        self.sqlparser.create_table_properties(currenttable)


    """
        main method of this program
    """
    def run(self):
        print("Begin execution")
        self.parse_pom()
        self.parsesqlfile()
        # for each table found, do:
        for name in self.tablenames:
            currenttable = Table(name, self.tabledata[name])
            self.create_table_properties(currenttable)
            self.create_base_project_folders(currenttable)
            currenttable.properties()
            self.create_application_resources_file(currenttable)
            self.create_main_method_file(currenttable)
            self.create_main_test_file(currenttable)
            self.create_swagger_file(currenttable)
            self.create_exceptions_file(currenttable)
            self.create_repository_file(currenttable)
            self.create_pojo_class(currenttable)
            self.create_controller_class(currenttable)
            self.create_pojo_test_file(currenttable)
            self.create_controller_test_file(currenttable)

"""
    main executable of this program
"""
if __name__ == '__main__':
    executable = SpringBootProjectGenerator()
    executable.init()
    executable.run()


