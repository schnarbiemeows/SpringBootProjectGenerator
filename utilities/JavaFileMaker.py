from popos.Table import *
from utilities.Utilities import *
from utilities.Constants import *
from configuration.Configuration import *
import os
import sys
import xml.etree.ElementTree as ET
import shutil

"""
    this class creates the different Java files(excluding the test files)
"""
class JavaFileMaker:

    def create_main_method_class(self, project):
        """
        this method creates the main Application class for the project
        :param project:
        :return:
        """
        filename = project.topmainpackage + "/" + project.camelcasejavaname + "Application.java"
        main_file = open("files/main.txt", "r")
        resources_file = open(filename, "w")
        resources_file.write("package " + project.rootpackage + ";\n\n")
        for line in main_file:
            linestr = str(line)
            if (linestr.find("YYY") > -1):
                if(Configuration.use_naming_server == True):
                    resources_file.write(Constants.import_feign+"\n")
            elif (linestr.find("XXX") > -1):
                if (Configuration.use_naming_server == True):
                    resources_file.write(Constants.ann_feign.replace("XXX", project.rootpackage)+"\n")
            else:
                resources_file.write(linestr.replace("^", Configuration.author).replace("%", project.camelcasejavaname))
        resources_file.close()
        main_file.close()

    def make_base_exc_class(self, project):
        """
        this method will make the base Exception class
        :param project:
        :return:
        """
        filename = project.topmainpackage + "/" + Constants.pckg_exc + "/ExceptionResponse.java"
        exception_file = open("files/exception.txt", "r")
        resources_file = open(filename, "w")
        resources_file.write("package " + project.rootpackage + "." + Constants.pckg_exc + ";\n\n")
        for line in exception_file:
            linestr = str(line)
            if (linestr.find("^") > -1):
                resources_file.write(linestr.replace("^", Configuration.author))
            else:
                resources_file.write(linestr)
        resources_file.close()
        exception_file.close()
        
    def make_rnf_exc_class(self, table):
        """
        this method will make the ResourceNotFoundException class
        :param table:
        :return:
        """
        filename = table.topmainpackage + "/" + Constants.pckg_exc + "/ResourceNotFoundException.java"
        exception_file = open("files/rnf_exc.txt", "r")
        resources_file = open(filename, "w")
        resources_file.write("package " + table.rootpackage + "." + Constants.pckg_exc + ";\n\n")
        for line in exception_file:
            linestr = str(line)
            if (linestr.find("^") > -1):
                resources_file.write(linestr.replace("^", Configuration.author))
            else:
                resources_file.write(linestr)
        resources_file.close()
        exception_file.close()
        
    def make_spec_eh_class(self, table):
        """
        this method will make the SpecializedExceptionHandler class
        :param table:
        :return:
        """
        filename = table.topmainpackage + "/" + Constants.pckg_exc + "/SpecializedExceptionHandler.java"
        exception_file = open("files/spec_eh.txt", "r")
        resources_file = open(filename, "w")
        resources_file.write("package " + table.rootpackage + "." + Constants.pckg_exc + ";\n\n")
        for line in exception_file:
            linestr = str(line)
            if (linestr.find("^") > -1):
                resources_file.write(linestr.replace("^", Configuration.author))
            else:
                resources_file.write(linestr)
        resources_file.close()
        exception_file.close()

    def create_pojo_and_dto_classes(self, table, src):
        """
        this method will make a POJO from a Table object
        :param table:
        :return:
        """
        # create the file and open
        filename = ''
        if src == "pojo":
            filename = table.topmainpackage + "/" + Constants.pckg_pojos + "/" + table.camelcasejavaname + ".java"
        else:
            filename = table.topmainpackage + "/" + Constants.pckg_dtos + "/" + table.dtoname + ".java"
        resources_file = open(filename, "w")
        # create the package statement
        self.create_package_stmt(table,resources_file,src)
        # create the imports
        self.create_imports(table,resources_file,src)
        # create the main class declaration with javadoc
        self.create_class_decl(table,resources_file,src)
        # create the fields
        self.create_the_fields(table, resources_file,src)
        # create the default constructor
        self.create_def_constr(table, resources_file,src)
        # create the fields constructor
        self.create_field_constr(table, resources_file,src)
        # create the getters and setters
        self.create_get_n_set(table,resources_file)
        # create the toString
        self.create_tostring(table, resources_file,src)
        # create the GSON json --> object conversion method
        self.create_gson_conv(table, resources_file,src)
        # create the static dto <--> pojo conversion method
        self.create_dto_pojo_conv(table, resources_file, src)
        # finish the class with a trailing }
        resources_file.write("}\n")
        resources_file.close()

    def create_randomizer_class(self, project):
        """
        this creates a class called Randomizer in the utilities package
        :param project:
        :return:
        """
        filename = project.topmainpackage + "/" + Constants.pckg_util + "/" + "Randomizer.java"
        randomizer_file = open("files/randomizer_text.txt", "r")
        resources_file = open(filename, "w")
        resources_file.write("package " + project.rootpackage + "." + Constants.pckg_util + ";\n\n")
        for line in randomizer_file:
            linestr = str(line).replace("^", Configuration.author)
            resources_file.write(linestr)
        resources_file.close()
        randomizer_file.close()

    def create_proxy_class(self, table, projectnames, projectdata):
        """
        this method will create the Repository class file
        :param table:
        :return:
        """
        if(Configuration.naming_server_proxy_mode == 2):
            for projectname in projectnames:
                currentproject = projectdata[projectname]
                if(table.projectname != currentproject.pomname):
                    for tablename in currentproject.tablenames:
                        proxytable = currentproject.tabledata[tablename]
                        filename = table.topmainpackage + "/" + Constants.pckg_services + "/" + proxytable.camelcasejavaname + "ServiceProxy.java"
                        resources_file = open(filename, "w")
                        resources_file.write("package " + table.rootpackage + "." + Constants.pckg_services + ";\n\n")
                        proxy_file = open("files/specific_proxy.txt", "r")
                        for line in proxy_file:
                            linestr = str(line)
                            resources_file.write(linestr.replace("^", Configuration.author).replace("%", proxytable.camelcasejavaname).replace("XXX",currentproject.pomname))
                        resources_file.close()
                        proxy_file.close()
        else:
            filename = table.topmainpackage + "/" + Constants.pckg_services + "/" + "GenericServiceProxy.java"
            resources_file = open(filename, "w")
            resources_file.write("package " + table.rootpackage + "." + Constants.pckg_services + ";\n\n")
            proxy_file = open("files/generic_proxy.txt", "r")
            for line in proxy_file:
                linestr = str(line)
                resources_file.write(linestr.replace("^",Configuration.author))
            resources_file.close()
            proxy_file.close()

    def create_repository_class(self, table):
        """
        this method will create the Repository class file
        :param table:
        :return:
        """
        filename = table.topmainpackage + "/" + Constants.pckg_services + "/" + table.camelcasejavaname + "Repository.java"
        resources_file = open(filename, "w")
        resources_file.write("package " + table.rootpackage + "." + Constants.pckg_services + ";\n\n")
        resources_file.write(Constants.import_repo + "\n")
        resources_file.write(Constants.import_pojo.replace("%",table.rootpackage+".pojos."+table.camelcasejavaname)+"\n")
        resources_file.write(Constants.doc_main_class.replace("^", Configuration.author) + "\n")
        resources_file.write(Constants.class_decl_repo.replace("*",table.camelcasejavaname) + "\n")
        resources_file.close()

    def create_swagger_class(self, project):
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

    def create_business_class(self,table):
        """
        this method will create a business class for the project
        :param table:
        :return:
        """
        # create the file and open
        filename = table.topmainpackage + "/" + Constants.pckg_bus + "/" + table.camelcasejavaname + "Business.java"
        resources_file = open(filename, "w")
        business_file = open("files/business.txt")
        resources_file.write("package " + table.rootpackage + "." + Constants.pckg_bus + ";\n\n")
        for line in business_file:
            linestr = str(line)
            if (linestr.find("XXX")) > -1:
                text = self.create_get_pk_stmt(table)
                resources_file.write(linestr.replace("%", table.camelcasejavaname).replace("&", table.lowercasename).replace("XXX",text))
            else:
                resources_file.write(linestr.replace("%", table.camelcasejavaname).replace("&", table.lowercasename).replace("^",Configuration.author))
        resources_file.close()
        business_file.close()

    def create_controller_class(self, table):
        """
        this method will create the RestController for the project
        the rest controller will have methods to
        - get all objects(GET)
        - get an object by ID(only if they have a primary key or a unique key(GET)
        - create an object(POST)
        - update an object(POST)
        - delete an object(DELETE)
        :param table:
        :return:
        """
        # create the file and open
        filename = table.topmainpackage + "/" + Constants.pckg_contr + "/" + table.camelcasejavaname + "Controller.java"
        resources_file = open(filename, "w")
        test_controller = open("files/controller.txt")
        resources_file.write("package " + table.rootpackage + "." + Constants.pckg_contr + ";\n\n")
        for line in test_controller:
            linestr = str(line)
            if (linestr.find("XXX")) > -1:
                resources_file.write(
                    "import " + table.rootpackage + "." + Constants.pckg_pojos + "." + table.camelcasejavaname + ";\n")
                resources_file.write(
                    "import " + table.rootpackage + "." + Constants.pckg_dtos + "." + table.dtoname + ";\n")
                resources_file.write(
                    "import " + table.rootpackage + "." + Constants.pckg_services + "." + table.camelcasejavaname + "Repository;\n")
                resources_file.write("import " + table.rootpackage + "." + Constants.pckg_exc + "." + "ResourceNotFoundException;\n")
            elif linestr.find("QQQ") > -1:
                text = self.create_get_pk_stmt(table)
                resources_file.write(linestr.replace("%", table.camelcasejavaname).replace("&", table.lowercasename).replace("QQQ",text))
            else:
                resources_file.write(linestr.replace("%", table.camelcasejavaname).replace("&", table.lowercasename).replace("^",Configuration.author))
        resources_file.close()
        test_controller.close()

    def create_get_pk_stmt(self,table):
        """
        finds the primary key and adds it into the script
        :param table:
        :param file:
        :return:
        """
        tabs = "\t"
        text = "get"
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            if fielddata.isprimary == True:
                text += fielddata.gettername+"()"
        return text

    def create_package_stmt(self,table, file, src):
        """
        create the package statement
        :param table:
        :param file:
        :return:
        """
        if src == "pojo":
            file.write("package " + table.rootpackage + "." + Constants.pckg_pojos + ";\n\n")
        else:
                    file.write("package " + table.rootpackage + "." + Constants.pckg_dtos + ";\n\n")

    def create_imports(self, table, file, src):
        """
        create the imports
        :param table:
        :param file:
        :return:
        """
        if src == "pojo":
            file.write("import " + table.rootpackage + "." + Constants.pckg_dtos + "." + table.dtoname + ";\n")
            file.write("import javax.persistence.*;\n")
        else:
            file.write("import " + table.rootpackage + "." + Constants.pckg_pojos + "." + table.camelcasejavaname + ";\n")
            file.write("import javax.validation.constraints.*;\n")
        file.write("import com.google.gson.Gson;\n")
        bigdatafield = False
        bigintfield = False
        datefield = False
        tsfield = False
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            if(fielddata.datatype == "BigDecimal" and bigdatafield == False):
                file.write(Constants.import_bd+"\n")
                bigdatafield = True
            elif(fielddata.datatype == "BigInteger" and bigintfield == False):
                file.write(Constants.import_bi+"\n")
                bigintfield = True
            elif (fielddata.datatype == "Date" and datefield == False):
                file.write(Constants.import_date + "\n")
                datefield = True
            elif (fielddata.datatype == "Timestamp" and tsfield == False):
                file.write(Constants.import_ts + "\n")
                tsfield = True
        file.write("\n")

    def create_class_decl(self, table, file, src):
        """
        create the POJO class declaration
        :param table:
        :param file:
        :return:
        """
        file.write(Constants.doc_main_class.replace("^",Configuration.author)+"\n")
        if src == "pojo":
            file.write(Constants.ann_entity+"\n")
            file.write(Constants.ann_table.replace("*",table.tablename)+"\n")
            file.write("public class " + table.camelcasejavaname + " {\n\n")
        else:
            file.write("public class " + table.dtoname + " {\n\n")

    def create_the_fields(self, table, file, src):
        """
        create the POJO fields
        :param table:
        :param file:
        :return:
        """
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            # create the javadoc comment
            self.create_field_javadoc(fielddata, file)
            # create the annotations
            self.create_field_ann(fielddata, file, src)
            # create the field
            self.create_field(fielddata, file)

    def create_field_javadoc(self, fielddata, file):
        """
        create the field's javadoc
        :param fielddata:
        :param file:
        :return:
        """
        tabs = "\t"
        text = tabs + Constants.doc_opn + "\n" + tabs + Constants.doc_str + " ^\n" + tabs + Constants.doc_cls + "\n"
        if(len(fielddata.comment)>0):
            text = text.replace("^",fielddata.comment)
        else:
            text = text.replace("^","")
        file.write(text)

    def create_field_ann(self, fielddata, file, src):
        """
        create the field annotations
        :param fielddata:
        :param file:
        :return:
        """
        tabs = "\t"
        if src == "pojo":
            # these are the JPA annotations
            file.write(tabs+Constants.ann_column.replace("*",fielddata.name)+"\n")
            if(fielddata.isprimary == True):
                file.write(tabs+Constants.ann_id+"\n")
            if (fielddata.primarytype != None):
                file.write(tabs+Constants.ann_autogen + "\n")
        else:
            # these are the possible DTO validation annotations
            if(fielddata.canbenull == False):
                file.write(tabs+Constants.ann_notnull.replace("*", fielddata.name)+"\n")
            if (fielddata.lengthreq == True):
                file.write(tabs+Constants.ann_sizemax.replace("*", str(fielddata.length),1).replace("*",fielddata.name,1).replace("*",str(fielddata.length),1)+"\n")

    def create_field(self, fielddata, file):
        """
        create the field declaration
        :param fielddata:
        :param file:
        :return:
        """
        tabs = "\t"
        file.write(tabs + "private " + fielddata.datatype + " " + fielddata.javaname + ";\n\n")

    def create_def_constr(self, table, file, src):
        """
        create the default constructor
        :param table:
        :param file:
        :return:
        """
        tabs = "\t"
        if src == "pojo":
            file.write(tabs + "public " + table.camelcasejavaname + "() {\n" + tabs + tabs + "super();\n" + tabs + "}\n\n")
        else:
            file.write(
                tabs + "public " + table.dtoname + "() {\n" + tabs + tabs + "super();\n" + tabs + "}\n\n")

    def create_field_constr(self, table, file, src):
        """
        create the field constructor
        :param table:
        :param file:
        :return:
        """
        tabs = "\t"
        if src == "pojo":
            text = tabs+"public "+table.camelcasejavaname+"("
        else:
            text = tabs + "public " + table.dtoname + "("
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            text += fielddata.datatype + " " + fielddata.javaname + ", "
        text = text[0:-2]
        text += ") {\n"
        file.write(text)
        file.write(tabs+tabs+Constants.str_super+"\n")
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            file.write(tabs+tabs+"this."+fielddata.javaname+" = "+fielddata.javaname+";\n")
        file.write(tabs+"}\n\n")

    def create_get_n_set(self, table, file):
        """
        create the getters and setters
        :param table:
        :param file:
        :return:
        """
        tabs = "\t"
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            file.write(tabs + "public " + fielddata.datatype + " get" + fielddata.gettername + "() {\n" + tabs + tabs + "return " + fielddata.javaname + ";\n" + tabs + "}\n\n")
            file.write(tabs + "public void set" + fielddata.gettername + "(" + fielddata.datatype + " " + fielddata.javaname + ") {\n" + tabs + tabs + "this." + fielddata.javaname + "=" + fielddata.javaname + ";\n" + tabs + "}\n\n")

    def create_tostring(self, table, file, src):
        """
        create the toString method
        :param table:
        :param file:
        :return:
        """
        tabs = "\t"
        file.write(tabs + Constants.ann_override + "\n" + tabs + Constants.str_tostring + "{\n")
        if src == "pojo":
            text = 'return "' + table.camelcasejavaname + ' ['
        else:
            text = 'return "' + table.dtoname + ' ['
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            text += fielddata.javaname + '=" + ' + fielddata.javaname + ' + ", '
        text = text[0:-3] + '"]";'
        file.write(tabs+tabs+text+"\n"+tabs+"}\n\n")

    def create_gson_conv(self, table, file, src):
        """
        create the static gson json->object converter
        :param table:
        :param file:
        :param src:
        :return:
        """
        tabs = "\t"
        name = ""
        if src == "pojo":
            name = table.camelcasejavaname
        else:
            name = table.dtoname
        file.write(tabs + "public static " + name + " fromJson(String input) {\n")
        file.write(tabs + tabs + "Gson gson = new Gson();\n")
        file.write(tabs + tabs +"return gson.fromJson(input, " + name + ".class );\n")
        file.write(tabs + "}\n")

    def create_dto_pojo_conv(self, table, file, src):
        """

        :param table:
        :param file:
        :param src:
        :return:
        """
        tabs = "\t"
        text = ''
        if src == "pojo":
            file.write(tabs + "public " + table.dtoname + " toDTO() {\n")
            file.write(tabs + tabs + "return new " + table.dtoname + "(")
        else:
            file.write(tabs + "public " + table.camelcasejavaname + " toEntity() {\n")
            file.write(tabs + tabs + "return new " + table.camelcasejavaname + "(")
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            text += "this.get" + fielddata.gettername + "(),"
        text = text[0:-1] + ");\n"
        file.write(text)
        file.write(tabs + "}\n")
