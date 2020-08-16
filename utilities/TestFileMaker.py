from configuration.Constants import *
from configuration.Configuration import *
from utilities.Utilities import *

"""
    this class generates all of the test classes
"""
class TestFileMaker:

    @staticmethod
    def create_main_test_class( project):
        """
        this method creates the main Java file in the project
        :param project:
        :return:
        """
        filename = project.toptestpackage + "/" + project.camelcasejavaname + "ApplicationTests.java"
        resources_file = open(filename, "w")
        resources_file.write("package " + project.rootpackage + ";\n\n")
        resources_file.write("import org.junit.jupiter.api.Test;\n")
        resources_file.write("import org.springframework.boot.test.context.SpringBootTest;\n\n")
        resources_file.write("@SpringBootTest\n")
        resources_file.write(Constants.doc_main_class.replace("^", Configuration.author) + "\n")
        resources_file.write("class " + project.camelcasejavaname + "ApplicationTests {\n\n")
        resources_file.write("\t@Test\n")
        resources_file.write("\tvoid contextLoads() {\n")
        resources_file.write("\t}\n\n")
        resources_file.write("}")
        resources_file.close()

    @staticmethod
    def extract_get_pk_stmt(table):
        """

        :param table:
        :param file:
        :return:
        """
        tabs = Constants.tab
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            if fielddata.isprimary == True:
                return fielddata.gettername

    @staticmethod
    def create__exceptions_test_class( table):
        """
        create the ExceptionResponseTest class
        :param table:
        :return:
        """
        # create the file and open
        filename = table.toptestpackage + "/" + Constants.pckg_exc + "/ExceptionResponseTest.java"
        resources_file = open(filename, "w")
        resources_file.write("package " + table.rootpackage + "." + Constants.pckg_exc + ";\n\n")
        test_exc = open("files/base_exception_test.txt")
        for line in test_exc:
            linestr = str(line)
            resources_file.write(linestr.replace("^",Configuration.author))
        resources_file.close()

    @staticmethod
    def create_randomizer_test_class( table):
        """
        create the RandomizerTest class
        :param table:
        :return:
        """
        # create the file and open
        filename = table.toptestpackage + "/" + Constants.pckg_util + "/RandomizerTest.java"
        resources_file = open(filename, "w")
        resources_file.write("package " + table.rootpackage + "." + Constants.pckg_util + ";\n\n")
        resources_file.write("import " + table.rootpackage + "." + Constants.pckg_util + ".Randomizer;\n")
        test_exc = open("files/rand_test.txt")
        for line in test_exc:
            linestr = str(line)
            resources_file.write(linestr.replace("^", Configuration.author))
        resources_file.close()
