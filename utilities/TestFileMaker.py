from popos.Table import *
from utilities.Constants import *
from configuration.Configuration import *
import os
import sys

"""
    this class generates all of the test classes
"""
class TestFileMaker:

    def create_main_test_class(self, table):
        """
        this method creates the main Java file in the project
        :param table:
        :return:
        """
        filename = table.toptestpackage + "/" + table.camelcasejavaname + "ApplicationTests.java"
        resources_file = open(filename, "w")
        resources_file.write("package " + table.rootpackage + ";\n\n")
        resources_file.write("import org.junit.jupiter.api.Test;\n")
        resources_file.write("import org.springframework.boot.test.context.SpringBootTest;\n\n")
        resources_file.write("@SpringBootTest\n")
        resources_file.write(Constants.doc_main_class.replace("^", Configuration.author) + "\n")
        resources_file.write("class " + table.camelcasejavaname + "ApplicationTests {\n\n")
        resources_file.write("\t@Test\n")
        resources_file.write("\tvoid contextLoads() {\n")
        resources_file.write("\t}\n\n")
        resources_file.write("}")
        resources_file.close()
        

    def create_pojo_test_class(self,table):
        """
        create the POJO test class
        :param table:
        :return:
        """
        # create the file and open
        filename = table.toptestpackage + "/" + Constants.pckg_pojos + "/" + table.camelcasejavaname + "Test.java"
        resources_file = open(filename, "w")
        test_pojo = open("files/pojo_test.txt")
        resources_file.write("package " + table.rootpackage + ".pojos;\n\n")
        for line in test_pojo:
            linestr = str(line)
            if(linestr.find("XXX"))>-1:
                self.create__pojo_setters_stmt(table, resources_file,"Y")
            elif linestr.find("YYY")>-1:
                self.create__pojo_setters_stmt(table, resources_file, "N")
            else:
                resources_file.write(linestr.replace("&",table.camelcasejavaname).replace("%",table.tablename).replace("^",Configuration.author))
        resources_file.close()


    def create__pojo_setters_stmt(self, table, file, set):
        """
        generate the getters and setters statement for the test class
        :param table:
        :param file:
        :param set: will always be Y or N
        :return:
        """
        tabs = "\t"
        text = ''
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            if set == "Y":
                file.write(tabs + tabs + table.tablename + ".set" + fielddata.gettername+"(")
                if (fielddata.datatype == "BigDecimal"):
                    file.write("new BigDecimal(1.00));\n")
                elif (fielddata.datatype == "BigInteger"):
                    file.write("new BigInteger(1));\n")
                elif (fielddata.datatype == "Integer"):
                    file.write("new Integer(1));\n")
                elif (fielddata.datatype == "Float"):
                    file.write("1.0f);\n")
                elif (fielddata.datatype == "Double"):
                    file.write("1.0);\n")
                elif (fielddata.datatype == "Date"):
                    file.write("new Date());\n")
                elif (fielddata.datatype == "Timestamp"):
                    file.write("new Timestamp(1000));\n")
                elif (fielddata.datatype == "Time"):
                    file.write("new java.sql.Time(1000));\n")
                elif (fielddata.datatype == "byte[]"):
                    file.write('"a".getBytes());\n')
                elif (fielddata.datatype == "String"):
                    file.write('"a");\n')
                elif (fielddata.datatype == "Long"):
                    file.write("new Long(1));\n")
            else:
                text += tabs + tabs + table.tablename + ".get" + fielddata.gettername + "(),\n"
        if set == 'N':
            text = text[0:-2]+");\n"
            file.write(text)


    def create_controller_test_class(self,table):
        """
        create the POJO test class
        :param table:
        :return:
        """
        # create the file and open
        filename = table.toptestpackage + "/" + Constants.pckg_contr + "/" + table.camelcasejavaname + "ControllerTest.java"
        resources_file = open(filename, "w")
        test_controller = open("files/controller_test.txt")
        resources_file.write("package " + table.rootpackage + ".controllers;\n\n")
        for line in test_controller:
            linestr = str(line)
            if(linestr.find("XXX"))>-1:
                resources_file.write("import " + table.topmainpackage+ ".pojos." + table.camelcasejavaname + ".java;\n")
            elif linestr.find("YYY")>-1:
                resources_file.write("\t\t% & = new %();".replace("%",table.camelcasejavaname).replace("&",table.tablename)+"\n")
                self.create__pojo_setters_stmt(table, resources_file, "Y")
            else:
                resources_file.write(linestr.replace("%",table.camelcasejavaname).replace("&",table.tablename).replace("^",Configuration.author))
        resources_file.close()

    def create__pojo_test_imports(self, table, file):
        """
        # create the imports
        :param file:
        :return:
        """
        None

    def create__pojo_test_class_decl(self, table, file):
        """
        # create the main class declaration with javadoc
        :param file:
        :return:
        """
        None

    def create__pojo_test_static_class(self, table, file):
        """
        # create a static instance of the table class
        :param file:
        :return:
        """
        None

    def create__pojo_test_def_const_and_setters(self, table, file):
        """
        # create the static object using the default constructor
        # and set each of the objects properties to test the setters
        :param file:
        :return:
        """
        None
    def create__pojo_test_field_constr_with_getters(self, table, file):
        """
        # create a second instance of the table object, calling the getters
        # to copy the values from the first object to this new object
        :param file:
        :return:
        """
        None

    def create__pojo_test_tostring(self, table, file):
        """
        # call the toString() method to test
        :param file:
        :return:
        """
        None