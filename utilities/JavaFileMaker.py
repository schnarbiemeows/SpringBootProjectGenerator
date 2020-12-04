#from configuration.Constants import *
from configuration.Configuration import *
from utilities.Utilities import *
"""
    this class creates the different Java files(excluding the test files)
"""
class JavaFileMaker:

    @staticmethod
    def create_main_method_class( project):
        """
        this method creates the main Application class for the project
        :param project:
        :return:
        """
        tabs = Constants.tab
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
                    resources_file.write(tabs*2+"return Sampler.ALWAYS_SAMPLE;\n")
                    resources_file.write(tabs +"}\n")
            elif (linestr.find("RIBBON_CLIENT_ANN") > -1):
                if (Configuration.use_naming_server == True or Configuration.use_docker == True):
                    resources_file.write(Constants.ann_feign.replace("RIBBON_CLIENT_ANN", project.rootpackage)+"\n")
                    resources_file.write(Constants.ann_dc + "\n")
            else:
                resources_file.write(linestr.replace("^", Configuration.author).replace("%", project.camelcasejavaname))
        resources_file.close()
        main_file.close()

    @staticmethod
    def make_base_exc_class( project):
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

    @staticmethod
    def make_rnf_exc_class( table):
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

    @staticmethod
    def make_spec_eh_class( table):
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

    @staticmethod
    def create_randomizer_class( project):
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

    @staticmethod
    def create_proxy_class( currentprojectdata, projectnames, projectdata):
        """
        this method will create the proxy interfaces to the other projects' REST controllers
        :param table:
        :return:
        """
        if Configuration.use_naming_server == True and Configuration.naming_server_proxy_mode == 2:
            for projectname in projectnames:
                if(projectname != currentprojectdata.pomname):
                    otherproject = projectdata[projectname]
                    filename = currentprojectdata.topmainpackage + "/" + Constants.path_proxy_services + "/" + otherproject.camelcasejavaname + "ServiceProxy.java"
                    resources_file = open(filename, "w")
                    resources_file.write("package " + currentprojectdata.rootpackage + "." + Constants.pckg_proxy_services + ";\n\n")
                    proxy_file = open("files/specific_proxy.txt", "r")
                    for line in proxy_file:
                        linestr = str(line)
                        # below does not appear in the specific_proxy.txt file - ???
                        if(linestr.find("YYY"))>-1:
                            for tablename in otherproject.tablenames:
                                proxytable = otherproject.tabledata[tablename]
                                resources_file.write("import "+currentprojectdata.rootpackage + "." + Constants.pckg_proxy_dtos+"."+proxytable.dtoname+";\n")
                        elif (linestr.find("PROXY_REST_CALLS")) > -1:
                            JavaFileMaker.create_rest_calls_for_proxy(otherproject, resources_file)
                        elif(linestr.find("FEIGN_CLIENT_ANN"))>-1:
                            if(Configuration.use_gateway_server == True):
                                resources_file.write(linestr.replace("FEIGN_CLIENT_ANN",'@FeignClient(name="zuul-api-gateway-server")'))
                            elif(Configuration.use_docker == True):
                                resources_file.write(linestr.replace("FEIGN_CLIENT_ANN", '@FeignClient(name = "'+otherproject.pomname+'", url = "${CURRENCY_EXCHANGE_SERVICE_HOST:http://localhost}:'+str(otherproject.portnum)+'")'))
                            elif(Configuration.use_naming_server == True):
                                resources_file.write(
                                    linestr.replace("FEIGN_CLIENT_ANN", '@FeignClient(name="' + otherproject.pomname + '")'))
                            else:
                                resources_file.write(linestr.replace("FEIGN_CLIENT_ANN", otherproject.pomname))      # this is not correct
                        elif (linestr.find("RIBBON_CLIENT_ANN")) > -1:
                            if (Configuration.use_naming_server == True):
                                resources_file.write(
                                    linestr.replace("RIBBON_CLIENT_ANN", '@RibbonClient(name="' + otherproject.pomname + '")'))
                        elif (linestr.find("FEIGN_CLIENT_IMPORT")) > -1:
                            if (Configuration.use_naming_server == True or Configuration.use_gateway_server == True or Configuration.use_docker == True):
                                resources_file.write("import org.springframework.cloud.openfeign.FeignClient;\n")
                        elif (linestr.find("RIBBON_CLIENT_IMPORT")) > -1:
                            if (Configuration.use_naming_server == True):
                                resources_file.write("import org.springframework.cloud.netflix.ribbon.RibbonClient;\n")
                        else:
                            resources_file.write(linestr.replace("^", Configuration.author).replace("%", otherproject.camelcasejavaname).replace(
                            "&", currentprojectdata.rootpackage))
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

    @staticmethod
    def create_proxy_classes_for_mid_levels( mid_lvl_proj, crud_proj_names, crud_proj_data):
        """
        this method will create proxy interfaces for the mid-level project to each of the tables that the user wants
        proxies to
        :param mid_lvl_proj:
        :return:
        """
        mid_lvl_map = {}
        for project_name in mid_lvl_proj.lowerprojectnames:
            mid_lvl_map[project_name] = "YES"
        for projectname in crud_proj_names:
            currentproject = crud_proj_data[projectname]
            if currentproject.referencename in mid_lvl_map:
                filename = mid_lvl_proj.topmainpackage + "/" + Constants.path_proxy_services + "/" + currentproject.camelcasejavaname + "ServiceProxy.java"
                resources_file = open(filename, "w")
                resources_file.write("package " + mid_lvl_proj.rootpackage + "." + Constants.pckg_proxy_services + ";\n\n")
                proxy_file = open("files/specific_proxy.txt", "r")
                for line in proxy_file:
                    linestr = str(line)
                    if(linestr.find("PROXY_REST_CALLS")) > -1:
                        JavaFileMaker.create_rest_calls_for_proxy(currentproject,resources_file)
                    elif (linestr.find("FEIGN_CLIENT_ANN")) > -1:
                        if (Configuration.use_gateway_server == True):
                            resources_file.write(linestr.replace("FEIGN_CLIENT_ANN", "zuul-api-gateway-server"))
                        elif (Configuration.use_docker == True):
                            service_name = currentproject.pomname.upper().replace("-","_") + "_SERVICE_HOST"
                            mid_lvl_proj.service_config.append(service_name)
                            text = '@FeignClient(name = "' + currentproject.pomname + '", url = "${' + service_name + ':http://RIBBON_CLIENT_ANN}:' + str(currentproject.portnum) + '")'
                            resources_file.write(linestr.replace("FEIGN_CLIENT_ANN",text.replace("RIBBON_CLIENT_ANN", "localhost")))
                        elif (Configuration.use_naming_server == True):
                            resources_file.write(
                                linestr.replace("FEIGN_CLIENT_ANN", '@FeignClient(name = "' + currentproject.pomname + '")'))
                        else:
                            resources_file.write(linestr.replace("FEIGN_CLIENT_ANN", "//" + currentproject.pomname))                 # this is not correct
                    elif(linestr.find("RIBBON_CLIENT_ANN")) > -1:
                        if (Configuration.use_naming_server == True):
                            resources_file.write(linestr.replace("RIBBON_CLIENT_ANN", '@RibbonClient(name="'+currentproject.pomname+'")'))
                    elif (linestr.find("FEIGN_CLIENT_IMPORT")) > -1:
                        if (Configuration.use_naming_server == True or Configuration.use_gateway_server == True or Configuration.use_docker == True):
                            resources_file.write("import org.springframework.cloud.openfeign.FeignClient;\n")
                    elif (linestr.find("RIBBON_CLIENT_IMPORT")) > -1:
                        if (Configuration.use_naming_server == True):
                            resources_file.write("import org.springframework.cloud.netflix.ribbon.RibbonClient;\n")
                    else:
                        resources_file.write(linestr.replace("^", Configuration.author).replace("%",currentproject.camelcasejavaname).replace(
                            "&", mid_lvl_proj.rootpackage))
                resources_file.close()
                proxy_file.close()

    @staticmethod
    def create_proxy_dtos( destinationroot, currentprojectdata, projectnames, projectdata):
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
                        #resources_file.write("import java.math.*;\n")
                        #resources_file.write("import java.sql.*;\n")
                        #resources_file.write("import java.util.*;\n")
                        source_file = open(destinationroot + "/" + otherprojectdata.pomname + "/" + otherprojectdata.pomname + "/src/main/java/" + Configuration.groupid.replace(".","/") + "/" + otherprojectdata.lowercasename + "/dtos/" + proxytable.dtoname + ".java", "r")
                        count = 0
                        proxytablename = proxytable.camelcasejavaname+";"
                        hasDate, hasTime, hasTimestamp = JavaFileMaker.findDateAndTimeFields(proxytable)
                        for line in source_file:
                            if count > 0:
                                linestr = str(line)
                                if linestr.find(proxytablename) >-1 and linestr.find("import")>-1:
                                    resources_file.write(
                                        "import " + currentprojectdata.rootpackage + "." + Constants.pckg_proxy_pojos + "." + proxytable.camelcasejavaname + ";\n")
                                elif linestr.find("import java.util.*;") > -1:
                                    if hasDate == True:
                                        resources_file.write("import java.util.Date;\n")
                                elif linestr.find("import java.sql.*;") > -1:
                                    if hasTime == True:
                                        resources_file.write("import java.sql.Time;\n")
                                    if hasTimestamp == True:
                                        resources_file.write("import java.sql.Timestamp;\n")
                                else:
                                    resources_file.write(linestr)
                            else:
                                count += 1
                        resources_file.close()
                        source_file.close()
        else:
            None

    @staticmethod
    def findDateAndTimeFields(tabledata):
        """
        this method will parse the table to find if the table has any Date or Time fields
        this is used for import statements
        :param tabledata:
        :return:
        """
        hasDate = False
        hasTime = False
        hasTimestamp = False
        for fieldname in tabledata.fieldnames:
            fielddata = tabledata.fielddata[fieldname]
            if fielddata.datatype.lower() == "date":
                hasDate = True
            if fielddata.datatype.lower() == "time":
                hasTime = True
            if fielddata.datatype.lower() == "timestamp":
                hasTimestamp = True
        return (hasDate,hasTime,hasTimestamp)

    @staticmethod
    def create_proxy_dtos_for_mid_lvl( destinationroot, mid_lvl_proj, crud_proj_names, crud_proj_data):
        """
        this method will create the DTOs needed for the proxies for the mid-level projects
        :param destinationroot:
        :param mid_lvl_proj:
        :param crud_proj_names:
        :param crud_proj_data:
        :return:
        """
        mid_lvl_map = {}
        for tablename in mid_lvl_proj.lowerprojectnames:
            mid_lvl_map[tablename] = "YES"
        for projectname in crud_proj_names:
            currentproject = crud_proj_data[projectname]
            if currentproject.referencename in mid_lvl_map:
                for tablename in currentproject.tablenames:
                    currenttable = currentproject.tabledata[tablename]
                    filename = mid_lvl_proj.topmainpackage + "/" + Constants.path_proxy_dtos + "/" + currenttable.dtoname + ".java"
                    resources_file = open(filename, "w")
                    resources_file.write("package " + mid_lvl_proj.rootpackage + "." + Constants.pckg_proxy_dtos + ";\n")
                    source_file = open(destinationroot + "/" + currentproject.pomname + "/" + currentproject.pomname + "/src/main/java/" + Configuration.groupid.replace(".","/") + "/" + currentproject.lowercasename + "/dtos/" + currenttable.dtoname + ".java", "r")
                    count = 0
                    proxytablename = currenttable.camelcasejavaname+";"
                    hasDate, hasTime, hasTimestamp = JavaFileMaker.findDateAndTimeFields(currenttable)
                    for line in source_file:
                        if count > 0:
                            linestr = str(line)
                            if linestr.find(proxytablename) >-1 and linestr.find("import")>-1:
                                resources_file.write(
                                    "import " + mid_lvl_proj.rootpackage + "." + Constants.pckg_proxy_pojos + "." + currenttable.camelcasejavaname + ";\n")
                            elif linestr.find("import java.util.*;") > -1:
                                if hasDate == True:
                                    resources_file.write("import java.util.Date;\n")
                            elif linestr.find("import java.sql.*;") > -1:
                                if hasTime == True:
                                    resources_file.write("import java.sql.Time;\n")
                                if hasTimestamp == True:
                                    resources_file.write("import java.sql.Timestamp;\n")
                            else:
                                resources_file.write(linestr)
                        else:
                            count += 1
                    resources_file.close()
                    source_file.close()

    @staticmethod
    def create_proxy_pojos( destinationroot, currentprojectdata, projectnames, projectdata):
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
                        #resources_file.write("import java.math.*;\n")
                        #resources_file.write("import java.sql.*;\n")
                        #resources_file.write("import java.util.*;\n")
                        source_file = open(destinationroot + "/" + otherprojectdata.pomname + "/" + otherprojectdata.pomname + "/src/main/java/" + Configuration.groupid.replace(".","/") + "/" + otherprojectdata.lowercasename + "/pojos/" + proxytable.camelcasejavaname + ".java", "r")
                        count = 0
                        proxytablename = proxytable.dtoname+";"
                        hasDate, hasTime, hasTimestamp = JavaFileMaker.findDateAndTimeFields(proxytable)
                        for line in source_file:
                            if count > 0 :
                                linestr = str(line)
                                if linestr.find(proxytablename) >-1 and linestr.find("import")>-1:
                                    resources_file.write("import " + currentprojectdata.rootpackage + "." + Constants.pckg_proxy_dtos + "." + proxytable.dtoname +";\n")
                                elif linestr.find("import java.util.*;") > -1:
                                    if hasDate == True:
                                        resources_file.write("import java.util.Date;\n")
                                elif linestr.find("import java.sql.*;") > -1:
                                    if hasTime == True:
                                        resources_file.write("import java.sql.Time;\n")
                                    if hasTimestamp == True:
                                        resources_file.write("import java.sql.Timestamp;\n")
                                else:
                                    resources_file.write(linestr)
                            else:
                                count += 1
                        resources_file.close()
                        source_file.close()
        else:
            None

    @staticmethod
    def create_proxy_pojos_for_mid_lvl( destinationroot, mid_lvl_proj, crud_proj_names, crud_proj_data):
        """
        this method will create the DTOs needed for the proxies for the mid-level projects
        :param destinationroot:
        :param mid_lvl_proj:
        :param crud_proj_names:
        :param crud_proj_data:
        :return:
        """
        mid_lvl_map = {}
        for tablename in mid_lvl_proj.lowerprojectnames:
            mid_lvl_map[tablename] = "YES"
        for projectname in crud_proj_names:
            currentproject = crud_proj_data[projectname]
            if currentproject.referencename in mid_lvl_map:
                for tablename in currentproject.tablenames:
                    currenttable = currentproject.tabledata[tablename]
                    filename = mid_lvl_proj.topmainpackage + "/" + Constants.path_proxy_pojos + "/" + currenttable.camelcasejavaname + ".java"
                    resources_file = open(filename, "w")
                    resources_file.write("package " + mid_lvl_proj.rootpackage + "." + Constants.pckg_proxy_pojos + ";\n")
                    source_file = open(destinationroot + "/" + currentproject.pomname + "/" + currentproject.pomname + "/src/main/java/" + Configuration.groupid.replace(".","/") + "/" + currentproject.lowercasename + "/pojos/" + currenttable.camelcasejavaname + ".java", "r")
                    count = 0
                    proxytablename = currenttable.dtoname+";"
                    hasDate, hasTime, hasTimestamp = JavaFileMaker.findDateAndTimeFields(currenttable)
                    for line in source_file:
                        if count > 0:
                            linestr = str(line)
                            if linestr.find(proxytablename) >-1 and linestr.find("import")>-1:
                                resources_file.write(
                                    "import " + mid_lvl_proj.rootpackage + "." + Constants.pckg_proxy_dtos + "." + currenttable.dtoname + ";\n")
                            elif linestr.find("import java.util.*;") > -1:
                                if hasDate == True:
                                    resources_file.write("import java.util.Date;\n")
                            elif linestr.find("import java.sql.*;") > -1:
                                if hasTime == True:
                                    resources_file.write("import java.sql.Time;\n")
                                if hasTimestamp == True:
                                    resources_file.write("import java.sql.Timestamp;\n")
                            else:
                                resources_file.write(linestr)
                        else:
                            count += 1
                    resources_file.close()
                    source_file.close()
        else:
            None

    @staticmethod
    def create_swagger_class( project):
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

    @staticmethod
    def create_health_check_controller( project):
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

    @staticmethod
    def create_rest_calls_for_proxy( project, file):
        """
        this method will create the REST service calls to all tables of the proxy for the given project
        :param project:
        :param file: output file
        :return:
        """
        tabs = Constants.tab
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
                        if Configuration.use_gateway_server == True:
                            relativepath = "/"+project.pomname+"/"+tabledata.lowercasename+"/"
                        else:
                            relativepath = "/" + tabledata.lowercasename + "/"
                        file.write(Constants.doc_proxy)
                        file.write(linestr.replace("/",relativepath,1))

                elif linestr.find('Mapping(') > -1:
                    requestmappingfound = True
            tablefile.close()

    @staticmethod
    def create_pojo_response_class( project):
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

    @staticmethod
    def create_pojo_response_class_for_mid_level( project):
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