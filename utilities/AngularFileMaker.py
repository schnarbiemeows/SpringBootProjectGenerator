import sys
import os
import glob
from configuration.Constants import *
from popos.AngularObject import *
from utilities.FileMaker import *
"""
    this class will create the angular 8 project for a given project
"""
class AngularFileMaker:

    def __init__(self):
        self.projectsnames = []
        self.projectdata = {}
        self.filemaker = FileMaker()
        self.root_directory = ''

    def make_angular_project(self):
        """
        this method will create the angular 8 project for a given project
        :param project:
        :return:
        """
        # for each project:
        for projectname in self.projectsnames:
            project = self.projectdata[projectname]
            # make the base file structure of the project
            self.root_directory = self.filemaker.make_base_angular_project(project)
            self.make_folders(project)
            # make an AngularObject
            angular_object = AngularObject()
            # make angular module classes from the DTOs
            self.make_angular_classes(project, angular_object)
            # parse the controller class to get some important information that we will need in order to make both the service file
            # and the component ts file
            self.parse_controller_class(project, angular_object)
            # make the services
            self.make_services(project, angular_object)
            # make the components
            self.make_components(project,angular_object)
            # make the navigation bar
            self.make_navigation_bar(project, angular_object)
            # make the app-routing.module.ts file
            self.make_app_routing_module(project, angular_object)
            # make the app.module.ts file
            self.make_app_modules_ts_file(project, angular_object)
            # make the config files
            self.make_angularjson_file(project)
            self.make_packagejson_file(project)
            # make the index.html files
            self.make_app_component_file(project)
            self.make_index_html_file(project)

    def parse_controller_class(self, project, angular_object):
        """
        this method will create the urls in the service class for calling the backing controller
        it will also assemble a map of other information inside the AngularObject for that DTO, so
        that we can use this stuff later and not ahve to parse this controller file again
        :param project:
        :param angular_object:
        :return:
        """
        print("Analyzing the Controller class for project : " + project.pomname)
        tabs = "\t"
        requestmappingfound = False
        requestfound = False
        currentdto = ''
        root_url = ''
        new_root_url = ''
        if (Configuration.use_gateway_server == True):
            root_url = Configuration.gateway_server_url+"/"+project.pomname
            print("ROOT_URL = " + root_url)
        else:
            root_url = Configuration.hostname + ":" + project.portnum
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
                        angular_object.rest_call_parameters[currentdto].append(self.remove_annotations_from_string(linestr))
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

    def remove_annotations_from_string(self, inputstring):
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

    def make_app_routing_module(self,project, angular_object):
        """
        this method will make the app-routing.module.ts file
        :param project:
        :param angular_object:
        :return:
        """
        tabs = "\t"
        app_routing_input = None
        app_routing_output = None
        try:
            app_routing_input = open("files/angular/app-routing.module.ts", "r")
            app_routing_output = open(
                self.root_directory + "/src/app/app-routing.module.ts",
                "w")
            for line in app_routing_input:
                linestr = str(line)
                if (linestr.find("XXX") > -1):
                    counter = 0
                    for item in angular_object.components:
                        app_routing_output.write("import { " + item + " } from './components/" + angular_object.names[counter] + "/" + angular_object.names[counter] + ".component';\n")
                        counter += 1
                elif (linestr.find("YYY") > -1):
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




    def make_components(self, project, angular_object):
        """
        this method will make all of the component files for a project
        :param project:
        :param angular_object:
        :return:
        """
        tabs = "\t"
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
                if not os.path.exists(self.root_directory + "/src/app/components/" + lowercasename):
                    os.mkdir(self.root_directory + "/src/app/components/" + lowercasename)
                output_html_file = open(
                    self.root_directory + "/src/app/components/" + lowercasename + "/" + lowercasename + ".component.html",
                    "w")
                for line in component_html_file:
                    linestr = str(line)
                    if (linestr.find("XXX") > -1):
                        output_html_file.write(linestr.replace("XXX", javaname))
                    elif (linestr.find("YYY") > -1):
                        self.add_html_header(dtoname, angular_object, output_html_file)
                    elif (linestr.find("ZZZ") > -1):
                        self.add_html_body(dtoname, angular_object, output_html_file)
                    elif (linestr.find("WWW") > -1):
                        self.add_html_form_body(dtoname, angular_object, output_html_file)
                    else:
                        output_html_file.write(linestr.replace("%",lowercasename+"list"))

                # make the .ts file

                component_ts_file = open("files/angular/component.ts", "r")
                output_ts_file = open(
                    self.root_directory + "/src/app/components/" + lowercasename + "/" + lowercasename + ".component.ts",
                    "w")
                for line in component_ts_file:
                    linestr = str(line)
                    if(linestr.find("XXX")>-1):
                        output_ts_file.write("import { " + javaname+"Service } from '../../services/" + lowercasename + ".service';\n")
                        output_ts_file.write("import { " + dtoname + " } from '../../models/" + dtoname + "';\n")
                    elif(linestr.find("YYY")>-1):
                        output_ts_file.write(tabs + "constructor( ")
                        output_ts_file.write("private " + lowercasename + "service: " + javaname+"Service")
                        output_ts_file.write(" ) { }\n")
                    elif (linestr.find("ZZZ") > -1):
                        self.initialize_ts_object(dtoname,angular_object,output_ts_file)
                        output_ts_file.write(tabs+ lowercasename + "list: " + dtoname + "[];\n")
                    elif (linestr.find("WWW") > -1):
                        output_ts_file.write(tabs + "this."+ lowercasename + "service." + angular_object.rest_call_names[dtoname][0] + "().subscribe(" + lowercasename + "list => {\n")
                        output_ts_file.write(tabs+tabs+"this."+lowercasename+"list = " + lowercasename + "list;\n")
                        output_ts_file.write(tabs + tabs + "this.loaded = true;\n")
                        output_ts_file.write(tabs +"});\n")
                    elif (linestr.find("VVV") > -1):
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
                            if (fieldtype == 'number' or fieldtype == 'date'):
                                output_ts_file.write(tabs + "this." + lowercasename + "." + name + " = null;\n")
                            else:
                                output_ts_file.write(tabs + "this." + lowercasename + "." + name + " = '';\n")
                    elif (linestr.find("QQQ") > -1):
                        output_ts_file.write(tabs + "this." + lowercasename + " = this." + lowercasename + "list[i];\n")
                        output_ts_file.write(tabs + "this.show" + javaname + "Form = true;\n")
                    elif (linestr.find("SSS") > -1):
                        output_ts_file.write(tabs + "this." + lowercasename + "service." +
                                             angular_object.rest_call_names[dtoname][
                                                 4] + "(this." + lowercasename +"list[i]." + angular_object.fieldnames[dtoname][0] + ").subscribe(response => {\n")
                        output_ts_file.write(tabs + tabs + "this.reload();\n")
                        output_ts_file.write(tabs + "});\n")
                    else:
                        output_ts_file.write(linestr.replace("%", javaname).replace("&", lowercasename))

                # make the css file

                output_css_file = open(
                    self.root_directory + "/src/app/components/" + lowercasename + "/" + lowercasename + ".component.css",
                    "w")
            except:
                print("something went wrong inside the AngularFileMaker.make_components method")
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

    def initialize_ts_object(self,dtoname, angular_object,output_ts_file):
        """
        this method will initialize the dto object that is in each component .ts file
        :param dtoname:
        :param angular_object:
        :param output_ts_file:
        :return:
        """
        tabs = "\t"
        lowercasename = dtoname.replace("DTO", "").lower()
        output_ts_file.write(tabs + lowercasename + ": " + dtoname + " = {\n")
        counter = 0
        for name in angular_object.fieldnames[dtoname]:
            fieldtype = angular_object.fieldtypes[dtoname][name]
            if(fieldtype == 'number' or fieldtype == 'date'):
                output_ts_file.write(tabs + tabs + name + ": null")
            else:
                output_ts_file.write(tabs + tabs + name + ": ''")
            counter += 1
            if(counter<len(angular_object.fieldnames[dtoname])):
                output_ts_file.write(",")
            output_ts_file.write("\n")
        output_ts_file.write(tabs+"};\n")

    def add_html_header(self,dtoname, angular_object, output_html_file):
        """

        :param dtoname:
        :param angular_object:
        :param output_html_file:
        :return:
        """
        tab3 = "\t\t\t"
        tab4 = "\t\t\t\t"
        print("making the html for dtoname = " + dtoname)
        for name in angular_object.fieldnames[dtoname]:
            output_html_file.write(tab3+"<th>\n")
            output_html_file.write(tab4+'<i class="text-size-10">'+name+'</i>\n')
            output_html_file.write(tab3 + "</th>\n")
        output_html_file.write(tab3 + "<th>\n")
        output_html_file.write(tab4 + '<i class="text-size-8">Edit Item</i>\n')
        output_html_file.write(tab3 + "</th>\n")
        output_html_file.write(tab3 + "<th>\n")
        output_html_file.write(tab4 + '<i class="text-size-8">Delete Item</i>\n')
        output_html_file.write(tab3 + "</th>\n")

    def add_html_body(self,dtoname, angular_object, output_html_file):
        """

        :param dtoname:
        :param angular_object:
        :param output_html_file:
        :return:
        """
        tab3 = "\t\t\t"
        tab4 = "\t\t\t\t"
        tab5 = "\t\t\t\t\t"
        print("making the html for dtoname = " + dtoname)
        output_html_file.write(tab3 + '<td [hidden]="alwaysHidden">{{ i + 1 }}</td>\n')
        for name in angular_object.fieldnames[dtoname]:
            output_html_file.write(tab3+"<td>\n")
            output_html_file.write(tab4+'<i class="text-size-10">{{dto.'+name+'}}</i>\n')
            output_html_file.write(tab3 + "</td>\n")
        output_html_file.write(tab3 + "<td>\n")
        output_html_file.write(tab4 + '<button class="btn-edit" type="submit" (click)="editItem(i)">\n')
        output_html_file.write(tab5 + '<span class="iconspan fa fa-edit"></span>\n')
        output_html_file.write(tab4 + '</button>\n')
        output_html_file.write(tab3 + "</td>\n")
        output_html_file.write(tab3 + "<td>\n")
        output_html_file.write(tab4 + '<button class="btn-edit" type="submit" (click)="deleteItem(i)">\n')
        output_html_file.write(tab5 + '<span class="iconspan fa fa-trash"></span>\n')
        output_html_file.write(tab4 + '</button>\n')
        output_html_file.write(tab3 + "</td>\n")

    def add_html_form_body(self,dtoname, angular_object, output_html_file):
        """

        :param dtoname:
        :param angular_object:
        :param output_html_file:
        :return:
        """
        tab1 = "\t\t\t"
        tab2 = "\t\t\t\t"
        lowercasename = dtoname.replace("DTO", "").lower()
        print("making the html form for dtoname = " + dtoname)
        counter = 0
        for name in angular_object.fieldnames[dtoname]:
            if (counter > 0):
                output_html_file.write(tab1+'<div class="form-group">\n')
                output_html_file.write(tab2 + '<label>'+name+'</label>\n')
                type = "text"
                fieldtype = angular_object.fieldtypes[dtoname][name]
                if (fieldtype == 'number'):
                    type = "number"
                elif(fieldtype == 'date'):
                    type = "date"
                output_html_file.write(tab2+'<input type="'+type+'" class="form-control" [(ngModel)]="'+lowercasename+'.'+name+'" name="'+name+'">\n')
                output_html_file.write(tab1 + "</div>\n")
            counter += 1
    """
    
    <th>
              <i class="text-size-10">ServTypeId</i>
            </th>
            <th>
              <i class="text-size-10">ServTypeCde</i>
            </th>
            <th>
              <i class="text-size-10">ServTypeDesc</i>
            </th>
            <th>
              <i class="text-size-10">Actv</i>
            </th>
            
            <td>
              <i class="text-size-10">{{dto.servtypeid}}</i>
            </td>
            <td>
              <i class="text-size-10">{{dto.servtypecde}}</i>
            </td>
            <td>
              <i class="text-size-10">{{dto.servtypedesc}}</i>
            </td>
            <td>
              <i class="text-size-10">{{dto.actv}}</i>
            </td>
    """
    def make_services(self, project, angular_object):
        """
        this method will make all of the component files for a project
        :param project:
        :param angular_object:
        :return:
        """
        tabs = "\t"
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
                    self.root_directory + "/src/app/services/" + lowercasename + ".service.ts",
                    "w")
                for line in component_service_file:
                    linestr = str(line)
                    if (linestr.find("XXX") > -1):
                        output_service_file.write("import { " + dtoname + " } from '../models/" + dtoname + "';\n")
                    elif(linestr.find("YYY")>-1):
                        counter = range(len(angular_object.rest_call_names[dtoname]))
                        for x in counter:
                            self.make_rest_call_code_block(dtoname, angular_object.rest_call_names[dtoname][x], angular_object.rest_call_types[dtoname][x],angular_object.rest_call_parameters[dtoname][x],output_service_file)
                    elif (linestr.find("ZZZ") > -1):
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


    def make_rest_call_code_block(self, dtoname, name, type, paramlist, output_service_file):
        """
        this method will make the actual code in the service class that makes the REST call
        :param dtoname
        :param name:
        :param type:
        :param paramlist:
        :param output_service_file:
        :return:
        """
        tabs = "\t"
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



    def make_angularjson_file(self, project):
        """
        this method generates the angular.json file
        :param project:
        :return:
        """
        tabs = "\t"
        angularjsonfile = None
        altered_aj_file = None
        try:
            angularjsonfile = open("files/angular/angular.json","r")
            altered_aj_file = open(self.root_directory+"/angular.json","w")
            stylesfound = False
            scriptsfound = False
            for line in angularjsonfile:
                linestr = str(line)
                if(stylesfound == False and linestr.find('"src/styles.css"')>-1):
                    altered_aj_file.write(linestr.replace('"src/styles.css"','"src/styles.css",'))
                    altered_aj_file.write(tabs+tabs+tabs+'"./node_modules/font-awesome/css/font-awesome.css",\n')
                    altered_aj_file.write(tabs + tabs + tabs +'"./node_modules/bootstrap/dist/css/bootstrap.css"\n')
                    stylesfound = True
                elif(scriptsfound == False and linestr.find('"scripts": []')>-1):
                    altered_aj_file.write(linestr.replace('"scripts": []', '"scripts": ['))
                    altered_aj_file.write(tabs + tabs + tabs +'"./node_modules/jquery/dist/jquery.js",\n')
                    altered_aj_file.write(tabs + tabs + tabs +'"./node_modules/popper.js/dist/umd/popper.js",\n')
                    altered_aj_file.write(tabs + tabs + tabs +'"./node_modules/bootstrap/dist/js/bootstrap.js"\n')
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

    def make_packagejson_file(self, project):
        """
        this method generates the package.json file
        :param project:
        :return:
        """
        tabs = "\t"
        packagejsonfile = None
        altered_pj_file = None
        try:
            packagejsonfile = open("files/angular/package.json","r")
            altered_pj_file = open(self.root_directory+"/package.json","w")
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

    def make_folders(self, project):
        """
        this program makes the src folder and app subfolder and components,models,guards,services subfolders
        :param project:
        :return:
        """
        if not os.path.exists(self.root_directory+"/src"):
            os.mkdir(self.root_directory+"/src")
        if not os.path.exists(self.root_directory + "/src/app"):
            os.mkdir(self.root_directory + "/src/app")
        if not os.path.exists(self.root_directory + "/src/app/components"):
            os.mkdir(self.root_directory + "/src/app/components")
        if not os.path.exists(self.root_directory + "/src/app/models"):
            os.mkdir(self.root_directory + "/src/app/models")
        if not os.path.exists(self.root_directory + "/src/app/guards"):
            os.mkdir(self.root_directory + "/src/app/guards")
        if not os.path.exists(self.root_directory + "/src/app/services"):
            os.mkdir(self.root_directory + "/src/app/services")

    def make_app_modules_ts_file(self, project, angular_object):
        """
        this method will make the app.module.ts file
        :param project:
        :param angular_object:
        :return:
        """
        tabs = "\t"
        old_app_module_ts_file = None
        new_app_module_ts_file = None
        try:
            old_app_module_ts_file = open("files/angular/app.module.ts","r")
            new_app_module_ts_file = open(self.root_directory+"/src/app/app.module.ts","w")
            for line in old_app_module_ts_file:
                linestr = str(line)
                if (linestr.find("XXX") > -1):
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
                elif(linestr.find("YYY") > -1):
                    new_app_module_ts_file.write(tabs+"AppComponent,\n")
                    new_app_module_ts_file.write(tabs + "NavbarComponent,\n")
                    counter = 0
                    for item in angular_object.components:
                        new_app_module_ts_file.write(tabs+tabs+item)
                        counter += 1
                        if (counter < len(angular_object.components)):
                            new_app_module_ts_file.write(",")
                        new_app_module_ts_file.write("\n")
                elif(linestr.find("ZZZ") > -1):
                    new_app_module_ts_file.write(tabs + "BrowserModule,\n")
                    new_app_module_ts_file.write(tabs + "AppRoutingModule,\n")
                    new_app_module_ts_file.write(tabs + "HttpClientModule,\n")
                    new_app_module_ts_file.write(tabs + "FormsModule\n")
                    #new_app_module_ts_file.write(tabs + "// modules added here\n")
                    self.figureout_module_additions(project, new_app_module_ts_file)
                elif(linestr.find("WWW") > -1):
                    new_app_module_ts_file.write(linestr.replace("WWW",",".join(angular_object.services)))
                else:
                    new_app_module_ts_file.write(linestr)
        except:
            print("something went wrong inside the AngularFileMaker.make_packagejson_file method")
        finally:
            if(old_app_module_ts_file is not None):
                old_app_module_ts_file.close()
            if (new_app_module_ts_file is not None):
                new_app_module_ts_file

    def figureout_imports(self, project, new_app_module_ts_file):
        """

        :param project:
        :param new_app_module_ts_file:
        :return:
        """
        new_app_module_ts_file.write("import { NavbarComponent } from './components/navbar/navbar.component';\n")

    def figureout_module_additions(self, project, new_app_module_ts_file):
        """

        :param project:
        :param new_app_module_ts_file:
        :return:
        """
        None

    def figureout_service_additions(self, project, new_app_module_ts_file):
        """

        :param project:
        :param new_app_module_ts_file:
        :return:
        """
        None

    def make_index_html_file(self, project):
        """
        this method will make the app.module.ts file
        :param project:
        :return:
        """
        tabs = "\t"
        old_index_file = None
        new_index_file = None
        try:
            old_index_file = open("files/angular/index.html","r")
            new_index_file = open(self.root_directory+"/src/index.html","w")
            for line in old_index_file:
                linestr = str(line)
                if (linestr.find("XXX") > -1):
                    new_index_file.write(linestr.replace("XXX",project.pomname))
                else:
                    new_index_file.write(linestr)
        except:
            print("something went wrong inside the AngularFileMaker.make_index_html_file method")
        finally:
            if(old_index_file is not None):
                old_index_file.close()
            if (new_index_file is not None):
                new_index_file

    def make_angular_classes(self, project, angular_obj):
        """
        this method will make the DTO objects for a given project in Angular
        :param project:
        :return:
        """
        tabs = "\t"
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
            outputfile = open(self.root_directory+"/src/app/models/"+outputfilename+".ts","w")
            outputfile.write("export interface " + outputfilename + "{\n")

            angular_obj.dto_names.append(outputfilename)
            angular_obj.fieldnames[outputfilename] = []
            angular_obj.fieldtypes[outputfilename] = {}
            inputfile.close()
            inputfile = open(filename,"r")
            for line in inputfile:
                linestr = str(line)
                if (linestr.find("private") > -1):
                    fieldarray = linestr.split(" ")
                    key = fieldarray[2].replace(";","").rstrip()
                    print("field name " + key)
                    angular_obj.fieldnames[outputfilename].append(key)
                    if(fieldarray[1].lower() == "int" or fieldarray[1].lower() == "integer" or fieldarray[1].lower() == "long" or fieldarray[1].lower() == "float" or fieldarray[1].lower() == "double" or fieldarray[1].lower() == "biginteger" or fieldarray[1].lower() == "bigdecimal" ):
                        angular_obj.fieldtypes[outputfilename][key] = "number"
                    elif(fieldarray[1].lower() == "date" or fieldarray[1].lower() == "datetime" or fieldarray[1].lower() == "time"):
                        angular_obj.fieldtypes[outputfilename][key] = "date"
                    else:
                        angular_obj.fieldtypes[outputfilename][key] = fieldarray[1].lower()
            counter = 0
            for name in angular_obj.fieldnames[outputfilename]:
                outputfile.write(tabs + name + "?: " + angular_obj.fieldtypes[outputfilename][name])
                counter +=1
                if(counter<len(angular_obj.fieldnames[outputfilename])):
                    outputfile.write(",")
                outputfile.write("\n")
            outputfile.write("}")
            inputfile.close()
            outputfile.close()
        inputfile = open("files/angular/response_message.ts", "r")
        outputfile = open(self.root_directory + "/src/app/models/ResponseMessage.ts", "w")
        for line in inputfile:
            linestr = str(line)
            outputfile.write(linestr)
        inputfile.close()
        outputfile.close()

    def make_navigation_bar(self, project, angular_project):
        """
        this method will make a navigation bar component
        :param project:
        :return:
        """
        tabs = "\t"
        if not os.path.exists(self.root_directory + "/src/app/components/navbar"):
            os.mkdir(self.root_directory + "/src/app/components/navbar")
        inputfile = open("files/angular/navbar.component.html", "r")
        outputfile = open(self.root_directory + "/src/app/components/navbar/navbar.component.html", "w")
        for line in inputfile:
            linestr = str(line)
            if(linestr.find("XXX")>-1):
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
        outputfile = open(self.root_directory + "/src/app/components/navbar/navbar.component.ts", "w")
        for line in inputfile:
            linestr = str(line)
            outputfile.write(linestr)
        inputfile.close()
        outputfile.close()
        outputfile = open(self.root_directory + "/src/app/components/navbar/navbar.component.css", "w")
        outputfile.close()

    def make_app_component_file(self, project):
        """
        this method makes the app.component.html file
        :param project:
        :return:
        """
        tabs = "\t"
        outputfile = open(self.root_directory + "/src/app/app.component.html", "w")
        outputfile.write('<app-navbar></app-navbar>\n')
        outputfile.write(tabs + '<div class="container">\n')
        outputfile.write(tabs + '<router-outlet></router-outlet>\n')
        outputfile.write(tabs + '</div>')
        outputfile.close()

    """    
            if(project.is_mid_level == True):
                angular_object.components.append(project.camelcasejavaname + "Component")
                angular_object.selectors.append("app-" + project.lowercasename)
                angular_object.routes.append("/" + project.lowercasename)
                component_html_file = None
                output_html_file = None
                component_ts_file = None
                output_ts_file = None
                output_css_file = None
                try:
                    component_html_file = open("files/angular/component.html", "r")
                    if not os.path.exists(self.root_directory + "/src/app/components/" + project.lowercasename):
                        os.mkdir(self.root_directory + "/src/app/components/" + project.lowercasename)
                    output_html_file = open(
                        self.root_directory + "/src/app/components/" + project.lowercasename + "/" + project.lowercasename + ".component.html",
                        "w")
                    for line in component_html_file:
                        linestr = str(line)
                        if (linestr.find("XXX") > -1):
                            output_html_file.write(linestr.replace("XXX", project.lowercasename))
                        else:
                            output_html_file.write(linestr)
                    component_ts_file = open("files/angular/component.ts", "r")
                    output_ts_file = open(
                        self.root_directory + "/src/app/components/" + project.lowercasename + "/" + project.lowercasename + ".component.ts",
                        "w")
                    for line in component_ts_file:
                        linestr = str(line)
                        if(linestr.find("XXX")>-1):
                            output_ts_file.write("import { " + project.camelcasejavaname+"Service } from '../../services/" + project.lowercasename + ".service';\n")
                            for item in angular_object.dto_names:
                                output_ts_file.write("import { " + item + " } from '../../models/" + item + "';\n")
                        elif(linestr.find("YYY")>-1):
                            if (len(angular_object.services) > 0):
                                output_ts_file.write(tabs + tabs + "constructor( ")
                                count = 0
                                for item in angular_object.services:
                                    output_ts_file.write("private " + item.lower() + ": " + item)
                                    count += 1
                                    if (count < len(angular_object.services)):
                                        output_ts_file.write(", ")
                                output_ts_file.write(" ) { }\n")
                            else:
                                output_ts_file.write(tabs+tabs+"constructor() {}\n")
                        else:
                            output_ts_file.write(linestr.replace("%", project.camelcasejavaname).replace("&", project.lowercasename))
                    output_css_file = open(
                        self.root_directory + "/src/app/components/" + project.lowercasename + "/" + project.lowercasename + ".component.css",
                        "w")
                except:
                    print("something went wrong inside the AngularFileMaker.make_components method")
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
            else:
                for name in project.tablenames:
                    tabledata = project.tabledata[name]
                    angular_object.components.append(tabledata.camelcasejavaname+"Component")
                    angular_object.selectors.append("app-"+tabledata.lowercasename)
                    angular_object.routes.append("/" + tabledata.lowercasename)
                    component_html_file = None
                    output_html_file = None
                    component_ts_file = None
                    output_ts_file = None
                    output_css_file = None
                    try:
                        component_html_file = open("files/angular/component.html", "r")
                        if not os.path.exists(self.root_directory + "/src/app/components/" + tabledata.lowercasename):
                            os.mkdir(self.root_directory + "/src/app/components/" + tabledata.lowercasename)
                        output_html_file = open(self.root_directory + "/src/app/components/" + tabledata.lowercasename + "/" + tabledata.lowercasename + ".component.html", "w")
                        for line in component_html_file:
                            linestr = str(line)
                            if (linestr.find("XXX") > -1):
                                output_html_file.write(linestr.replace("XXX",tabledata.lowercasename))
                            else:
                                output_html_file.write(linestr)
                        component_ts_file = open("files/angular/component.ts", "r")
                        output_ts_file = open(self.root_directory + "/src/app/components/" + tabledata.lowercasename + "/" + tabledata.lowercasename + ".component.ts", "w")
                        for line in component_ts_file:
                            linestr = str(line)
                            if (linestr.find("XXX") > -1):
                                output_ts_file.write(
                                    "import { " + tabledata.camelcasejavaname + "Service } from '../../services/" + tabledata.lowercasename + ".service';\n")
                                for item in angular_object.dto_names:
                                    output_ts_file.write(
                                    "import { " + item + " } from '../../models/" + item + "';\n")
                            elif (linestr.find("YYY") > -1):
                                if (len(angular_object.services) > 0):
                                    output_ts_file.write(tabs + tabs + "constructor( ")
                                    count = 0
                                    for item in angular_object.services:
                                        output_ts_file.write("private " + item.lower() + ": " + item)
                                        count += 1
                                        if(count<len(angular_object.services)):
                                            output_ts_file.write(", ")
                                    output_ts_file.write(" ) { }\n")
                                else:
                                    output_ts_file.write(tabs + tabs + "constructor() {}\n")
                            else:
                                output_ts_file.write(linestr.replace("%",tabledata.camelcasejavaname).replace("&",tabledata.lowercasename))
                        output_css_file = open(self.root_directory + "/src/app/components/" + tabledata.lowercasename + "/" + tabledata.lowercasename + ".component.css", "w")

                    except:
                        print("something went wrong inside the AngularFileMaker.make_components method")
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
            """

    """
            if (project.is_mid_level == True):
                angular_object.names.append(project.lowercasename)
                angular_object.services.append(project.camelcasejavaname + "Service")
                component_service_file = None
                output_service_file = None
                try:
                    component_service_file = open("files/angular/service.ts", "r")
                    output_service_file = open(
                        self.root_directory + "/src/app/services/" + project.lowercasename + ".service.ts",
                        "w")
                    for line in component_service_file:
                        linestr = str(line)
                        if (linestr.find("XXX") > -1):
                            for item in angular_object.dto_names:
                                output_service_file.write("import { " + item + " } from '../models/" + item + "';\n")
                        else:
                            output_service_file.write(linestr.replace("%", project.camelcasejavaname).replace("&", project.lowercasename))
                except:
                    print("something went wrong inside the AngularFileMaker.make_services method")
                finally:
                    if (component_service_file is not None):
                        component_service_file.close()
                    if (output_service_file is not None):
                        output_service_file.close()
            else:
                for name in project.tablenames:
                    tabledata = project.tabledata[name]
                    angular_object.names.append(tabledata.lowercasename)
                    angular_object.services.append(tabledata.camelcasejavaname + "Service")
                    component_service_file = None
                    output_service_file = None
                    try:
                        component_service_file = open("files/angular/service.ts", "r")
                        output_service_file = open(
                            self.root_directory + "/src/app/services/" + tabledata.lowercasename + ".service.ts",
                            "w")
                        for line in component_service_file:
                            linestr = str(line)
                            if (linestr.find("XXX") > -1):
                                for item in angular_object.dto_names:
                                    output_service_file.write(
                                        "import { " + item + " } from '../models/" + item + "';\n")
                            else:
                                output_service_file.write(linestr.replace("%", tabledata.camelcasejavaname).replace("&", tabledata.lowercasename))
                    except:
                        print("something went wrong inside the AngularFileMaker.make_services method")
                    finally:
                        if (component_service_file is not None):
                            component_service_file.close()
                        if (output_service_file is not None):
                            output_service_file.close()
            """