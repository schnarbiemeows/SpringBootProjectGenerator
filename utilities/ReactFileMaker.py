

from configuration.Configuration import *
from configuration.Constants import Constants
from utilities.AngularFileMaker import AngularFileMaker
from utilities.FileMaker import *
import os

class ReactFileMaker:

    def __init__(self):
        None

    @staticmethod
    def make_react_projects(projectnames, projectdata):
        for projectname in projectnames:
            project = projectdata[projectname]
            root_directory = FileMaker.make_base_react_project(project)

            ReactFileMaker.make_folders(root_directory)
            ReactFileMaker.make_base_files(root_directory)
            ReactFileMaker.make_package_file(project, root_directory)
            ReactFileMaker.make_app_file(project, root_directory)

            ReactFileMaker.make_components(projectnames, projectdata, project, root_directory)
            print("DONE!")
    @staticmethod
    def make_folders(root_directory):
        if not os.path.exists(root_directory+"/src"):
            os.mkdir(root_directory+"/src")
        if not os.path.exists(root_directory + "/src/components"):
            os.mkdir(root_directory + "/src/components")
        if not os.path.exists(root_directory + "/src/components/common"):
            os.mkdir(root_directory + "/src/components/common")
        if not os.path.exists(root_directory + "/src/components/specific"):
            os.mkdir(root_directory + "/src/components/specific")
        if not os.path.exists(root_directory + "/src/models"):
            os.mkdir(root_directory + "/src/models")

    @staticmethod
    def make_base_files(root_directory):
        FileMaker.copy_file("files/react/src/App.css", root_directory + "/src/App.css")
        FileMaker.copy_file("files/react/src/App.test.js", root_directory + "/src/App.test.js")
        FileMaker.copy_file("files/react/src/index.css", root_directory + "/src/index.css")
        FileMaker.copy_file("files/react/src/index.js", root_directory + "/src/index.js")

    @staticmethod
    def make_package_file(project,root_directory):
        inputfile = open("files/react/package.json", "r")
        outputfile = open(root_directory+"/package.json", "w")
        for line in str(inputfile) :
            linestr = str(line)
            outputfile.write(linestr.replace("APP_NAME",project.pomname+"\n"))
        if inputfile is not None:
            inputfile.close()
        if outputfile is not None:
            outputfile.close()

    @staticmethod
    def make_app_file(project, root_directory):
        inputfile = open("files/react/src/App.js", "r")
        outputfile = open(root_directory + "/src/App.js", "w")
        for line in inputfile:
            linestr = str(line)
            if linestr.find("IMPORTS_SECTION")>-1:
                ReactFileMaker.make_imports(outputfile, project)
            elif linestr.find("LINKS_SECTION")>-1:
                ReactFileMaker.make_links(outputfile, project)
            elif linestr.find("ROUTE_SECTION")>-1:
                ReactFileMaker.make_routes(outputfile, project)
            else:
                outputfile.write(linestr.replace("APP_NAME", project.pomname + "\n"))
        if inputfile is not None:
            inputfile.close()
        if outputfile is not None:
            outputfile.close()

    @staticmethod
    def make_imports(outputfile, project):
        for tablename in project.tablenames:
            tabledata = project.tabledata[tablename]
            outputfile.write('import '+tabledata.camelcasejavaname+'Component from "./components/specific/'+
                    tabledata.lowercasename + "/" + tabledata.camelcasejavaname + 'Component.js"\n')

    @staticmethod
    def make_links(outputfile, project):
        tabs = Constants.tab
        for tablename in project.tablenames:
            tabledata = project.tabledata[tablename]
            outputfile.write(tabs * 7 +'<Nav.Link as={Link} to="/'+tabledata.lowercasename+
                             '">'+tabledata.camelcasejavaname+'</Nav.Link>\n')

    @staticmethod
    def make_routes(outputfile, project):
        tabs = Constants.tab
        for tablename in project.tablenames:
            tabledata = project.tabledata[tablename]
            outputfile.write(tabs * 5 +'<Route path="/'+tabledata.lowercasename+'" element={<'+
                             tabledata.camelcasejavaname+'Component />} />\n')
        outputfile.write(tabs*5 + '<Route path="/" element={<h2>Welcome! Select a component.</h2>} />\n')


    @staticmethod
    def make_components(projectnames, projectdata, project, root_directory):
        ReactFileMaker.make_models(projectnames, projectdata, project, root_directory)
        ReactFileMaker.make_common_components(root_directory)
        ReactFileMaker.make_table_components(projectnames, projectdata, project, root_directory)

    @staticmethod
    def make_models(projectnames, projectdata, project, root_directory):
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
            outputfile = open(root_directory + "/src/models/" + dtoname + ".js", "w")
            outputfile.write("export class " + dtoname + "{\n")
            inputfile.close()
            print("making the React DTO for : " + dtoname)
            inputfile = open(filename, "r")
            parameterlist = ""
            for line in inputfile:
                linestr = str(line)
                if linestr.find(Constants.privateval) > -1 and linestr.find(
                        Constants.serial_uid) == -1 and linestr.find(Constants.logger) == -1:
                    fieldarray = linestr.split(" ")
                    key = fieldarray[2].replace(";", "").rstrip()
                    print("DTO field name " + key)
                    outputfile.write(tabs + key + "\n")
                    parameterlist+=key+","
            outputfile.write("\n" + tabs + "constructor(")
            parameterlist = parameterlist[:-1].split(",")
            for item in parameterlist:
                outputfile.write(item+", ")
            outputfile.write(") {\n")
            for item in parameterlist:
                outputfile.write(tabs+tabs+"this."+item+" = " + item + "\n")
            outputfile.write(tabs+"}\n")
            outputfile.write("}")
            if inputfile is not None:
                inputfile.close()
            if outputfile is not None:
                outputfile.close()

    @staticmethod
    def make_common_components(root_directory):
        FileMaker.copy_file("files/react/src/components/common/SearchComponent.js",root_directory+"/src/components/common/SearchComponent.js")
        FileMaker.copy_file("files/react/src/components/common/FormFieldComponent.js", root_directory + "/src/components/common/FormFieldComponent.js")
        FileMaker.copy_file("files/react/src/components/common/ButtonComponent.js", root_directory + "/src/components/common/ButtonComponent.js")
        FileMaker.copy_file("files/react/src/components/common/FormComponent.js", root_directory + "/src/components/common/FormComponent.js")
        FileMaker.copy_file("files/react/src/components/common/ListItemComponent.js", root_directory + "/src/components/common/ListItemComponent.js")
        FileMaker.copy_file("files/react/src/components/common/ListComponent.js", root_directory + "/src/components/common/ListComponent.js")
        FileMaker.copy_file("files/react/src/components/common/ListHeadComponent.js", root_directory + "/src/components/common/ListHeadComponent.js")
        FileMaker.copy_file("files/react/src/components/common/TitleComponent.js", root_directory + "/src/components/common/TitleComponent.js")

    @staticmethod
    def make_table_components(projectnames, projectdata, project, root_directory):
        tabs = Constants.tab
        for tablename in project.tablenames:
            tabledata = project.tabledata[tablename]
            dtoname = tabledata.dtoname
            javaname = dtoname.replace("DTO", "")
            lowercasename = dtoname.replace("DTO", "").lower()
            project.components.append(javaname + "Component")
            component_template = None
            component_file = None
            try:
                # make the component file
                component_template = open("files/react/src/components/specific/TableComponent.js", "r")
                if not os.path.exists(root_directory + "/src/components/specific/"+ lowercasename):
                    os.mkdir(root_directory + "/src/components/specific/"+ lowercasename)
                component_file = open(
                    root_directory + "/src/components/specific/" + lowercasename + "/" + javaname + "Component.js",
                    "w")
                for line in component_template:
                    linestr = str(line)
                    if (linestr.find("DTO_FIELDS") > -1):
                        ReactFileMaker.add_dto_fields_section(tabledata, component_file)
                    elif (linestr.find("HEADER_LIST") > -1):
                        ReactFileMaker.create_header_list(tabledata, component_file)
                    elif (linestr.find("FIELD_CONFIG_LIST") > -1):
                        ReactFileMaker.create_field_config_list(tabledata, component_file)
                    elif (linestr.find("TOUCHED_SECTION") > -1):
                        ReactFileMaker.create_touched_section(tabledata, component_file)
                    elif (linestr.find("ERRORS_SECTION") > -1):
                        ReactFileMaker.create_errors_section(tabledata, component_file)
                    else:
                        component_file.write(linestr.replace("*", javaname).replace("&", lowercasename)
                                             .replace("XX","&&")
                                             .replace("^","*"))

            except Exception:
                print("something went wrong inside the AngularFileMaker.make_components method : " + Exception)
            finally:
                if component_template is not None:
                    component_template.close()
                if component_file is not None:
                    component_file.close()

    @staticmethod
    def add_dto_fields_section(tabledata, component_file):
        tabs = Constants.tab
        for fieldname in tabledata.fieldnames:
            field = tabledata.fielddata[fieldname]
            if field.datatype == "String":
                component_file.write(tabs+tabs+" '',\n")
            else:
                component_file.write(tabs + tabs + "null,\n")

    @staticmethod
    def create_header_list(tabledata, component_file):
        tabs = Constants.tab
        for fieldname in tabledata.fieldnames:
            field = tabledata.fielddata[fieldname]
            component_file.write(tabs+tabs+'{ key: "'+field.name+'", label: "'+field.name+'" },\n')

    @staticmethod
    def create_field_config_list(tabledata, component_file):
        tabs = Constants.tab
        for fieldname in tabledata.fieldnames:
            field = tabledata.fielddata[fieldname]
            component_file.write(tabs + tabs + '{name: "'+field.name+'", type: "'+field.datatype+'", label: "'+field.name+
                                 '", placeholder: "Enter a '+field.name+'"},\n')


    @staticmethod
    def create_touched_section(tabledata, component_file):
        tabs=Constants.tab
        fieldstring = tabs+tabs+"setTouched({"
        for fieldname in tabledata.fieldnames:
            field = tabledata.fielddata[fieldname]
            fieldstring += field.name+': false, '
        fieldstring = fieldstring[:-2]+"})\n"
        component_file.write(fieldstring)

    @staticmethod
    def create_errors_section(tabledata, component_file):
        tabs = Constants.tab
        fieldstring = tabs + tabs + "setErrors({"
        for fieldname in tabledata.fieldnames:
            field = tabledata.fielddata[fieldname]
            fieldstring += field.name + ': "", '
        fieldstring = fieldstring[:-2] + "})\n"
        component_file.write(fieldstring)




