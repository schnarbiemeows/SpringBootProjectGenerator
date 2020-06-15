from configuration.Constants import *
from configuration.Configuration import *

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
        tabs = "\t"
        filename = project.topmainpackage + "/" + project.camelcasejavaname + "Application.java"
        main_file = open("files/main.txt", "r")
        resources_file = open(filename, "w")
        resources_file.write("package " + project.rootpackage + ";\n\n")
        for line in main_file:
            linestr = str(line)
            if (linestr.find("YYY") > -1):
                if(Configuration.use_naming_server == True or Configuration.use_docker == True):
                    resources_file.write(Constants.import_feign+"\n")
                    resources_file.write(Constants.import_dc + "\n")
                    if(Configuration.use_distributed_tracing == True):
                        resources_file.write(Constants.import_bean + "\n")
                        resources_file.write(Constants.import_sampler + "\n")
            elif (linestr.find("ZZZ") > -1):
                if (Configuration.use_distributed_tracing == True):
                    resources_file.write(tabs+"@Bean\n")
                    resources_file.write(tabs+"public Sampler defaultSampler() {\n")
                    resources_file.write(tabs+tabs+"return Sampler.ALWAYS_SAMPLE;\n")
                    resources_file.write(tabs +"}\n")
            elif (linestr.find("XXX") > -1):
                if (Configuration.use_naming_server == True or Configuration.use_docker == True):
                    resources_file.write(Constants.ann_feign.replace("XXX", project.rootpackage)+"\n")
                    resources_file.write(Constants.ann_dc + "\n")
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

    def create_proxy_class(self, currentprojectdata, projectnames, projectdata):
        """
        this method will create the proxy interfaces to the other projects' REST controllers
        :param table:
        :return:
        """
        if(Configuration.naming_server_proxy_mode == 2):
            for projectname in projectnames:
                if(projectname != currentprojectdata.pomname):
                    otherproject = projectdata[projectname]
                    filename = currentprojectdata.topmainpackage + "/" + Constants.path_proxy_services + "/" + otherproject.camelcasejavaname + "ServiceProxy.java"
                    resources_file = open(filename, "w")
                    resources_file.write("package " + currentprojectdata.rootpackage + "." + Constants.pckg_proxy_services + ";\n\n")
                    proxy_file = open("files/specific_proxy.txt", "r")
                    for line in proxy_file:
                        linestr = str(line)
                        if(linestr.find("YYY"))>-1:
                            for tablename in otherproject.tablenames:
                                proxytable = otherproject.tabledata[tablename]
                                resources_file.write("import "+currentprojectdata.rootpackage + "." + Constants.pckg_proxy_dtos+"."+proxytable.dtoname+";\n")
                        elif (linestr.find("ZZZ")) > -1:
                            None
                        elif(linestr.find("WWW"))>-1:
                            if(Configuration.use_gateway_server == True):
                                resources_file.write(linestr.replace("WWW",'@FeignClient(name="zuul-api-gateway-server")'))
                            elif(Configuration.use_docker == True):
                                resources_file.write(linestr.replace("WWW", '@FeignClient(name = "'+otherproject.pomname+'", url = "${CURRENCY_EXCHANGE_SERVICE_HOST:http://localhost}:'+str(otherproject.portnum)+'")'))
                            else:
                                resources_file.write(linestr.replace("WWW", otherproject.pomname))
                        elif (linestr.find("XXX")) > -1:
                            if (Configuration.use_naming_server == True):
                                resources_file.write(
                                    linestr.replace("XXX", '@RibbonClient(name="' + otherproject.pomname + '")'))
                        elif (linestr.find("WW1")) > -1:
                            if (Configuration.use_naming_server == True or Configuration.use_gateway_server == True or Configuration.use_docker == True):
                                resources_file.write("import org.springframework.cloud.openfeign.FeignClient;\n")
                        elif (linestr.find("XX1")) > -1:
                            if (Configuration.use_naming_server == True):
                                resources_file.write("import org.springframework.cloud.netflix.ribbon.RibbonClient;\n")
                        else:
                            resources_file.write(linestr.replace("^", Configuration.author).replace("%", otherproject.camelcasejavaname))
                    resources_file.close()
                    proxy_file.close()
        else:
            filename = currentprojectdata.topmainpackage + "/" + Constants.path_proxy_services + "/" + "GenericServiceProxy.java"
            resources_file = open(filename, "w")
            resources_file.write("package " + currentprojectdata.rootpackage + "." + Constants.pckg_proxy_services + ";\n\n")
            proxy_file = open("files/generic_proxy.txt", "r")
            for line in proxy_file:
                linestr = str(line)
                resources_file.write(linestr.replace("^",Configuration.author))
            resources_file.close()
            proxy_file.close()

    def create_proxy_classes_for_mid_levels(self, mid_lvl_proj, crud_proj_names, crud_proj_data):
        """
        this method will create proxy interfaces for the mid-level project to each of the tables that the user wants
        proxies to
        :param mid_lvl_proj:
        :return:
        """
        mid_lvl_map = {}
        for project_name in mid_lvl_proj.tablenames:
            mid_lvl_map[project_name] = "YES"
        for projectname in crud_proj_names:
            currentproject = crud_proj_data[projectname]
            if currentproject.pomname in mid_lvl_map:
                filename = mid_lvl_proj.topmainpackage + "/" + Constants.path_proxy_services + "/" + currentproject.camelcasejavaname + "ServiceProxy.java"
                resources_file = open(filename, "w")
                resources_file.write("package " + mid_lvl_proj.rootpackage + "." + Constants.pckg_proxy_services + ";\n\n")
                proxy_file = open("files/specific_proxy.txt", "r")
                for line in proxy_file:
                    linestr = str(line)
                    if(linestr.find("YYY")) > -1:
                        None
                    elif(linestr.find("ZZZ")) > -1:
                        self.create_rest_calls_for_proxy(currentproject,resources_file)
                    elif (linestr.find("WWW")) > -1:
                        if (Configuration.use_gateway_server == True):
                            resources_file.write(linestr.replace("WWW", "zuul-api-gateway-server"))
                        elif (Configuration.use_docker == True):
                            service_name = currentproject.pomname.upper().replace("-","_") + "_SERVICE_HOST"
                            mid_lvl_proj.service_config.append(service_name)
                            text = '@FeignClient(name = "' + currentproject.pomname + '", url = "${' + service_name + ':http://XXX}:' + str(currentproject.portnum) + '")'
                            resources_file.write(linestr.replace("WWW",text.replace("XXX", "localhost")))
                        else:
                            resources_file.write(linestr.replace("WWW", currentproject.pomname))
                    elif(linestr.find("XXX")) > -1:
                        if (Configuration.use_naming_server == True):
                            resources_file.write(linestr.replace("XXX", '@RibbonClient(name="'+currentproject.pomname+'")'))
                    elif (linestr.find("WW1")) > -1:
                        if (Configuration.use_naming_server == True or Configuration.use_gateway_server == True or Configuration.use_docker == True):
                            resources_file.write("import org.springframework.cloud.openfeign.FeignClient;\n")
                    elif (linestr.find("XX1")) > -1:
                        if (Configuration.use_naming_server == True):
                            resources_file.write("import org.springframework.cloud.netflix.ribbon.RibbonClient;\n")
                    else:
                        resources_file.write(linestr.replace("^", Configuration.author).replace("%",currentproject.camelcasejavaname).replace(
                            "&", mid_lvl_proj.rootpackage))
                resources_file.close()
                proxy_file.close()

    def create_proxy_dtos(self, destinationroot, currentprojectdata, projectnames, projectdata):
        """
        this method will create the DTOs needed for the proxies
        :param table:
        :return:
        """
        if(Configuration.naming_server_proxy_mode == 2):
            for projectname in projectnames:
                otherprojectdata = projectdata[projectname]
                if(currentprojectdata.pomname != otherprojectdata.pomname):
                    for tablename in otherprojectdata.tablenames:
                        proxytable = otherprojectdata.tabledata[tablename]
                        filename = currentprojectdata.topmainpackage + "/" + Constants.path_proxy_dtos + "/" + proxytable.dtoname + ".java"
                        resources_file = open(filename, "w")
                        resources_file.write("package " + currentprojectdata.rootpackage + "." + Constants.pckg_proxy_dtos + ";\n\n")
                        resources_file.write("import java.math.*;\n")
                        resources_file.write("import java.sql.*;\n")
                        resources_file.write("import java.util.*;\n")
                        source_file = open(destinationroot + "/" + otherprojectdata.pomname + "/" + otherprojectdata.pomname + "/src/main/java/" + Configuration.groupid.replace(".","/") + "/" + otherprojectdata.lowercasename + "/dtos/" + proxytable.dtoname + ".java", "r")
                        count = 0
                        proxytablename = proxytable.camelcasejavaname+";"
                        for line in source_file:
                            if count > 0:
                                linestr = str(line)
                                if (linestr.find(proxytablename))>-1:
                                    resources_file.write(
                                        "import " + currentprojectdata.rootpackage + "." + Constants.pckg_proxy_pojos + "." + proxytable.camelcasejavaname + ";\n")
                                else:
                                    resources_file.write(linestr)
                            else:
                                count += 1
                        resources_file.close()
                        source_file.close()
        else:
            None

    def create_proxy_dtos_for_mid_lvl(self, destinationroot, mid_lvl_proj, crud_proj_names, crud_proj_data):
        """
        this method will create the DTOs needed for the proxies for the mid-level projects
        :param destinationroot:
        :param mid_lvl_proj:
        :param crud_proj_names:
        :param crud_proj_data:
        :return:
        """
        mid_lvl_map = {}
        for tablename in mid_lvl_proj.tablenames:
            mid_lvl_map[tablename] = "YES"
        for projectname in crud_proj_names:
            currentproject = crud_proj_data[projectname]
            if currentproject.pomname in mid_lvl_map:
                for tablename in currentproject.tablenames:
                    currenttable = currentproject.tabledata[tablename]
                    filename = mid_lvl_proj.topmainpackage + "/" + Constants.path_proxy_dtos + "/" + currenttable.dtoname + ".java"
                    resources_file = open(filename, "w")
                    resources_file.write("package " + mid_lvl_proj.rootpackage + "." + Constants.pckg_proxy_dtos + ";\n")
                    source_file = open(destinationroot + "/" + currentproject.pomname + "/" + currentproject.pomname + "/src/main/java/" + Configuration.groupid.replace(".","/") + "/" + currentproject.lowercasename + "/dtos/" + currenttable.dtoname + ".java", "r")
                    count = 0
                    proxytablename = currenttable.camelcasejavaname+";"
                    for line in source_file:
                        if count > 0:
                            linestr = str(line)
                            if (linestr.find(proxytablename))>-1:
                                resources_file.write(
                                    "import " + mid_lvl_proj.rootpackage + "." + Constants.pckg_proxy_pojos + "." + currenttable.camelcasejavaname + ";\n")
                            else:
                                resources_file.write(linestr)
                        else:
                            count += 1
                    resources_file.close()
                    source_file.close()

    def create_proxy_pojos(self, destinationroot, currentprojectdata, projectnames, projectdata):
        """
        this method will create the DTOs needed for the proxies
        :param table:
        :return:
        """
        if(Configuration.naming_server_proxy_mode == 2):
            for projectname in projectnames:
                otherprojectdata = projectdata[projectname]
                if(currentprojectdata.pomname != otherprojectdata.pomname):
                    for tablename in otherprojectdata.tablenames:
                        proxytable = otherprojectdata.tabledata[tablename]
                        filename = currentprojectdata.topmainpackage + "/" + Constants.path_proxy_pojos + "/" + proxytable.camelcasejavaname + ".java"
                        resources_file = open(filename, "w")
                        resources_file.write("package " + currentprojectdata.rootpackage + "." + Constants.pckg_proxy_pojos + ";\n\n")
                        resources_file.write("import java.math.*;\n")
                        resources_file.write("import java.sql.*;\n")
                        resources_file.write("import java.util.*;\n")
                        source_file = open(destinationroot + "/" + otherprojectdata.pomname + "/" + otherprojectdata.pomname + "/src/main/java/" + Configuration.groupid.replace(".","/") + "/" + otherprojectdata.lowercasename + "/pojos/" + proxytable.camelcasejavaname + ".java", "r")
                        count = 0
                        proxytablename = proxytable.dtoname+";"
                        for line in source_file:
                            if count > 0 :
                                linestr = str(line)
                                if (linestr.find(proxytablename))>-1:
                                    resources_file.write("import " + currentprojectdata.rootpackage + "." + Constants.pckg_proxy_dtos + "." + proxytable.dtoname +";\n")
                                else:
                                    resources_file.write(linestr)
                            else:
                                count += 1
                        resources_file.close()
                        source_file.close()
        else:
            None

    def create_proxy_pojos_for_mid_lvl(self, destinationroot, mid_lvl_proj, crud_proj_names, crud_proj_data):
        """
        this method will create the DTOs needed for the proxies for the mid-level projects
        :param destinationroot:
        :param mid_lvl_proj:
        :param crud_proj_names:
        :param crud_proj_data:
        :return:
        """
        mid_lvl_map = {}
        for tablename in mid_lvl_proj.tablenames:
            mid_lvl_map[tablename] = "YES"
        for projectname in crud_proj_names:
            currentproject = crud_proj_data[projectname]
            if currentproject.pomname in mid_lvl_map:
                for tablename in currentproject.tablenames:
                    currenttable = currentproject.tabledata[tablename]
                    filename = mid_lvl_proj.topmainpackage + "/" + Constants.path_proxy_pojos + "/" + currenttable.camelcasejavaname + ".java"
                    resources_file = open(filename, "w")
                    resources_file.write("package " + mid_lvl_proj.rootpackage + "." + Constants.pckg_proxy_pojos + ";\n")
                    source_file = open(destinationroot + "/" + currentproject.pomname + "/" + currentproject.pomname + "/src/main/java/" + Configuration.groupid.replace(".","/") + "/" + currentproject.lowercasename + "/pojos/" + currenttable.camelcasejavaname + ".java", "r")
                    count = 0
                    proxytablename = currenttable.dtoname+";"
                    for line in source_file:
                        if count > 0:
                            linestr = str(line)
                            if (linestr.find(proxytablename))>-1:
                                resources_file.write(
                                    "import " + mid_lvl_proj.rootpackage + "." + Constants.pckg_proxy_dtos + "." + currenttable.dtoname + ";\n")
                            else:
                                resources_file.write(linestr)
                        else:
                            count += 1
                    resources_file.close()
                    source_file.close()
        else:
            None

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
                resources_file.write(linestr.replace("$", table.rootpackage).replace("%", table.camelcasejavaname).replace("&", table.lowercasename).replace("^",Configuration.author))
        resources_file.close()
        business_file.close()

    def create_business_class_for_mid_lvl(self, mid_lvl_proj, crud_proj_names, crud_proj_data):
        """
        this method will create a business class for the mid-level projects
        :param mid_lvl_proj:
        :return:
        """
        # create the file and open
        filename = mid_lvl_proj.topmainpackage + "/" + Constants.pckg_bus + "/" + mid_lvl_proj.camelcasejavaname + "Business.java"
        resources_file = open(filename, "w")
        business_file = open("files/business_mid_lvl.txt")
        resources_file.write("package " + mid_lvl_proj.rootpackage + "." + Constants.pckg_bus + ";\n\n")
        for line in business_file:
            linestr = str(line)
            if (linestr.find("XXX")) > -1:
                self.create_business_service_proxy_calls(mid_lvl_proj, crud_proj_names, crud_proj_data,resources_file)
            else:
                resources_file.write(linestr.replace("%", mid_lvl_proj.camelcasejavaname).replace("&", mid_lvl_proj.lowercasename).replace("^", Configuration.author).replace("$",mid_lvl_proj.rootpackage))
        resources_file.close()
        business_file.close()


    def create_business_service_proxy_calls(self, mid_lvl_proj, crud_proj_names, crud_proj_data, resources_file):
        """

        :param mid_lvl_proj:
        :param crud_proj_names:
        :param crud_proj_data:
        :param resources_file:
        :return:
        """
        tabs = "\t"
        mid_lvl_map = {}
        for project_name in mid_lvl_proj.tablenames:
            mid_lvl_map[project_name] = "YES"
        for projectname in crud_proj_names:
            currentproject = crud_proj_data[projectname]
            if currentproject.pomname in mid_lvl_map:
                filename = mid_lvl_proj.topmainpackage + "/" + Constants.path_proxy_services + "/" + currentproject.camelcasejavaname + "ServiceProxy.java"
                resources_file.write(Constants.doc_proxy)
                resources_file.write(tabs+Constants.ann_autowired+"\n")
                service_name = currentproject.lowercasename+"serviceproxy"
                resources_file.write(tabs+currentproject.camelcasejavaname+"ServiceProxy "+service_name+" ;\n\n")
                source_file = open(filename, "r")
                for line in source_file:
                    linestr = str(line)
                    if(linestr.find("public ResponseEntity<Object>")) > -1:
                        method_name = self.remove_datatypes_from_string(linestr)
                        resources_file.write(Constants.doc_proxy)
                        resources_file.write(self.remove_annotations_from_string(linestr).replace(";","{")+"\n")
                        resources_file.write(tabs+tabs+"return "+service_name+"."+method_name+";\n"+tabs+"}\n\n")
                source_file.close()

    def create_health_check_controller(self, project):
        """
        this method will create a health check controller for the project
        :param project:
        :return:
        """
        # create the file and open
        filename = project.topmainpackage + "/" + Constants.pckg_contr + "/HealthCheckController.java"
        resources_file = open(filename, "w")
        controller_file = open("files/health_check.txt")
        resources_file.write("package " + project.rootpackage + "." + Constants.pckg_contr + ";\n\n")
        for line in controller_file:
            linestr = str(line)
            resources_file.write(linestr)
        resources_file.close()
        controller_file.close()

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
        controller_file = open("files/controller.txt")
        resources_file.write("package " + table.rootpackage + "." + Constants.pckg_contr + ";\n\n")
        for line in controller_file:
            linestr = str(line)
            resources_file.write(linestr.replace("$", table.rootpackage).replace("%", table.camelcasejavaname).replace("&", table.lowercasename).replace("^",Configuration.author))
        resources_file.close()
        controller_file.close()

    def create_controller_class_for_mid_lvl(self, mid_lvl_proj, crud_proj_names, crud_proj_data):
        """
        this method will create the RestController for the mid-lvl projects
        :param mid_lvl_proj:
        :return:
        """
        # create the file and open
        filename = mid_lvl_proj.topmainpackage + "/" + Constants.pckg_contr + "/" + mid_lvl_proj.camelcasejavaname + "Controller.java"
        resources_file = open(filename, "w")
        test_controller = open("files/controller_mid_lvl.txt")
        resources_file.write("package " + mid_lvl_proj.rootpackage + "." + Constants.pckg_contr + ";\n\n")
        for line in test_controller:
            linestr = str(line)
            if(linestr.find("XXX")>-1):
                self.create_controller_business_calls_for_mid_level(mid_lvl_proj, crud_proj_names, crud_proj_data,resources_file)
            else:
                resources_file.write(linestr.replace("$",mid_lvl_proj.rootpackage).replace("%", mid_lvl_proj.camelcasejavaname).replace("&", mid_lvl_proj.lowercasename).replace("^", Configuration.author))
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
        file.write("import java.math.*;\n")
        file.write("import java.sql.*;\n")
        file.write("import java.util.*;\n")
        bigdatafield = False
        bigintfield = False
        datefield = False
        tsfield = False
        # FOR EACH FIELD:
        """
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
        """
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

    def create_rest_calls_for_proxy(self, project, file):
        """
        this method will create the REST service calls to all tables of the proxy for the given project
        :param project:
        :return:
        """
        tabs = "\t"
        for tablename in project.tablenames:
            tabledata = project.tabledata[tablename]
            tablefile = open(project.topmainpackage + "/" + Constants.pckg_contr + "/" + tabledata.camelcasejavaname + "Controller.java","r")
            requestmappingfound = False
            itemfound = False
            for line in tablefile:
                linestr = str(line)
                if requestmappingfound == True:
                    if itemfound == True:
                        file.write(linestr.replace("{", ";"))
                        file.write("\n\n")
                        itemfound = False
                    elif linestr.find('Mapping(') > -1:
                        itemfound = True
                        if(Configuration.use_naming_server == True):
                            relativepath = "/"+project.pomname+"/"+tabledata.lowercasename+"/"
                        else:
                            relativepath = "/" + tabledata.lowercasename + "/"
                        file.write(Constants.doc_proxy)
                        file.write(linestr.replace("/",relativepath,1))

                elif linestr.find('Mapping(') > -1:
                    requestmappingfound = True
            tablefile.close()

    def remove_annotations_from_string(self, inputstring):
        """
        this method is for the mid-level proxies, it will remove annotations from the method declarations
        :param inputstring:
        :return:
        """
        stringarray = inputstring.split("(")
        outputstring = stringarray[0]+'('
        remaining = stringarray[1].split(" ")
        for word in remaining:
            wordstr = str(word)
            if wordstr.find('@') == -1:
                outputstring += wordstr + " "
        return outputstring.rstrip()

    def remove_datatypes_from_string(self, inputstring):
        """
        this method is for the mid-level business classes; it will remove the data types from an input parameter string
        :param inputstring:
        :return:
        """
        tempstring = inputstring[inputstring.find("public ResponseEntity<Object>") + 30:]
        methodname = tempstring[0:tempstring.find("(")]
        parameterlist = tempstring[tempstring.find("("):tempstring.find(")")]
        paramsstring = ''
        if(len(parameterlist)==0):
            return methodname+"()"
        if(parameterlist.find(",") > -1):
            parameterpairs = parameterlist.split(",")
            for pair in parameterpairs:
                items = pair.split(" ")
                oddfield = True
                for item in items:
                    if(len(item)>0):
                        if(item.find("@")>-1):
                            None
                        elif(oddfield == False):
                            paramsstring += item + ","
                            oddfield = True
                        else:
                            oddfield = False
            return methodname+"("+paramsstring[:-1]+")"
        else:
            items = parameterlist.split(" ")
            oddfield = True
            for item in items:
                if (len(item) > 0):
                    if (item.find("@") > -1):
                        None
                    elif (oddfield == False):
                        paramsstring += item + ","
                        oddfield = True
                    else:
                        oddfield = False
            return methodname + "(" + paramsstring[:-1] + ")"

    def create_controller_business_calls_for_mid_level(self, mid_lvl_proj, crud_proj_names, crud_proj_data, resources_file):
        """

        :param mid_lvl_proj:
        :param crud_proj_names:
        :param crud_proj_data:
        :param resources_file:
        :return:
        """
        tabs = "\t"
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
                                        resources_file.write(tabs+tabs+"try{\n")
                                    elif (linecount == 6):
                                        newlinestr = tabs + tabs + tabs + "Object result = " + linestr[linestr.find(
                                            "businessService"):linestr.find(";")] + ".getBody();\n"
                                        resources_file.write(newlinestr)
                                    elif (linecount == 5):
                                        resources_file.write(
                                            tabs + tabs + tabs + "return ResponseEntity.status(HttpStatus.OK).body(result);\n")
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
                                        newlinestr = tabs+tabs+"Object result = " + linestr[linestr.find("businessService"):linestr.find(";")] + ".getBody();\n"
                                        resources_file.write(newlinestr)
                                    elif(linecount == 2):
                                        resources_file.write(tabs+tabs+"return ResponseEntity.status(HttpStatus.OK).body(result);\n")
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

    def create_pojo_resonse_class(self, project):
        """
        this method creates a ResponseMessage object that is needed by the DELETE REST calls
        :param table:
        :return:
        """
        filename = project.topmainpackage + "/" + Constants.pckg_pojos + "/ResponseMessage.java"
        main_file = open("files/response_message.txt", "r")
        resources_file = open(filename, "w")
        resources_file.write("package " + project.rootpackage + "." + Constants.pckg_pojos + ";\n\n")
        for line in main_file:
            linestr = str(line)
            resources_file.write(linestr)
        resources_file.close()
        main_file.close()

    def create_pojo_resonse_class_for_mid_level(self, project):
        """
        this method creates a ResponseMessage object that is needed by the DELETE REST calls
        :param table:
        :return:
        """
        filename = project.topmainpackage + "/" + Constants.path_proxy_pojos + "/ResponseMessage.java"
        main_file = open("files/response_message.txt", "r")
        resources_file = open(filename, "w")
        resources_file.write("package " + project.rootpackage + "." + Constants.pckg_proxy_pojos + ";\n\n")
        for line in main_file:
            linestr = str(line)
            resources_file.write(linestr)
        resources_file.close()
        main_file.close()