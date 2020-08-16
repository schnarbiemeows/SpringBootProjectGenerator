from configuration.Constants import *
from configuration.Configuration import *
from utilities.Utilities import *

class RestControllerGenerator:

    def __init__(self):
        None

    @staticmethod
    def create_controller_class(table):
        """
        this method will create the RestController for the project
        the rest controller will have methods to
        - get all objects(GET)
        - get an object by ID(only if they have a primary key or a unique key(GET)
        - create an object(POST)
        - update an object(POST)
        - delete an object(DELETE)
        - in addition, if there are any foreign keys in the table, there will be calls
            to find by each foreign key, as well as find by all foreign keys
        :param table:
        :return:
        """
        # create the file and open
        filename = table.topmainpackage + "/" + Constants.pckg_contr + "/" + table.camelcasejavaname + "Controller.java"
        resources_file = open(filename, "w")
        controller_file = open("files/controller/controller.txt")
        resources_file.write("package " + table.rootpackage + "." + Constants.pckg_contr + ";\n\n")
        for line in controller_file:
            linestr = str(line)
            if linestr.find("FKSECTION")>-1:
                if len(table.fksymbolnames)>0:
                    RestControllerGenerator.createForeignKeyCalls(table,resources_file)
            else:
                resources_file.write(linestr.replace("$", table.rootpackage).replace("%", table.camelcasejavaname).replace("&", table.lowercasename).replace("^",Configuration.author))
        resources_file.close()
        controller_file.close()

    @staticmethod
    def createForeignKeyCalls(table, resources_file):
        """
        this method will create one findBy foreign key call for each foreign key that a table has, and,
        in the event that the table has more than one, will create a findByAllForeignKeys for search
        by all of them at once
        :param table:
        :param resources_file:
        :return:
        """
        tabs = Constants.tab
        compoundFK = []
        datatypes = []
        inputparameters = []
        counter = 0
        for symbolname in table.fksymbolnames:
            fklist = table.fksymboldata[symbolname]
            for item in fklist:
                field = table.fielddata[item[0]]
                compoundFK.append(field.gettername)
                datatypes.append("@PathVariable " + Utilities.translateDataType(field.datatype) + " id" + str(counter))
                inputparameters.append("id" + str(counter))
                resources_file.write(tabs + Constants.doc_get_fk.replace("z",field.javaname)
                                     .replace("^",table.camelcasejavaname))
                resources_file.write(tabs + Constants.ann_getfkmapping.replace("^",field.gettername) + "\n")
                resources_file.write(tabs + "public ResponseEntity<Object> findBy" + field.gettername +
                    "(@PathVariable " + Utilities.translateDataType(field.datatype) + " id) throws Exception {\n")
                resources_file.write(tabs*2 + "List<" + table.camelcasejavaname + "DTO> results = businessService.findBy" +
                    field.gettername + "(id);\n")
                resources_file.write(tabs * 2 + "return ResponseEntity.status(HttpStatus.OK).body(results);\n" +
                    tabs + "}\n\n")
                counter +=1
        if len(compoundFK)>1:
            compoundFKstr = "And".join(compoundFK)
            resources_file.write(tabs + Constants.doc_get_fk.replace("z", compoundFKstr)
                                 .replace("^", table.camelcasejavaname))
            resources_file.write(tabs + Constants.ann_get_mult_fk_maps.replace("^", compoundFKstr).replace("X", "{" + "}/{".join(inputparameters) + "}") + "\n")
            text = tabs + "public ResponseEntity<Object> findBy" + compoundFKstr +"("
            text += ",".join(datatypes)
            text += ") throws Exception {\n"
            resources_file.write(text)
            resources_file.write(
                tabs * 2 + "List<" + table.camelcasejavaname + "DTO> results = businessService.findBy" +
                compoundFKstr + "(" + ", ".join(inputparameters) + ");\n")
            resources_file.write(tabs * 2 + "return ResponseEntity.status(HttpStatus.OK).body(results);\n" +
                                 tabs + "}\n\n")

    @staticmethod
    def create_controller_class_for_mid_lvl(mid_lvl_proj, crud_proj_names, crud_proj_data):
        """
        this method will create the RestController for the mid-lvl projects
        :param mid_lvl_proj:
        :return:
        """
        # create the file and open
        filename = mid_lvl_proj.topmainpackage + "/" + Constants.pckg_contr + "/" + mid_lvl_proj.camelcasejavaname + "Controller.java"
        resources_file = open(filename, "w")
        test_controller = open("files/controller/controller_mid_lvl.txt")
        resources_file.write("package " + mid_lvl_proj.rootpackage + "." + Constants.pckg_contr + ";\n\n")
        for line in test_controller:
            linestr = str(line)
            if(linestr.find("XXX")>-1):
                RestControllerGenerator.create_controller_business_calls_for_mid_level(mid_lvl_proj,
                                            crud_proj_names, crud_proj_data,resources_file)
            else:
                resources_file.write(linestr.replace("$",mid_lvl_proj.rootpackage).replace("%", mid_lvl_proj.camelcasejavaname).replace("&", mid_lvl_proj.lowercasename).replace("^", Configuration.author))
        resources_file.close()
        test_controller.close()

    @staticmethod
    def create_controller_business_calls_for_mid_level(mid_lvl_proj, crud_proj_names, crud_proj_data, resources_file):
        """

        :param mid_lvl_proj:
        :param crud_proj_names:
        :param crud_proj_data:
        :param resources_file:
        :return:
        """
        tabs = Constants.tab
        mid_lvl_map = {}
        for project_name in mid_lvl_proj.tablenames:
            mid_lvl_map[project_name] = "YES"
        for projectname in crud_proj_names:
            currentproject = crud_proj_data[projectname]
            if currentproject.pomname in mid_lvl_map:
                for tablename in currentproject.tablenames:
                    tabledata = currentproject.tabledata[tablename]
                    tablefile = open(currentproject.topmainpackage + "/" + Constants.pckg_contr + "/" + tabledata.camelcasejavaname + "Controller.java","r")
                    requestmappingfound = False
                    linecount = 0
                    is_create = False
                    for line in tablefile:
                        linestr = str(line)
                        if requestmappingfound == True:
                            if linecount > 0:
                                if is_create == True:
                                    if(linecount == 8):
                                        resources_file.write(linestr)
                                    elif(linecount == 7):
                                        resources_file.write(tabs*2+"try{\n")
                                    elif (linecount == 6):
                                        newlinestr = tabs*3 + "Object result = " + linestr[linestr.find(
                                            "businessService"):linestr.find(";")] + ".getBody();\n"
                                        resources_file.write(newlinestr)
                                    elif (linecount == 5):
                                        if(is_create):
                                            resources_file.write(
                                                tabs*3 + "return ResponseEntity.status(HttpStatus.CREATED).body(result);\n")
                                        else:
                                            resources_file.write(
                                            tabs*3 + "return ResponseEntity.status(HttpStatus.OK).body(result);\n")
                                    elif (linecount == 4):
                                        resources_file.write(linestr)
                                    elif (linecount == 3):
                                        resources_file.write(linestr)
                                    elif (linecount == 2):
                                        resources_file.write(linestr)
                                    elif (linecount == 1):
                                        resources_file.write(linestr+"\n")
                                        is_create = False
                                    linecount -= 1
                                else:
                                    if(linecount == 4):
                                        resources_file.write(linestr)
                                    elif(linecount == 3):
                                        newlinestr = tabs*2+"Object result = " + linestr[linestr.find("businessService"):linestr.find(";")] + ".getBody();\n"
                                        resources_file.write(newlinestr)
                                    elif(linecount == 2):
                                        resources_file.write(tabs*2+"return ResponseEntity.status(HttpStatus.OK).body(result);\n")
                                    else:
                                        resources_file.write(tabs+"}\n\n")
                                    linecount -= 1
                            elif linestr.find('Mapping(') > -1:
                                is_create = False
                                if(linestr.find("/create")>-1):
                                    is_create = True
                                linecount = 4
                                if is_create == True:
                                    linecount = 8
                                relativepath = "/"+tabledata.lowercasename+"/"
                                resources_file.write(Constants.doc_proxy)
                                resources_file.write(linestr.replace("/",relativepath,1))
                        elif linestr.find('Mapping(') > -1:
                            requestmappingfound = True
                    tablefile.close()
            else:
                print("curd table not in mid-level map!")