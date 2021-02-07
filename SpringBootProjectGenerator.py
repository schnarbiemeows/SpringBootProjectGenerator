from popos.Project import *
from utilities.SqlParser import *
from utilities.JsonUtility import *
from configuration.Configuration import *
from utilities.AngularFileMaker import *
from utilities.main.business.BusinessGenerator import BusinessGenerator
from utilities.main.entities.PojoAndDtoGenerator import *
from utilities.test.business.BusinessTestGenerator import BusinessTestGenerator
from utilities.test.entities.PojoAndDtoTestGenerator import *
from utilities.main.controllers.RestControllerGenerator import *
from utilities.test.controllers.RestControllerTestGenerator import *
from utilities.main.services.GenerateRepository import *
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
        self.artifactid = "demo"
        self.projectsnames = []
        self.projectdata = {}
        self.ang_proj_names = []
        self.ang_proj_data = {}
        self.ang_root_dir = ''
        self.tablenames = []
        self.tabledata = {}
        self.sqlparser = SqlParser(self.tablenames,self.tabledata)

    def create_base_project_folders(self, project):
        """
        this method will create the basic folder structure of a SB project
        :param project:
        :return:
        """
        FileMaker.create_base_project_folders(project, self.sourceprojectfolder, self.destinationroot, self.artifactid, Configuration.groupid)

    def parsesqlfile(self):
        """
        this method parses the main SQL file
        :return:
        """
        self.tablenames,self.tabledata = self.sqlparser.processSQL(self.sourcesqlfile)

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
                currenttable = self.tabledata[name]
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
                currenttable = self.tabledata[name]
                project.tablenames.append(name)
                project.tabledata[name] = currenttable
            self.projectdata[Configuration.project_name] = project
        elif(setting == 3):
            utilities = Utilities()
            projectnames,projectttables = utilities.parseGroupingsTextFile("configuration/groupings.txt")
            for name in projectnames:
                self.projectsnames.append(name)
                project = Project(name,portnum)
                portnum +=1
                for table in projectttables[name]:
                    # we have to account for tables with backticks
                    # @ this point, if there is a table named: `hi there`, that name is lost
                    # so we need to replace any spaces with ~|*
                    correctedtablename = table.replace(" ", "~|*")
                    if self.tabledata[correctedtablename] is None:
                        raise Exception("table name " + table + " not found in SQL file!")
                    else:
                        project.tablenames.append(correctedtablename)
                        currenttable = self.tabledata[correctedtablename]
                        project.tabledata[table] = currenttable
                self.projectdata[name] = project
        else:
            None

    def parseMidLevelFile(self):
        """

        :return:
        """
        # parse the mid-level --> lower level projects groupings file
        # get a list of mid-level project names and a map of mid-lvl-name --> List(lower-lvl-names)
        mid_lvl_projects, lwr_lvl_projects = Utilities.parseGroupingsTextFile("configuration/mid_level.txt")
        # get the starting mid-lvl project port #
        portnum = int(Configuration.mid_lvl_port_num)
        # list of mid-lvl project names
        localprojectsnames = []
        # map of mid-lvl-name --> Project object
        localprojectdata = {}
        # for each name found
        for mid_lvl_proj in mid_lvl_projects:
            # add its name to the name list
            localprojectsnames.append(mid_lvl_proj)
            # create a Project object
            project = Project(mid_lvl_proj, portnum)
            project.is_mid_level = True
            portnum += 1
            # get the list of lower level project names for this project
            lwr_lvl_projs = lwr_lvl_projects[mid_lvl_proj]
            # for each lower level project name
            for lwr_lvl_proj in lwr_lvl_projs:
                # get the lower level project
                lwr_proj = self.projectdata[lwr_lvl_proj]
                # get this project's tablenames
                lwr_tablenames = lwr_proj.tablenames
                # for each lower level project table name
                for lwr_tablename in lwr_tablenames:
                    # get the lower table
                    lwr_table = lwr_proj.tabledata[lwr_tablename]
                    # add it's name to the list of lower level table names for the mid-lvl project
                    project.tablenames.append(lwr_tablename)
                    # add this table's data to the map of lower level table data for the mid-level project
                    project.tabledata[lwr_tablename] = lwr_table
                project.lowerprojectnames.append(lwr_lvl_proj)
            # add the Project object to the map of project data
            localprojectdata[mid_lvl_proj] = project
        return (localprojectsnames,localprojectdata)


    def create_application_resources_file(self, project):
        """
        this method creates the application.properties file for the project
        :param project:
        :return:
        """
        FileMaker.create_application_resources_file(project)

    def create_main_method_file(self, project):
        """
        this method creates the main Java file in the project
        :param project:
        :return:
        """
        JavaFileMaker.create_main_method_class(project)

    def create_main_test_file(self, project):
        """
        this method creates the main test Java file in the project
        :param project:
        :return:
        """
        TestFileMaker.create_main_test_class(project)

    def create_swagger_file(self, project):
        """
        this method creates the swagger Java file in the project
        :param project:
        :return:
        """
        JavaFileMaker.create_swagger_class(project)

    def create_randomizer_class(self, project):
        """
        this method creates the swagger Java file in the project
        :param project:
        :return:
        """
        JavaFileMaker.create_randomizer_class(project)

    def create_exceptions_file(self, project):
        """
        this method creates the base Exceptions Java file in the project
        :param project:
        :return:
        """
        JavaFileMaker.make_base_exc_class(project)

    def make_rnf_exc_class(self, project):
        """
        this method creates the ResourceNotFoundException Java file in the project
        :param project:
        :return:
        """
        JavaFileMaker.make_rnf_exc_class(project)

    def make_spec_eh_class(self, project):
        """
        this method creates the SpecializedExceptionHandler Java file in the project
        :param project:
        :return:
        """
        JavaFileMaker.make_spec_eh_class(project)

    def create_repository_file(self, table):
        """
        this method creates the Repository Java file in the project
        :param table:
        :return:
        """
        GenerateRepository.create_repository_class(table)

    def create_proxy_classes(self, currentproject, projectnames, projectdata):
        """
        this method will create a GenericProxy Java file in the project
        :param table:
        :return:
        """
        JavaFileMaker.create_proxy_class(currentproject, projectnames, projectdata)

    def create_proxy_classes_for_mid_levels(self, mid_level_proj):
        """
        this method will create proxy classes for a mid_level project
        :param mid_level_proj:
        :return:
        """
        JavaFileMaker.create_proxy_classes_for_mid_levels(mid_level_proj, self.projectsnames, self.projectdata)

    def create_proxy_dtos(self, currentproject, projectnames, projectdata):
        """
        this method will create the DTOs needed for the proxy interfaces
        :param table:
        :return:
        """
        None
        JavaFileMaker.create_proxy_dtos(self.destinationroot, currentproject, projectnames, projectdata)

    def create_proxy_dtos_for_mid_lvl(self, currentproject):
        """
        this method will create the DTOs needed for the proxies for the mid-level projects
        :param table:
        :return:
        """
        None
        JavaFileMaker.create_proxy_dtos_for_mid_lvl(self.destinationroot, currentproject, self.projectsnames, self.projectdata)

    def create_proxy_pojos(self, currentproject, projectnames, projectdata):
        """
        this method will create the POJOs needed for the proxy interfaces
        :param table:
        :return:
        """
        None
        JavaFileMaker.create_proxy_pojos(self.destinationroot, currentproject, projectnames, projectdata)

    def create_proxy_pojos_for_mid_lvl(self, currentproject):
        """
        this method will create the POJOs needed for the proxies for the mid-level projects
        :param table:
        :return:
        """
        None
        JavaFileMaker.create_proxy_pojos_for_mid_lvl(self.destinationroot, currentproject, self.projectsnames, self.projectdata)

    def create_pojo_class(self, table):
        """
        this method creates the POJO Java file in the project
        :param table:
        :return:
        """
        PojoAndDtoGenerator.create_pojo_and_dto_classes(table, "pojo", self.tabledata)

    def create_pojo_response_class(self, project):
        """
        this method creates the POJO Java file in the project
        :param table:
        :return:
        """
        JavaFileMaker.create_pojo_response_class(project)

    def create_pojo_resonse_class_for_mid_level(self, project):
        """
        this method creates the POJO Java file in the project
        :param table:
        :return:
        """
        JavaFileMaker.create_pojo_response_class_for_mid_level(project)

    def create_dto_class(self, table):
        """
        this method creates the DTO Java file in the project
        :param table:
        :return:
        """
        PojoAndDtoGenerator.create_pojo_and_dto_classes(table, "dto", self.tabledata)

    def create_health_check_controller(self, project):
        """
        this method will create a health check controller for the project
        :param project:
        :return:
        """
        JavaFileMaker.create_health_check_controller(project)

    def create_controller_class(self, table):
        """
        this method creates the controller class for the project
        :param table:
        :return:
        """
        RestControllerGenerator.create_controller_class(table)

    def create_controller_class_for_mid_lvl(self, project):
        """
        this method creates the controller class for the mid-lvl projects
        :param project:
        :return:
        """
        RestControllerGenerator.create_controller_class_for_mid_lvl(project, self.projectsnames, self.projectdata)

    def create_business_class(self, table):
        """
        this method creates the Business class in the project
        :param table:
        :return:
        """
        BusinessGenerator.create_business_class(table)

    def create_business_class_for_mid_lvl(self, project):
        """
        this method creates the Business class in the mid-level project
        :param table:
        :return:
        """
        BusinessGenerator.create_business_class_for_mid_lvl(project, self.projectsnames, self.projectdata)

    def create_pojo_test_file(self, table):
        """
        this method creates the POJO test Java file
        :param table:
        :return:
        """
        PojoAndDtoTestGenerator.create_pojo_test_class(table,"pojo",self.tabledata)

    def create_dto_test_file(self, table):
        """
        this method creates the DTO test Java file
        :param table:
        :return:
        """
        PojoAndDtoTestGenerator.create_pojo_test_class(table,"dto",self.tabledata)

    def create__exceptions_test_class(self, table):
        """
        this method creates the exceptions test Java file
        :param table:
        :return:
        """
        TestFileMaker.create__exceptions_test_class(table)

    def create_randomizer_test_class(self, table):
        """
        this method creates the randomizer test Java file
        :param table:
        :return:
        """
        TestFileMaker.create_randomizer_test_class(table)

    def create_controller_test_file(self, table):
        """
        this method creates the main test Java file in the project
        :param table:
        :return:
        """
        RestControllerTestGenerator.create_controller_test_class(table)

    def create_controller_test_file_for_mid_level(self, project):
        """
        this method creates the main test Java file in the project
        :param project:
        :return:
        """
        RestControllerTestGenerator.create_controller_test_class_for_mid_level(project, self.projectsnames, self.projectdata)

    def create_business_test_class(self, table):
        """
        this method creates the Mock Business class for testing the Controller classes in the project
        :param table:
        :return:
        """
        BusinessTestGenerator.create_business_test_class(table)

    def create_business_test_class_for_mid_lvl(self, project):
        """
        this method creates the Mock Business class for testing the Controller classes in the mid-level project
        :param table:
        :return:
        """
        BusinessTestGenerator.create_business_test_class_for_mid_lvl(project, self.projectsnames, self.projectdata)

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
        FileMaker.createPostmanCollection(project)

    def make_postman_for_mid_level(self, project):
        """
        this method calls the JsonUtility class to generate a postman test collection for the project
        :param project:
        :return:
        """
        FileMaker.make_postman_for_mid_level(project)

    def backup_project(self, project):
        """
        this method will backup any project before changing it
        :param project:
        :return:
        """
        FileMaker.backup_project(project, self.destinationroot)

    def make_angular_projects(self):
        """
        this method will create the angular 8 project for a given project
        :param project:
        :return:
        """
        AngularFileMaker.make_angular_projects(self.ang_proj_names, self.ang_proj_data)

    def create_docker_file(self, project):
        """
        this method will make the docker file for the project
        :param project:
        :return:
        """
        FileMaker.create_docker_file(project)

    def initialize_kubernetes_file(self):
        """
        this method will initialize a complete kubernetes file for our project
        :return:
        """
        FileMaker.initialize_kubernetes_file()

    def create_kubernetes_file(self, project):
        """
        this method will make the kubernetes file for the project
        :param project:
        :return:
        """
        FileMaker.create_kubernetes_file(project)

    def create_kubernetes_commands_file(self, project):
        """
        this method will make the docker file for the project
        :param project:
        :return:
        """
        FileMaker.create_kubernetes_commands_file(project)

    def populate_kubernetes_commands_file(self, project):
        """
        this method will make the docker file for the project
        :param project:
        :return:
        """
        FileMaker.populate_kubernetes_commands_file(project)

    def generate_ingress_file(self,localprojectsnames,localprojectdata):
        """

        :return:
        """
        FileMaker.create_ingress_file(self.projectsnames, self.projectdata,localprojectsnames,localprojectdata)

    def run(self):
        """
        main method of this program
        :return:
        """
        print("Begin execution")
        localprojectsnames = []
        localprojectdata = []
        if(Configuration.use_docker == True):
            self.initialize_kubernetes_file()
        self.parsesqlfile()
        self.parsesqlfileToGroupProjects()
        for project in self.projectsnames:
            currentproject = self.projectdata[project]
            if(Configuration.create_angular_projects == True):
                self.ang_proj_names.append(project)
                self.ang_proj_data[project] = currentproject
            if(Configuration.backup_all_projects == True):
                self.backup_project(currentproject)
            self.create_base_project_folders(currentproject)
            if(Configuration.use_docker == True):
                self.create_docker_file(currentproject)
                self.create_kubernetes_file(currentproject)
                self.create_kubernetes_commands_file(currentproject)
                self.create_health_check_controller(currentproject)
            self.create_application_resources_file(currentproject)
            self.create_main_method_file(currentproject)
            self.create_main_test_file(currentproject)
            self.create_randomizer_class(currentproject)
            self.create_swagger_file(currentproject)
            self.create_exceptions_file(currentproject)
            self.make_rnf_exc_class(currentproject)
            self.make_spec_eh_class(currentproject)
            self.create_pojo_response_class(currentproject)
            self.create__exceptions_test_class(currentproject)
            self.create_randomizer_test_class(currentproject)
            self.populate_kubernetes_commands_file(currentproject)
            # for each table found for this project, do:
            for name in currentproject.tablenames:
                currenttable = currentproject.tabledata[name]
                currenttable.projectname = currentproject.pomname
                currenttable.rootpackage = currentproject.rootpackage
                currenttable.topmainpackage = currentproject.topmainpackage
                currenttable.toptestpackage = currentproject.toptestpackage
                #self.create_table_properties(currenttable)
                self.create_repository_file(currenttable)
                self.create_pojo_class(currenttable)
                self.create_dto_class(currenttable)
                if(Configuration.bypass_controllers != True):
                    self.create_controller_class(currenttable)
                if (Configuration.bypass_business != True):
                    self.create_business_class(currenttable)
                self.create_pojo_test_file(currenttable)
                self.create_dto_test_file(currenttable)
                if (Configuration.bypass_controllers != True):
                    self.create_controller_test_file(currenttable)
                    self.create_business_test_class(currenttable)
            self.create_postman_collection(currentproject)
        if (Configuration.use_naming_server == True):
            for project in self.projectsnames:
                currentproject = self.projectdata[project]
                self.create_proxy_classes(currentproject, self.projectsnames, self.projectdata)
                self.create_proxy_dtos(currentproject, self.projectsnames, self.projectdata)
                self.create_proxy_pojos(currentproject, self.projectsnames, self.projectdata)
        if(Configuration.make_mid_lvl_services==True):
            localprojectsnames, localprojectdata = self.parseMidLevelFile()
            for projectname in localprojectsnames:
                currentproject = localprojectdata[projectname]
                if (Configuration.create_angular_projects == True):
                    self.ang_proj_names.append(projectname)
                    self.ang_proj_data[projectname] = currentproject
                if (Configuration.backup_all_projects == True):
                    self.backup_project(currentproject)
                self.create_base_project_folders(currentproject)
                if (Configuration.use_docker == True):
                    self.create_docker_file(currentproject)
                    self.create_kubernetes_file(currentproject)
                    self.create_kubernetes_commands_file(currentproject)
                    self.create_health_check_controller(currentproject)
                self.create_application_resources_file(currentproject)
                self.create_main_method_file(currentproject)
                self.create_main_test_file(currentproject)
                self.create_randomizer_class(currentproject)
                self.create_swagger_file(currentproject)
                self.create_exceptions_file(currentproject)
                self.make_rnf_exc_class(currentproject)
                self.make_spec_eh_class(currentproject)
                self.create_pojo_resonse_class_for_mid_level(currentproject)
                self.create__exceptions_test_class(currentproject)
                self.create_randomizer_test_class(currentproject)
                self.create_proxy_classes_for_mid_levels(currentproject)
                self.create_proxy_dtos_for_mid_lvl(currentproject)
                self.create_proxy_pojos_for_mid_lvl(currentproject)
                if (Configuration.bypass_business != True):
                    self.create_business_class_for_mid_lvl(currentproject)
                if (Configuration.bypass_controllers != True):
                    self.create_controller_class_for_mid_lvl(currentproject)
                    self.create_controller_test_file_for_mid_level(currentproject)
                    self.create_business_test_class_for_mid_lvl(currentproject)
                self.make_postman_for_mid_level(currentproject)
                self.populate_kubernetes_commands_file(currentproject)
        if (Configuration.create_angular_projects == True):
                self.make_angular_projects()
        if(Configuration.use_docker == True):
            self.generate_ingress_file(localprojectsnames, localprojectdata)

"""
    main executable of this program
"""
if __name__ == '__main__':
    executable = SpringBootProjectGenerator()
    executable.init()
    executable.run()


