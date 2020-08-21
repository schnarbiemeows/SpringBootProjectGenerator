import glob
from popos.AngularObject import *
from utilities.FileMaker import *
"""
    this class will create the angular 8 project for a given project
"""
class AngularFileMaker:

    def __init__(self):
        None

    @staticmethod
    def make_angular_project(projectsnames,projectdata,root_directory):
        """
        this method will create the angular 8 project for a given project
        :param projectsnames:
        :param projectdata:
        :param root_directory:
        :return:
        """
        # for each project:
        for projectname in projectsnames:
            project = projectdata[projectname]
            # make the base file structure of the project
            root_directory = FileMaker.make_base_angular_project(project)
            AngularFileMaker.make_folders(project,root_directory)
            # make an AngularObject
            angular_object = AngularObject()
            # make angular module classes from the DTOs
            AngularFileMaker.make_angular_classes(project, angular_object, root_directory)
            # parse the controller class to get some important information that we will need in order to make both the service file
            # and the component ts file
            AngularFileMaker.parse_controller_class(project, angular_object)
            # make the services
            AngularFileMaker.make_services(project, angular_object, root_directory)
            # make the components
            AngularFileMaker.make_components(project,angular_object, root_directory)
            # make the navigation bar
            AngularFileMaker.make_navigation_bar(project, angular_object, root_directory)
            # make the app-routing.module.ts file
            AngularFileMaker.make_app_routing_module(project, angular_object, root_directory)
            # make the app.module.ts file
            AngularFileMaker.make_app_modules_ts_file(project, angular_object, root_directory)
            # make the config files
            AngularFileMaker.make_angularjson_file(project, root_directory)
            AngularFileMaker.make_packagejson_file(project, root_directory)
            # make the index.html files
            AngularFileMaker.make_app_component_file(project, root_directory)
            AngularFileMaker.make_index_html_file(project, root_directory)

    @staticmethod
    def parse_controller_class( project, angular_object):
        """
        this method will create the urls in the service class for calling the backing controller
        it will also assemble a map of other information inside the AngularObject for that DTO, so
        that we can use this stuff later and not ahve to parse this controller file again
        :param project:
        :param angular_object:
        :return:
        """
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
        for dtoname in angular_object.dto_names:
            print("Analyzing the Controller class for dtoname : " + dtoname)
            angular_object.urls[dtoname] = []
            angular_object.rest_call_names[dtoname] = []
            angular_object.rest_call_types[dtoname] = []
            angular_object.rest_call_parameters[dtoname] = []
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
                        linestr = linestr.replace("public ResponseEntity<Object> ","")
                        rest_call_name = linestr[0:linestr.find("(")].lstrip()
                        print("Which has a rest-call-name of : " + rest_call_name)
                        print("Which we are attempting to put into key = : " + currentdto)
                        angular_object.rest_call_names[currentdto].append(rest_call_name)
                        angular_object.rest_call_parameters[currentdto].append(AngularFileMaker.remove_annotations_from_string(linestr))
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
                                    angular_object.urls[dtoname].append(full_url)
                                    angular_object.rest_call_types[dtoname].append(request_type)
                                else:
                                    print("which does not qualify")
                                    requestfound = False
                            else:
                                currentdto = dtoname
                                print("2 - which we are putting into " + dtoname)
                                angular_object.urls[dtoname].append(full_url)
                                angular_object.rest_call_types[dtoname].append(request_type)
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
    def remove_annotations_from_string( inputstring):
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
    def make_app_routing_module(project, angular_object,root_directory):
        """
        this method will make the app-routing.module.ts file
        :param project:
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
                    for item in angular_object.components:
                        app_routing_output.write("import { " + item + " } from './components/" + angular_object.names[counter] + "/" + angular_object.names[counter] + ".component';\n")
                        counter += 1
                elif (linestr.find("ROUTES") > -1):
                    counter = 0
                    for item in angular_object.components:
                        app_routing_output.write("{ path: '" + angular_object.names[counter] + "', component: " + item + " }")
                        counter += 1
                        if(counter<len(angular_object.components)):
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
    def make_components( project, angular_object, root_directory):
        """
        this method will make all of the component files for a project
        :param project:
        :param angular_object:
        :param root_directory:
        :return:
        """
        tabs = Constants.tab
        for dtoname in angular_object.dto_names:
            javaname = dtoname.replace("DTO","")
            lowercasename = dtoname.replace("DTO","").lower()
            angular_object.components.append(javaname + "Component")
            angular_object.selectors.append("app-" + lowercasename)
            angular_object.routes.append("/" + lowercasename)
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
                    if (linestr.find("XXX") > -1):
                        output_html_file.write(linestr.replace("XXX", javaname))
                    elif (linestr.find("YYY") > -1):
                        AngularFileMaker.add_html_header(dtoname, angular_object, output_html_file)
                    elif (linestr.find("ZZZ") > -1):
                        AngularFileMaker.add_html_body(dtoname, angular_object, output_html_file)
                    elif (linestr.find("WWW") > -1):
                        AngularFileMaker.add_html_form_body(dtoname, angular_object, output_html_file)
                    else:
                        output_html_file.write(linestr.replace("%",lowercasename+"list"))

                # make the .ts file

                component_ts_file = open("files/angular/component.ts", "r")
                output_ts_file = open(
                    root_directory + "/src/app/components/" + lowercasename + "/" + lowercasename + ".component.ts",
                    "w")
                for line in component_ts_file:
                    linestr = str(line)
                    if(linestr.find("IMPORTS")>-1):
                        output_ts_file.write("import { " + javaname+"Service } from '../../services/" + lowercasename + ".service';\n")
                        output_ts_file.write("import { " + dtoname + " } from '../../models/" + dtoname + "';\n")
                    elif(linestr.find("CONSTRUCTOR")>-1):
                        output_ts_file.write(tabs + "constructor( ")
                        output_ts_file.write("private " + lowercasename + "service: " + javaname+"Service")
                        output_ts_file.write(" ) { }\n")
                    elif (linestr.find("LIST_ITEM_DTO") > -1):
                        AngularFileMaker.initialize_ts_object(dtoname,angular_object,output_ts_file)
                        output_ts_file.write(tabs+ lowercasename + "list: " + dtoname + "[];\n")
                    elif (linestr.find("GET_ALL_RECORDS") > -1):
                        output_ts_file.write(tabs + "this."+ lowercasename + "service." + angular_object.rest_call_names[dtoname][0] + "().subscribe(" + lowercasename + "list => {\n")
                        output_ts_file.write(tabs+tabs+"this."+lowercasename+"list = " + lowercasename + "list;\n")
                        output_ts_file.write(tabs + tabs + "this.loaded = true;\n")
                        output_ts_file.write(tabs +"});\n")
                    elif (linestr.find("CREATE_SERVICE") > -1):
                        output_ts_file.write(tabs + "if(this." + lowercasename +"." + angular_object.fieldnames[dtoname][0] + " === null ) {\n")
                        output_ts_file.write(tabs + tabs + "this." + lowercasename + "service." +
                                             angular_object.rest_call_names[dtoname][
                                                 2] + "(this."+lowercasename +").subscribe(" + lowercasename + " => {\n")
                        output_ts_file.write(
                            tabs + tabs + "this." + lowercasename + " = " + lowercasename + ";\n")
                        output_ts_file.write(tabs + tabs + "this.reload();\n")
                        output_ts_file.write(tabs + "});\n")

                        output_ts_file.write(tabs + "} else {\n")

                        output_ts_file.write(tabs + tabs + "this." + lowercasename + "service." +
                                             angular_object.rest_call_names[dtoname][
                                                 3] + "(this." + lowercasename + ").subscribe(" + lowercasename + " => {\n")
                        output_ts_file.write(
                            tabs + tabs + "this." + lowercasename + " = " + lowercasename + ";\n")
                        output_ts_file.write(tabs + tabs + "this.reload();\n")
                        output_ts_file.write(tabs + "});\n")
                        output_ts_file.write(tabs + "}\n")
                        counter = 0
                        for name in angular_object.fieldnames[dtoname]:
                            fieldtype = angular_object.fieldtypes[dtoname][name]
                            if (fieldtype == 'number' or fieldtype == 'Date' or fieldtype == 'boolean'):
                                output_ts_file.write(tabs + "this." + lowercasename + "." + name + " = null;\n")
                            else:
                                output_ts_file.write(tabs + "this." + lowercasename + "." + name + " = '';\n")
                    elif (linestr.find("EDIT_SERVICE") > -1):
                        output_ts_file.write(tabs + "this." + lowercasename + " = this." + lowercasename + "list[i];\n")
                        output_ts_file.write(tabs + "this.show" + javaname + "Form = true;\n")
                    elif (linestr.find("DELETE_SERVICE") > -1):
                        output_ts_file.write(tabs + "this." + lowercasename + "service." +
                                             angular_object.rest_call_names[dtoname][
                                                 4] + "(this." + lowercasename +"list[i]." + angular_object.fieldnames[dtoname][0] + ").subscribe(response => {\n")
                        output_ts_file.write(tabs + tabs + "this.reload();\n")
                        output_ts_file.write(tabs + "});\n")
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
    def initialize_ts_object(dtoname, angular_object,output_ts_file):
        """
        this method will initialize the dto object that is in each component .ts file
        :param dtoname:
        :param angular_object:
        :param output_ts_file:
        :return:
        """
        tabs = Constants.tab
        lowercasename = dtoname.replace("DTO", "").lower()
        output_ts_file.write(tabs + lowercasename + ": " + dtoname + " = {\n")
        counter = 0
        for name in angular_object.fieldnames[dtoname]:
            fieldtype = angular_object.fieldtypes[dtoname][name]
            if(fieldtype == 'number' or fieldtype == 'Date' or fieldtype == 'boolean'):
                output_ts_file.write(tabs + tabs + name + ": null")
            else:
                output_ts_file.write(tabs + tabs + name + ": ''")
            counter += 1
            if(counter<len(angular_object.fieldnames[dtoname])):
                output_ts_file.write(",")
            output_ts_file.write("\n")
        output_ts_file.write(tabs+"};\n")

    @staticmethod
    def add_html_header(dtoname, angular_object, output_html_file):
        """

        :param dtoname:
        :param angular_object:
        :param output_html_file:
        :return:
        """
        tabs = Constants.tab
        print("making the html for dtoname = " + dtoname)
        for name in angular_object.fieldnames[dtoname]:
            output_html_file.write(tabs*3+"<th>\n")
            output_html_file.write(tabs*4+'<i class="text-size-10">'+name+'</i>\n')
            output_html_file.write(tabs*3 + "</th>\n")
        output_html_file.write(tabs*3 + "<th>\n")
        output_html_file.write(tabs*4 + '<i class="text-size-8">Edit Item</i>\n')
        output_html_file.write(tabs*3 + "</th>\n")
        output_html_file.write(tabs*3 + "<th>\n")
        output_html_file.write(tabs*4 + '<i class="text-size-8">Delete Item</i>\n')
        output_html_file.write(tabs*3 + "</th>\n")

    @staticmethod
    def add_html_body(dtoname, angular_object, output_html_file):
        """

        :param dtoname:
        :param angular_object:
        :param output_html_file:
        :return:
        """
        tabs = Constants.tab
        print("making the html for dtoname = " + dtoname)
        output_html_file.write(tabs*3 + '<td [hidden]="alwaysHidden">{{ i + 1 }}</td>\n')
        for name in angular_object.fieldnames[dtoname]:
            output_html_file.write(tabs*3+"<td>\n")
            output_html_file.write(tabs*4+'<i class="text-size-10">{{dto.'+name+'}}</i>\n')
            output_html_file.write(tabs*3 + "</td>\n")
        output_html_file.write(tabs*3 + "<td>\n")
        output_html_file.write(tabs*4 + '<button class="btn-edit" type="submit" (click)="editItem(i)">\n')
        output_html_file.write(tabs*5 + '<span class="iconspan fa fa-edit"></span>\n')
        output_html_file.write(tabs*4 + '</button>\n')
        output_html_file.write(tabs*3 + "</td>\n")
        output_html_file.write(tabs*3 + "<td>\n")
        output_html_file.write(tabs*4 + '<button class="btn-edit" type="submit" (click)="deleteItem(i)">\n')
        output_html_file.write(tabs*5 + '<span class="iconspan fa fa-trash"></span>\n')
        output_html_file.write(tabs*4 + '</button>\n')
        output_html_file.write(tabs*3 + "</td>\n")

    @staticmethod
    def add_html_form_body(dtoname, angular_object, output_html_file):
        """

        :param dtoname:
        :param angular_object:
        :param output_html_file:
        :return:
        """
        tabs = Constants.tab
        lowercasename = dtoname.replace("DTO", "").lower()
        print("making the html form for dtoname = " + dtoname)
        counter = 0
        for name in angular_object.fieldnames[dtoname]:
            if (counter > 0):
                output_html_file.write(tabs*3+'<div class="form-group">\n')
                output_html_file.write(tabs*4 + '<label>'+name+'</label>\n')
                type = "text"
                fieldtype = angular_object.fieldtypes[dtoname][name]
                if (fieldtype == 'number'):
                    type = "number"
                elif(fieldtype == 'date'):
                    type = "date"
                output_html_file.write(tabs*4+'<input type="'+type+'" class="form-control" [(ngModel)]="'+lowercasename+'.'+name+'" name="'+name+'">\n')
                output_html_file.write(tabs*3 + "</div>\n")
            counter += 1

    @staticmethod
    def make_services( project, angular_object, root_directory):
        """
        this method will make all of the component files for a project
        :param project:
        :param angular_object:
        :param root_directory:
        :return:
        """
        tabs = Constants.tab
        for dtoname in angular_object.dto_names:
            javaname = dtoname.replace("DTO","")
            lowercasename = dtoname.replace("DTO","").lower()
            angular_object.names.append(lowercasename)
            angular_object.services.append(javaname + "Service")
            component_service_file = None
            output_service_file = None
            try:
                component_service_file = open("files/angular/service.ts", "r")
                output_service_file = open(
                    root_directory + "/src/app/services/" + lowercasename + ".service.ts",
                    "w")
                for line in component_service_file:
                    linestr = str(line)
                    if (linestr.find("IMPORTS") > -1):
                        output_service_file.write("import { " + dtoname + " } from '../models/" + dtoname + "';\n")
                    elif(linestr.find("SERVICE_CALLS")>-1):
                        counter = range(len(angular_object.rest_call_names[dtoname]))
                        for x in counter:
                            AngularFileMaker.make_rest_call_code_block(dtoname, angular_object.rest_call_names[dtoname][x], angular_object.rest_call_types[dtoname][x],angular_object.rest_call_parameters[dtoname][x],output_service_file)
                    elif (linestr.find("URLS") > -1):
                        counter = range(len(angular_object.rest_call_names[dtoname]))
                        for x in counter:
                            output_service_file.write(tabs+angular_object.rest_call_names[dtoname][x]+"URL : string = '" + angular_object.urls[dtoname][x]+"';\n")
                    else:
                        output_service_file.write(linestr.replace("%", javaname).replace("&", lowercasename))
            except:
                print("something went wrong inside the AngularFileMaker.make_services method")
            finally:
                if (component_service_file is not None):
                    component_service_file.close()
                if (output_service_file is not None):
                    output_service_file.close()

    @staticmethod
    def make_rest_call_code_block( dtoname, name, type, paramlist, output_service_file):
        """
        this method will make the actual code in the service class that makes the REST call
        :param dtoname
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
    def make_angularjson_file( project, root_directory):
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
                    altered_aj_file.write(linestr)
        except:
            print("something went wrong inside the AngularFileMaker.make_angularjson_file method")
        finally:
            if(angularjsonfile is not None):
                angularjsonfile.close()
            if (altered_aj_file is not None):
                altered_aj_file

    @staticmethod
    def make_packagejson_file( project, root_directory):
        """
        this method generates the package.json file
        :param project:
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
    def make_folders( project, root_directory):
        """
        this program makes the src folder and app subfolder and components,models,guards,services subfolders
        :param project:
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
    def make_app_modules_ts_file( project, angular_object, root_directory):
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
                    for item in angular_object.components:
                        new_app_module_ts_file.write(
                            "import { " + item + " } from './components/" + angular_object.names[counter] + "/" +
                            angular_object.names[counter] + ".component';\n")
                        counter += 1
                    counter = 0
                    for item in angular_object.services:
                        new_app_module_ts_file.write(
                            "import { " + item + " } from './services/" + angular_object.names[counter] + ".service';\n")
                        counter += 1
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
                    for item in angular_object.components:
                        new_app_module_ts_file.write(tabs+tabs+item)
                        counter += 1
                        if (counter < len(angular_object.components)):
                            new_app_module_ts_file.write(",")
                        new_app_module_ts_file.write("\n")
                elif(linestr.find("ADD_MODULES") > -1):
                    new_app_module_ts_file.write(tabs + "BrowserModule,\n")
                    new_app_module_ts_file.write(tabs + "AppRoutingModule,\n")
                    new_app_module_ts_file.write(tabs + "HttpClientModule,\n")
                    new_app_module_ts_file.write(tabs + "NgxPaginationModule,\n")
                    new_app_module_ts_file.write(tabs + "FormsModule\n")
                    #new_app_module_ts_file.write(tabs + "// modules added here\n")
                    AngularFileMaker.figureout_module_additions(project, new_app_module_ts_file)
                elif(linestr.find("ADD_PROVIDERS") > -1):
                    new_app_module_ts_file.write(linestr.replace("ADD_PROVIDERS",",".join(angular_object.services)))
                else:
                    new_app_module_ts_file.write(linestr)
        except:
            print("something went wrong inside the AngularFileMaker.make_packagejson_file method")
        finally:
            if(old_app_module_ts_file is not None):
                old_app_module_ts_file.close()
            if (new_app_module_ts_file is not None):
                new_app_module_ts_file

    @staticmethod
    def figureout_imports( project, new_app_module_ts_file):
        """

        :param project:
        :param new_app_module_ts_file:
        :return:
        """
        new_app_module_ts_file.write("import { NavbarComponent } from './components/navbar/navbar.component';\n")

    @staticmethod
    def figureout_module_additions( project, new_app_module_ts_file):
        """

        :param project:
        :param new_app_module_ts_file:
        :return:
        """
        None

    @staticmethod
    def figureout_service_additions( project, new_app_module_ts_file):
        """

        :param project:
        :param new_app_module_ts_file:
        :return:
        """
        None

    @staticmethod
    def make_index_html_file( project, root_directory):
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
    def make_angular_classes( project, angular_obj, root_directory):
        """
        this method will make the DTO objects for a given project in Angular
        :param project:
        :param angular_obj:
        :param root_directory:
        :return:
        """
        tabs = Constants.tab
        filenames = []
        if(project.is_mid_level == True):
            filenames = glob.glob(project.topmainpackage + "/" + Constants.path_proxy_dtos + "/*")
        else:
            filenames = glob.glob(project.topmainpackage+ "/" + Constants.pckg_dtos + "/*")
        outputfilename = ''
        for filename in filenames:
            inputfile = open(filename,"r")
            for line in inputfile:
                linestr = str(line)
                if (linestr.find("public class") > -1):
                    outputfilename = linestr.split(" ")[2].replace("{","")
                    print("output file name will be = " + outputfilename)
            outputfile = open(root_directory+"/src/app/models/"+outputfilename+".ts","w")
            outputfile.write("export interface " + outputfilename + "{\n")

            angular_obj.dto_names.append(outputfilename)
            angular_obj.fieldnames[outputfilename] = []
            angular_obj.fieldtypes[outputfilename] = {}
            inputfile.close()
            inputfile = open(filename,"r")
            for line in inputfile:
                linestr = str(line)
                if linestr.find("private") > -1 and linestr.find(Constants.serial_uid) == -1:
                    fieldarray = linestr.split(" ")
                    key = fieldarray[2].replace(";","").rstrip()
                    print("field name " + key)
                    angular_obj.fieldnames[outputfilename].append(key)
                    if(fieldarray[1].lower() == "int" or fieldarray[1].lower() == "integer" or fieldarray[1].lower() == "long" or fieldarray[1].lower() == "float" or fieldarray[1].lower() == "double" or fieldarray[1].lower() == "biginteger" or fieldarray[1].lower() == "bigdecimal" ):
                        angular_obj.fieldtypes[outputfilename][key] = "number"
                    elif(fieldarray[1].lower() == "date" or fieldarray[1].lower() == "datetime"
                         or fieldarray[1].lower() == "timestamp" or fieldarray[1].lower() == "time"):
                        angular_obj.fieldtypes[outputfilename][key] = "Date"
                    else:
                        angular_obj.fieldtypes[outputfilename][key] = fieldarray[1].lower()
            #counter = 0
            for name in angular_obj.fieldnames[outputfilename]:
                outputfile.write(tabs + name + "?: " + angular_obj.fieldtypes[outputfilename][name]+";")
                #counter +=1
                #if(counter<len(angular_obj.fieldnames[outputfilename])):
                #    outputfile.write(",")
                outputfile.write("\n")
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
    def make_navigation_bar( project, angular_project, root_directory):
        """
        this method will make a navigation bar component
        :param project:
        :param angular_project:
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
                for item in angular_project.routes:
                    outputfile.write(tabs+tabs+tabs+'<li class="nav-item">\n')
                    outputfile.write(tabs+tabs+tabs+tabs+'<a routerLink="'+ item + '" class="nav-link">' + angular_project.names[counter] + '</a>\n')
                    outputfile.write(tabs+tabs+tabs+'</li>\n')
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
    def make_app_component_file( project, root_directory):
        """
        this method makes the app.component.html file
        :param project:
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
