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
        self.tablenames = []
        self.tabledata = {}
        self.sqlparser = SqlParser(self.tablenames,self.tabledata)
        self.filemaker = FileMaker()
        self.javafilemaker = JavaFileMaker()
        self.testfilemaker = TestFileMaker()

    def create_base_project_folders(self, table):
        """
        this method will create the basic folder structure of a SB project
        :param table:
        :return:
        """
        self.filemaker.create_base_project_folders(table, self.sourceprojectfolder, self.destinationroot, self.artifactid, Configuration.groupid)

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
        self.tablenames,self.tabledata = self.sqlparser.parseSqlFile(self.sourcesqlfile)

    def create_application_resources_file(self,table):
        """
        this method creates the application.properties file for the project
        :param table:
        :return:
        """
        self.filemaker.create_application_resources_file(table)

    def create_main_method_file(self,table):
        """
        this method creates the main Java file in the project
        :param table:
        :return:
        """
        self.javafilemaker.create_main_method_class(table)

    def create_main_test_file(self, table):
        """
        this method creates the main test Java file in the project
        :param table:
        :return:
        """
        self.testfilemaker.create_main_test_class(table)

    def create_swagger_file(self, table):
        """
        this method creates the swagger Java file in the project
        :param table:
        :return:
        """
        self.javafilemaker.create_swagger_class(table)

    def create_randomizer_class(self, table):
        """
        this method creates the swagger Java file in the project
        :param table:
        :return:
        """
        self.javafilemaker.create_randomizer_class(table)

    def create_exceptions_file(self, table):
        """
        this method creates the base Exceptions Java file in the project
        :param table:
        :return:
        """
        self.javafilemaker.make_base_exc_class(table)

    def make_rnf_exc_class(self, table):
        """
        this method creates the ResourceNotFoundException Java file in the project
        :param table:
        :return:
        """
        self.javafilemaker.make_rnf_exc_class(table)

    def make_spec_eh_class(self, table):
        """
        this method creates the SpecializedExceptionHandler Java file in the project
        :param table:
        :return:
        """
        self.javafilemaker.make_spec_eh_class(table)

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

    def run(self):
        """
        main method of this program
        :return:
        """
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
            self.create_randomizer_class(currenttable)
            self.create_swagger_file(currenttable)
            self.create_exceptions_file(currenttable)
            self.make_rnf_exc_class(currenttable)
            self.make_spec_eh_class(currenttable)
            self.create_repository_file(currenttable)
            self.create_pojo_class(currenttable)
            self.create_dto_class(currenttable)
            self.create_controller_class(currenttable)
            self.create_pojo_test_file(currenttable)
            self.create_dto_test_file(currenttable)
            self.create_controller_test_file(currenttable)
            self.create__exceptions_test_class(currenttable)
            self.create_randomizer_test_class(currenttable)

"""
    main executable of this program
"""
if __name__ == '__main__':
    executable = SpringBootProjectGenerator()
    executable.init()
    executable.run()


