from configuration.Configuration import *
from configuration.Constants import *
from utilities.Utilities import *

class ProxyGenerator:
    
    def __init__(self):
        """

        """
        None

    @staticmethod
    def create_proxy_class(currentprojectdata, projectnames, projectdata):
        """
        this method will create the proxy interfaces to the other projects' REST controllers
        :param table:
        :return:
        """
        tabs = Constants.tab
        if Configuration.use_naming_server == True and Configuration.naming_server_proxy_mode == 2:
            for projectname in projectnames:
                if (projectname != currentprojectdata.pomname):
                    otherproject = projectdata[projectname]
                    filename = currentprojectdata.topmainpackage + "/" + Constants.path_proxy_services + "/" + otherproject.camelcasejavaname + "ServiceProxy.java"
                    resources_file = open(filename, "w")
                    resources_file.write(
                        "package " + currentprojectdata.rootpackage + "." + Constants.pckg_proxy_services + ";\n\n")
                    proxy_file = open("files/proxy/specific_proxy.txt", "r")
                    for line in proxy_file:
                        linestr = str(line)
                        # below does not appear in the specific_proxy.txt file - ???
                        if (linestr.find("YYY")) > -1:
                            for tablename in otherproject.tablenames:
                                proxytable = otherproject.tabledata[tablename]
                                resources_file.write(
                                    "import " + currentprojectdata.rootpackage + "." + Constants.pckg_proxy_dtos + "." + proxytable.dtoname + ";\n")
                        elif (linestr.find("PROXY_REST_CALLS")) > -1:
                            ProxyGenerator.create_rest_calls_for_proxy(otherproject, resources_file)
                        elif (linestr.find("FEIGN_CLIENT_ANN")) > -1:
                            if (Configuration.use_gateway_server == True):
                                resources_file.write(linestr.replace("FEIGN_CLIENT_ANN",
                                                                     '@FeignClient(name="zuul-api-gateway-server")'))
                            elif (Configuration.use_docker == True):
                                resources_file.write(linestr.replace("FEIGN_CLIENT_ANN",
                                                                     '@FeignClient(name = "' + otherproject.pomname + '", url = "${CURRENCY_EXCHANGE_SERVICE_HOST:http://localhost}:' + str(
                                                                         otherproject.portnum) + '")'))
                            elif (Configuration.use_naming_server == True):
                                resources_file.write(
                                    linestr.replace("FEIGN_CLIENT_ANN",
                                                    '@FeignClient(name="' + otherproject.pomname + '")'))
                            else:
                                resources_file.write(linestr.replace("FEIGN_CLIENT_ANN",
                                                                     otherproject.pomname))  # this is not correct
                        elif (linestr.find("RIBBON_CLIENT_ANN")) > -1:
                            if (Configuration.use_naming_server == True):
                                resources_file.write(
                                    linestr.replace("RIBBON_CLIENT_ANN",
                                                    '@RibbonClient(name="' + otherproject.pomname + '")'))
                        elif (linestr.find("FEIGN_CLIENT_IMPORT")) > -1:
                            if (
                                    Configuration.use_naming_server == True or Configuration.use_gateway_server == True or Configuration.use_docker == True):
                                resources_file.write("import org.springframework.cloud.openfeign.FeignClient;\n")
                        elif (linestr.find("RIBBON_CLIENT_IMPORT")) > -1:
                            if (Configuration.use_naming_server == True):
                                resources_file.write(
                                    "import org.springframework.cloud.netflix.ribbon.RibbonClient;\n")
                        else:
                            resources_file.write(linestr.replace("^", Configuration.author).replace("%",
                                                                                                    otherproject.camelcasejavaname).replace(
                                "&", currentprojectdata.rootpackage))
                    resources_file.close()
                    proxy_file.close()
        else:
            filename = currentprojectdata.topmainpackage + "/" + Constants.path_proxy_services + "/" + "GenericServiceProxy.java"
            resources_file = open(filename, "w")
            resources_file.write(
                "package " + currentprojectdata.rootpackage + "." + Constants.pckg_proxy_services + ";\n\n")
            proxy_file = open("files/proxy/generic_proxy.txt", "r")
            for line in proxy_file:
                linestr = str(line)
                resources_file.write(linestr.replace("^", Configuration.author))
            resources_file.close()
            proxy_file.close()

    @staticmethod
    def create_rest_calls_for_proxy(project, file):
        """
        this method will create the REST service calls to all tables of the proxy for the given project
        :param project:
        :param file: output file
        :return:
        """
        tabs = Constants.tab
        for tablename in project.tablenames:
            tabledata = project.tabledata[tablename]
            tablefile = open(
                project.topmainpackage + "/" + Constants.pckg_contr + "/" + tabledata.camelcasejavaname + "Controller.java",
                "r")
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
                            relativepath = "/" + project.pomname + "/" + tabledata.lowercasename + "/"
                        else:
                            relativepath = "/" + tabledata.lowercasename + "/"
                        file.write(Constants.doc_proxy)
                        file.write(linestr.replace("/", relativepath, 1))

                elif linestr.find('Mapping(') > -1:
                    requestmappingfound = True
            tablefile.close()

    @staticmethod
    def create_proxy_classes_for_mid_levels(mid_lvl_proj, crud_proj_names, crud_proj_data):
        """
        this method will create proxy interfaces for the mid-level project to each of the tables that the user wants
        proxies to
        :param mid_lvl_proj:
        :return:
        """
        tabs = Constants.tab
        mid_lvl_map = {}
        for project_name in mid_lvl_proj.lowerprojectnames:
            mid_lvl_map[project_name] = "YES"
        for projectname in crud_proj_names:
            currentproject = crud_proj_data[projectname]
            if currentproject.referencename in mid_lvl_map:
                filename = mid_lvl_proj.topmainpackage + "/" + Constants.path_proxy_services + "/" + currentproject.camelcasejavaname + "ServiceProxy.java"
                resources_file = open(filename, "w")
                resources_file.write(
                    "package " + mid_lvl_proj.rootpackage + "." + Constants.pckg_proxy_services + ";\n\n")
                proxy_file = open("files/proxy/specific_proxy.txt", "r")
                for line in proxy_file:
                    linestr = str(line)
                    if (linestr.find("PROXY_REST_CALLS")) > -1:
                        ProxyGenerator.create_rest_calls_for_proxy(currentproject, resources_file)
                    elif linestr.find("LOGGER_IMPORT") > -1:
                        if Configuration.use_logging == True:
                            resources_file.write(Constants.import_logger_1 + "\n")
                            resources_file.write(Constants.import_logger_2 + "\n")
                    elif linestr.find("SINGLETON_LOGGER") > -1:
                        if Configuration.use_logging == True:
                            resources_file.write(tabs + Constants.logger_singleton + "\n")
                    elif (linestr.find("FEIGN_CLIENT_ANN")) > -1:
                        if (Configuration.use_gateway_server == True):
                            resources_file.write(linestr.replace("FEIGN_CLIENT_ANN", "zuul-api-gateway-server"))
                        elif (Configuration.use_docker == True):
                            service_name = currentproject.pomname.upper().replace("-", "_") + "_SERVICE_HOST"
                            mid_lvl_proj.service_config.append(service_name)
                            text = '@FeignClient(name = "' + currentproject.pomname + '", url = "${' + service_name + ':http://RIBBON_CLIENT_ANN}:' + str(
                                currentproject.portnum) + '")'
                            resources_file.write(
                                linestr.replace("FEIGN_CLIENT_ANN", text.replace("RIBBON_CLIENT_ANN", "localhost")))
                        elif (Configuration.use_naming_server == True):
                            resources_file.write(
                                linestr.replace("FEIGN_CLIENT_ANN",
                                                '@FeignClient(name = "' + currentproject.pomname + '")'))
                        else:
                            resources_file.write(linestr.replace("FEIGN_CLIENT_ANN",
                                                                 "//" + currentproject.pomname))  # this is not correct
                    elif (linestr.find("RIBBON_CLIENT_ANN")) > -1:
                        if (Configuration.use_naming_server == True):
                            resources_file.write(linestr.replace("RIBBON_CLIENT_ANN",
                                                                 '@RibbonClient(name="' + currentproject.pomname + '")'))
                    elif (linestr.find("FEIGN_CLIENT_IMPORT")) > -1:
                        if (
                                Configuration.use_naming_server == True or Configuration.use_gateway_server == True or Configuration.use_docker == True):
                            resources_file.write("import org.springframework.cloud.openfeign.FeignClient;\n")
                    elif (linestr.find("RIBBON_CLIENT_IMPORT")) > -1:
                        if (Configuration.use_naming_server == True):
                            resources_file.write("import org.springframework.cloud.netflix.ribbon.RibbonClient;\n")
                    else:
                        resources_file.write(linestr.replace("^", Configuration.author).replace("%",
                                                                                                currentproject.camelcasejavaname).replace(
                            "&", mid_lvl_proj.rootpackage))
                resources_file.close()
                proxy_file.close()

    @staticmethod
    def create_proxy_dtos(destinationroot, currentprojectdata, projectnames, projectdata):
        """
        this method will create the DTOs needed for the proxies
        :param table:
        :return:
        """
        if (Configuration.naming_server_proxy_mode == 2):
            for projectname in projectnames:
                otherprojectdata = projectdata[projectname]
                if (currentprojectdata.pomname != otherprojectdata.pomname):
                    for tablename in otherprojectdata.tablenames:
                        proxytable = otherprojectdata.tabledata[tablename]
                        filename = currentprojectdata.topmainpackage + "/" + Constants.path_proxy_dtos + "/" + proxytable.dtoname + ".java"
                        resources_file = open(filename, "w")
                        resources_file.write(
                            "package " + currentprojectdata.rootpackage + "." + Constants.pckg_proxy_dtos + ";\n\n")
                        # resources_file.write("import java.math.*;\n")
                        # resources_file.write("import java.sql.*;\n")
                        # resources_file.write("import java.util.*;\n")
                        source_file = open(
                            destinationroot + "/" + otherprojectdata.pomname + "/" + otherprojectdata.pomname + "/src/main/java/" + Configuration.groupid.replace(
                                ".",
                                "/") + "/" + otherprojectdata.lowercasename + "/dtos/" + proxytable.dtoname + ".java",
                            "r")
                        count = 0
                        proxytablename = proxytable.camelcasejavaname + ";"
                        hasDate, hasTime, hasTimestamp = ProxyGenerator.findDateAndTimeFields(proxytable)
                        for line in source_file:
                            if count > 0:
                                linestr = str(line)
                                if linestr.find(proxytablename) > -1 and linestr.find("import") > -1:
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
        return (hasDate, hasTime, hasTimestamp)

    @staticmethod
    def create_proxy_dtos_for_mid_lvl(destinationroot, mid_lvl_proj, crud_proj_names, crud_proj_data):
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
                    resources_file.write(
                        "package " + mid_lvl_proj.rootpackage + "." + Constants.pckg_proxy_dtos + ";\n")
                    source_file = open(
                        destinationroot + "/" + currentproject.pomname + "/" + currentproject.pomname + "/src/main/java/" + Configuration.groupid.replace(
                            ".",
                            "/") + "/" + currentproject.lowercasename + "/dtos/" + currenttable.dtoname + ".java",
                        "r")
                    count = 0
                    proxytablename = currenttable.camelcasejavaname + ";"
                    hasDate, hasTime, hasTimestamp = ProxyGenerator.findDateAndTimeFields(currenttable)
                    for line in source_file:
                        if count > 0:
                            linestr = str(line)
                            if linestr.find(proxytablename) > -1 and linestr.find("import") > -1:
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
    def create_proxy_pojos(destinationroot, currentprojectdata, projectnames, projectdata):
        """
        this method will create the DTOs needed for the proxies
        :param table:
        :return:
        """
        if (Configuration.naming_server_proxy_mode == 2):
            for projectname in projectnames:
                otherprojectdata = projectdata[projectname]
                if (currentprojectdata.pomname != otherprojectdata.pomname):
                    for tablename in otherprojectdata.tablenames:
                        proxytable = otherprojectdata.tabledata[tablename]
                        filename = currentprojectdata.topmainpackage + "/" + Constants.path_proxy_pojos + "/" + proxytable.camelcasejavaname + ".java"
                        resources_file = open(filename, "w")
                        resources_file.write(
                            "package " + currentprojectdata.rootpackage + "." + Constants.pckg_proxy_pojos + ";\n\n")
                        # resources_file.write("import java.math.*;\n")
                        # resources_file.write("import java.sql.*;\n")
                        # resources_file.write("import java.util.*;\n")
                        source_file = open(
                            destinationroot + "/" + otherprojectdata.pomname + "/" + otherprojectdata.pomname + "/src/main/java/" + Configuration.groupid.replace(
                                ".",
                                "/") + "/" + otherprojectdata.lowercasename + "/pojos/" + proxytable.camelcasejavaname + ".java",
                            "r")
                        count = 0
                        proxytablename = proxytable.dtoname + ";"
                        hasDate, hasTime, hasTimestamp = ProxyGenerator.findDateAndTimeFields(proxytable)
                        for line in source_file:
                            if count > 0:
                                linestr = str(line)
                                if linestr.find(proxytablename) > -1 and linestr.find("import") > -1:
                                    resources_file.write(
                                        "import " + currentprojectdata.rootpackage + "." + Constants.pckg_proxy_dtos + "." + proxytable.dtoname + ";\n")
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
    def create_proxy_pojos_for_mid_lvl(destinationroot, mid_lvl_proj, crud_proj_names, crud_proj_data):
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
                    resources_file.write(
                        "package " + mid_lvl_proj.rootpackage + "." + Constants.pckg_proxy_pojos + ";\n")
                    source_file = open(
                        destinationroot + "/" + currentproject.pomname + "/" + currentproject.pomname + "/src/main/java/" + Configuration.groupid.replace(
                            ".",
                            "/") + "/" + currentproject.lowercasename + "/pojos/" + currenttable.camelcasejavaname + ".java",
                        "r")
                    count = 0
                    proxytablename = currenttable.dtoname + ";"
                    hasDate, hasTime, hasTimestamp = ProxyGenerator.findDateAndTimeFields(currenttable)
                    for line in source_file:
                        if count > 0:
                            linestr = str(line)
                            if linestr.find(proxytablename) > -1 and linestr.find("import") > -1:
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