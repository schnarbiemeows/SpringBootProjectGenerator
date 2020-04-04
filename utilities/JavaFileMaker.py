from popos.Table import *
from utilities.Utilities import *
from utilities.Constants import *
from configuration.Configuration import *
import os
import sys
import xml.etree.ElementTree as ET
import shutil

class JavaFileMaker:


    """
        this method creates the main Application class for the project
    """
    def create_main_method_class(self, table):
        filename = table.topmainpackage + "/" + table.camelcasejavaname + "Application.java"
        main_file = open("files/main.txt", "r")
        resources_file = open(filename, "w")
        resources_file.write("package " + table.rootpackage + ";\n\n")
        for line in main_file:
            linestr = str(line)
            if (linestr.find("^") > -1):
                resources_file.write(linestr.replace("^", Configuration.author))
            elif (linestr.find("%") > -1):
                resources_file.write(linestr.replace("%", table.camelcasejavaname))
            else:
                resources_file.write(linestr)
        resources_file.close()
        main_file.close()


    """
        this method will make the base Exception class
    """
    def make_base_exc_class(self, table):
        filename = table.topmainpackage + "/exceptions/ExceptionResponse.java"
        exception_file = open("files/exception.txt", "r")
        resources_file = open(filename, "w")
        resources_file.write("package " + table.rootpackage + ".exceptions;\n\n")
        for line in exception_file:
            linestr = str(line)
            if (linestr.find("^") > -1):
                resources_file.write(linestr.replace("^", Configuration.author))
            else:
                resources_file.write(linestr)
        resources_file.close()
        exception_file.close()

    """
        this method will make a POJO from a Table object
    """
    def create_pojo_class(self, table):
        # create the file and open
        filename = table.topmainpackage + "/" + Constants.pckg_pojos + "/" + table.camelcasejavaname + ".java"
        resources_file = open(filename, "w")
        # create the package statement
        self.create_package_stmt(table,resources_file)
        # create the imports
        self.create_imports(table,resources_file)
        # create the main class declaration with javadoc
        self.create_class_decl(table,resources_file)
        # create the fields
        self.create_the_fields(table,resources_file)
        # create the default constructor
        self.create_def_constr(table,resources_file)
        # create the fields constructor
        self.create_field_constr(table,resources_file)
        # create the getters and setters
        self.create_get_n_set(table,resources_file)
        # create the toString
        self.create_tostring(table,resources_file)
        # finish the class with a trailing }
        resources_file.write("}\n")
        resources_file.close()


    """
        create the package statement
    """
    def create_package_stmt(self,table, file):
        file.write("package " + table.rootpackage + "." + Constants.pckg_pojos + ";\n\n")

    """
        create the imports
    """
    def create_imports(self, table, file):
        file.write("import javax.persistence.*;\n")
        file.write("import javax.validation.constraints.*;\n")
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

    """
        create the class declaration
    """
    def create_class_decl(self, table, file):
        file.write(Constants.doc_main_class.replace("^",Configuration.author)+"\n")
        file.write(Constants.ann_entity+"\n")
        file.write(Constants.ann_table.replace("*",table.tablename)+"\n")
        file.write("public class " + table.camelcasejavaname + " {\n\n")

    """
        create the field
    """
    def create_the_fields(self, table, file):
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            # create the javadoc comment
            self.create_field_javadoc(fielddata, file)
            # create the annotations
            self.create_field_ann(fielddata, file)
            # create the field
            self.create_field(fielddata, file)

    """
        create the field's javadoc
    """
    def create_field_javadoc(self, fielddata, file):
        tabs = "\t"
        text = tabs + Constants.doc_opn + "\n" + tabs + Constants.doc_str + " ^\n" + tabs + Constants.doc_cls + "\n"
        if(len(fielddata.comment)>0):
            text = text.replace("^",fielddata.comment)
        else:
            text = text.replace("^","")
        file.write(text)

    """
        create the field annotations
    """
    def create_field_ann(self, fielddata, file):
        tabs = "\t"
        file.write(tabs+Constants.ann_column.replace("*",fielddata.name)+"\n")
        if(fielddata.isprimary == True):
            file.write(tabs+Constants.ann_id+"\n")
        if (fielddata.primarytype != None):
            file.write(tabs+Constants.ann_autogen + "\n")
        if(fielddata.canbenull == False):
            file.write(tabs+Constants.ann_notnull.replace("*", fielddata.name)+"\n")
        if (fielddata.lengthreq == True):
            file.write(tabs+Constants.ann_sizemax.replace("*", str(fielddata.length),1).replace("*",fielddata.name,1).replace("*",str(fielddata.length),1)+"\n")

    """
        create the field declaration
    """
    def create_field(self, fielddata, file):
        tabs = "\t"
        file.write(tabs + "private " + fielddata.datatype + " " + fielddata.javaname + ";\n\n")

    """
        create the default constructor
    """
    def create_def_constr(self, table, file):
        tabs = "\t"
        file.write(tabs + "public " + table.camelcasejavaname + "() {\n" + tabs + tabs + "super();\n" + tabs + "}\n\n")

    """
        create the field constructor
    """
    def create_field_constr(self, table, file):
        tabs = "\t"
        text = tabs+"public "+table.camelcasejavaname+"("
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

    """
        create the getters and setters
    """
    def create_get_n_set(self, table, file):
        tabs = "\t"
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            file.write(tabs + "public " + fielddata.datatype + " get" + fielddata.gettername + "() {\n" + tabs + tabs + "return " + fielddata.javaname + ";\n" + tabs + "}\n\n")
            file.write(tabs + "public void set" + fielddata.gettername + "(" + fielddata.datatype + " " + fielddata.javaname + ") {\n" + tabs + tabs + "this." + fielddata.javaname + "=" + fielddata.javaname + ";\n" + tabs + "}\n\n")

    """
        create the toString method
    """
    def create_tostring(self, table, file):
        tabs = "\t"
        file.write(tabs + Constants.ann_override + "\n" + tabs + Constants.str_tostring + "{\n")
        text = 'return "' + table.camelcasejavaname + ' ['
        # FOR EACH FIELD:
        for field in table.fieldnames:
            fielddata = table.fielddata[field]
            text += fielddata.javaname + '=" + ' + fielddata.javaname + ' + ", '
        text = text[0:-3] + '"]";'
        file.write(tabs+tabs+text+"\n"+tabs+"}\n")

    """
        this method will create the Repositry class file
    """
    def create_repository_class(self, table):
        filename = table.topmainpackage + "/" + Constants.pckg_repo + "/" + table.camelcasejavaname + "Repository.java"
        resources_file = open(filename, "w")
        resources_file.write("package " + table.rootpackage + "." + Constants.pckg_repo + ";\n\n")
        resources_file.write(Constants.import_repo + "\n")
        resources_file.write(Constants.import_pojo.replace("%",table.rootpackage+".pojos."+table.camelcasejavaname)+"\n")
        resources_file.write(Constants.doc_main_class.replace("^", Configuration.author) + "\n")
        resources_file.write(Constants.class_decl_repo.replace("*",table.camelcasejavaname) + "\n")
        resources_file.close()

    """
        this method will create the Controller class
    """
    def create_controller_class(self, table):
        tabs = ""

    """
        this method will make the swagger2 config file
    """
    def create_swagger_class(self,table):
        filename = table.topmainpackage + "/" + "SwaggerConfig.java"
        resources_file = open(filename, "w")
        swagger_file = open("files/swagger_text.txt","r")
        resources_file.write("package " + table.rootpackage + ";\n\n")
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

    """
        this method will create the RestController for the project
        the rest controller will have methods to 
        - get all objects(GET)
        - get an object by ID(only if they have a primary key or a unique key(GET)
        - create an object(POST)
        - update an object(POST)
        - delete an object(DELETE)
    """
    def create_controller_class(self,table):
        # create the file and open
        filename = table.topmainpackage + "/" + Constants.pckg_contr + "/" + table.camelcasejavaname + "Controller.java"
        resources_file = open(filename, "w")
        # create the package statement
        self.cc_package_stmt(table, resources_file)
        # create the imports
        self.cc_imports(table, resources_file)
        # create the main class declaration with javadoc
        self.cc_class_decl(table, resources_file)
        # create the repository reference
        self.cc_repo_ref(table, resources_file)
        # create the GET ALL service
        self.cc_getall_obj(table, resources_file)
        # create the GET by PK or UK method
        if table.hasprimary == True:
            self.cc_getby_pk(table, resources_file)
        # create the POST create object
        self.cc_create_obj(table, resources_file)
        # create the POST update object
        self.cc_update_obj(table, resources_file)
        # create the DELETE object
        self.cc_del_obj(table, resources_file)
        # finish the class with a trailing }
        resources_file.write("}\n")
        resources_file.close()


    """
        create the package statement
    """
    def cc_package_stmt(self, table, file):
        file.write("package " + table.rootpackage + "." + Constants.pckg_contr + ";\n\n")

    """  
        create the imports
    """
    def cc_imports(self, table, file):
        file.write(Constants.import_ctrl_anns+"\n")
        file.write(Constants.import_autowired+"\n")
        file.write(Constants.import_respentity+"\n")
        file.write(Constants.import_https_status+"\n")
        file.write(Constants.import_valid+"\n")
        file.write(Constants.import_utils + "\n\n")
        # need to import the actual POJO class
        file.write("import " + table.rootpackage + "." + Constants.pckg_pojos + "." + table.camelcasejavaname + ".java;\n")
        # need to import the repository class
        file.write("import " + table.rootpackage + "." + Constants.pckg_repo + "." + table.camelcasejavaname + "Repository.java;\n\n")

    """  
        create the main class declaration with javadoc
    """
    def cc_class_decl(self, table, file):
        file.write(Constants.doc_main_class.replace("^", Configuration.author) + "\n")
        file.write(Constants.ann_restctrlr + "\n")
        file.write(Constants.ann_root_mapping.replace("*",table.pomname)+"\n")
        file.write("public class " + table.camelcasejavaname + "Controller {\n\n")

    """  
        create the repository reference
    """
    def cc_repo_ref(self, table, file):
        tabs = "\t"
        text = tabs + Constants.doc_opn + "\n" + tabs + Constants.doc_str + " JPA Repositry handle\n" + tabs + Constants.doc_cls + "\n"
        file.write(text)
        file.write(tabs+Constants.ann_autowired+"\n")
        file.write(tabs +"private " + table.camelcasejavaname + "Repositry service;\n\n")

    """  
        create the GET ALL service
    """
    def cc_getall_obj(self, table, file):
        tabs = "\t"
        file.write(tabs+Constants.doc_get_all.replace("^",table.camelcasejavaname))
        file.write(tabs + Constants.ann_getmapping.replace("*","all") + "\n")
        file.write(tabs + "public ResponseEntity<Object> getAll*() {".replace("*",table.camelcasejavaname)+"\n")
        file.write(tabs+tabs + "try {\n")
        file.write(tabs+tabs+tabs+"Iterable<*> ^ = service.findAll();\n".replace("*",table.camelcasejavaname).replace("^",table.lowercasename))
        file.write(tabs+tabs+tabs+"return ResponseEntity.status(HttpStatus.OK).body(*);\n".replace("*",table.lowercasename))
        file.write(tabs+tabs+"} catch (Exception e) {\n"+tabs+tabs+tabs+"throw e;\n"+tabs+tabs+"}\n")
        file.write(tabs+"}\n\n")

    """  
        create the GET by PK or UK method
    """
    def cc_getby_pk(self, table, file):
        tabs = "\t"
        file.write(tabs + Constants.doc_get_pk.replace("^",table.camelcasejavaname))
        file.write(tabs + Constants.ann_getsinglemapping + "\n")
        file.write(tabs + "public ResponseEntity<Object> find*ById(@PathVariable int id) {".replace("*", table.camelcasejavaname) + "\n")
        file.write(tabs + tabs + "try {\n"+tabs+tabs+tabs+"Integer primaryKey = new Integer(id);\n")
        file.write(tabs+tabs+tabs+"Optional<*> ^Optional = service.findById(primaryKey);\n".replace("*",table.camelcasejavaname).replace("^",table.lowercasename))
        file.write(tabs+tabs+tabs+"* results = ^Optional.get();\n".replace("*",table.camelcasejavaname).replace("^",table.lowercasename))
        file.write(tabs + tabs + tabs + "return ResponseEntity.status(HttpStatus.OK).body(results);\n")
        file.write(tabs + tabs + "} catch (Exception e) {\n" + tabs + tabs + tabs + "throw e;\n" + tabs + tabs + "}\n")
        file.write(tabs + "}\n\n")

    """  
        create the POST create object
    """
    def cc_create_obj(self, table, file):
        tabs = "\t"
        file.write(tabs + Constants.doc_create.replace("^", table.camelcasejavaname))
        file.write(tabs + Constants.ann_postmapping.replace("*","create") + "\n")
        file.write(tabs + "public ResponseEntity<Object> create^(@RequestBody ^ data) {\n".replace("^", table.camelcasejavaname))
        file.write(tabs + tabs + "try {\n" + tabs + tabs + tabs + "data = service.save(data);\n")
        file.write(tabs + tabs + tabs + "return ResponseEntity.status(HttpStatus.OK).body(data);\n")
        file.write(tabs + tabs + "} catch (Exception e) {\n" + tabs + tabs + tabs + "throw e;\n" + tabs + tabs + "}\n")
        file.write(tabs + "}\n\n")

    """  
        create the POST update object
    """
    def cc_update_obj(self, table, file):
        tabs = "\t"
        file.write(tabs + Constants.doc_update.replace("^", table.camelcasejavaname))
        file.write(tabs + Constants.ann_postmapping.replace("*", "update") + "\n")
        file.write(tabs + "public ResponseEntity<Object> update^(@RequestBody ^ data) {\n".replace("^",table.camelcasejavaname))
        file.write(tabs + tabs + "try {\n" + tabs + tabs + tabs + "data = service.save(data);\n")
        file.write(tabs + tabs + tabs + "return ResponseEntity.status(HttpStatus.OK).body(data);\n")
        file.write(tabs + tabs + "} catch (Exception e) {\n" + tabs + tabs + tabs + "throw e;\n" + tabs + tabs + "}\n")
        file.write(tabs + "}\n\n")

    """  
        create the DELETE object
    """
    def cc_del_obj(self, table, file):
        tabs = "\t"
        file.write(tabs + Constants.doc_delete.replace("^", table.camelcasejavaname))
        file.write(tabs + Constants.ann_delmapping.replace("*", "delete") + "\n")
        file.write(tabs + "public ResponseEntity<Object> delete*(@PathVariable int id) {".replace("*",table.camelcasejavaname) + "\n")
        file.write(tabs + tabs + "try {\n" + tabs + tabs + tabs + "Integer primaryKey = new Integer(id);\n")
        file.write(tabs + tabs + tabs + "data = service.deleteById(primaryKey);\n")
        file.write(tabs + tabs + tabs + "return ResponseEntity.status(HttpStatus.OK).body(data);\n")
        file.write(tabs + tabs + "} catch (Exception e) {\n" + tabs + tabs + tabs + "throw e;\n" + tabs + tabs + "}\n")
        file.write(tabs + "}\n\n")