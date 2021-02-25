import glob
from popos.AngularObject import *
from utilities.FileMaker import *
"""
    this class will create the angular 10 project for a given project
"""
class AngularFileMaker:

    def __init__(self):
        None

    @staticmethod
    def make_angular_projects(projectnames, projectdata):
        """
        this method will create the angular 10 code for a given project
        :param projectnames:
        :param projectdata:
        :return:
        """
        # for each project:
        AngularFileMaker.parse_controller_classes(projectnames, projectdata)
        for projectname in projectnames:
            project = projectdata[projectname]
            # make the base file structure of the project
            root_directory = FileMaker.make_base_angular_project(project)
            AngularFileMaker.make_folders(root_directory)
            # make an AngularObject - each project has its own AngularObject
            angular_object = AngularObject()
            # make angular module classes from the DTOs
            AngularFileMaker.make_angular_classes(project, root_directory)
            # parse the controller class to get some important information that we will need in order to make both the service file
            # and the component ts file
            AngularFileMaker.make_angular_classes_for_foreign_keys(projectnames, projectdata, project, root_directory)
            # make the services
            AngularFileMaker.make_services(project, angular_object, root_directory)
            AngularFileMaker.make_services_for_foreign_keys(projectnames, projectdata, project, angular_object, root_directory)
            # make the components
            AngularFileMaker.make_components(projectnames, projectdata, project, root_directory)
            # make the navigation bar
            AngularFileMaker.make_navigation_bar(project, root_directory)
            # make the app-routing.module.ts file
            AngularFileMaker.make_app_routing_module(project, root_directory)
            # make the app.module.ts file
            AngularFileMaker.make_app_modules_ts_file(project, angular_object, root_directory)
            # make the config files
            AngularFileMaker.make_angularjson_file(project, root_directory)
            AngularFileMaker.make_packagejson_file(root_directory)
            # make the index.html files
            AngularFileMaker.make_app_component_file(root_directory)
            AngularFileMaker.make_index_html_file(project, root_directory)
            AngularFileMaker.make_style_css_file(root_directory)

    @staticmethod
    def translateDataType(input):
        """
        this is needed to translate between the java data type
        and the angular/typescript data type
        :param input:
        :return:
        """
        fieldtype = "string"
        if (input.lower() == "int" or input.lower() == "integer"
                or input.lower() == "long" or input.lower() == "float"
                or input.lower() == "double" or input.lower() == "biginteger"
                or input.lower() == "bigdecimal"):
            fieldtype = "number"
        elif (input.lower() == "date" or input.lower() == "datetime"
              or input.lower() == "timestamp" or input.lower() == "time"):
            fieldtype = "Date"
        elif (input.lower() == "boolean"):
            fieldtype = "boolean"
        if input.lower().find("[]") > -1:
            fieldtype += "[]"
        return fieldtype

    @staticmethod
    def make_angular_classes(project, root_directory):
        """
        this method will make the DTO objects for a given project in Angular
        :param project:
        :param root_directory:
        :return:
        """
        AngularFileMaker.make_dropdown_options_dto(root_directory)
        tabs = Constants.tab
        filename = ''
        for tablename in project.tablenames:
            tabledata = project.tabledata[tablename]
            dtoname = tabledata.dtoname
            if (project.is_mid_level == True):
                filename = project.topmainpackage + "/" + Constants.path_proxy_dtos + "/" + dtoname + ".java"
            else:
                filename = project.topmainpackage + "/" + Constants.pckg_dtos + "/" + dtoname + ".java"
            inputfile = open(filename, "r")
            outputfile = open(root_directory + "/src/app/models/" + dtoname + ".ts", "w")
            outputfile.write("export interface " + dtoname + "{\n")
            inputfile.close()
            print("making the Angular DTO for : " + dtoname)
            inputfile = open(filename, "r")
            for line in inputfile:
                linestr = str(line)
                if linestr.find(Constants.private) > -1 and linestr.find(Constants.serial_uid) == -1 and linestr.find(Constants.logger) == -1:
                    fieldarray = linestr.split(" ")
                    key = fieldarray[2].replace(";", "").rstrip()
                    print("DTO field name " + key)
                    fieldtype = AngularFileMaker.translateDataType(fieldarray[1])
                    outputfile.write(tabs + key + "?: " + fieldtype + ";\n")
            outputfile.write("}")
            inputfile.close()
            outputfile.close()
        inputfile = open("files/angular/response_message.ts", "r")
        outputfile = open(root_directory + "/src/app/models/ResponseMessage.ts", "w")
        for line in inputfile:
            linestr = str(line)
            outputfile.write(linestr)
        inputfile.close()
        outputfile.close()

    @staticmethod
    def make_angular_classes_for_foreign_keys(projectnames, projectdata, project, root_directory):
        """
        this method will make the DTO objects for a given project in Angular
        :param projectnames:
        :param projectdata:
        :param project:
        :param root_directory:
        :return:
        """
        # multiple for loops - BAD CODE, FIX LATER
        tabs = Constants.tab
        filename = ''
        for tablename in project.tablenames:
            tabledata = project.tabledata[tablename]
            for fksymbolname in tabledata.fksymbolnames:
                fksymboldata = tabledata.fksymboldata[fksymbolname]
                parenttablename = str(fksymboldata[0][1])
                # for each project:
                for projectname in projectnames:
                    project = projectdata[projectname]
                    if parenttablename in project.tabledata.keys():
                        parenttable = project.tabledata[parenttablename]
                        dtoname = parenttable.dtoname
                        if (project.is_mid_level == True):
                            filename = project.topmainpackage + "/" + Constants.path_proxy_dtos + "/" + dtoname + ".java"
                        else:
                            filename = project.topmainpackage + "/" + Constants.pckg_dtos + "/" + dtoname + ".java"
                        inputfile = open(filename, "r")
                        outputfile = open(root_directory + "/src/app/models/" + dtoname + ".ts", "w")
                        outputfile.write("export interface " + dtoname + "{\n")
                        for line in inputfile:
                            linestr = str(line)
                            if linestr.find("private") > -1 and linestr.find(Constants.serial_uid) == -1 and linestr.find(Constants.logger) == -1:
                                fieldarray = linestr.split(" ")
                                key = fieldarray[2].replace(";", "").rstrip()
                                print("field name " + key)
                                fieldtype = AngularFileMaker.translateDataType(fieldarray[1])
                                outputfile.write(tabs + key + "?: " + fieldtype + ";\n")
                        outputfile.write("}")
                        inputfile.close()
                        outputfile.close()

    @staticmethod
    def parse_controller_classes(projectnames, projectdata):
        """
        this method will create the urls in the service class for calling the backing controller
        it will also assemble a map of other information inside the AngularObject for that DTO, so
        that we can use this stuff later and not have to parse this controller file again
        :param projectnames:
        :param projectdata:
        :return:
        """
        for projectname in projectnames:
            project = projectdata[projectname]
            print("Analyzing the Controller class for project : " + project.pomname)
            tabs = Constants.tab
            requestmappingfound = False
            requestfound = False
            currentdto = ''
            root_url = ''
            new_root_url = ''
            if (Configuration.use_gateway_server == True):
                root_url = Configuration.gateway_server_url+"/"+project.pomname
                print("ROOT_URL = " + root_url)
            else:
                root_url = Configuration.hostname + ":" + str(project.portnum)
            for tablename in project.tablenames:
                tabledata = project.tabledata[tablename]
                dtoname = tabledata.dtoname
                print("Analyzing the Controller class for dtoname : " + dtoname)
                project.urls[dtoname] = []
                project.rest_call_names[dtoname] = []
                if(project.is_mid_level == True):
                    print("This project is mid-level")
                    controller_file = open(project.topmainpackage + "/" + Constants.pckg_contr + "/" + project.camelcasejavaname + "Controller.java","r")
                else:
                    print("This project is NOT mid-level")
                    controller_file = open(project.topmainpackage + "/" + Constants.pckg_contr + "/" + dtoname.replace("DTO","") + "Controller.java","r")
                for line in controller_file:
                    linestr = str(line)
                    if requestmappingfound == True:
                        if requestfound == True:
                            linestrtemp = linestr.replace(">>",">")
                            linestr = linestrtemp[linestr.find(">")+1:]
                            rest_call_name = linestr[0:linestr.find("(")].lstrip()
                            print("Which has a rest-call-name of : " + rest_call_name)
                            print("Which we are attempting to put into key = : " + currentdto)
                            project.rest_call_names[currentdto].append(rest_call_name)
                            requestfound = False
                        elif linestr.find('Mapping(') > -1:
                            if(linestr.find("health")==-1):
                                requestfound = True
                                url = linestr[linestr.find('"')+1:-3]
                                print("URL = " + url)
                                full_url = new_root_url+url
                                request_type = linestr[linestr.find('@') + 1:linestr.find('Mapping')].lower()
                                print("We found a Mapping of type: " + request_type)
                                print("Which has a URL of : " + full_url)
                                if(project.is_mid_level == True):
                                    wordtolookfor = "/"+dtoname.replace("DTO","").lower()+"/"
                                    if (linestr.find(wordtolookfor)>-1):
                                        currentdto = dtoname
                                        print("1 - which we are putting into " + dtoname)
                                        project.urls[dtoname].append(full_url)
                                    else:
                                        print("which does not qualify")
                                        requestfound = False
                                else:
                                    currentdto = dtoname
                                    print("2 - which we are putting into " + dtoname)
                                    project.urls[dtoname].append(full_url)
                            else:
                                print("skipping healthcheck")
                    elif linestr.find('@RequestMapping(') > -1:
                        print("We found the RequestMapping")
                        requestmappingfound = True
                        new_root_url = root_url + linestr[linestr.find('@RequestMapping(path="')+22:-3]
                        print("NEW root_url = " + new_root_url)
                controller_file.close()
                requestmappingfound = False

    @staticmethod
    def remove_annotations_from_string(inputstring):
        """
        this method is for the mid-level proxies, it will remove annotations from the method declarations
        :param inputstring:
        :return:
        """
        stringarray = inputstring[inputstring.find("(")+1:inputstring.find(")")]
        outputstring = ''
        remaining = stringarray.split(" ")
        for word in remaining:
            wordstr = str(word)
            if wordstr.find('@') == -1:
                outputstring += wordstr.replace(",","") + " "
        print("removed annotations results in : " + outputstring.rstrip())
        return outputstring.rstrip()

    @staticmethod
    def make_app_routing_module(project,root_directory):
        """
        this method will make the app-routing.module.ts file
        :param angular_object:
        :param root_directory:
        :return:
        """
        tabs = Constants.tab
        app_routing_input = None
        app_routing_output = None
        try:
            app_routing_input = open("files/angular/app-routing.module.ts", "r")
            app_routing_output = open(
                root_directory + "/src/app/app-routing.module.ts",
                "w")
            for line in app_routing_input:
                linestr = str(line)
                if (linestr.find("IMPORTS") > -1):
                    counter = 0
                    for item in project.components:
                        lowername = str(item)[0:-9].lower()
                        app_routing_output.write("import { " + item + " } from './components/" + lowername + "/" + lowername + ".component';\n")
                        counter += 1
                elif (linestr.find("ROUTES") > -1):
                    counter = 0
                    for item in project.components:
                        lowername = str(item)[0:-9].lower()
                        app_routing_output.write("{ path: '" + lowername + "', component: " + item + " }")
                        counter += 1
                        if(counter<len(project.components)):
                            app_routing_output.write(",")
                        app_routing_output.write("\n")
                else:
                    app_routing_output.write(linestr)
        except:
            print("something went wrong inside the AngularFileMaker.make_components method")
        finally:
            if (app_routing_input is not None):
                app_routing_input.close()
            if (app_routing_output is not None):
                app_routing_output.close()

    @staticmethod
    def make_components(projectnames,projectdata,project,root_directory):
        """
        this method will make all of the component files for a project
        :param projectnames:
        :param projectdata:
        :param project:
        :param root_directory:
        :return:
        """
        tabs = Constants.tab
        for tablename in project.tablenames:
            tabledata = project.tabledata[tablename]
            AngularFileMaker.make_fk_names(projectnames, projectdata, tabledata)
            dtoname = tabledata.dtoname
            javaname = dtoname.replace("DTO","")
            lowercasename = dtoname.replace("DTO","").lower()
            project.components.append(javaname + "Component")
            component_html_file = None
            output_html_file = None
            component_ts_file = None
            output_ts_file = None
            output_css_file = None
            try:

                # make the html file

                component_html_file = open("files/angular/component.html", "r")
                if not os.path.exists(root_directory + "/src/app/components/" + lowercasename):
                    os.mkdir(root_directory + "/src/app/components/" + lowercasename)
                output_html_file = open(
                    root_directory + "/src/app/components/" + lowercasename + "/" + lowercasename + ".component.html",
                    "w")
                for line in component_html_file:
                    linestr = str(line)
                    if (linestr.find("TABLE_NAME") > -1):
                        output_html_file.write(linestr.replace("TABLE_NAME", javaname))
                    elif (linestr.find("TABLE_HEADER") > -1):
                        AngularFileMaker.add_html_header(tabledata,output_html_file)
                    elif (linestr.find("TABLE_BODY") > -1):
                        AngularFileMaker.add_html_body(tabledata, output_html_file)
                    elif (linestr.find("PAGE_FORM") > -1):
                        AngularFileMaker.add_html_form_body(tabledata, output_html_file)
                    elif linestr.find("TEST_FK") >-1:
                        if len(tabledata.fksymbolnames) > 0:
                            AngularFileMaker.make_test_fk_html_section(tabledata, output_html_file)
                    elif (linestr.find("PARENT_FORM") > -1):
                        output_html_file.write(linestr.replace("PARENT_FORM", javaname))
                    else:
                        output_html_file.write(linestr.replace("%",lowercasename+"list"))

                # make the typescript file

                component_ts_file = open("files/angular/component.ts", "r")
                output_ts_file = open(
                    root_directory + "/src/app/components/" + lowercasename + "/" + lowercasename + ".component.ts",
                    "w")
                for line in component_ts_file:
                    linestr = str(line)
                    if(linestr.find("IMPORTS")>-1):
                        AngularFileMaker.add_component_imports(tabledata, output_ts_file)
                    elif(linestr.find("MINS_&_MAXS")>-1):
                        AngularFileMaker.makeMinsAndMaxes(tabledata,output_ts_file)
                    elif(linestr.find("CONSTRUCTOR")>-1):
                        AngularFileMaker.create_component_constructor(tabledata, javaname, lowercasename, output_ts_file, tabs)
                    elif (linestr.find("LIST_ITEM_DTO") > -1):
                        AngularFileMaker.initialize_ts_object(tabledata, output_ts_file, True)
                        output_ts_file.write(tabs+ lowercasename + "list: " + dtoname + "[];\n")
                        # a full list needed by the search feature
                        output_ts_file.write(tabs + "full" + lowercasename + "list: " + dtoname + "[];\n")
                    elif (linestr.find("FK_DTO_LISTS") > -1):
                        AngularFileMaker.create_fk_dto_lists(tabledata, output_ts_file)
                    elif (linestr.find("INIT_FK_LISTS") > -1):
                        AngularFileMaker.initialize_fk_dto_lists(tabledata, output_ts_file)
                    elif (linestr.find("CLEAR_ITEM_DTO") > -1):
                        AngularFileMaker.initialize_ts_object(tabledata, output_ts_file, False)
                    elif (linestr.find("GET_ALL_RECORDS") > -1):
                        AngularFileMaker.create_getall_items_codeblock(project, dtoname, lowercasename, javaname,output_ts_file, tabs)
                    elif (linestr.find("NULL_OR_UNDEFINED") > -1):
                        AngularFileMaker.make_null_or_undefined_method(output_ts_file)
                    elif (linestr.find("CREATE_SERVICE") > -1):
                        AngularFileMaker.create_createitem_codeblock(tabledata, project, dtoname, lowercasename,
                                                                     output_ts_file, tabs)
                    elif (linestr.find("EDIT_SERVICE") > -1):
                        AngularFileMaker.create_updateitem_codeblock(javaname, lowercasename, output_ts_file, tabs)
                    elif (linestr.find("DELETE_SERVICE") > -1):
                        AngularFileMaker.create_deleteitem_codeblock(tabledata, project, dtoname, lowercasename,
                                                                     output_ts_file, tabs)
                    elif linestr.find("FOREIGN_KEY_CALLS") >-1:
                        if len(tabledata.fksymbolnames) > 0:
                            AngularFileMaker.make_test_fk_ts_section(tabledata, output_ts_file)
                    elif linestr.find("VALIDATOR_CALLS") >-1:
                        AngularFileMaker.make_validator_calls(tabledata, output_ts_file)
                    elif linestr.find("SEARCH_FEATURE")>-1:
                        AngularFileMaker.make_search(tabledata, output_ts_file)
                    else:
                        output_ts_file.write(linestr.replace("%", javaname).replace("&", lowercasename))

                # make the css file

                output_css_file = open(
                    root_directory + "/src/app/components/" + lowercasename + "/" + lowercasename + ".component.css",
                    "w")
            except Exception :
                print("something went wrong inside the AngularFileMaker.make_components method : " + Exception)
            finally:
                if (component_html_file is not None):
                    component_html_file.close()
                if (output_html_file is not None):
                    output_html_file.close()
                if (component_ts_file is not None):
                    component_ts_file.close()
                if (output_ts_file is not None):
                    output_ts_file.close()
                if (output_css_file is not None):
                    output_css_file.close()

    @staticmethod
    def make_fk_names(projectnames,projectdata,tabledata):
        """
        this method groups together some important foreign key data for other methods
        to use later
        :param projectnames:
        :param projectdata:
        :param tabledata:
        :return:
        """
        parentnames = {}
        for name in tabledata.fieldnames:
            fielddata = tabledata.fielddata[name]
            if fielddata.isforeignkey == True:
                fksymbol = fielddata.fksymbol
                fksymboldata = tabledata.fksymboldata[fksymbol]
                parenttablename = str(fksymboldata[0][1])
                parentfieldname = str(fksymboldata[0][2])
                """
                    the premise here is that the parent table could be in any of the projects,
                    the assumption here is that, because these projects are made from a DDL(which
                    can't have more than 1 table with the same name), ONLY ONE of the projects
                    will have a table with the given parent table name
                """
                parenttablefound = False
                parentprojectname = None
                for projectname in projectnames:
                    if parenttablefound == False:
                        parentprojectdata = projectdata[projectname]
                        if parenttablename in parentprojectdata.tabledata.keys():
                            parenttablefound = True
                            parentprojectname = projectname
                            print(
                                "field - " + name + " has a parent key found in project : " + parentprojectname + " , table : " + parenttablename)
                parentproject = projectdata[parentprojectname]
                parenttable = parentproject.tabledata[parenttablename]
                # we don't want to have tables imported multiple times
                if parenttable not in parentnames:
                    parentfield = parenttable.fielddata[parentfieldname]
                    parentkeyname = parentfield.javaname
                    parentnames[parenttable] = "1"
                    displayname = None
                    if len(parenttable.fieldnames)>2:
                        descriptorfieldname = parenttable.fieldnames[2]
                        descriptorfielddata = parenttable.fielddata[descriptorfieldname]
                        displayname = descriptorfielddata.javaname
                    else:
                        descriptorfieldname = parenttable.fieldnames[1]
                        descriptorfielddata = parenttable.fielddata[descriptorfieldname]
                        displayname = descriptorfielddata.javaname
                    parentdtoname = parenttable.dtoname
                    parentjavaname = parentdtoname.replace("DTO", "")
                    parentlowercasename = parentdtoname.replace("DTO", "").lower()
                    tabledata.fknames.append((parentdtoname,parentjavaname,parentlowercasename,parentkeyname,displayname,name,parentfield))

    @staticmethod
    def add_component_imports(tabledata,output_ts_file):
        """
        this method adds the imports to the typescript controller
        :param tabledata:
        :param dtoname:
        :param javaname:
        :param lowercasename:
        :param output_ts_file:
        :return:
        """
        dtoname = tabledata.dtoname
        javaname = dtoname.replace("DTO", "")
        lowercasename = dtoname.replace("DTO", "").lower()
        output_ts_file.write(
            "import { " + javaname + "Service } from '../../services/" + lowercasename + ".service';\n")
        output_ts_file.write("import { " + dtoname + " } from '../../models/" + dtoname + "';\n")
        if len(tabledata.fknames)>0:
            output_ts_file.write("import { ForeignKeyOptionsDTO } from '../../models/ForeignKeyOptionsDTO';\n")
        for x in range(0,len(tabledata.fknames)):
            fktuple = tabledata.fknames[x]
            parentdtoname = fktuple[0]
            parentjavaname = fktuple[1]
            parentlowercasename = fktuple[2]
            output_ts_file.write(
                "import { " + parentjavaname + "Service } from '../../services/" + parentlowercasename + ".service';\n")
            output_ts_file.write("import { " + parentdtoname + " } from '../../models/" + parentdtoname + "';\n")

    @staticmethod
    def create_component_constructor(tabledata, javaname, lowercasename, output_ts_file, tabs):
        """
        creates the constructor method for the component, adding any service handles needed by the component
        :param tabledata:
        :param javaname:
        :param lowercasename:
        :param output_ts_file:
        :param tabs:
        :return:
        """
        output_ts_file.write(tabs + "constructor( ")
        services = []
        services.append("private " + lowercasename + "service: " + javaname + "Service")
        for x in range(0, len(tabledata.fknames)):
            fktuple = tabledata.fknames[x]
            parentjavaname = fktuple[1]
            parentlowercasename = fktuple[2]
            services.append("private " + parentlowercasename + "service: " + parentjavaname + "Service")
        servicesstr = ",".join(services)
        output_ts_file.write(servicesstr)
        output_ts_file.write(" ) { }\n")

    @staticmethod
    def create_deleteitem_codeblock(tabledata, project, dtoname, lowercasename, output_ts_file, tabs):
        """
        creates the body for the delete record method in the component
        :param tabledata:
        :param project:
        :param dtoname:
        :param lowercasename:
        :param output_ts_file:
        :param tabs:
        :return:
        """
        fielddata = tabledata.fielddata[tabledata.fieldnames[0]]
        output_ts_file.write(tabs * 2 + "this.subscriptions.push(\n")
        output_ts_file.write(tabs * 3 + "this." + lowercasename + "service." +
                             project.rest_call_names[dtoname][
                                 4] + "(this." + lowercasename + "list[i]." + fielddata.javaname +
                             ").subscribe(response => {\n")
        output_ts_file.write(tabs * 3 + "this.reload();\n")
        output_ts_file.write(tabs * 3 + "this.paginationDisabled = false;\n")
        output_ts_file.write(tabs * 3 + "})\n")
        output_ts_file.write(tabs * 2 + ");\n")

    @staticmethod
    def create_updateitem_codeblock(javaname, lowercasename, output_ts_file, tabs):
        """
        creates the body for the update record method in the component
        :param javaname:
        :param lowercasename:
        :param output_ts_file:
        :param tabs:
        :return:
        """
        output_ts_file.write(tabs + "this." + lowercasename + " = this." + lowercasename + "list[i];\n")
        output_ts_file.write(tabs + "this.show" + javaname + "Form = true;\n")

    @staticmethod
    def create_createitem_codeblock(tabledata, project, dtoname, lowercasename, output_ts_file, tabs):
        """
        creates the body for the create record method in the component
        :param tabledata:
        :param project:
        :param dtoname:
        :param lowercasename:
        :param output_ts_file:
        :param tabs:
        :return:
        """
        AngularFileMaker.array_converter(tabledata,output_ts_file)
        output_ts_file.write(
            tabs + "if(this.addMode) {\n")
        output_ts_file.write(tabs * 2 + "this.subscriptions.push(\n")
        output_ts_file.write(tabs * 3 + "this." + lowercasename + "service." +
                             project.rest_call_names[dtoname][
                                 2] + "(this." + lowercasename + ").subscribe(" + lowercasename + " => {\n")
        output_ts_file.write(
            tabs * 3 + "this." + lowercasename + " = " + lowercasename + ";\n")
        output_ts_file.write(tabs * 2 + "this.reload();\n")
        counter = 0
        AngularFileMaker.initialize_blank_form_object(lowercasename, output_ts_file, tabledata)
        output_ts_file.write(tabs * 2 + "this.paginationDisabled = false;\n")
        output_ts_file.write(tabs * 2 + "})\n")
        output_ts_file.write(tabs + ");\n")
        output_ts_file.write(tabs + "} else if(this.editMode) {\n")
        output_ts_file.write(tabs * 2 + "this.subscriptions.push(\n")
        output_ts_file.write(tabs * 3 + "this." + lowercasename + "service." +
                             project.rest_call_names[dtoname][
                                 3] + "(this." + lowercasename + ").subscribe(" + lowercasename + " => {\n")
        output_ts_file.write(
            tabs * 3 + "this." + lowercasename + " = " + lowercasename + ";\n")
        output_ts_file.write(tabs * 3 + "this.reload();\n")
        counter = 0
        AngularFileMaker.initialize_blank_form_object(lowercasename, output_ts_file, tabledata)
        output_ts_file.write(tabs * 2 + "this.paginationDisabled = false;\n")
        output_ts_file.write(tabs * 2 + "})\n")
        output_ts_file.write(tabs + ");\n")
        output_ts_file.write(tabs + "}\n")

    @staticmethod
    def initialize_blank_form_object(lowercasename, output_ts_file, tabledata):
        tabs = Constants.tab
        for name in tabledata.fieldnames:
            fielddata = tabledata.fielddata[name]
            fieldtype = AngularFileMaker.translateDataType(fielddata.datatype)
            if fieldtype.find("[]") > -1:
                output_ts_file.write(tabs * 2 + "this." + lowercasename + "." + fielddata.javaname + " = [];\n")
            elif (fieldtype == 'number' or fieldtype == 'Date' or fieldtype == 'boolean'):
                output_ts_file.write(tabs * 2 + "this." + lowercasename + "." + fielddata.javaname + " = null;\n")
            else:
                output_ts_file.write(tabs * 2 + "this." + lowercasename + "." + fielddata.javaname + " = '';\n")

    @staticmethod
    def make_search(tabledata, output_ts_file):
        """
        this method creates the search feature code block
        :param tabledata:
        :param output_ts_file:
        :return:
        """
        tabs = Constants.tab
        javaname = tabledata.dtoname.replace("DTO", "")
        lowercasename = javaname.lower()
        output_ts_file.write(tabs * 2 + "const results: " + javaname + "DTO[] = [];\n")
        output_ts_file.write(tabs * 2 + "for (const " + lowercasename + " of this.full" + lowercasename + "list) {\n")
        liststr = tabs * 3 + "if("
        number_of_fields = len(tabledata.fieldnames)
        count = 1
        for name in tabledata.fieldnames:
            fielddata = tabledata.fielddata[name]
            if count == number_of_fields:
                if fielddata.datatype == "String":
                    liststr += "!this.isNullOrUndefined(" + lowercasename + "." + fielddata.javaname + ") && "
                    liststr += lowercasename + "." + fielddata.javaname + ".toLowerCase().indexOf(searchTerm.toLowerCase()) !== -1) {\n"
                else:
                    liststr += "!this.isNullOrUndefined(" + lowercasename + "." + fielddata.javaname + ") && "
                    liststr += lowercasename + "." + fielddata.javaname + ".toString().toLowerCase().indexOf(searchTerm.toLowerCase()) !== -1) {\n"
            else:
                count += 1
                if fielddata.datatype == "String":
                    liststr += "!this.isNullOrUndefined(" + lowercasename + "." + fielddata.javaname + ") && "
                    liststr += lowercasename + "." + fielddata.javaname + ".toLowerCase().indexOf(searchTerm.toLowerCase()) !== -1 ||\n" + tabs * 4
                else:
                    liststr += "!this.isNullOrUndefined(" + lowercasename + "." + fielddata.javaname + ") && "
                    liststr += lowercasename + "." + fielddata.javaname + ".toString().toLowerCase().indexOf(searchTerm.toLowerCase()) !== -1 ||\n" + tabs * 4
        output_ts_file.write(liststr)
        output_ts_file.write(tabs * 4 + "results.push(" + lowercasename + ");\n")
        output_ts_file.write(tabs * 3 + "}\n")
        output_ts_file.write(tabs * 2 + "}\n")
        output_ts_file.write(tabs * 2 + "this." + lowercasename + "list = results;\n")
        output_ts_file.write(tabs * 2 + "if (results.length === 0 || !searchTerm) {\n")
        output_ts_file.write(tabs * 3 + "this." + lowercasename + "list = this.full" + lowercasename + "list;\n")
        output_ts_file.write(tabs * 2 + "}\n")

    @staticmethod
    def create_getall_items_codeblock(project, dtoname, lowercasename, javaname, output_ts_file, tabs):
        """
        creates the body for the select * method in the component
        :param project:
        :param dtoname:
        :param lowercasename:
        :param output_ts_file:
        :param tabs:
        :return:
        """
        output_ts_file.write(tabs * 2 + "this.subscriptions.push(\n")
        output_ts_file.write(tabs * 3 + "this." + lowercasename + "service." + project.rest_call_names[dtoname][
            0] + "().subscribe(" + lowercasename + "list => {\n")
        output_ts_file.write(tabs * 3 + "this." + lowercasename + "list = " + lowercasename + "list;\n")
        output_ts_file.write(tabs * 3 + "this.full" + lowercasename + "list = " + lowercasename + "list;\n")
        output_ts_file.write(tabs * 3 + "this.loaded = true;\n")
        output_ts_file.write(tabs * 3 + "this.show" + javaname + "Form = false;\n")
        output_ts_file.write(tabs * 3 + "this.editMode = false;\n")
        output_ts_file.write(tabs * 3 + "this.addMode = false;\n")
        output_ts_file.write(tabs * 3 + "this.paginationDisabled = false;\n")
        output_ts_file.write(tabs * 2 + "})\n")
        output_ts_file.write(tabs + ");\n")

    @staticmethod
    def initialize_ts_object(tabledata,output_ts_file,new=False):
        """
        this method will initialize the dto object that is in each component .ts file
        :param tabledata:
        :param output_ts_file:
        :param new:
        :return:
        """
        tabs = Constants.tab
        lowercasename = tabledata.lowercasename
        if new == True:
            output_ts_file.write(tabs + lowercasename + ": " + tabledata.dtoname + " = {\n")
        else:
            output_ts_file.write(tabs + 'this.' + lowercasename + " = {\n")
        counter = 0
        for name in tabledata.fieldnames:
            fielddata = tabledata.fielddata[name]
            fieldtype = AngularFileMaker.translateDataType(fielddata.datatype)
            if fieldtype.find("[]") > -1:
                output_ts_file.write(tabs * 2 + fielddata.javaname + ": []")
            elif(fieldtype == 'number' or fieldtype == 'Date' or fieldtype == 'boolean'):
                output_ts_file.write(tabs * 2 + fielddata.javaname + ": null")
            else:
                output_ts_file.write(tabs * 2 + fielddata.javaname + ": ''")
            counter += 1
            if(counter<len(tabledata.fieldnames)):
                output_ts_file.write(",")
            output_ts_file.write("\n")
        output_ts_file.write(tabs+"};\n")

    @staticmethod
    def create_fk_dto_lists(tabledata,output_ts_file):
        """
        this method will create empty DTO lists for any parent tables needed by the current table
        :param tabledata:
        :param output_ts_file:
        :return:
        """
        tabs = Constants.tab
        for x in range(0, len(tabledata.fknames)):
            fktuple = tabledata.fknames[x]
            parentdtoname = fktuple[0]
            parentlowercasename = fktuple[2]
            output_ts_file.write(tabs + parentlowercasename + "list: ForeignKeyOptionsDTO[] = [];\n")
            output_ts_file.write(tabs + parentlowercasename + "map = new Map();\n")

    @staticmethod
    def initialize_fk_dto_lists(tabledata,output_ts_file):
        """
        this method will add calls to the getAll REST call for each parent key
        :param tabledata:
        :param output_ts_file:
        :return:
        """
        tabs = Constants.tab
        for x in range(0, len(tabledata.fknames)):
            fktuple = tabledata.fknames[x]
            parentdtoname = fktuple[0]
            parentjavaname = fktuple[1]
            parentlowercasename = fktuple[2]
            parentfieldname = fktuple[3]
            descriptorfield = fktuple[4]
            output_ts_file.write(tabs + "this.subscriptions.push(\n")
            output_ts_file.write(tabs + "this." + parentlowercasename + "service.getAll" + parentjavaname + "().subscribe(" + parentlowercasename + "list => {\n")
            output_ts_file.write(tabs * 2 + 'console.log("length of ' + parentlowercasename + 'list = " + ' + parentlowercasename + 'list.length);\n')
            output_ts_file.write(tabs * 2 + "for (let entry of " + parentlowercasename + "list) {\n")
            output_ts_file.write(tabs * 3 + "// change the value of entry.xxxx to be the actual field that you want to display\n")
            output_ts_file.write(tabs * 3 + "let optionDTO = new ForeignKeyOptionsDTO();\n")
            output_ts_file.write(tabs * 3 + "optionDTO.value = entry." + parentfieldname + ";\n")
            output_ts_file.write(tabs * 3 + "optionDTO.viewValue = entry." + descriptorfield + ";\n")
            output_ts_file.write(tabs * 3 + "this." + parentlowercasename + "list.push(optionDTO);\n")
            output_ts_file.write(tabs * 3 + "this." + parentlowercasename + "map.set(entry." + parentfieldname + ",entry." + descriptorfield + ");\n")
            output_ts_file.write(tabs * 2 + "}\n")
            output_ts_file.write(tabs + "})\n")
            output_ts_file.write(tabs + ");\n")

    @staticmethod
    def add_html_header(tabledata,output_html_file):
        """
        this method creates the table header section in the component.html file
        :param dtoname:
        :param angular_object:
        :param output_html_file:
        :return:
        """
        tabs = Constants.tab
        print("making the html for dtoname = " + tabledata.dtoname)
        for name in tabledata.fieldnames:
            fielddata = tabledata.fielddata[name]
            output_html_file.write(tabs*3+"<th>\n")
            output_html_file.write(tabs*4+'<i class="text-size-10">'+fielddata.javaname+'</i>\n')
            output_html_file.write(tabs*3 + "</th>\n")
        output_html_file.write(tabs*3 + "<th>\n")
        output_html_file.write(tabs*4 + '<i class="text-size-8">Edit Item</i>\n')
        output_html_file.write(tabs*3 + "</th>\n")
        output_html_file.write(tabs*3 + "<th>\n")
        output_html_file.write(tabs*4 + '<i class="text-size-8">Delete Item</i>\n')
        output_html_file.write(tabs*3 + "</th>\n")

    @staticmethod
    def add_html_body(tabledata,output_html_file):
        """
        this method creates the table body section in the component.html file
        :param tabledata:
        :param output_html_file:
        :return:
        """
        tabs = Constants.tab
        print("making the html for dtoname = " + tabledata.dtoname)
        output_html_file.write(tabs*3 + '<td [hidden]="alwaysHidden">{{ i + 1 }}</td>\n')
        fktuples = {}
        for x in range(0, len(tabledata.fknames)):
            tuple = tabledata.fknames[x]
            childfieldname = tuple[5]
            fktuples[childfieldname] = tuple
        for name in tabledata.fieldnames:
            fielddata = tabledata.fielddata[name]
            if name in fktuples.keys():
                tuple = fktuples[name]
                output_html_file.write(tabs * 3 + "<td>\n")
                output_html_file.write(tabs * 4 + '<i class="text-size-6">{{this.' + tuple[2] + 'map.get(dto.' + tuple[6].javaname + ')}}</i>\n')
                output_html_file.write(tabs * 3 + "</td>\n")
            else:
                output_html_file.write(tabs*3+"<td>\n")
                output_html_file.write(tabs*4+'<i class="text-size-6">{{dto.'+fielddata.javaname+'}}</i>\n')
                output_html_file.write(tabs*3 + "</td>\n")
        output_html_file.write(tabs*3 + "<td>\n")
        output_html_file.write(tabs*4 + '<button class="btn-edit" type="submit" [disabled]="addMode || editMode" (click)="editItem(i + (p-1)*itemsPerPage)">\n')
        output_html_file.write(tabs*5 + '<span class="fas fa-edit" style="color:red"></span>\n')
        output_html_file.write(tabs*4 + '</button>\n')
        output_html_file.write(tabs*3 + "</td>\n")
        output_html_file.write(tabs*3 + "<td>\n")
        output_html_file.write(tabs*4 + '<button class="btn-edit" type="submit" [disabled]="addMode || editMode" (click)="deleteItem(i + (p-1)*itemsPerPage)">\n')
        output_html_file.write(tabs*5 + '<span class="fas fa-trash" style="color:blue"></span>\n')
        output_html_file.write(tabs*4 + '</button>\n')
        output_html_file.write(tabs*3 + "</td>\n")

    @staticmethod
    def add_html_form_body(tabledata, output_html_file):
        """
        this method will create the add/edit form on the component's html page
        :param tabledata:
        :param output_html_file:
        :return:
        """
        tabs = Constants.tab
        lowercasename = tabledata.lowercasename
        fktuples = {}
        for x in range (0,len(tabledata.fknames)):
            tuple = tabledata.fknames[x]
            childfieldname = tuple[5]
            fktuples[childfieldname] = tuple
        print("making the html form for dtoname = " + tabledata.dtoname)
        for name in tabledata.fieldnames:
            fielddata = tabledata.fielddata[name]
            if fielddata.isprimary == False:
                if name in fktuples.keys():
                    tuple = fktuples[name]
                    output_html_file.write(tabs * 4 + '<label>' + fielddata.javaname + '</label>\n')
                    output_html_file.write(tabs * 5 + '<div class="col col-sm-4">\n')
                    output_html_file.write(tabs * 5 + '<select class="form-control border-info text-center"\n')
                    output_html_file.write(tabs * 5 + '[(ngModel)]="' + tabledata.lowercasename + '.' + fielddata.javaname + '"\n')
                    if fielddata.canbenull == False:
                        output_html_file.write(tabs * 5 + 'required\n')
                    output_html_file.write(tabs * 5 + 'name="' + fielddata.javaname + '_dropdown">\n')
                    output_html_file.write(tabs * 6 + '<option *ngFor="let option of ' + tuple[2] + 'list" [value]="option.value">\n')
                    output_html_file.write(tabs * 7 + '{{ option.viewValue }}\n')
                    output_html_file.write(tabs * 6 + '</option>\n')
                    output_html_file.write(tabs * 5 + '</select>\n')
                    output_html_file.write(tabs * 4 + '</div>\n')
                else:
                    output_html_file.write(tabs*4 + '<label>'+fielddata.javaname+'</label>\n')
                    type = "text"
                    fieldtype = fielddata.datatype.lower()
                    if fieldtype == "integer" or fieldtype == "long"  or fieldtype == "biginteger":
                        type = "number"
                    elif (fieldtype == "date" or fieldtype == "datetime"
                              or fieldtype == "timestamp" or fieldtype == "time"):
                        type = "date"
                    elif (fieldtype == 'decimal' or fieldtype == "float" or fieldtype == "double" or fieldtype == "bigdecimal"):
                        type = "text"
                    elif fieldtype == 'boolean':
                        type = "boolean"
                    if type != "boolean":
                        output_html_file.write(tabs*4+'<input type="'+type+'" class="form-control" [(ngModel)]="'+
                                lowercasename+'.'+fielddata.javaname+'" name="'+fielddata.javaname+'" #'+
                                fielddata.javaname+'="ngModel"\n')
                        if (fieldtype == 'decimal' or fieldtype == "float" or fieldtype == "double" or fieldtype == "bigdecimal"):
                            output_html_file.write(tabs * 5 + '(keyup)="make' + fielddata.javaname + 'PositiveDecimalOnly()"\n')
                        if fielddata.canbenull == False:
                            output_html_file.write(tabs * 5 + 'required\n')
                        if fielddata.lengthreq == True:
                            output_html_file.write(tabs * 5 + 'maxlength=' + str(fielddata.length) + '\n')
                        output_html_file.write(tabs*4+'>\n')
                        if fielddata.canbenull == False:
                            output_html_file.write(tabs * 4 +'<div *ngIf="'+
                                name + '.invalid && (' + fielddata.javaname +
                                '.dirty || '+ fielddata.javaname + '.touched)"\n')
                            output_html_file.write(tabs * 5 + 'class="alert alert-danger">\n')
                            output_html_file.write(tabs * 5 +'<div *ngIf="'+
                                fielddata.javaname + '.errors.required">\n')
                            output_html_file.write(tabs * 6 + fielddata.javaname + ' is required.\n')
                            output_html_file.write(tabs * 5 + '</div>\n')
                            output_html_file.write(tabs * 4 + "</div>\n")
                    else:
                        output_html_file.write(tabs * 5 + '<div class="col col-sm-4">\n')
                        output_html_file.write(tabs * 5 + '<select class="form-control border-info text-center"\n')
                        output_html_file.write(
                            tabs * 5 + '[(ngModel)]="' + tabledata.lowercasename + '.' + fielddata.javaname + '"\n')
                        if fielddata.canbenull == False:
                            output_html_file.write(tabs * 5 + 'required\n')
                        output_html_file.write(tabs * 5 + 'name="' + fielddata.javaname + '_dropdown">\n')
                        output_html_file.write(
                            tabs * 6 + '<option [value]="true">true</option>\n')
                        output_html_file.write(
                            tabs * 6 + '<option [value]="false">false</option>\n')
                        output_html_file.write(tabs * 5 + '</select>\n')
                        output_html_file.write(tabs * 4 + '</div>\n')
                    #output_html_file.write(tabs * 3 + "</div>\n")

    @staticmethod
    def makeMinsAndMaxes(tabledata,output_ts_file):
        """
        this method is used to make fields that specify the minimums and maximums for any decimal fields
        :param tabledata:
        :param output_ts_file:
        :return:
        """
        tabs = Constants.tab
        for name in tabledata.fieldnames:
            fielddata = tabledata.fielddata[name]
            if fielddata.isprimary == False:
                fieldtype = fielddata.datatype.lower()
                if (fieldtype == "integer" or fieldtype == "long" or fieldtype == "biginteger"):
                    None
                elif (fieldtype == 'decimal' or fieldtype == "float" or fieldtype == "double" or fieldtype == "bigdecimal"):
                    output_ts_file.write(tabs+fielddata.javaname + "Max: number = " + str(fielddata.length) + ";\n")
                    output_ts_file.write(tabs+fielddata.javaname + "SigDigits: number = " + str(fielddata.decimals) + ";\n")

    @staticmethod
    def make_validator_calls(tabledata, output_ts_file):
        """
        this method will make the validator methods for numbers in the typescript file
        :param tabledata:
        :param output_ts_file:
        :return:
        """
        tabs = Constants.tab
        for name in tabledata.fieldnames:
            fielddata = tabledata.fielddata[name]
            if fielddata.isprimary == False:
                type = "text"
                fieldtype = fielddata.datatype.lower()
                if (fieldtype == "integer" or fieldtype == "long" or fieldtype == "biginteger"):
                    None
                elif (fieldtype == 'decimal' or fieldtype == "float" or fieldtype == "double" or fieldtype == "bigdecimal"):
                    inputfile = open("files/angular/component/makeFieldPositiveDecimalOnly.ts","r")
                    for line in inputfile:
                        linestr = str(line)
                        output_ts_file.write(linestr.replace("FIELD_NAME",fielddata.javaname).replace("TABLE_NAME",tabledata.tablename))
                    inputfile.close()

    @staticmethod
    def make_test_fk_html_section(tabledata, output_file):
        """
        this method will put a small temporary section section on the html page that will
        allow us to test any/all findByForeignKey methods
        :param tabledata:
        :param output_file:
        :return:
        """
        compoundFK = []
        inputparameters = []
        counter = 0
        for symbolname in tabledata.fksymbolnames:
            fklist = tabledata.fksymboldata[symbolname]
            for item in fklist:
                html_snippet = open("files/angular/fk_miniform.html", "r")
                field = tabledata.fielddata[item[0]]
                compoundFK.append(field.gettername)
                inputparameters.append(field)
                for line in html_snippet:
                    linestr = str(line)
                    if linestr.find("PARAM_SECTION")>-1:
                        param_snippet = open("files/angular/params.html", "r")
                        for innerline in param_snippet:
                            innerlinestr = str(innerline)
                            output_file.write(innerlinestr.replace("_FK_NAME_",field.javaname)
                                .replace("_TBL_NME_", tabledata.lowercasename)
                                .replace("_DATA_TYPE_",Utilities.translateAngularDataType(field.datatype)))
                        param_snippet.close()
                    else:
                        output_file.write(linestr.replace("_MTHD_NM_", "findBy"+field.gettername)
                                .replace("_BTN_MSG_","findBy" + field.gettername))
                counter += 1
                html_snippet.close()

        if len(compoundFK) > 1:
            compoundFKstr = "And".join(compoundFK)
            html_snippet = open("files/angular/fk_miniform.html", "r")
            for line in html_snippet:
                linestr = str(line)
                if linestr.find("PARAM_SECTION")>-1:
                    for field in inputparameters:
                        param_snippet = open("files/angular/params.html", "r")
                        for innerline in param_snippet:
                            innerlinestr = str(innerline)
                            output_file.write(innerlinestr.replace("_FK_NAME_", field.javaname)
                                        .replace("_TBL_NME_",tabledata.lowercasename)
                                              .replace("_DATA_TYPE_",
                                                       Utilities.translateAngularDataType(field.datatype)))
                        param_snippet.close()
                else:
                    output_file.write(linestr.replace("_MTHD_NM_", "findBy"+compoundFKstr)
                                      .replace("_BTN_MSG_", "findBy" + compoundFKstr))
            html_snippet.close()

    @staticmethod
    def make_test_fk_ts_section(tabledata, output_file):
        """
        this method will add methods in the typescript page that will
        allow us to test any/all findByForeignKey methods
        :param tabledata:
        :param output_file:
        :return:
        """
        tabs = Constants.tab
        compoundFK = []
        datatypes = []
        inputparameters = []
        counter = 0
        for symbolname in tabledata.fksymbolnames:
            fklist = tabledata.fksymboldata[symbolname]
            for item in fklist:
                field = tabledata.fielddata[item[0]]
                compoundFK.append(field.gettername)
                datatypes.append("id" + str(counter) + ": " + Utilities.translateAngularDataType(field.datatype))
                inputparameters.append('this.' + tabledata.lowercasename + '.' + field.javaname)
                output_file.write(tabs +"findBy" + field.gettername + "() {\n")

                output_file.write(tabs * 2 + "this.subscriptions.push(\n")
                output_file.write(
                    tabs * 3 + 'this.' + tabledata.lowercasename + 'service.find' + tabledata.camelcasejavaname + 'By' + field.gettername +
                    '(this.' + tabledata.lowercasename + '.' + field.javaname + ').subscribe(response => {\n')
                output_file.write(tabs * 4 + 'console.log("back from findBy' + field.gettername + '");\n' +
                                tabs * 4 + 'console.log("array size = " + response.length );\n' +
                                  tabs * 4 + "this.reload();\n" + tabs * 3 + "})\n")
                output_file.write(tabs * 2 + ");\n" + tabs + "}\n\n")

                counter += 1
        if len(compoundFK) > 1:
            compoundFKstr = "And".join(compoundFK)
            output_file.write(tabs + "findBy" + compoundFKstr + "() {\n")
            output_file.write(tabs * 2 + "this.subscriptions.push(\n")
            output_file.write(tabs * 3 + 'this.' + tabledata.lowercasename + 'service.find' + tabledata.camelcasejavaname + 'By' + compoundFKstr +
                '(' + ",".join(inputparameters) + ').subscribe(response => {\n')
            output_file.write(tabs * 4 + 'console.log("back from findBy' + compoundFKstr + '");\n'  +
                              tabs * 4 + 'console.log("array size = " + response.length );\n' +
                              tabs * 4 + "this.reload();\n" + tabs * 3 + "})\n")
            output_file.write(tabs * 2 + ");\n" + tabs + "}\n\n")

    @staticmethod
    def make_services(project, angular_object, root_directory):
        """
        this method will make all of the component files for a project
        :param project:
        :param angular_object:
        :param root_directory:
        :return:
        """
        tabs = Constants.tab
        for tablename in project.tablenames:
            tabledata = project.tabledata[tablename]
            dtoname = tabledata.dtoname
            # TODO - remove this later
            javaname = dtoname.replace("DTO", "")
            lowercasename = dtoname.replace("DTO", "").lower()
            angular_object.names.append(lowercasename)
            angular_object.services.add(javaname + "Service")
            # END TODO
            component_service_file = None
            output_service_file = None
            try:
                component_service_file = open("files/angular/service.ts", "r")
                output_service_file = open(
                    root_directory + "/src/app/services/" + tabledata.lowercasename + ".service.ts",
                    "w")
                for line in component_service_file:
                    linestr = str(line)
                    if (linestr.find("IMPORTS") > -1):
                        output_service_file.write("import { " + dtoname + " } from '../models/" + dtoname + "';\n")
                    elif (linestr.find("FK_SECTION") > -1):
                        AngularFileMaker.make_findby_fk_calls(tabledata, output_service_file)
                    elif (linestr.find("URLS") > -1):
                        counter = range(len(project.rest_call_names[dtoname]))
                        for x in counter:
                            output_service_file.write(
                                tabs + project.rest_call_names[dtoname][x] + "URL : string = '" +
                                project.urls[dtoname][x] + "';\n")
                    else:
                        output_service_file.write(linestr.replace("_TBL_NM_", tabledata.camelcasejavaname))
            except:
                print("something went wrong inside the AngularFileMaker.make_services method")
            finally:
                if (component_service_file is not None):
                    component_service_file.close()
                if (output_service_file is not None):
                    output_service_file.close()

    @staticmethod
    def make_services_for_foreign_keys(projectnames, projectdata, project, angular_object, root_directory):
        """
        this method will make all of the component files for a project
        :param projectnames:
        :param projectdata:
        :param project:
        :param angular_object:
        :param root_directory:
        :return:
        """
        # multiple for loops - BAD CODE, FIX LATER
        tabs = Constants.tab
        filename = ''
        for tablename in project.tablenames:
            tabledata = project.tabledata[tablename]
            for fksymbolname in tabledata.fksymbolnames:
                fksymboldata = tabledata.fksymboldata[fksymbolname]
                parenttablename = str(fksymboldata[0][1])
                # for each project:
                for projectname in projectnames:
                    project = projectdata[projectname]
                    if project.is_mid_level == False and parenttablename in project.tabledata.keys():
                        parenttable = project.tabledata[parenttablename]
                        dtoname = parenttable.dtoname
                        # TODO - remove this later
                        javaname = dtoname.replace("DTO", "")
                        angular_object.services.add(javaname + "Service")
                        # END TODO
                        component_service_file = None
                        output_service_file = None
                        try:
                            component_service_file = open("files/angular/service.ts", "r")
                            output_service_file = open(
                                root_directory + "/src/app/services/" + parenttable.lowercasename + ".service.ts",
                                "w")
                            for line in component_service_file:
                                linestr = str(line)
                                if (linestr.find("IMPORTS") > -1):
                                    output_service_file.write("import { " + dtoname + " } from '../models/" + dtoname + "';\n")
                                elif (linestr.find("FK_SECTION") > -1):
                                    AngularFileMaker.make_findby_fk_calls(parenttable, output_service_file)
                                elif (linestr.find("URLS") > -1):
                                    counter = range(len(project.rest_call_names[dtoname]))
                                    for x in counter:
                                        output_service_file.write(
                                            tabs + project.rest_call_names[dtoname][x] + "URL : string = '" +
                                            project.urls[dtoname][x] + "';\n")
                                else:
                                    output_service_file.write(linestr.replace("_TBL_NM_", parenttable.camelcasejavaname))
                        except:
                            print("something went wrong inside the AngularFileMaker.make_services method")
                        finally:
                            if (component_service_file is not None):
                                component_service_file.close()
                            if (output_service_file is not None):
                                output_service_file.close()

    @staticmethod
    def make_findby_fk_calls(tabledata, output_file):
        """
        this method will make the actual code in the service class that makes the REST calls
        :param tabledata:
        :param output_file:
        :return:
        """
        tabs = Constants.tab
        compoundFK = []
        datatypes = []
        inputparameters = []
        counter = 0
        for symbolname in tabledata.fksymbolnames:
            fklist = tabledata.fksymboldata[symbolname]
            for item in fklist:
                field = tabledata.fielddata[item[0]]
                compoundFK.append(field.gettername)
                datatypes.append("id" + str(counter) + ": " + Utilities.translateAngularDataType(field.datatype))
                inputparameters.append('replace("{id' + str(counter) + '}", id' + str(counter) + '.toString(10))')
                output_file.write(tabs + "find" + tabledata.camelcasejavaname +
                    "By" + field.gettername + "(id: " +
                        Utilities.translateAngularDataType(field.datatype) + "): Observable<" + tabledata.camelcasejavaname +
                    "DTO[]>{\n")
                output_file.write(
                    tabs * 2 + 'let find' + tabledata.camelcasejavaname + 'By' + field.gettername + 'URL_temp = this.find' + tabledata.camelcasejavaname + 'By' + field.gettername +
                    'URL.replace("{id}", id.toString(10));\n')
                output_file.write(tabs * 2 + "return this.http.get<" + tabledata.camelcasejavaname +
                                     "DTO[]>(find" + tabledata.camelcasejavaname +
                    "By" + field.gettername + "URL_temp);\n" + tabs + "}\n")
                counter += 1
        if len(compoundFK) > 1:
            compoundFKstr = "And".join(compoundFK)
            text = tabs + "find" + tabledata.camelcasejavaname + "By" + compoundFKstr + "("
            text += ",".join(datatypes)
            text += "): Observable<" + tabledata.camelcasejavaname + "DTO[]>{\n"
            output_file.write(text)
            output_file.write(
                tabs * 2 + 'this.find' + tabledata.camelcasejavaname +
                    'By' + compoundFKstr + 'URL = this.find' + tabledata.camelcasejavaname +
                    'By' + compoundFKstr +
                'URL.' + ".".join(inputparameters) + ";\n")
            output_file.write(tabs * 2 + "return this.http.get<" + tabledata.camelcasejavaname +
                              "DTO[]>(this.find" + tabledata.camelcasejavaname +
                    "By" + compoundFKstr + "URL);\n" + tabs + "}\n")

    @staticmethod
    def make_rest_call_codeblock(dtoname, name, type, paramlist, output_service_file):
        """
        this method will make the actual code in the service class that makes the REST calls
        :param dtoname:
        :param name:
        :param type:
        :param paramlist:
        :param output_service_file:
        :return:
        """
        tabs = Constants.tab
        if(type == "get"):
            if(len(paramlist) > 0):
                # find by primary key
                output_service_file.write(tabs+name+"(")
                paramarray = paramlist.split(" ")
                paramname = paramarray[1]
                paramtype = paramarray[0]
                if(paramtype == "int"):
                    paramtype = "number"
                output_service_file.write(paramname+": "+paramtype+"): Observable<"+dtoname+"> {\n")
                if (paramtype == "number"):
                    output_service_file.write(tabs+tabs+'this.'+name+'URL = this.'+name+'URL.replace("{id}",id.toString(10));\n')
                output_service_file.write(tabs+tabs+"return this.http.get<"+dtoname+">(this."+name+"URL);\n")
                output_service_file.write(tabs+"}\n")
            else:
                # this is the get all or the healthcheck
                if(name.find("health")>-1):
                    None
                else:
                    output_service_file.write(tabs + name + "(): Observable<"+ dtoname + "[]> {\n")
                    output_service_file.write(
                        tabs + tabs + "return this.http.get<" + dtoname + "[]>(this." + name + "URL);\n")
                    output_service_file.write(tabs + "}\n")
        elif(type == "post"):
            output_service_file.write(tabs + name + "(")
            paramarray = paramlist.split(" ")
            paramname = paramarray[1]
            paramtype = paramarray[0]
            output_service_file.write(paramname + ": " + paramtype + "): Observable<" + dtoname + "> {\n")
            output_service_file.write(tabs + tabs + "return this.http.post<" + dtoname + ">(this." + name + "URL, "+paramname+", httpOptions);\n")
            output_service_file.write(tabs + "}\n")
        elif(type == "delete"):
            output_service_file.write(tabs + name + "(")
            paramarray = paramlist.split(" ")
            paramname = paramarray[1]
            paramtype = paramarray[0]
            if (paramtype == "int"):
                paramtype = "number"
            output_service_file.write(paramname + ": " + paramtype + "): Observable<ResponseMessage> {\n")
            if (paramtype == "number"):
                output_service_file.write(tabs + tabs + 'this.' + name + 'URL = this.' + name + 'URL.replace("{id}",id.toString(10));\n')
            output_service_file.write(tabs + tabs + "return this.http.delete<ResponseMessage>(this." + name + "URL, httpOptions);\n")
            output_service_file.write(tabs + "}\n")

    @staticmethod
    def make_angularjson_file(project, root_directory):
        """
        this method generates the angular.json file
        :param project:
        :param root_directory:
        :return:
        """
        tabs = Constants.tab
        angularjsonfile = None
        altered_aj_file = None
        try:
            angularjsonfile = open("files/angular/angular.json","r")
            altered_aj_file = open(root_directory+"/angular.json","w")
            stylesfound = False
            scriptsfound = False
            for line in angularjsonfile:
                linestr = str(line)
                if(stylesfound == False and linestr.find('"src/styles.css"')>-1):
                    altered_aj_file.write(linestr.replace('"src/styles.css"','"src/styles.css",'))
                    altered_aj_file.write(tabs+tabs+tabs+'"node_modules/font-awesome/css/font-awesome.css",\n')
                    altered_aj_file.write(tabs + tabs + tabs +'"node_modules/bootstrap/dist/css/bootstrap.css"\n')
                    stylesfound = True
                elif(scriptsfound == False and linestr.find('"scripts": []')>-1):
                    altered_aj_file.write(linestr.replace('"scripts": []', '"scripts": ['))
                    altered_aj_file.write(tabs + tabs + tabs +'"node_modules/jquery/dist/jquery.js",\n')
                    altered_aj_file.write(tabs + tabs + tabs +'"node_modules/popper.js/dist/umd/popper.js",\n')
                    altered_aj_file.write(tabs + tabs + tabs +'"node_modules/bootstrap/dist/js/bootstrap.js"\n')
                    altered_aj_file.write(tabs+tabs+"]\n")
                    scriptsfound = True
                else:
                    altered_aj_file.write(linestr.replace("_PROJECT_NAME_",project.pomname))
        except:
            print("something went wrong inside the AngularFileMaker.make_angularjson_file method")
        finally:
            if(angularjsonfile is not None):
                angularjsonfile.close()
            if (altered_aj_file is not None):
                altered_aj_file

    @staticmethod
    def make_packagejson_file(root_directory):
        """
        this method generates the package.json file
        :param root_directory:
        :return:
        """
        tabs = Constants.tab
        packagejsonfile = None
        altered_pj_file = None
        try:
            packagejsonfile = open("files/angular/package.json","r")
            altered_pj_file = open(root_directory+"/package.json","w")
            for line in packagejsonfile:
                linestr = str(line)
                if(linestr.find('"zone.js"')>-1):
                    altered_pj_file.write(tabs + tabs + tabs + '"bootstrap": "xxx",'.replace('xxx',Configuration.angular_boostrap)+"\n")
                    altered_pj_file.write(tabs + tabs + tabs + '"core-js": "xxx",'.replace('xxx',Configuration.angular_core_js)+"\n")
                    altered_pj_file.write(tabs + tabs + tabs + '"font-awesome": "xxx",'.replace('xxx',Configuration.angular_font_awesome ) + "\n")
                    altered_pj_file.write(tabs + tabs + tabs + '"jquery": "xxx",'.replace('xxx',Configuration.angular_jquery ) + "\n")
                    altered_pj_file.write(tabs + tabs + tabs + '"popper.js": "xxx",'.replace('xxx',Configuration.angular_popper_js ) + "\n")
                    altered_pj_file.write(linestr)
                else:
                    altered_pj_file.write(linestr)
        except:
            print("something went wrong inside the AngularFileMaker.make_packagejson_file method")
        finally:
            if(packagejsonfile is not None):
                packagejsonfile.close()
            if (altered_pj_file is not None):
                altered_pj_file

    @staticmethod
    def make_folders(root_directory):
        """
        this program makes the src folder and app subfolder and components,models,guards,services subfolders
        :param root_directory:
        :return:
        """
        if not os.path.exists(root_directory+"/src"):
            os.mkdir(root_directory+"/src")
        if not os.path.exists(root_directory + "/src/app"):
            os.mkdir(root_directory + "/src/app")
        if not os.path.exists(root_directory + "/src/app/components"):
            os.mkdir(root_directory + "/src/app/components")
        if not os.path.exists(root_directory + "/src/app/models"):
            os.mkdir(root_directory + "/src/app/models")
        if not os.path.exists(root_directory + "/src/app/guards"):
            os.mkdir(root_directory + "/src/app/guards")
        if not os.path.exists(root_directory + "/src/app/services"):
            os.mkdir(root_directory + "/src/app/services")

    @staticmethod
    def make_app_modules_ts_file(project, angular_object, root_directory):
        """
        this method will make the app.module.ts file
        :param project:
        :param angular_object:
        :param root_directory:
        :return:
        """
        tabs = Constants.tab
        old_app_module_ts_file = None
        new_app_module_ts_file = None
        try:
            old_app_module_ts_file = open("files/angular/app.module.ts","r")
            new_app_module_ts_file = open(root_directory+"/src/app/app.module.ts","w")
            for line in old_app_module_ts_file:
                linestr = str(line)
                if (linestr.find("IMPORTS") > -1):
                    counter = 0
                    for item in project.components:
                        new_app_module_ts_file.write(
                            "import { " + item + " } from './components/" + angular_object.names[counter] + "/" +
                            angular_object.names[counter] + ".component';\n")
                        counter += 1
                    for item in angular_object.services:
                        lowername = str(item)[0:-7].lower()
                        new_app_module_ts_file.write(
                            "import { " + item + " } from './services/" + lowername + ".service';\n")
                    counter = 0
                    for item in angular_object.modules:
                        new_app_module_ts_file.write(
                            "import { " + item + " } from './modules/" + angular_object.names[counter] + "/" +
                            angular_object.names[counter] + ".component';\n")
                        counter += 1
                elif(linestr.find("ADD_DECLARATIONS") > -1):
                    new_app_module_ts_file.write(tabs+"AppComponent,\n")
                    new_app_module_ts_file.write(tabs + "NavbarComponent,\n")
                    counter = 0
                    for item in project.components:
                        new_app_module_ts_file.write(tabs+tabs+item)
                        counter += 1
                        if (counter < len(project.components)):
                            new_app_module_ts_file.write(",")
                        new_app_module_ts_file.write("\n")
                elif(linestr.find("ADD_MODULES") > -1):
                    new_app_module_ts_file.write(tabs + "BrowserModule,\n")
                    new_app_module_ts_file.write(tabs + "AppRoutingModule,\n")
                    new_app_module_ts_file.write(tabs + "HttpClientModule,\n")
                    new_app_module_ts_file.write(tabs + "NgxPaginationModule,\n")
                    new_app_module_ts_file.write(tabs + "FormsModule\n")
                elif(linestr.find("ADD_PROVIDERS") > -1):
                    new_app_module_ts_file.write(linestr.replace("ADD_PROVIDERS",",".join(list(angular_object.services))))
                else:
                    new_app_module_ts_file.write(linestr)
        except:
            print("something went wrong inside the AngularFileMaker.make_app_modules_ts_file method")
        finally:
            if(old_app_module_ts_file is not None):
                old_app_module_ts_file.close()
            if (new_app_module_ts_file is not None):
                new_app_module_ts_file

    @staticmethod
    def make_style_css_file(root_directory):
        """
        this method will generate the global css file
        :param root_directory:
        :return:
        """
        tabs = Constants.tab
        old_index_file = None
        new_index_file = None
        old_css_file = open("files/angular/styles.css", "r")
        new_css_file = open(root_directory + "/src/styles.css", "w")
        for line in old_css_file:
            linestr = str(line)
            new_css_file.write(linestr)
        if (old_css_file is not None):
            old_css_file.close()
        if (new_css_file is not None):
            new_css_file

    @staticmethod
    def make_index_html_file(project, root_directory):
        """
        this method will make the app.module.ts file
        :param project:
        :param root_directory:
        :return:
        """
        tabs = Constants.tab
        old_index_file = None
        new_index_file = None
        try:
            old_index_file = open("files/angular/index.html","r")
            new_index_file = open(root_directory+"/src/index.html","w")
            for line in old_index_file:
                linestr = str(line)
                if linestr.find("APP_TITLE") > -1:
                    new_index_file.write(linestr.replace("APP_TITLE",project.pomname))
                else:
                    new_index_file.write(linestr)
        except:
            print("something went wrong inside the AngularFileMaker.make_index_html_file method")
        finally:
            if(old_index_file is not None):
                old_index_file.close()
            if (new_index_file is not None):
                new_index_file

    @staticmethod
    def make_navigation_bar(project,root_directory):
        """
        this method will make a navigation bar component
        :param project:
        :param root_directory:
        :return:
        """
        tabs = Constants.tab
        if not os.path.exists(root_directory + "/src/app/components/navbar"):
            os.mkdir(root_directory + "/src/app/components/navbar")
        inputfile = open("files/angular/navbar.component.html", "r")
        outputfile = open(root_directory + "/src/app/components/navbar/navbar.component.html", "w")
        for line in inputfile:
            linestr = str(line)
            if(linestr.find("ROUTES")>-1):
                counter = 0
                for item in project.components:
                    rootname = str(item)[0:-9]
                    lowername = rootname.lower()
                    outputfile.write(tabs *3 +'<li class="nav-item">\n')
                    outputfile.write(tabs * 4 +'<a routerLink="/'+ lowername + '" class="nav-link">' + rootname + '</a>\n')
                    outputfile.write(tabs * 3 +'</li>\n')
                    counter += 1
            else:
                outputfile.write(linestr)
        outputfile.close()
        inputfile = open('files/angular/navbar.component.ts')
        outputfile = open(root_directory + "/src/app/components/navbar/navbar.component.ts", "w")
        for line in inputfile:
            linestr = str(line)
            outputfile.write(linestr)
        inputfile.close()
        outputfile.close()
        outputfile = open(root_directory + "/src/app/components/navbar/navbar.component.css", "w")
        outputfile.close()

    @staticmethod
    def make_app_component_file(root_directory):
        """
        this method makes the app.component.html file
        :param root_directory:
        :return:
        """
        tabs = Constants.tab
        outputfile = open(root_directory + "/src/app/app.component.html", "w")
        outputfile.write('<app-navbar></app-navbar>\n')
        outputfile.write(tabs + '<div class="container-fluid">\n')
        outputfile.write(tabs + '<router-outlet></router-outlet>\n')
        outputfile.write(tabs + '</div>')
        outputfile.close()

    @staticmethod
    def make_dropdown_options_dto(root_directory):
        """
        this method will make a DTO with value,viewValue fields, that is used in a form
        for each foreign key
        :return:
        """
        tabs = Constants.tab
        outputfile = open(root_directory + "/src/app/models/ForeignKeyOptionsDTO.ts", "w")
        outputfile.write('export class ForeignKeyOptionsDTO {\n')
        outputfile.write(tabs + 'value: any;\n')
        outputfile.write(tabs + 'viewValue: any;\n')
        outputfile.write('}')
        outputfile.close()

    @staticmethod
    def make_null_or_undefined_method(output_file):
        """
        this will make a method in each typescript component that will return a true if the
        input component being tested is null or undefined
        :param output_file:
        :return:
        """
        tabs = Constants.tab
        output_file.write(tabs + "private isNullOrUndefined(input: any): boolean {\n")
        output_file.write(tabs * 2 + "if(input === 'undefined') return true;\n")
        output_file.write(tabs *2 + "if(input == null) return true;\n")
        output_file.write(tabs * 2 + "return false;\n")
        output_file.write(tabs + "}\n")

    @staticmethod
    def array_converter(tabledata, output_file):
        """
        this method is used whenever one of our fields is an array of something
        it will convert the input field to an array
        :param tabledata:
        :param output_file:
        :return:
        """
        tabs = Constants.tab
        for fieldname in tabledata.fieldnames:
            fielddata = tabledata.fielddata[fieldname]
            if fielddata.datatype .find("[]") > -1:
                output_file.write(tabs * 2 + "let " + fielddata.javaname + "temp = this." + tabledata.lowercasename + "." + fielddata.javaname + ".toString();\n")
                output_file.write(
                    tabs * 2 + 'this.' + tabledata.lowercasename + '.' + fielddata.javaname + ' = ' + fielddata.javaname + 'temp.split(",");\n')

