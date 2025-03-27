from configuration.Constants import *
from configuration.Configuration import *
from utilities.Utilities import *
from utilities.main.business.BusinessGenerator import BusinessGenerator
from utilities.test.entities.PojoAndDtoTestGenerator import *


class BusinessTestGenerator:

    def __init__(self):
        None

    @staticmethod
    def create_business_test_class(table):
        """
        this method will create a business class for the project
        :param table:
        :return:
        """
        # create the file and open
        filename = table.toptestpackage + "/" + Constants.pckg_bus + "/" + table.camelcasejavaname + "ServiceTest.java"
        resources_file = open(filename, "w")
        business_file = open("files/business/business_test.txt")
        resources_file.write("package " + table.rootpackage + "." + Constants.pckg_bus + ";\n\n")
        for line in business_file:
            linestr = str(line)
            if (linestr.find("PRIMARY_KEY")) > -1:
                text = Utilities.create_get_pk_stmt(table, True)
                resources_file.write(linestr.replace("%", table.camelcasejavaname)
                                     .replace("&", table.lowercasename).replace("PRIMARY_KEY",text))
            elif linestr.find("RANDOM_DTO_GENERATOR") > -1:
                PojoAndDtoTestGenerator.create_pojo_and_dto_rand_gen_code(table, resources_file, "dto", True)
            elif linestr.find("RANDOM_POJO_GENERATOR") > -1:
                PojoAndDtoTestGenerator.create_pojo_and_dto_rand_gen_code(table, resources_file, "pojo", True)
            elif linestr.find("FKSECTION") > -1:
                BusinessTestGenerator.create_fk_section(table, resources_file)
            else:
                resources_file.write(linestr.replace("$", table.rootpackage)
                                     .replace("%", table.camelcasejavaname)
                                     .replace("&", table.lowercasename)
                                     .replace("^",Configuration.author))
        resources_file.close()
        business_file.close()

    @staticmethod
    def create_fk_section(table, output_file):
        """
        this method will create tests for all of the search by foreign key methods in the business classes
        :param table:
        :param output_file:
        :param test:
        :return:
        """
        BusinessGenerator.create_fk_section(table, output_file, True)

    @staticmethod
    def create_business_test_class_for_mid_lvl(mid_lvl_proj, crud_proj_names, crud_proj_data):
        """
        this method will create a business class for the mid-level projects
        :param mid_lvl_proj:
        :return:
        """
        # create the file and open
        filename = mid_lvl_proj.toptestpackage + "/" + Constants.pckg_bus + "/" + \
                   mid_lvl_proj.camelcasejavaname + "Service.java"
        resources_file = open(filename, "w")
        business_file = open("files/business/business_mid_lvl.txt")
        resources_file.write("package " + mid_lvl_proj.rootpackage + "." + Constants.pckg_bus + ";\n\n")
        for line in business_file:
            linestr = str(line)
            if (linestr.find("MAIN_SECTION")) > -1:
                BusinessTestGenerator.create_business_service_proxy_calls(mid_lvl_proj,
                                        crud_proj_names, crud_proj_data,resources_file)
            elif linestr.find("LOGGER_IMPORT") > -1:
                if Configuration.use_logging:
                    resources_file.write(Constants.import_logger_1 + "\n")
                    resources_file.write(Constants.import_logger_2 + "\n")
            elif linestr.find("SINGLETON_LOGGER") > -1:
                if Configuration.use_logging:
                    resources_file.write(Constants.tab + Constants.logger_singleton + "\n")
            else:
                resources_file.write(linestr.replace("%", mid_lvl_proj.camelcasejavaname)
                                     .replace("&", mid_lvl_proj.lowercasename)
                                     .replace("^", Configuration.author)
                                     .replace("$",mid_lvl_proj.rootpackage))
        resources_file.close()
        business_file.close()

    @staticmethod
    def create_business_service_proxy_calls(mid_lvl_proj, crud_proj_names, crud_proj_data, resources_file):
        """

        :param mid_lvl_proj:
        :param crud_proj_names:
        :param crud_proj_data:
        :param resources_file:
        :return:
        """
        tabs = Constants.tab
        mid_lvl_map = {}
        for project_name in mid_lvl_proj.lowerprojectnames:
            mid_lvl_map[project_name] = "YES"
        for projectname in crud_proj_names:
            currentproject = crud_proj_data[projectname]
            if currentproject.referencename in mid_lvl_map:
                filename = mid_lvl_proj.topmainpackage + "/" + Constants.path_proxy_services + \
                           "/" + currentproject.camelcasejavaname + "ServiceProxy.java"
                source_file = open(filename, "r")
                utilities = Utilities()
                for line in source_file:
                    linestr = str(line)
                    if(linestr.find("public ResponseEntity")) > -1:
                        templine = linestr.replace("public ResponseEntity<","").strip()
                        return_type = templine[0:templine.find(" ")-1]
                        method_name = utilities.remove_datatypes_from_string(linestr)
                        resources_file.write(Constants.doc_proxy)
                        resources_file.write(utilities.remove_annotations_from_string(linestr)
                                             .replace(";","{")+"\n")
                        if(linestr.find("create")>-1):
                            resources_file.write(
                                tabs + tabs + "return new ResponseEntity<" + return_type + ">(HttpStatus.CREATED);\n" +
                                tabs + "}\n\n")
                        else:
                            resources_file.write(tabs+tabs+
                                "return new ResponseEntity<" + return_type + ">(HttpStatus.OK);\n"+tabs+"}\n\n")
                source_file.close()