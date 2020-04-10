from popos.Table import *
from utilities.Constants import *
from configuration.Configuration import *
import os
import sys

"""
    this class generates all of the test classes
"""
class TestFileMaker:

    def create_main_test_class(self, project):
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
        

    def create_pojo_test_class(self,table,src):
        """
        create the POJO and DTO test classes
        :param table:
        :return:
        """
        # create the file and open
        filename = ''
        if src == "pojo":
            filename = table.toptestpackage + "/" + Constants.pckg_pojos + "/" + table.camelcasejavaname + "Test.java"
        else:
            filename = table.toptestpackage + "/" + Constants.pckg_dtos + "/" + table.dtoname + "Test.java"
        resources_file = open(filename, "w")
        test_pojo = open("files/pojo_and_dto_test.txt")
        if src == "pojo":
            resources_file.write("package " + table.rootpackage + "." + Constants.pckg_pojos + ";\n\n")
        else:
            resources_file.write("package " + table.rootpackage + "." + Constants.pckg_dtos + ";\n\n")
        for line in test_pojo:
            linestr = str(line)
            if(linestr.find("XXX"))>-1:
                self.create_pojo_setters_stmt(table, resources_file, "Y")
            elif linestr.find("YYY")>-1:
                self.create_pojo_setters_stmt(table, resources_file, "N")
            else:
                if src == "pojo":
                    resources_file.write(linestr.replace("&",table.camelcasejavaname).replace("%",table.tablename).replace("^",Configuration.author).replace("XXX","POJO"))
                else:
                    resources_file.write(linestr.replace("&", table.dtoname).replace("%", table.tablename).replace("^",Configuration.author).replace("XXX", "DTO"))
        resources_file.close()


    def create_pojo_setters_stmt(self, table, file, set):
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

    def create_pojo_and_dto_rand_gen_code(self, table, file, src):
        """
        this
        :param table:
        :param file:
        :param src:
        :return:
        """
        tabs = "\t"
        text = ''
        if src == "pojo":
            file.write(tabs + tabs + table.camelcasejavaname + " " + table.tablename + " = new " + table.camelcasejavaname + "();\n")
        else:
            file.write(tabs + tabs + table.dtoname + " " + table.tablename + " = new " + table.dtoname + "();\n")
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            if fielddata.isprimary == False:
                file.write(tabs + tabs + table.tablename + ".set" + fielddata.gettername+"(")
                if (fielddata.datatype == "BigDecimal"):
                    file.write('Randomizer.randomBigDecimal("1000"));\n')
                elif (fielddata.datatype == "BigInteger"):
                    file.write('Randomizer.randomBigInteger("1000"));\n')
                elif (fielddata.datatype == "Integer"):
                    file.write('Randomizer.randomInt(1000));\n')
                elif (fielddata.datatype == "Long"):
                    file.write('Randomizer.randomLong(1000L));\n')
                elif (fielddata.datatype == "Float"):
                    file.write('Randomizer.randomFloat(1000F));\n')
                elif (fielddata.datatype == "Double"):
                    file.write('Randomizer.randomDouble(1000D));\n')
                elif (fielddata.datatype == "Date"):
                    file.write('Randomizer.randomDate());\n')
                elif (fielddata.datatype == "Timestamp"):
                    file.write('Randomizer.randomTimestamp(1000));\n')
                elif (fielddata.datatype == "Time"):
                    file.write('Randomizer.randomTime(1000));\n')
                elif (fielddata.datatype == "byte[]"):
                    file.write('Randomizer.randomBytes(20));\n')
                elif (fielddata.datatype == "String"):
                    if fielddata.lengthreq == True:
                        if fielddata.length<20:
                            file.write('Randomizer.randomString('+str(fielddata.length)+'));\n')
                        else:
                            file.write('Randomizer.randomString(20));\n')
                    else:
                        file.write('Randomizer.randomString(20));\n')
        file.write(tabs + tabs + "return " + table.tablename + ";\n")

    def create_get_pk_stmt(self,table,file):
        """

        :param table:
        :param file:
        :return:
        """
        tabs = "\t"
        file.write(tabs+tabs+"int num = "+table.lowercasename+".get")
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            if fielddata.isprimary == True:
                file.write(fielddata.gettername+"();\n")

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
                resources_file.write("import " + table.rootpackage + "." + Constants.pckg_pojos + "." + table.camelcasejavaname + ";\n")
                resources_file.write("import " + table.rootpackage + "." + Constants.pckg_dtos + "." + table.dtoname + ";\n")
                resources_file.write("import " + table.rootpackage + "." + Constants.pckg_util + ".Randomizer;\n")
            elif linestr.find("ZZZ")>-1:
                self.create_pojo_and_dto_rand_gen_code(table, resources_file, "dto")
            elif linestr.find("QQQ")>-1:
                self.create_get_pk_stmt(table,resources_file)
            else:
                resources_file.write(linestr.replace("%",table.camelcasejavaname).replace("&",table.lowercasename).replace("^",Configuration.author))
        resources_file.close()

    def create__exceptions_test_class(self, table):
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

    def create_randomizer_test_class(self, table):
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
