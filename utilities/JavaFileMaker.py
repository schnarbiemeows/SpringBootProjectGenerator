#from configuration.Constants import *
from configuration.Configuration import *
from utilities.Utilities import *
"""
    this class creates the different Java files(excluding the test files)
"""
class JavaFileMaker:

    @staticmethod
    def create_main_method_class( project):
        """
        this method creates the main Application class for the project
        :param project:
        :return:
        """
        tabs = Constants.tab
        filename = project.topmainpackage + "/" + project.camelcasejavaname + "Application.java"
        main_file = open("files/main.txt", "r")
        resources_file = open(filename, "w")
        resources_file.write("package " + project.rootpackage + ";\n\n")
        for line in main_file:
            linestr = str(line)
            if linestr.find("IMPORTS") > -1:
                if Configuration.use_naming_server == True or Configuration.use_docker == True:
                    resources_file.write(Constants.import_feign+"\n")
                    resources_file.write(Constants.import_dc + "\n")
                    if Configuration.use_distributed_tracing == True:
                        resources_file.write(Constants.import_bean + "\n")
                        resources_file.write(Constants.import_sampler + "\n")
                if Configuration.use_logging == True:
                    resources_file.write(Constants.import_logger_1 + "\n")
                    resources_file.write(Constants.import_logger_2 + "\n")
            elif linestr.find("LOGGER_IMPORT")>-1:
                if Configuration.use_logging == True:
                    resources_file.write(tabs + Constants.logger_singleton + "\n")
            elif linestr.find("MAIN_BODY") > -1:
                if (Configuration.use_distributed_tracing == True):
                    resources_file.write(tabs+"@Bean\n")
                    resources_file.write(tabs+"public Sampler defaultSampler() {\n")
                    resources_file.write(tabs*2+"return Sampler.ALWAYS_SAMPLE;\n")
                    resources_file.write(tabs +"}\n")
            elif (linestr.find("RIBBON_CLIENT_ANN") > -1):
                if (Configuration.use_naming_server == True or Configuration.use_docker == True):
                    resources_file.write(Constants.ann_feign.replace("RIBBON_CLIENT_ANN", project.rootpackage)+"\n")
                    resources_file.write(Constants.ann_dc + "\n")
            else:
                resources_file.write(linestr.replace("^", Configuration.author).replace("%", project.camelcasejavaname))
        resources_file.close()
        main_file.close()

    @staticmethod
    def make_base_exc_class( project):
        """
        this method will make the base Exception class
        :param project:
        :return:
        """
        tabs = Constants.tab
        filename = project.topmainpackage + "/" + Constants.pckg_exc + "/ExceptionResponse.java"
        exception_file = open("files/exception.txt", "r")
        resources_file = open(filename, "w")
        resources_file.write("package " + project.rootpackage + "." + Constants.pckg_exc + ";\n\n")
        for line in exception_file:
            linestr = str(line)
            if (linestr.find("^") > -1):
                resources_file.write(linestr.replace("^", Configuration.author))
            elif linestr.find("LOGGER_IMPORT") > -1:
                if Configuration.use_logging == True:
                    resources_file.write(Constants.import_logger_1 + "\n")
                    resources_file.write(Constants.import_logger_2 + "\n")
            elif linestr.find("SINGLETON_LOGGER") > -1:
                if Configuration.use_logging == True:
                    resources_file.write(tabs + Constants.logger_singleton + "\n")
            else:
                resources_file.write(linestr)
        resources_file.close()
        exception_file.close()

    @staticmethod
    def make_rnf_exc_class( table):
        """
        this method will make the ResourceNotFoundException class
        :param table:
        :return:
        """
        tabs = Constants.tab
        filename = table.topmainpackage + "/" + Constants.pckg_exc + "/ResourceNotFoundException.java"
        exception_file = open("files/rnf_exc.txt", "r")
        resources_file = open(filename, "w")
        resources_file.write("package " + table.rootpackage + "." + Constants.pckg_exc + ";\n\n")
        for line in exception_file:
            linestr = str(line)
            if (linestr.find("^") > -1):
                resources_file.write(linestr.replace("^", Configuration.author))
            elif linestr.find("LOGGER_IMPORT") > -1:
                if Configuration.use_logging == True:
                    resources_file.write(Constants.import_logger_1 + "\n")
                    resources_file.write(Constants.import_logger_2 + "\n")
            elif linestr.find("SINGLETON_LOGGER") > -1:
                if Configuration.use_logging == True:
                    resources_file.write(tabs + Constants.logger_singleton + "\n")
            else:
                resources_file.write(linestr)
        resources_file.close()
        exception_file.close()

    @staticmethod
    def make_spec_eh_class( table):
        """
        this method will make the SpecializedExceptionHandler class
        :param table:
        :return:
        """
        tabs = Constants.tab
        filename = table.topmainpackage + "/" + Constants.pckg_exc + "/SpecializedExceptionHandler.java"
        exception_file = open("files/spec_eh.txt", "r")
        resources_file = open(filename, "w")
        resources_file.write("package " + table.rootpackage + "." + Constants.pckg_exc + ";\n\n")
        for line in exception_file:
            linestr = str(line)
            if (linestr.find("^") > -1):
                resources_file.write(linestr.replace("^", Configuration.author))
            elif linestr.find("LOGGER_IMPORT") > -1:
                if Configuration.use_logging == True:
                    resources_file.write(Constants.import_logger_1 + "\n")
                    resources_file.write(Constants.import_logger_2 + "\n")
            elif linestr.find("SINGLETON_LOGGER") > -1:
                if Configuration.use_logging == True:
                    resources_file.write(tabs + Constants.logger_singleton + "\n")
            else:
                resources_file.write(linestr)
        resources_file.close()
        exception_file.close()

    @staticmethod
    def create_randomizer_class( project):
        """
        this creates a class called Randomizer in the utilities package
        :param project:
        :return:
        """
        tabs = Constants.tab
        filename = project.topmainpackage + "/" + Constants.pckg_util + "/" + "Randomizer.java"
        randomizer_file = open("files/randomizer_text.txt", "r")
        resources_file = open(filename, "w")
        resources_file.write("package " + project.rootpackage + "." + Constants.pckg_util + ";\n\n")
        for line in randomizer_file:
            linestr = str(line).replace("^", Configuration.author)
            if linestr.find("LOGGER_IMPORT")>-1:
                if Configuration.use_logging == True:
                    resources_file.write(Constants.import_logger_1 + "\n")
                    resources_file.write(Constants.import_logger_2 + "\n")
            elif linestr.find("SINGLETON_LOGGER")>-1:
                if Configuration.use_logging == True:
                    resources_file.write(tabs + Constants.logger_singleton + "\n")
            else:
                resources_file.write(linestr)
        resources_file.close()
        randomizer_file.close()

    @staticmethod
    def create_swagger_class( project):
        """
        this method will make the swagger2 config file
        :param project:
        :return:
        """
        filename = project.topmainpackage + "/" + "SwaggerConfig.java"
        resources_file = open(filename, "w")
        swagger_file = open("files/swagger_text.txt","r")
        resources_file.write("package " + project.rootpackage + ";\n\n")
        for line in swagger_file:
            linestr = str(line)
            if(linestr.find("^")>-1):
                resources_file.write(linestr.replace("^", Configuration.author))
            elif(linestr.find("%")>-1):
                resources_file.write(linestr.replace("%", Configuration.author, 1).replace("%", Configuration.website, 1).replace("%", Configuration.email, 1))
            else:
                resources_file.write(linestr)
        resources_file.close()
        swagger_file.close()

    @staticmethod
    def create_health_check_controller(project):
        """
        this method will create a health check controller for the project
        :param project:
        :return:
        """
        # create the file and open
        tabs = Constants.tab
        filename = project.topmainpackage + "/" + Constants.pckg_contr + "/HealthCheckController.java"
        resources_file = open(filename, "w")
        controller_file = open("files/controller/health_check.txt")
        resources_file.write("package " + project.rootpackage + "." + Constants.pckg_contr + ";\n\n")
        for line in controller_file:
            linestr = str(line)
            if linestr.find("LOGGER_IMPORT") > -1:
                if Configuration.use_logging == True:
                    resources_file.write(Constants.import_logger_1 + "\n")
                    resources_file.write(Constants.import_logger_2 + "\n")
            elif linestr.find("SINGLETON_LOGGER") > -1:
                if Configuration.use_logging == True:
                    resources_file.write(tabs + Constants.logger_singleton + "\n")
            else:
                resources_file.write(linestr)
        resources_file.close()
        controller_file.close()
